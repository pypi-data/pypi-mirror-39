def lookup(dictionary:dict, key, default=None):
    return dictionary[key] if key in dictionary else default

def merge(*dictionaries):
    merged = {}
    for dictionary in dictionaries:
        merged.update(dictionary)
    return merged

def take(keys, dictionary):
    '''Filters dictionary for specified keys

    Args:
        keys (list): a list of dictionary keys
        dictionary (dict): a dictionary of which to filter

    Returns:
        filtered (dict): the provided dictionary filtered to only contain keys.
    '''
    return {k: dictionary[k] for k in filter(lambda k: k in keys, dictionary)}

def drop(keys, dictionary):
        '''Filters dictionary for specified keys

        Args:
            keys (list): a list of dictionary keys
            dictionary (dict): a dictionary of which to filter

        Returns:
            filtered (dict): the provided dictionary filtered to not contain
            keys.
        '''
    return {k: dictionary[k] for k in filter(lambda k: k not in keys, dictionary)}


def safe_merge(*dictionaries):
    return take(dictionaries[0].keys(), merge(*dictionaries))
