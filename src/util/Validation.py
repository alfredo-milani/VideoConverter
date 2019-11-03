import os
import sys
from pathlib import Path


class Validate(object):
    """

    """

    @staticmethod
    def not_null(val: object, msg: str = "") -> None:
        if val is None:
            raise TypeError(msg)

    @staticmethod
    def is_true(val: bool, msg: str = "") -> None:
        if not val:
            raise ValueError(msg)

    @staticmethod
    def is_int(val: object, msg: str = "") -> None:
        if type(val) != int:
            raise TypeError(msg)

    @staticmethod
    def is_float(val: object, msg: str = "") -> None:
        if type(val) != float:
            raise TypeError(msg)

    @staticmethod
    def is_str(val: object, msg: str = "") -> None:
        if type(val) != str:
            raise TypeError(msg)

    @staticmethod
    def is_list(val: object, msg: str = "") -> None:
        if type(val) != list:
            raise TypeError(msg)

    @staticmethod
    def is_tuple(val: object, msg: str = "") -> None:
        if type(val) != tuple:
            raise TypeError(msg)

    @staticmethod
    def is_dict(val: object, msg: str = "") -> None:
        if type(val) != dict:
            raise TypeError(msg)

    @staticmethod
    def path_exists(val: str, msg: str = "") -> None:
        if not Path(val).resolve().exists():
            raise FileNotFoundError(msg)

    @staticmethod
    def is_dir(val: str, msg: str = "") -> None:
        if not Path(val).resolve().is_dir():
            raise NotADirectoryError(msg)

    @staticmethod
    def is_file(val: str, msg: str = "") -> None:
        if not Path(val).resolve().is_file():
            raise FileNotFoundError(msg)

    @staticmethod
    def is_link(val: str, msg: str = "") -> None:
        if not Path(val).resolve().is_symlink():
            raise Validate.Errors.LinkError(msg)

    @staticmethod
    def are_symlinks(val1: str, val2: str, msg: str = "") -> None:
        path1 = Path(val1)
        path2 = Path(val2)
        if path1.resolve() == path2.resolve():
            raise Validate.Errors.LinksError(msg)

    @staticmethod
    def can_read(val: str, msg: str = "") -> None:
        if not os.access(val, os.R_OK):
            raise PermissionError(msg)

    @staticmethod
    def can_write(val: str, msg: str = "") -> None:
        if not os.access(val, os.W_OK):
            raise PermissionError(msg)

    @staticmethod
    def python_version(min_version: tuple, msg: str = "") -> None:
        actual_version = sys.version_info
        for v in min_version:
            if actual_version[min_version.index(v)] < int(v):
                raise Validate.Errors.PythonVersionError(msg)

    class Errors(object):

        class LinkError(Exception):

            def __init__(self, *args, **kwargs):
                super().__init__(args, kwargs)

        class LinksError(Exception):

            def __init__(self, *args, **kwargs):
                super().__init__(args, kwargs)

        class PythonVersionError(Exception):

            def __init__(self, *args, **kwargs):
                super().__init__(args, kwargs)
