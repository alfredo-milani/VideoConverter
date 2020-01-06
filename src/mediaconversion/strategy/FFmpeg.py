import logging
import shutil
from pathlib import Path

from converter import Converter

from mediaconversion.strategy import BaseConverter
from mediaconversion.model import MediaInfo
from util import LogManager
from util.Common import Common
from util.Validation import Validation


class FFmpeg(BaseConverter):

    __LOG = logging.getLogger(LogManager.Logger.CONVERTER.value)

    FFMPEG_BIN = "ffmpeg"
    FFPROBE_BIN = "ffprobe"

    def __init__(self, ffmpeg: str = FFMPEG_BIN, ffprobe: str = FFPROBE_BIN):
        super().__init__()

        if not Common.is_installed(ffmpeg) or \
                not Common.is_installed(ffprobe):
            raise FileNotFoundError(f"Wrong path for {FFmpeg.FFMPEG_BIN} or {FFmpeg.FFPROBE_BIN}")

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
        FFmpeg.__LOG.debug(f"[CONVERTING] '{media_info.filein}'")

        probe = self.__converter.probe(media_info.filein)
        FFmpeg.__LOG.debug(f"[PROBING] '{media_info.filein}': {probe}")
        Validation.not_none(
            probe,
            f"Probing failed: '{media_info.filein}' is not a valid media file"
        )

        FFmpeg.__LOG.info(f"[CONVERSION STARTED] '{media_info.filein}'")
        conversion = self.__converter.convert(
            media_info.filein,
            media_info.fileout,
            media_info.out_format
        )

        for _ in conversion:
            pass

    def on_success(self, media_info: MediaInfo = None) -> None:
        super().on_success(media_info)
        FFmpeg.__LOG.debug(f"[CONVERSION SUCCESS] '{media_info.filein}'")

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

    def on_error(self, media_info: MediaInfo = None, exception: Exception = None) -> None:
        super().on_error(media_info, exception)
        FFmpeg.__LOG.warning(f"[CONVERSION ERROR] '{media_info.filein}'")
        FFmpeg.__LOG.debug("[CONVERSION ERROR]", exc_info=True)

        try:
            Validation.is_file(media_info.fileout)
            Path(media_info.fileout).unlink()
            FFmpeg.__LOG.debug(f"Removed half parsed file '{media_info.fileout}'")
        except FileNotFoundError:
            pass
