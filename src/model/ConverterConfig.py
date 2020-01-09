import ast
import configparser
import pathlib
import threading
from datetime import date

import __version__
from util import Common, Validation


class ConverterConfig(dict):
    """

    """

    __INSTANCE = None
    __LOCK = threading.Lock()

    # Intern
    K_VERSION = "version"
    V_DEFAULT_VERSION = __version__.__version__
    K_APP_NAME = "app_name"
    V_DEFAULT_APP_NAME = "VideoConverter"
    K_LOG_FILENAME = "log.filename"
    V_DEFAULT_LOG_FILENAME = None

    # Section
    S_GENERAL = "GENERAL"
    # Keys
    K_LOG_DIR = "log.dir"
    V_DEFAULT_LOG_DIR = None
    K_TMP = "tmp"
    V_DEFAULT_TMP = "/tmp"
    K_PROCESSES = "processes"
    V_DEFAULT_PROCESSES = 2

    # Section
    S_MEDIA = "MEDIA"
    # Keys
    K_IN_FOLDER = "in.folder"
    V_DEFAULT_IN_FOLDER = None
    K_IN_CONVERTED_FOLDER = "in.converted_folder"
    V_DEFAULT_IN_CONVERTED_FOLDER = None
    K_IN_TIMEOUT = "in.timeout"
    V_DEFAULT_IN_TIMEOUT = 1
    K_OUT_FOLDER = "out.folder"
    V_DEFAULT_OUT_FOLDER = None
    K_OUT_FORMAT = "out.format"
    V_DEFAULT_OUT_FORMAT = None
    K_FFMPEG_BIN = "ffmpeg"
    V_DEFAULT_FFMPEG_BIN = None
    K_FFPROBE_BIN = "ffprobe"
    V_DEFAULT_FFPROBE_BIN = None

    def __init__(self):
        if ConverterConfig.__INSTANCE is not None:
            raise ConverterConfig.MultipleInstancesException(ConverterConfig)

        super().__init__()

        ConverterConfig.__INSTANCE = self
        self.__config_parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.__upload_config()

    @classmethod
    def get_instance(cls) -> "ConverterConfig":
        if cls.__INSTANCE is None:
            with cls.__LOCK:
                if cls.__INSTANCE is None:
                    ConverterConfig()
        return cls.__INSTANCE

    def load_from(self, config_file: str) -> None:
        """

        :param config_file:
        :raise: SyntaxError if there is a syntax error in configuration file
        """
        Validation.is_file_readable(
            config_file,
            f"File '{config_file}' *must* exists and be readable"
        )

        with self.__LOCK:
            self.__config_parser.read(config_file)
            self.__upload_config()

    def __upload_config(self):
        """

        :raise: SyntaxError if there is a syntax error in configuration file
        """
        # section [GENERAL]
        self.__put_str(ConverterConfig.K_LOG_DIR, ConverterConfig.S_GENERAL, ConverterConfig.K_LOG_DIR, ConverterConfig.V_DEFAULT_LOG_DIR)
        self.__put_str(ConverterConfig.K_TMP, ConverterConfig.S_GENERAL, ConverterConfig.K_TMP, ConverterConfig.V_DEFAULT_TMP)
        self.__put_int(ConverterConfig.K_PROCESSES, ConverterConfig.S_GENERAL, ConverterConfig.K_PROCESSES, ConverterConfig.V_DEFAULT_PROCESSES)

        # section [MEDIA]
        self.__put_str(ConverterConfig.K_IN_FOLDER, ConverterConfig.S_MEDIA, ConverterConfig.K_IN_FOLDER, ConverterConfig.V_DEFAULT_IN_FOLDER)
        self.__put_str(ConverterConfig.K_IN_CONVERTED_FOLDER, ConverterConfig.S_MEDIA, ConverterConfig.K_IN_CONVERTED_FOLDER, ConverterConfig.V_DEFAULT_IN_CONVERTED_FOLDER)
        self.__put_float(ConverterConfig.K_IN_TIMEOUT, ConverterConfig.S_MEDIA, ConverterConfig.K_IN_TIMEOUT, ConverterConfig.V_DEFAULT_IN_TIMEOUT)
        self.__put_str(ConverterConfig.K_OUT_FOLDER, ConverterConfig.S_MEDIA, ConverterConfig.K_OUT_FOLDER, ConverterConfig.V_DEFAULT_OUT_FOLDER)
        self.__put_dict(ConverterConfig.K_OUT_FORMAT, ConverterConfig.S_MEDIA, ConverterConfig.K_OUT_FORMAT, ConverterConfig.V_DEFAULT_OUT_FORMAT)
        self.__put_str(ConverterConfig.K_FFMPEG_BIN, ConverterConfig.S_MEDIA, ConverterConfig.K_FFMPEG_BIN, ConverterConfig.V_DEFAULT_FFMPEG_BIN)
        self.__put_str(ConverterConfig.K_FFPROBE_BIN, ConverterConfig.S_MEDIA, ConverterConfig.K_FFPROBE_BIN, ConverterConfig.V_DEFAULT_FFPROBE_BIN)

        # intern
        self.__put_str(ConverterConfig.K_VERSION, '', '', ConverterConfig.V_DEFAULT_VERSION)
        self.__put_str(ConverterConfig.K_APP_NAME, '', '', ConverterConfig.V_DEFAULT_APP_NAME)
        if self.general_log_dir is not None:
            from datetime import date
            self.__put_str(ConverterConfig.K_LOG_FILENAME, '', '', f"{self.general_log_dir}/{self.app_name}_{date.today().strftime('%d%m%Y')}.log")
        else:
            self.__put_str(ConverterConfig.K_LOG_FILENAME, '', '', ConverterConfig.V_DEFAULT_LOG_FILENAME)

    def __put_obj(self, key: str, section: str, section_key: str, default: object = None) -> None:
        try:
            self[key] = self.__config_parser.get(section, section_key)
        except (configparser.NoOptionError, configparser.NoSectionError):
            self[key] = default

    def __put_str(self, key: str, section: str, section_key: str, default: str = None) -> None:
        try:
            self[key] = str(self.__config_parser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            self[key] = default

    def __put_int(self, key: str, section: str, section_key: str, default: int = None) -> None:
        try:
            self[key] = int(self.__config_parser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            self[key] = default

    def __put_float(self, key: str, section: str, section_key: str, default: float = None) -> None:
        try:
            self[key] = float(self.__config_parser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            self[key] = default

    def __put_tuple(self, key: str, section: str, section_key: str, default: tuple = None) -> None:
        try:
            self[key] = tuple(self.__config_parser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            self[key] = default

    def __put_dict(self, key: str, section: str, section_key: str, default: dict = None) -> None:
        """

        :param key:
        :param section:
        :param section_key:
        :param default:
        :raise: SyntaxError if ast.literal_eval(node_or_string) fails parsing
            input string (syntax error in key/value pairs)
        """
        try:
            self[key] = ast.literal_eval(self.__config_parser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            self[key] = default

    def __put_bool(self, key: str, section: str, section_key: str, default: bool = None) -> None:
        try:
            self[key] = bool(self.__config_parser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            self[key] = default

    @property
    def version(self):
        return self.get(ConverterConfig.K_VERSION)

    @property
    def app_name(self) -> str:
        return self.get(ConverterConfig.K_APP_NAME)

    @property
    def log_filename(self) -> str:
        return self.get(ConverterConfig.K_LOG_FILENAME)

    @property
    def general_log_dir(self) -> str:
        return self.get(ConverterConfig.K_LOG_DIR)

    @property
    def general_tmp(self) -> str:
        return self.get(ConverterConfig.K_TMP)

    @property
    def general_processes(self) -> int:
        return self.get(ConverterConfig.K_PROCESSES)

    @property
    def media_in_folder(self) -> str:
        return self.get(ConverterConfig.K_IN_FOLDER)

    @property
    def media_in_converted_folder(self) -> str:
        return self.get(ConverterConfig.K_IN_CONVERTED_FOLDER)

    @property
    def media_in_timeout(self) -> float:
        return self.get(ConverterConfig.K_IN_TIMEOUT)

    @property
    def media_out_folder(self) -> str:
        return self.get(ConverterConfig.K_OUT_FOLDER, ConverterConfig.V_DEFAULT_OUT_FOLDER)

    @property
    def media_out_format(self) -> dict:
        return self.get(ConverterConfig.K_OUT_FORMAT, ConverterConfig.V_DEFAULT_OUT_FORMAT)

    @property
    def media_ffmpeg(self) -> str:
        return self.get(ConverterConfig.K_FFMPEG_BIN)

    @property
    def media_ffprobe(self) -> str:
        return self.get(ConverterConfig.K_FFPROBE_BIN)

    def __str__(self):
        # chr(9) = '\t'
        # chr(10) = '\n'
        return f"### Configuration for {self.__class__.__name__}: " \
               f"{str().join(f'{chr(10)}{chr(9)}{{ {k} : {v} }}' for k, v in self.items())}"

    # Called if: Config + "string"
    def __add__(self, other):
        return str(self) + other

    # Called if: "string" + Config
    def __radd__(self, other):
        return other + str(self)

    class MultipleInstancesException(Exception):
        """

        """

        def __init__(self, *args):
            super().__init__(f"Singleton instance: a second instance of {args[0]} can not be created")

        def __str__(self):
            if len(self.args) == 0:
                return ""
            if len(self.args) == 1:
                return str(self.args[0])
            return str(self.args[0][0])
