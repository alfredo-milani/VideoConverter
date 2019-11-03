import logging
from enum import Enum, auto

from mediaconversion.strategy import FFmpeg, BaseConverter
from model import Config
from util import Common


class ConverterFactory(object):

    log = logging.getLogger(Common.MEDIA_CONVERSION_LOGGER)
    config = Config.get_instance()

    class Types(Enum):
        FFMPEG = auto()

    @classmethod
    def get_type(cls, strategy: Types) -> BaseConverter:
        if strategy is None:
            raise ValueError

        if strategy == cls.Types.FFMPEG:
            if ConverterFactory.config.ffmpeg is not None and \
                    ConverterFactory.config.ffprobe is not None:
                return FFmpeg(
                    ConverterFactory.config.ffmpeg,
                    ConverterFactory.config.ffprobe
                )
            else:
                return FFmpeg()
        else:
            raise NotImplementedError
