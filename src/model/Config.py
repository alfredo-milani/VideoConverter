# -*- coding: utf-8 -*-
import ast
import configparser
import pathlib
import threading


class Config(dict):
    """

    """

    # Section
    S_GENERAL = "general"
    # Keys
    K_TMP = "tmp"
    V_DEFAULT_TMP = "/tmp"
    K_PROCESSES = "processes"
    V_DEFAULT_PROCESSES = 2

    # Section
    S_MEDIA = "media"
    # Keys
    K_IN_FOLDER = "in.folder"
    V_DEFAULT_IN_FOLDER = V_DEFAULT_TMP
    K_IN_CONVERTED_FOLDER = "in.converted.folder"
    V_DEFAULT_IN_CONVERTED_FOLDER = None
    K_OUT_FOLDER = "out.folder"
    V_DEFAULT_OUT_FOLDER = V_DEFAULT_TMP + "/VideoConverter/converted"
    K_OUT_FORMAT = "out.format"
    V_DEFAULT_OUT_FORMAT = None
    K_OBSERVING_TIMEOUT = "obs-timeout"
    V_DEFAULT_OBSERVING_TIMEOUT = 1
    K_FFMPEG_BIN = "ffmpeg"
    V_DEFAULT_FFMPEG_BIN = None
    K_FFPROBE_BIN = "ffprobe"
    V_DEFAULT_FFPROBE_BIN = None

    class ConfigException(Exception):
        """

        """

        def __init__(self, *args):
            super().__init__("Non può essere creata più di una istanza della classe {}".format(str(*args)))

    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if Config.__instance is not None:
            raise Config.ConfigException(Config)
        else:
            super().__init__()

            Config.__instance = self
            self.__configparser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

    @classmethod
    def get_instance(cls) -> "Config":
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    Config()
        return cls.__instance

    def __str__(self):
        return "### Configuration:\n" + \
               "".join("\t[ {} : {} ]\n".format(k, v) for k, v in self.items())

    # Called if: Config + "string"
    def __add__(self, other):
        return str(self) + other

    # Called if: "string" + Config
    def __radd__(self, other):
        return other + str(self)

    def load_from(self, config_file: str) -> None:
        path = pathlib.Path(config_file)
        if not path.exists() or not path.is_file():
            raise IOError("File '{}' not exists".format(config_file))

        self.__configparser.read(config_file)
        self.__upload_config()

    def __upload_config(self):
        # section general
        self.__put_str(Config.K_TMP, Config.S_GENERAL, Config.K_TMP)
        self.__put_int(Config.K_PROCESSES, Config.S_GENERAL, Config.K_PROCESSES)

        # section media
        self.__put_str(Config.K_IN_FOLDER, Config.S_MEDIA, Config.K_IN_FOLDER)
        self.__put_str(Config.K_IN_CONVERTED_FOLDER, Config.S_MEDIA, Config.K_IN_CONVERTED_FOLDER)
        self.__put_str(Config.K_OUT_FOLDER, Config.S_MEDIA, Config.K_OUT_FOLDER)
        self.__put_dict(Config.K_OUT_FORMAT, Config.S_MEDIA, Config.K_OUT_FORMAT)
        self.__put_float(Config.K_OBSERVING_TIMEOUT, Config.S_MEDIA, Config.K_OBSERVING_TIMEOUT)
        self.__put_str(Config.K_FFMPEG_BIN, Config.S_MEDIA, Config.K_FFMPEG_BIN)
        self.__put_str(Config.K_FFPROBE_BIN, Config.S_MEDIA, Config.K_FFPROBE_BIN)

    def __put_obj(self, key, section, section_key):
        try:
            self[key] = self.__configparser.get(section, section_key)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def __put_str(self, key, section, section_key):
        try:
            self[key] = str(self.__configparser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def __put_int(self, key, section, section_key):
        try:
            self[key] = int(self.__configparser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def __put_float(self, key, section, section_key):
        try:
            self[key] = float(self.__configparser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def __put_dict(self, key, section, section_key):
        try:
            self[key] = ast.literal_eval(self.__configparser.get(section, section_key))
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    @property
    def general_tmp(self) -> str:
        return self.get(Config.K_TMP, Config.V_DEFAULT_TMP)

    @property
    def general_processes(self) -> int:
        return self.get(Config.K_PROCESSES, Config.V_DEFAULT_PROCESSES)

    @property
    def media_in_folder(self) -> str:
        return self.get(Config.K_IN_FOLDER, Config.V_DEFAULT_IN_FOLDER)

    @property
    def media_in_converted_folder(self) -> str:
        return self.get(Config.K_IN_CONVERTED_FOLDER, Config.V_DEFAULT_IN_CONVERTED_FOLDER)

    @property
    def media_out_folder(self) -> str:
        return self.get(Config.K_OUT_FOLDER, Config.V_DEFAULT_OUT_FOLDER)

    @property
    def media_out_format(self) -> dict:
        return self.get(Config.K_OUT_FORMAT, Config.V_DEFAULT_OUT_FORMAT)

    @property
    def observing_timeout(self) -> float:
        return self.get(Config.K_OBSERVING_TIMEOUT, Config.V_DEFAULT_OBSERVING_TIMEOUT)

    @property
    def ffmpeg(self) -> str:
        return self.get(Config.K_FFMPEG_BIN, Config.V_DEFAULT_FFMPEG_BIN)

    @property
    def ffprobe(self) -> str:
        return self.get(Config.K_FFPROBE_BIN, Config.V_DEFAULT_FFPROBE_BIN)
