import sys
from typing import List


def print_out_msg(msg_level: str, msg: str):
    print(f"[{msg_level.upper()}] {msg}")


def print_errors_list(error_name: str, errors_list: List[str]):
    error_msg = f"There are error(s) {error_name}:"
    for elt_error in errors_list:
        error_msg += f"\n- {elt_error}"
    error_msg += "\n-> STOP"
    print_out_msg(msg_level="error", msg=error_msg)
    sys.exit(1)
