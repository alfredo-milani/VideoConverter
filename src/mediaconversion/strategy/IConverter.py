from abc import abstractmethod

from mediaconversion.model import MediaInfo


class IConverter(object):
    """
    Converter interface
    """

    @abstractmethod
    def convert(self, media_info: MediaInfo) -> None:
        """
        Method for the strategy of data
        :param media_info: object which incapsulate infformation for strategy
        """
        raise NotImplementedError

    @abstractmethod
    def on_error(self, media_info: MediaInfo = None,
                 exception: Exception = None) -> None:
        """
        Called on strategy error
        :param media_info: object which incapsulate infformation for strategy
        :param exception: exceotion thrown
        """
        raise NotImplementedError

    @abstractmethod
    def on_success(self, media_info: MediaInfo = None) -> None:
        """
        Called on strategy success
        :param media_info: object which incapsulate infformation for strategy
        """
        raise NotImplementedError
