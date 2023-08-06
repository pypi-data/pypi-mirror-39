#!/usr/bin/env python

""" Analysis configuration base module.

For usage information, see ``jet_hadron.base.analysisConfig``.

.. codeauthor:: Raymond Ehlers <raymond.ehlers@cern.ch>, Yale University
"""

import collections
import copy
import enum
import itertools
import logging
import string
import ruamel.yaml

logger = logging.getLogger(__name__)

def loadConfiguration(filename):
    """ Load an analysis configuration from a file.

    Args:
        filename (str): Filename of the YAML configuration file.
    Returns:
        dict-like: dict-like object containing the loaded configuration
    """
    # Initialize the YAML object in the round trip mode
    # NOTE: "typ" is a not a typo. It stands for "type"
    yaml = ruamel.yaml.YAML(typ = "rt")

    with open(filename, "r") as f:
        config = yaml.load(f)

    return config

def overrideOptions(config, selectedOptions, setOfPossibleOptions, configContainingOverride = None):
    """ Determine override options for a particular configuration.

    The options are determined by searching following the order specified in selectedOptions.

    For the example config,

    .. code-block:: yaml

        config:
            value: 3
            override:
                2.76:
                    track:
                        value: 5

    value will be assigned the value 5 if we are at 2.76 TeV with a track bias, regardless of the event
    activity or leading hadron bias. The order of this configuration is specified by the order of the
    selectedOptions passed. The above example configuration is from the jet-hadron analysis.

    Since anchors aren't kept for scalar values, if you want to override an anchored value, you need to
    specify it as a single value in a list (or dict, but list is easier). After the anchor values propagate,
    single element lists can be converted into scalar values using ``simplifyDataRepresentations()``.

    Args:
        config (CommentedMap): The dict-like configuration from ruamel.yaml which should be overridden.
        selectedOptions (tuple): The selected analysis options. They will be checked in the order with which
            they are passed, so make certain that it matches the order in the configuration file!
        setOfPossibleOptions (tuple of enums): Possible options for the override value categories.
        configContainingOverride (CommentedMap): The dict-like config containing the override options in a map called
            "override". If it is not specified, it will look for it in the main config.
    Returns:
        dict-like object: The updated configuration
    """
    if configContainingOverride is None:
        configContainingOverride = config
    override_opts = configContainingOverride.pop("override")
    overrideDict = determineOverrideOptions(selectedOptions, override_opts, setOfPossibleOptions)
    logger.debug(f"overrideDict: {overrideDict}")

    # Set the configuration values to those specified in the override options
    # Cannot just use update() on config because we need to maintain the anchors.
    for k, v in overrideDict.items():
        # Check if key is there and if it is not None! (The second part is important)
        if k in config:
            try:
                # We can't check for the anchor - we just have to try to access it.
                # However, we don't actually care about the value. We just want to
                # preserve it if it is exists.
                config[k].anchor
                logger.debug("type: {}, k: {}".format(type(config[k]), k))
                if isinstance(config[k], list):
                    # Clear out the existing list entries
                    del config[k][:]
                    if isinstance(overrideDict[k], str):
                        # We have to treat str carefully because it is an iterable, but it will be expanded as
                        # individual characters if it's treated the same as a list, which is not the desired
                        # behavior! If we wrap it in [], then it will be treated as the only entry in the list
                        config[k].append(overrideDict[k])
                    else:
                        # Here we just assign all entries of the list to all entries of overrideDict[k]
                        config[k].extend(overrideDict[k])
                elif isinstance(config[k], dict):
                    # Clear out the existing entries because we are trying to replace everything
                    # Then we can simply update the dict with our new values
                    config[k].clear()
                    config[k].update(overrideDict[k])
            except AttributeError:
                # If no anchor, just overwrite the value at this key
                config[k] = v
        else:
            raise KeyError(k, f"Trying to override key \"{k}\" that it is not in the config.")

    return config

def simplifyDataRepresentations(config):
    """ Convert one entry lists to the scalar value

    This step is necessary because anchors are not kept for scalar values - just for lists and dictionaries.
    Now that we are done with all of our anchor references, we can convert these single entry lists to
    just the scalar entry, which is more usable.

    Some notes on anchors in ruamel.yaml are here: https://stackoverflow.com/a/48559644

    Args:
        config (CommentedMap): The dict-like configuration from ruamel.yaml which should be simplified.
    Returns:
        dict-like object: The updated configuration
    """
    for k, v in config.items():
        if v and isinstance(v, list) and len(v) == 1:
            logger.debug("v: {}".format(v))
            config[k] = v[0]

    return config

def determineOverrideOptions(selectedOptions, override_opts, setOfPossibleOptions = ()):
    """ Recursively extract the dict described in overrideOptions().

    In particular, this searches for selected options in the override_opts dict.
    It stores only the override options that are selected.

    Args:
        selectedOptions (tuple): The options selected for this analysis, in the order defined used
            with overrideOptions() and in the configuration file.
        override_opts (CommentedMap): dict-like object returned by ruamel.yaml which contains the options that
            should be used to override the configuration options.
        setOfPossibleOptions (tuple of enums): Possible options for the override value categories.
    """
    overrideDict = {}
    for option in override_opts:
        # We need to cast the option to a string to effectively compare to the selected option,
        # since only some of the options will already be strings
        if str(option) in list(map(lambda opt: opt.str(), selectedOptions)):
            overrideDict.update(determineOverrideOptions(selectedOptions, override_opts[option], setOfPossibleOptions))
        else:
            logger.debug(f"override_opts: {override_opts}")
            # Look for whether the key is one of the possible but unselected options.
            # If so, we haven't selected it for this analysis, and therefore they should be ignored.
            # NOTE: We compare both the names and value because sometimes the name is not sufficient,
            #       such as in the case of the energy (because a number is not allowed to be a field name.)
            foundAsPossibleOption = False
            for possibleOptions in setOfPossibleOptions:
                # Same type of comparison as above, but for all possible options instead of the selected options.
                if str(option) in list(map(lambda opt: opt.str(), possibleOptions)):
                    foundAsPossibleOption = True
                # Below is more or less equivalent to the above (although .str() hides the details or whether
                # we should compare to the name or the value in the enum and only compares against the designated value).
                #for possibleOpt in possibleOptions:
                    #if possibleOpt.name == option or possibleOpt.value == option:
                    #    foundAsPossibleOption = True

            if not foundAsPossibleOption:
                # Store the override value, since it doesn't correspond with a selected option or a possible option
                # and therefore must be an option that we want to override.
                logger.debug(f"Storing override option \"{option}\", with value \"{override_opts[option]}\"")
                overrideDict[option] = override_opts[option]
            else:
                logger.debug(f"Found option \"{option}\" as possible option, so skipping!")

    return overrideDict

def determineSelectionOfIterableValuesFromConfig(config, possibleIterables):
    """ Determine iterable values to use to create objects for a given configuration.

    All values of an iterable can be included be setting the value to ``True`` (Not as a single value list,
    but as the only value.). Alternatively, an iterator can be disabled by setting the value to ``False``.

    Args:
        config (CommentedMap): The dict-like configuration from ruamel.yaml which should be overridden.
        possibleIterables (collections.OrderedDict): Key value pairs of names of enumerations and their values.
    Returns:
        collections.OrderedDict: Iterables values that were requested in the config.
    """
    iterables = collections.OrderedDict()
    requestedIterables = config["iterables"]
    for k, v in requestedIterables.items():
        if k not in possibleIterables:
            raise KeyError(k, "Cannot find requested iterable in possibleIterables: {possibleIterables}".format(possibleIterables = possibleIterables))
        logger.debug("k: {}, v: {}".format(k, v))
        additionalIterable = []
        enum_values = possibleIterables[k]
        # Check for a string. This is wrong, and the user should be notified.
        if isinstance(v, str):
            raise TypeError(type(v), "Passed string {v} when must be either bool or list".format(v = v))
        # Allow the possibility to skip
        if v is False:
            continue
        # Allow the possibility to including all possible values in the enum.
        elif v is True:
            additionalIterable = list(enum_values)
        else:
            # Otherwise, only take the requested values.
            for el in v:
                additionalIterable.append(enum_values[el])
        # Store for later
        iterables[k] = additionalIterable

    return iterables

def createObjectsFromIterables(obj, args, iterables, formattingOptions):
    """ Create objects for each set of values based on the given arguments.

    The values are available as keys in a nested dictionary which store the objects. The values
    must be convertible to a str() so they can be included in the formatting dictionary.

    Each set of values is also included in the object args.

    For example, for an iterables dict ``{"a" : ["a1","a2"], "b" : ["b1", "b2"]}``, the function would return:

    .. code-block:: python

        (
            ["a", "b"],
            {
                "a1" : {
                    "b1" : obj(a = "a1", b = "b1"),
                    "b2" : obj(a = "a1", b = "b2")
                },
                "a2" : {
                    "b1" : obj(a = "a2", b = "b1"),
                    "b2" : obj(a = "a2", b = "b2")
                }
            }
        )

    Args:
        obj (object): The object to be constructed.
        args (collections.OrderedDict): Arguments to be passed to the object to create it.
        iterables (collections.OrderedDict): Iterables to be used to create the objects, with entries of the form
            "nameOfIterable" : iterable.
        formattingOptions (dict): Values to apply to format strings in the arguments.
    Returns:
        (list, collections.OrderedDict): Roughly, (names, objects). Specifically, the list is the names
            of the iterables used. The ordered dict entries are of the form of a nested dict, with each
            object available at the iterable values used to constructed it. For example,
            output["a"]["b"] == obj(a = "a", b = "b", ...). For a full example, see above.
    """
    objects = collections.OrderedDict()
    names = list(iterables)
    logger.debug("iterables: {iterables}".format(iterables = iterables))
    for values in itertools.product(*iterables.values()):
        logger.debug("Values: {values}".format(values = values))
        tempDict = objects
        for i, val in enumerate(values):
            args[names[i]] = val
            logger.debug("i: {i}, val: {val}".format(i = i, val = repr(val)))
            # Convert the value, regardless of type, into a string that can be displayed.
            formattingOptions[names[i]] = str(val)
            # We should construct the object once we get to the last value
            if i != len(values) - 1:
                tempDict = tempDict.setdefault(val, collections.OrderedDict())
            else:
                # Apply formatting options
                # Need a deep copy to ensure that the iterable dependent values in the formatting are
                # properly set for each object individually.
                # NOTE: We don't need to do this for iterable value names because they will be overwritten
                #       for each object.
                objectArgs = copy.deepcopy(args)
                logger.debug(f"objectArgs pre format: {objectArgs}")
                objectArgs = applyFormattingDict(objectArgs, formattingOptions)
                # Skip printing the full config because it is quite long
                printArgs = {k: v for k, v in objectArgs.items() if k != "config"}
                printArgs["config"] = "..."
                logger.debug(f"Constructing obj \"{obj}\" with args: \"{printArgs}\"")

                # Create and store the object
                tempDict[val] = obj(**objectArgs)

    # If nothing has been created at this point, then we are didn't iterating over anything and something
    # has gone wrong.
    if not objects:
        raise ValueError(iterables, "There appear to be no iterables to use in creating objects.")

    return (names, objects)

class formattingDict(dict):
    """ Dict to handle missing keys when formatting a string. It returns the missing key
    for later use in formatting. See: https://stackoverflow.com/a/17215533 """
    def __missing__(self, key):
        return "{" + key + "}"

def applyFormattingDict(obj, formatting):
    """ Recursively apply a formatting dict to all strings in a configuration.

    Note that it skips applying the formatting if the string appears to contain latex (specifically,
    if it contains an "$"), since the formatting fails on nested brackets.

    Args:
        obj (dict): Some configuration object to recursively applying the formatting to.
        formatting (dict): String formatting options to apply to each configuration field.
    Returns:
        dict: Configuration with formatting applied to every field.
    """
    #logger.debug("Processing object of type {}".format(type(obj)))

    if isinstance(obj, str):
        # Apply the formatting options to the string.
        # We explicitly allow for missing keys. They will be kept so they can be filled later.
        # see: https://stackoverflow.com/a/17215533
        # If a more sophisticated solution is needed,
        # see: https://ashwch.github.io/handling-missing-keys-in-str-format-map.html
        # Note that we can't use format_map because it is python 3.2+ only.
        # The solution below works in py 2/3
        if "$" not in obj:
            obj = string.Formatter().vformat(obj, (), formattingDict(**formatting))
        #else:
        #    logger.debug("Skipping str {} since it appears to be a latex string, which may break the formatting.".format(obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            # Using indirect access to ensure that the original object is updated.
            obj[k] = applyFormattingDict(v, formatting)
    elif isinstance(obj, list):
        for i, el in enumerate(obj):
            # Using indirect access to ensure that the original object is updated.
            obj[i] = applyFormattingDict(el, formatting)
    elif isinstance(obj, int) or isinstance(obj, float) or obj is None:
        # Skip over this, as there is nothing to be done - we just keep the value.
        pass
    elif isinstance(obj, enum.Enum):
        # Skip over this, as there is nothing to be done - we just keep the value.
        # This only occurs when a formatting value has already been transformed
        # into an enumeration.
        pass
    else:
        # This may or may not be expected, depending on the particular value.
        logger.info("NOTE: Unrecognized type {} of obj {}".format(type(obj), obj))

    return obj

def unrollNestedDict(d, keys = None):
    """ Unroll (flatten) an analysis object dictionary to get the objects and corresponding keys.

    This function yields the keys to get to the analysis object, as well as the object itself. Note
    that this function is designed to be called recursively.

    As an example, consider the input:

    >>> d = {
    ...    "a1" : {
    ...        "b" : {
    ...            "c1" : "obj",
    ...            "c2" : "obj2",
    ...            "c3" : "obj3"
    ...        }
    ...    }
    ...    "a2" : {
    ...        "b" : {
    ...            "c1" : "obj",
    ...            "c2" : "obj2",
    ...            "c3" : "obj3"
    ...        }
    ...    }
    ... }
    >>> unroll = unrollNestedDict(d)
    >>> next(unroll) == (["a1", "b", "c1"], "obj")
    >>> next(unroll) == (["a1", "b", "c12"], "obj2")
    ...
    >>> next(unroll) == (["a2", "b", "c3"], "obj3") # Last result.

    Args:
        d (dict): Analysis dictionary to unroll (flatten)
        keys (list): Keys navigated to get to the analysis object
    Returns:
        tuple: (list of keys to get to the object, the object)
    """
    if keys is None:
        keys = []
    #logger.debug("d: {}".format(d))
    for k, v in d.items():
        #logger.debug("k: {}, v: {}".format(k, v))
        #logger.debug("keys: {}".format(keys))
        # We need a copy of keys before we append to ensure that we don't
        # have the final keys build up (ie. first yield [a], next [a, b], then [a, b, c], etc...)
        copyOfKeys = keys[:]
        copyOfKeys.append(k)

        if isinstance(v, dict):
            #logger.debug("v is a dict!")
            # Could be `yield from`, but then it wouldn't work in python 2.
            # We take a small performance hit here, but it's fine.
            # See: https://stackoverflow.com/a/38254338
            for val in unrollNestedDict(d = v, keys = copyOfKeys):
                yield val
        else:
            #logger.debug("Yielding {}".format(v))
            yield (copyOfKeys, v)

