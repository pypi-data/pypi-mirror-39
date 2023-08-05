def table_mapping(source, maps=None, transform=None, keys=None):
    return [dict_mapping(x, maps, transform, keys) for x in source]


def dict_mapping(source, maps=None, transform=None, keys=None):
    if not maps:
        maps = {}
    if not transform:
        transform = {}
    if not keys:
        keys = []
    trans = lambda key: transform.get(key, lambda identical: identical)
    mapping = lambda k: dict([(maps.get(key, key), trans(key)(value)) for (key, value) in k.items()])
    return dict_reduce(mapping(source), keys)


def dict_reduce(source, keys):
    if len(keys) == 0:
        return source
    return dict([(key, value) for (key, value) in source.items() if key in keys])
