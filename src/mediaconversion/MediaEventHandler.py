import signal
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler

from mediaconversion.model import MediaInfo
from model import ConverterConfig
from mediaconversion.strategy import ConverterFactory
from util import LogManager
from util.Validation import Validation


class MediaEventHandler(FileSystemEventHandler):

    __LOG = None

    _CONFIG = ConverterConfig.get_instance()

    DEFAULT_MAX_PROCESSES = 2
    DEFAULT_CONVERTER = ConverterFactory.Converters.FFMPEG

    def __init__(self, max_processes: int = DEFAULT_MAX_PROCESSES,
                 converter: ConverterFactory.Converters = DEFAULT_CONVERTER):
        super().__init__()

        MediaEventHandler.__LOG = LogManager.get_instance().get(LogManager.Logger.OBSERVER)
        self.__converter = ConverterFactory.get_type(converter)
        self.__executor = ProcessPoolExecutor(
            max_workers=max_processes,
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
            Validation.is_file(event.src_path)
        except FileNotFoundError:
            MediaEventHandler.__LOG.debug(f"[SKIPPING] '{event.src_path}': not a file")
            return

        MediaEventHandler.__LOG.debug(f"[CREATED] '{event.src_path}'")

        fileout = self.__get_fileout_from(
            event.src_path,
            MediaEventHandler._CONFIG.media_out_folder,
            MediaEventHandler._CONFIG.media_out_format.get('format')
        )
        converter_object = MediaInfo(
            event.src_path,
            MediaEventHandler._CONFIG.media_in_converted_folder,
            fileout,
            MediaEventHandler._CONFIG.media_out_format
        )
        self.__executor.submit(
            self.__converter.execute,
            converter_object
        )

    def on_deleted(self, event: FileSystemEvent) -> None:
        super().on_deleted(event)
        MediaEventHandler.__LOG.debug(f"[DELETED] '{event.src_path}'")

    def shutdown(self):
        self.__executor.shutdown(wait=True)

    @classmethod
    def __get_fileout_from(cls, filein: str, dirout: str, extension: str) -> str:
        path_filein = Path(filein)
        path_dirout = Path(dirout)
        return str(path_dirout.joinpath(path_filein.stem).with_suffix(f".{extension}"))
