from typing import Union, List, Dict

from datahelper.lib import represent_int


def assign(obj: Union[Dict[any, any], List[any]], paths: Union[str, int, List[any]], value: any) -> Union[List[any], Dict[any, any]]:
    """
    Author: DoonDoony
    Description: Set nested dict values with dotted-decimal strings from dict type data (lodash style)
    If path is int and target is not a list, create a list and change original value
    If path is str and target is not a dict, create a dict and change original value
    :param obj: Union[Dict[any, any], List[any]]
    :param paths: Union[str, List[any]]
    :param value: any
    :return: Union[List[any], Dict[any, any]]
    """
    # paths is last
    if isinstance(paths, list) and len(paths) == 1:
        key = paths.pop()
        if represent_int(key):
            if isinstance(obj, dict):
                return [value]
            if isinstance(obj, list):
                index = int(key)
                if len(obj) > index:
                    arr = obj.copy()
                    arr[index] = value
                    return arr
                if obj and len(obj) <= index:
                    return [*obj, value]
                else:
                    return [value]
        else:
            if isinstance(obj, dict) and obj:
                obj.update({key: value})
                return obj
            if isinstance(obj, dict) and not obj:
                return {key: value}
            if isinstance(obj, dict) and obj and key not in obj:
                new_obj = obj.copy()
                return {**new_obj, key: value}
            if not isinstance(obj, dict):
                return {key: value}

    # paths 가 문자열이면서, 속성 값이 하나뿐일때
    if isinstance(paths, str) and '.' not in paths:
        new_obj = obj.copy()
        return {**new_obj, paths: value}

    # type of paths is integer and paths is not dotted-decimal string
    if isinstance(paths, int) and '.' not in paths:
        # check obj is type of list
        if isinstance(obj, list):
            # if obj is empty return list which has one element
            if not obj:
                return [value]
            # if list index is greater than length of list
            if obj and len(obj) <= paths:
                arr = obj.copy()
                arr.insert(paths, value)
                return arr
            # if list index is smaller than length of list
            if obj and len(obj) > paths:
                arr = obj.copy()
                arr[paths] = value
                return arr
        if isinstance(obj, dict):
            raise KeyError

    tmp_list = []

    if isinstance(paths, str):
        split = paths.split('.')
        for piece in split:
            if represent_int(piece):
                tmp_list.append(int(piece))
                continue
            tmp_list.append(piece)

    tmp_list.reverse()
    new_paths = tmp_list and tmp_list.copy() or paths
    path = new_paths.pop()

    # if obj is dict and has attribute
    if isinstance(obj, dict) and path in obj:
        new_obj = obj.copy()
        return {**new_obj, path: assign(obj[path], new_paths, value)}
    # if obj is dict and hasn't attribute
    if isinstance(obj, dict) and path not in obj:
        if new_paths and isinstance(new_paths[-1], int):
            return {path: assign([], new_paths, value)}
        return {path: assign({}, new_paths, value)}
    # list and path is str
    if isinstance(obj, list) and isinstance(path, str):
        return {path: assign({}, new_paths, value)}
    # list and path is int
    if isinstance(obj, list) and isinstance(path, int):
        if obj and len(obj) - 1 == path:
            if isinstance(new_paths[-1], int):
                return [*obj[:path], assign([], new_paths, value)]
            return [*obj[:path], assign({}, new_paths, value)]
        if obj and len(obj) <= path:
            if isinstance(new_paths[-1], int):
                return [*obj, assign([], new_paths, value)]
            return [*obj, assign({}, new_paths, value)]
        if not obj:
            if isinstance(new_paths[-1], int):
                return [assign([], new_paths, value)]
            return [assign({}, new_paths, value)]
        if obj and len(obj) >= path:
            if isinstance(new_paths[-1], int):
                return [obj[:path], assign([], new_paths, value), obj[path: + 1]]
            return [obj[:path], assign({}, new_paths, value), obj[path: + 1]]
    # list and has index
    if isinstance(obj, list) and path < len(obj):
        return [*obj[:path], assign(obj[path], new_paths, value), *obj[path + 1:]]
    # empty list
    if isinstance(obj, list) and not obj:
        return [assign([], new_paths, value)]
    # obj is primary and path is int:
    if not (isinstance(obj, list) or isinstance(obj, dict)) and isinstance(path, int):
        return [assign([], new_paths, value)]
    # obj is primary and path is str:
    if not (isinstance(obj, list) or isinstance(obj, dict)) and isinstance(path, str):
        return {path: assign({}, new_paths, value)}
