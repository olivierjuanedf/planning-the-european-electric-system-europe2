from datetime import datetime
from typing import List, Optional, Tuple, Union
import numpy as np

from long_term_uc.common.constants_temporal import DAY_OF_WEEK
from long_term_uc.common.long_term_uc_io import DATE_FORMAT_PRINT


def str_sanitizer(raw_str: Optional[str], replace_empty_char: bool = True, 
                  ad_hoc_replacements: dict = None) -> Optional[str]:
    # sanitize only if str
    if isinstance(raw_str, str) is False:
        return raw_str

    sanitized_str = raw_str
    sanitized_str = sanitized_str.strip()
    if replace_empty_char is True:
        sanitized_str = sanitized_str.replace(" ", "_")
    sanitized_str = sanitized_str.lower()

    # if specific replacements to be applied
    if ad_hoc_replacements is not None:
        for old_char, new_char in ad_hoc_replacements.items():
            sanitized_str = sanitized_str.replace(old_char, new_char)
    return sanitized_str


def get_key_of_val(val, my_dict: dict, dict_name: str = None):
    corresp_keys = []
    for key in my_dict:
        if val in my_dict[key]:
            corresp_keys.append(key)
    if dict_name is None:
        dict_name = ""
    else:
        dict_name = f" {dict_name}"
    if len(corresp_keys) == 0:
        print(f"[WARNING] No corresponding key found in {dict_name} dict. for value {val} -> None returned")
        return None
    if len(corresp_keys) > 1:
        print(f"[WARNING] Multiple corresponding keys found in{dict_name} dict. for value {val} "
              f"-> only first one returned")
    return corresp_keys[0]


def get_period_str(period_start: datetime, period_end: datetime):
    dow_start = DAY_OF_WEEK[period_start.isoweekday()]
    dow_end = DAY_OF_WEEK[period_end.isoweekday()]
    period_start_str = f"{dow_start} {period_start.strftime(DATE_FORMAT_PRINT)}"
    period_end_str = f"{dow_end} {period_end.strftime(DATE_FORMAT_PRINT)}"
    return f"[{period_start_str}, {period_end_str}]"


def is_str_bool(bool_str: Optional[str]) -> bool:
    if isinstance(bool_str, str) is False:
        return False
    return bool_str.lower() in ["true", "false"]


def cast_str_bool(bool_str: str) -> Union[str, bool]:
    if is_str_bool(bool_str=bool_str) is True:
        return bool(bool_str)
    else:
        return bool_str


def are_lists_eq(list_of_lists: List[list]) -> bool:
    first_list = list_of_lists[0]
    len_first_list = len(first_list)
    set_first_list = set(first_list)
    n_lists = len(list_of_lists)
    for i_list in range(1, n_lists):
        current_list = list_of_lists[i_list]
        if (len(current_list) == len_first_list and set(current_list) == set_first_list) is False:
            return False
    return True


def lexico_compar_str(string1: str, string2: str, return_tuple: bool = False) -> Union[str, Tuple[str, str]]:
    i = 0
    while i < len(string1) and i < len(string2):
        if string1[i] < string2[i]:
            return (string1, string2) if return_tuple is True else string1
        elif string1[i] > string2[i]:
            return (string2, string1) if return_tuple is True else string2
        i += 1
    # one of the strings starts with the other
    if len(string2) > len(string1):
        return (string1, string2) if return_tuple is True else string1
    else:
        return (string2, string1) if return_tuple is True else string2


def flatten_list_of_lists(list_of_lists: List[list]) -> list:
    return np.concatenate(list_of_lists).tolist()
