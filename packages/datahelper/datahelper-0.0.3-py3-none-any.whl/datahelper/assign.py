from typing import Union, List, Dict

from datahelper.private.base_assign import base_assign


def assign(obj: Union[Dict[any, any], List[any]], paths: Union[str, int, List[any]], value: any) -> Union[
    List[any], Dict[any, any]]:
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
    return base_assign(obj, paths, value)
