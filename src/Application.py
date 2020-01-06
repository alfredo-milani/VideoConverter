import atexit
import sys

from mediaconversion import MediaObserver
from model import ConverterConfig
from util import Common
from util.Validation import Validation


class Application(object):
    """
    Launcher
    """

    def __init__(self):
        super().__init__()

        self.__media_observer = None

    def stop(self) -> None:
        if self.__media_observer is None:
            raise Exception("Application not started.")

        self.__media_observer.stop()

    def start(self) -> None:
        # Construct configuration file
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        else:
            config_file = f"{Common.get_proj_root_path()}/res/conf/conf.ini"

        try:
            Validation.is_file_readable(
                config_file,
                f"Error on '{config_file}': configuration file *must* exists and be readable"
            )

            converter_config = ConverterConfig.get_instance()
            converter_config.load_from(config_file)

            self.__media_observer = MediaObserver(converter_config)
            atexit.register(self.stop)
            # Blocking call
            self.__media_observer.start()
        except SyntaxError:
            print(
                f"Syntax error in configuration file.\n"
                f"Make sure to follow JSON format while defining formats, sources, destinations and rules."
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    Application().start()
