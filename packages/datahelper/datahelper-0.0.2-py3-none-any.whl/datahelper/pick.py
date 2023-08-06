from typing import Dict, List, Union


def pick(obj: Dict[any, any], *key) -> List[any]:
    """
    Author: DoonDoony
    Description: Pick nested dict values with dotted-decimal strings from dict type data (lodash style)
    :param obj: Dict[any]
    :param key: List[...str]
    :return: List[Union[None, any]]
    """
    paths: List[List[Union[str, int]], ...] = [selector.split('.') for selector in key]
    accumulator = []

    for selector in paths:
        # if path string doesn't contain a dot character, append it directly and continue
        if len(selector) == 1:
            accumulator.append(obj.get(selector.pop()))
            continue

        tmp_arr = []

        for key in selector:
            # Check whether the first loop, get the data from dict right away
            if not tmp_arr:
                result = obj.get(key)
                # If result is None (Invalid key) break the loop
                if not result:
                    break
                tmp_arr.append(result)

                # In the first loop, Append an item and continue to next path
                continue

            # From the second loop, retrieve a value from "tmp_arr" recursively
            item = tmp_arr.pop()

            # Support extract value from List type data
            if isinstance(item, list):
                tmp_arr.append(item[int(key)])
            else:
                tmp_arr.append(item.get(key))

        accumulator.append(tmp_arr.pop())
        tmp_arr.clear()

    return accumulator
