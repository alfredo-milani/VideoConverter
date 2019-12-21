import logging
import shutil
from pathlib import Path

from converter import Converter

from mediaconversion.strategy import BaseConverter
from mediaconversion.model import MediaInfo
from util.Common import Common
from util.Validation import Validate


class FFmpeg(BaseConverter):

    log = logging.getLogger(Common.MEDIA_CONVERSION_LOGGER)

    FFMPEG_BIN = "ffmpeg"
    FFPROBE_BIN = "ffprobe"

    def __init__(self, ffmpeg: str = FFMPEG_BIN, ffprobe: str = FFPROBE_BIN):
        super().__init__()

        if not Common.is_installed(ffmpeg) or \
                not Common.is_installed(ffprobe):
            raise FileNotFoundError("Wrong path for {} or {}".format(FFmpeg.FFMPEG_BIN, FFmpeg.FFPROBE_BIN))

        self.__converter = Converter(ffmpeg, ffprobe)

    def prepare(self, media_info: MediaInfo) -> None:
        super().prepare(media_info)
        super()._wait_file(media_info)

    def convert(self, media_info: MediaInfo) -> None:
        """
        This method uses ffmpeg and ffprobe tool, which MUST BE installed on the system
        Visit http://ffmpeg.org/ or https://ffbinaries.com/downloads to download the tool
        :param media_info: object which incapsulate infformation for strategy
        """
        probe = self.__converter.probe(media_info.filein)
        FFmpeg.log.debug("Probing '{}': {}".format(media_info.filein, probe))
        Validate.not_null(
            probe,
            "Probing failed: '{}' is not a valid media file".format(media_info.filein)
        )

        FFmpeg.log.info("Conversion started '{}'".format(media_info.filein))
        conversion = self.__converter.convert(
            media_info.filein,
            media_info.fileout,
            media_info.out_format
        )

        for _ in conversion:
            pass

    def on_error(self, media_info: MediaInfo = None, exception: Exception = None) -> None:
        super().on_error(media_info, exception)
        FFmpeg.log.warning("Conversion error '{}'".format(media_info.filein))
        FFmpeg.log.debug("Conversion error", exc_info=True)

        try:
            Validate.is_file(media_info.fileout)
            Path(media_info.fileout).unlink()
            FFmpeg.log.debug("Removed half parsed file '{}'".format(media_info.fileout))
        except FileNotFoundError:
            pass

    def on_success(self, media_info: MediaInfo = None) -> None:
        super().on_success(media_info)
        FFmpeg.log.info("Conversion completed '{}'".format(media_info.filein))

        filein_converted_folder = media_info.filein_converted_folder
        if filein_converted_folder is None:  # no action
            return
        elif filein_converted_folder == "":  # remove file
            Path(media_info.filein).unlink()
        else:  # move file in the specified directory
            filein_converted_path = Path(filein_converted_folder)

            filein_path = Path(media_info.filein)
            fileout_path = filein_converted_path.joinpath(filein_path.name)

            shutil.move(filein_path, fileout_path)
