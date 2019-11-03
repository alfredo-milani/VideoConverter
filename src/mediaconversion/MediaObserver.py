import logging
from pathlib import Path

from watchdog.observers import Observer

from mediaconversion.MediaEventHandler import MediaEventHandler
from model import Config
from util import Common
from util.Validation import Validate


class MediaObserver(object):

    log = logging.getLogger(Common.MEDIA_CONVERSION_LOGGER)
    config = Config.get_instance()

    OBSERVING_TIMEOUT = 1

    def __init__(self, timeout: float = OBSERVING_TIMEOUT):
        super().__init__()

        self.__event_handler = MediaEventHandler()
        self.__observer = Observer(timeout=timeout)

    def observe(self) -> None:
        try:
            MediaObserver.__validate()
        except Exception as e:
            MediaObserver.log.critical(str(e))
            MediaObserver.log.debug(str(e), exc_info=True)
            return

        self.__observer.schedule(
            self.__event_handler,
            MediaObserver.config.media_in_folder,
            recursive=False
        )
        self.__observer.start()

        MediaObserver.log.info("START observing '{}'".format(MediaObserver.config.media_in_folder))

        try:
            self.__observer.join()
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        self.__observer.stop()
        self.__observer.join()
        self.__event_handler.shutdown()
        MediaObserver.log.info("STOP observing '{}'".format(MediaObserver.config.media_in_folder))

    @classmethod
    def __validate(cls) -> None:
        """
        Check permissions on directories before the operations
        :raise ValueError if input directory is equal to output directory
        :raise NotADirectoryError
        :raise PermissionError
        :raise LinksError
        """
        Validate.is_dir(
            MediaObserver.config.media_in_folder,
            "Missing input directory: '{}'".format(MediaObserver.config.media_in_folder)
        )
        Validate.can_read(
            MediaObserver.config.media_in_folder,
            "Can not read '{}'".format(MediaObserver.config.media_in_folder)
        )

        try:
            Validate.is_dir(
                MediaObserver.config.media_out_folder,
                "Not a directory '{}'".format(MediaObserver.config.media_out_folder)
            )
        except NotADirectoryError:
            # create if not exists
            Path(MediaObserver.config.media_out_folder).mkdir(parents=True, exist_ok=True)
        Validate.can_write(
            MediaObserver.config.media_out_folder,
            "Missing write permission on '{}'".format(MediaObserver.config.media_out_folder)
        )

        if MediaObserver.config.media_in_converted_folder is not None and \
                MediaObserver.config.media_in_converted_folder != "":
            try:
                Validate.is_dir(
                    MediaObserver.config.media_in_converted_folder,
                    "Not a directory '{}'".format(MediaObserver.config.media_in_converted_folder)
                )
            except NotADirectoryError:
                # create if not exists
                Path(MediaObserver.config.media_in_converted_folder).mkdir(parents=True, exist_ok=True)
            Validate.can_write(
                MediaObserver.config.media_in_converted_folder,
                "Missing write permission on '{}'".format(MediaObserver.config.media_in_converted_folder)
            )

        Validate.are_symlinks(
            MediaObserver.config.media_in_folder,
            MediaObserver.config.media_out_folder,
            "Input and output directory can not be the same"
        )
