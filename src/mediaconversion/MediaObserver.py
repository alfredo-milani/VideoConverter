from pathlib import Path

from watchdog.observers import Observer

import __version__
from mediaconversion.MediaEventHandler import MediaEventHandler
from model import ConverterConfig
from util import LogManager
from util.Validation import Validation


class MediaObserver(object):
    """
    This class provide observable behavior for specified directory.
    Files within this directory will be converted in the specified format, if possible.
    """

    # TODO
    #  - add verbose and debug cli option
    #  - unit test

    __LOG = None

    PY_VERSION_MIN = (3, 7)
    OBSERVING_TIMEOUT = 1

    def __init__(self, converter_config: ConverterConfig):
        """

        :param converter_config:
        :raise:
        """
        super().__init__()

        print(f"version: {__version__.__version__}")

        # Validate python version
        Validation.python_version(MediaObserver.PY_VERSION_MIN, f"Python version required >= {MediaObserver.PY_VERSION_MIN}")

        self.__converter_config = converter_config

        # Load loggers
        self.__init_loggers(converter_config.general_log_config_file)
        # Check permissions
        self.__check_permissions()

        self.__observer = Observer(timeout=converter_config.media_in_timeout)
        self.__event_handler = MediaEventHandler(converter_config.general_processes)

    @classmethod
    def __init_loggers(cls, log_filename: str) -> None:
        log_manager = LogManager.get_instance()
        log_manager.load(log_filename)
        MediaObserver.__LOG = log_manager.get(LogManager.Logger.OBSERVER)

    def __check_permissions(self):
        """
        Check permissions on directories before performing the operations

        :raise ValueError if input directory is equal to output directory
        :raise NotADirectoryError
        :raise PermissionError
        :raise LinksError
        """
        media_in_folder = self.__converter_config.media_in_folder
        media_out_folder = self.__converter_config.media_out_folder
        media_in_converted_folder = self.__converter_config.media_in_converted_folder

        Validation.is_dir(media_in_folder, f"Missing input directory '{media_in_folder}'")
        Validation.can_read(media_in_folder, f"Missing read permission on '{media_in_folder}'")
        Validation.can_write(media_in_folder, f"Missing write permission on '{media_in_folder}'")

        try:
            Validation.is_dir_writeable(media_out_folder, f"Directory '{media_out_folder}' *must* be writable")
        except NotADirectoryError:
            parent_directory = str(Path(media_out_folder).parent)
            Validation.can_write(parent_directory, f"Missing write permission on '{parent_directory}'")
            MediaObserver.__LOG.info(f"Creating missing destination directory for converted files '{media_out_folder}'")
            # create if not exists
            Path(media_out_folder).mkdir(parents=True, exist_ok=True)

        Validation.are_symlinks(
            media_in_folder,
            media_out_folder,
            f"Input ('{media_in_folder}') and output ('{media_out_folder}') directory can not be the same (or symlinks)"
        )

        try:
            Validation.is_empty(media_in_converted_folder)
            Validation.is_dir_writeable(media_in_converted_folder, f"Directory '{media_in_converted_folder}' *must* be writable")
            Validation.are_symlinks(
                media_in_folder,
                media_in_converted_folder,
                f"Input ('{media_in_folder}') and output ('{media_in_converted_folder}') directory can not be the same (or symlinks)"
            )
        except ValueError:
            pass
        except NotADirectoryError:
            parent_directory = str(Path(media_in_converted_folder).parent)
            Validation.can_write(parent_directory, f"Missing write permission on '{parent_directory}'")
            MediaObserver.__LOG.info(f"Creating missing destination directory for original files converted '{media_in_converted_folder}'")
            # create if not exists
            Path(media_in_converted_folder).mkdir(parents=True, exist_ok=True)

            Validation.are_symlinks(
                media_in_folder,
                media_in_converted_folder,
                f"Input ('{media_in_folder}') and output ('{media_in_converted_folder}') directory can not be the same (or symlinks)"
            )

    def __observe(self) -> None:
        # Start observing directories
        self.__observer.schedule(
            self.__event_handler,
            self.__converter_config.media_in_folder,
            recursive=False
        )
        self.__observer.start()
        MediaObserver.__LOG.debug(f"Start observing {self.__converter_config.media_in_folder}")

        self.__observer.join()

    def start(self) -> None:
        """

        :raise: KeyboardInterrupt
        :raise: Exception
        """
        MediaObserver.__LOG.debug(chr(10) + self.__converter_config)
        MediaObserver.__LOG.info("*** START *** monitoring")

        try:
            self.__observe()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            MediaObserver.__LOG.fatal(f"Error occurred: {e}")
            MediaObserver.__LOG.debug(f"{e}", exc_info=True)

    def __cleanup(self) -> None:
        MediaObserver.__LOG.debug("Detaching event handlers")
        self.__event_handler.shutdown()

        MediaObserver.__LOG.debug("Shutting down observers")
        try:
            self.__observer.unschedule_all()
            self.__observer.stop()
            self.__observer.join()
            MediaObserver.__LOG.debug(f"Stop observing {self.__converter_config.media_in_folder}")
        except RuntimeError as e:
            MediaObserver.__LOG.debug(f"{e}", exc_info=True)

        MediaObserver.__LOG.debug("Shutting down logging service")
        LogManager.get_instance().shutdown()

    def stop(self) -> None:
        MediaObserver.__LOG.info("*** STOP *** monitoring")

        MediaObserver.__LOG.debug("Cleanup")
        self.__cleanup()

        MediaObserver.__LOG.debug("Exit")
