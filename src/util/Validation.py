import os
import sys
from pathlib import Path


class Validation(object):
    """

    """

    @staticmethod
    def not_none(val: object, msg: str = "") -> None:
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
    def key_exists(val: dict, key: object, msg: str = "") -> None:
        try:
            val[key]
        except KeyError:
            raise KeyError(msg)

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
            raise ValidationException.LinkError(msg)

    @staticmethod
    def are_symlinks(val1: str, val2: str, msg: str = "") -> None:
        if Path(val1).resolve() == Path(val2).resolve():
            raise ValidationException.SymLinksError(msg)

    @staticmethod
    def can_read(val: str, msg: str = "") -> None:
        if not os.access(val, os.R_OK):
            raise PermissionError(msg)

    @staticmethod
    def can_write(val: str, msg: str = "") -> None:
        if not os.access(val, os.W_OK):
            raise PermissionError(msg)

    @staticmethod
    def is_file_readable(val: str, msg: str = "") -> None:
        Validation.is_file(val, msg)
        Validation.can_read(val, msg)

    @staticmethod
    def is_dir_writeable(val: str, msg: str = "") -> None:
        Validation.is_dir(val, msg)
        Validation.can_write(val, msg)

    @staticmethod
    def is_empty(val: str, msg: str = "") -> None:
        if val in ("", None):
            raise ValueError(msg)

    @staticmethod
    def has_extension(val: str, msg: str = ""):
        if '.' not in val:
            raise ValidationException.MissingExtensionError(msg)

    @staticmethod
    def python_version(min_version: tuple, msg: str = "") -> None:
        actual_version = sys.version_info
        for v in min_version:
            if actual_version[min_version.index(v)] < int(v):
                raise ValidationException.PythonVersionError(msg)

    @staticmethod
    def is_installed(binary: str, msg: str = "") -> None:
        """
        Check whether binary is on PATH and marked as executable

        :param binary: binary to check
        :param msg: message to pass to exception
        :raise: FileNotFoundError iff binary is not in PATH
        """
        from shutil import which
        if which(binary) is None:
            raise FileNotFoundError(msg)


class ValidationException(object):

    class BaseException(Exception):

        def __init__(self, *args, **kwargs):
            super().__init__(args, kwargs)

        def __str__(self):
            if len(self.args) == 0:
                return ""
            if len(self.args) == 1:
                return str(self.args[0])
            return str(self.args[0][0])

    class LinkError(BaseException):

        def __init__(self, *args, **kwargs):
            super().__init__(args, kwargs)

    class SymLinksError(BaseException):

        def __init__(self, *args, **kwargs):
            super().__init__(args, kwargs)

    class PythonVersionError(BaseException):

        def __init__(self, *args, **kwargs):
            super().__init__(args, kwargs)

    class MissingExtensionError(BaseException):

        def __init__(self, *args, **kwargs):
            super().__init__(args, kwargs)
