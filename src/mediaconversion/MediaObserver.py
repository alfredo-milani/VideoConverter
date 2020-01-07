import logging.config
from pathlib import Path

from watchdog.observers import Observer

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
    #  - programmatic logs
    #  - unit test

    __LOG = None

    _CONVERTER_CONFIG = None

    PY_VERSION_MIN = (3, 7)
    OBSERVING_TIMEOUT = 1

    def __init__(self, converter_config: ConverterConfig):
        """

        :param converter_config:
        :raise:
        """
        super().__init__()

        MediaObserver._CONVERTER_CONFIG = converter_config
        self.__observer = None
        self.__event_handler = None

        # Validate python version
        self.__validate_py_version(MediaObserver.PY_VERSION_MIN)
        # Load loggers
        self.__init_loggers(converter_config.general_log_config_file)
        # Check permissions
        self.__check_permissions()

        self.__observer = Observer(timeout=converter_config.media_in_timeout)
        self.__event_handler = MediaEventHandler(converter_config.general_processes)

    @classmethod
    def __validate_py_version(cls, min_version):
        Validation.python_version(
            min_version,
            f"Python version required >= {min_version}"
        )

    @classmethod
    def __init_loggers(cls, log_config_file):
        Validation.is_file_readable(
            log_config_file,
            f"Log configuration file *must* exists and be readable '{log_config_file}'"
        )

        # Loading log's configuration file
        logging.config.fileConfig(fname=log_config_file)
        MediaObserver.__LOG = logging.getLogger(LogManager.Logger.OBSERVER.value)

    def __check_permissions(self):
        """
        Check permissions on directories before performing the operations

        :raise ValueError if input directory is equal to output directory
        :raise NotADirectoryError
        :raise PermissionError
        :raise LinksError
        """
        media_in_folder = self._CONVERTER_CONFIG.media_in_folder
        media_out_folder = self._CONVERTER_CONFIG.media_out_folder
        media_in_converted_folder = self._CONVERTER_CONFIG.media_in_converted_folder

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
            MediaObserver._CONVERTER_CONFIG.media_in_folder,
            recursive=False
        )
        self.__observer.start()
        MediaObserver.__LOG.info(f"Start observing {MediaObserver._CONVERTER_CONFIG.media_in_folder}")

        self.__observer.join()

    def start(self) -> None:
        """

        :raise: KeyboardInterrupt
        :raise: Exception
        """
        MediaObserver.__LOG.debug(chr(10) + MediaObserver._CONVERTER_CONFIG)
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
            MediaObserver.__LOG.info(f"Stop observing {MediaObserver._CONVERTER_CONFIG.media_in_folder}")
        except RuntimeError as e:
            MediaObserver.__LOG.debug(f"{e}", exc_info=True)

        MediaObserver.__LOG.debug("Shutting down logging service")
        logging.shutdown()

    def stop(self) -> None:
        MediaObserver.__LOG.info("*** STOP *** monitoring")

        MediaObserver.__LOG.info("Cleanup")
        self.__cleanup()

        MediaObserver.__LOG.info("Exit")
