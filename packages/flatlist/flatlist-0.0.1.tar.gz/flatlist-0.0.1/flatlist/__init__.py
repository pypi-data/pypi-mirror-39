__version__ = '0.0.1'


def flatten_list(input_list):
    """
    Flattens list with many nested lists.

    >>> flatten_list([1, [2, [3], [4]]])
    [1, 2, 3, 4]
    """
    result = []
    for item in input_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
            # yield from flatten_list(item)
        else:
            result.append(item)
            # yield item

    return result
