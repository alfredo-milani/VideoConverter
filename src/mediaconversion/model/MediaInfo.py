class MediaInfo(object):
    """

    """

    def __init__(self, filein: str, filein_converted_folder: str,
                 fileout: str, out_format: dict):
        super().__init__()

        self.__filein = filein
        self.__filein_converted_folder = filein_converted_folder
        self.__fileout = fileout
        self.__out_format = out_format

    @property
    def filein(self) -> str:
        return self.__filein

    @filein.setter
    def filein(self, value: str) -> None:
        self.__filein = value

    @property
    def filein_converted_folder(self) -> str:
        return self.__filein_converted_folder

    @filein_converted_folder.setter
    def filein_converted_folder(self, value: str) -> None:
        self.__filein_converted_folder = value

    @property
    def fileout(self) -> str:
        return self.__fileout

    @fileout.setter
    def fileout(self, value: str) -> None:
        self.__fileout = value

    @property
    def out_format(self) -> dict:
        return self.__out_format

    @out_format.setter
    def out_format(self, value: dict) -> None:
        self.__out_format = value
