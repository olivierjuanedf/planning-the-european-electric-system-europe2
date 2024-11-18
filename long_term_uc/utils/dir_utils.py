import sys
import os


def check_file_existence(file: str, file_descr: str = None):
    """
    Check existence of a given file before doing some operations on it (e.g., reading it)

    :param file: file whose existence must be checked
    :param file_descr: description of this file, used in error msg if missing
    """
    if not os.path.isfile(file):
        msg_prefix = "File" if file_descr is None else f"{file_descr} file"
        print(f"[ERROR] {msg_prefix} {file} does not exist -> STOP")
        sys.exit(1)
