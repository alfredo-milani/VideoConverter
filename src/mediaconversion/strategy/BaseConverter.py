import time
from abc import ABC
from os.path import getsize

from mediaconversion.model import MediaInfo
from mediaconversion.strategy import IConverter


class BaseConverter(ABC, IConverter):
    """

    """

    TRANSFER_DATA_POLL = 0.5

    def execute(self, media_info: MediaInfo) -> None:
        """
        DO NOT EDIT OR OVERRIDE THIS METHOD
        :param media_info: object which incapsulate information for strategy
        """
        self.prepare(media_info)

        try:
            self.convert(media_info)
        except Exception as e:
            return self.on_error(media_info, e)

        return self.on_success(media_info)

    def prepare(self, media_info: MediaInfo) -> None:
        pass

    def on_error(self, media_info: MediaInfo = None,
                 exception: Exception = None) -> None:
        pass

    def on_success(self, media_info: MediaInfo = None) -> None:
        pass

    @classmethod
    def _wait_file(cls, media_info: MediaInfo,
                   poll_time: float = TRANSFER_DATA_POLL) -> None:
        """
        This function blocks until file is not completely transferred on disk
        This action is mandatory on low speed network, otherwise file could be
         read even if it is not completely transferred on the server
        :param media_info: object to obtain filename
        :param poll_time: poll time
        """
        size = -1
        while size != getsize(media_info.filein):
            size = getsize(media_info.filein)
            time.sleep(poll_time)
