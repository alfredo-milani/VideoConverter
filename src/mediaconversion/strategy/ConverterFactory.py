from enum import Enum, auto

from mediaconversion.strategy import FFmpeg, BaseConverter
from model import ConverterConfig


class ConverterFactory(object):

    _CONFIG = ConverterConfig.get_instance()

    class Types(Enum):
        FFMPEG = auto()

    @classmethod
    def get_type(cls, strategy: Types) -> BaseConverter:
        if strategy is None:
            raise ValueError

        if strategy == cls.Types.FFMPEG:
            if ConverterFactory._CONFIG.media_ffmpeg is not None and \
                    ConverterFactory._CONFIG.media_ffprobe is not None:
                return FFmpeg(
                    ConverterFactory._CONFIG.media_ffmpeg,
                    ConverterFactory._CONFIG.media_ffprobe
                )
            else:
                return FFmpeg()
        else:
            raise NotImplementedError
