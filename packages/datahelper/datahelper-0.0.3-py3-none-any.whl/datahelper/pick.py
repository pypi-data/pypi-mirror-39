from typing import Dict, List, Union

from datahelper.private.cast_path import cast_path
from datahelper.private.base_get import base_get


def pick(obj: Union[Dict[any, any], List[any]], *key) -> List[any]:
    """
    Author: DoonDoony
    Description: Pick nested dict values with dotted-decimal strings from dict type data (lodash style)
    :param obj: Dict[any]
    :param key: List[...str]
    :return: List[Union[None, any]]
    """
    paths: List[List[Union[str, int]], ...] = [selector.split('.') for selector in key]
    accumulator = []

    for path in paths:
        # if path string doesn't contain a dot character, append it directly and continue
        tmp_arr = []

        for key in path:
            key = cast_path(key)
            # Check whether the first loop, get the data from dict right away
            if not tmp_arr:
                result = base_get(obj, key)
                # If result is None (Invalid key) break the loop
                if not result:
                    break
                tmp_arr.append(result)

                # In the first loop, Append an item and continue to next path
                continue

            # From the second loop, retrieve a value from "tmp_arr" recursively
            item = tmp_arr.pop()
            tmp_arr.append(base_get(item, key))

        if not tmp_arr:
            return [None]

        accumulator.append(tmp_arr.pop())
        tmp_arr.clear()

    return accumulator
