import logging
import signal
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path

from watchdog.events import PatternMatchingEventHandler, FileSystemEvent

from mediaconversion.model import MediaInfo
from model import Config
from mediaconversion.strategy import ConverterFactory, FFmpeg
from util import Common
from util.Validation import Validate


class MediaEventHandler(PatternMatchingEventHandler):

    log = logging.getLogger(Common.MEDIA_CONVERSION_LOGGER)
    config = Config.get_instance()

    def __init__(self, patterns=None, ignore_patterns=None,
                 ignore_directories=False, case_sensitive=False):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)

        self.__converter = ConverterFactory.get_type(ConverterFactory.Types.FFMPEG)
        self.__executor = ProcessPoolExecutor(
            max_workers=MediaEventHandler.config.general_processes,
            initializer=MediaEventHandler.__init_worker
        )

    @classmethod
    def __init_worker(cls) -> None:
        """
        Workaround for managing Python's bug: while on wait syscall, KeyboardInterrupt is not handled
        Prevent the child processes from ever receiving KeyboardInterrupt and leaving it
         completely up to the parent process to catch the interrupt and clean up
         the process pool.
        :author: John Reese, https://noswap.com/blog/python-multiprocessing-keyboardinterrupt
         and https://github.com/jreese/multiprocessing-keyboardinterrupt
        """
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def on_created(self, event: FileSystemEvent) -> None:
        super().on_created(event)
        try:
            Validate.is_file(event.src_path)
        except FileNotFoundError:
            MediaEventHandler.log.debug("Object created is not file '{}'). Skipping...".format(event.src_path))
            return

        MediaEventHandler.log.debug("File created '{}'".format(event.src_path))

        fileout = self.__get_fileout_from(
            event.src_path,
            MediaEventHandler.config.media_out_folder,
            MediaEventHandler.config.media_out_format.get('format')
        )
        converter_object = MediaInfo(
            event.src_path,
            MediaEventHandler.config.media_in_converted_folder,
            fileout,
            MediaEventHandler.config.media_out_format
        )
        self.__executor.submit(
            self.__converter.execute,
            converter_object
        )

    def on_deleted(self, event: FileSystemEvent) -> None:
        super().on_deleted(event)
        MediaEventHandler.log.debug("File removed '{}'".format(event.src_path))

    def shutdown(self):
        self.__executor.shutdown(wait=True)

    @classmethod
    def __get_fileout_from(cls, filein: str, dirout: str, extension: str) -> str:
        path_filein = Path(filein)
        path_dirout = Path(dirout)
        return str(path_dirout.joinpath(path_filein.stem).with_suffix(".{}".format(extension)))
