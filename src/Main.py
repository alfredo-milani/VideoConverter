import logging.config
import sys

from mediaconversion import MediaObserver
from model import Config
from util import Common
from util.Validation import Validate


class Main(object):
    """
    Launcher
    """

    @classmethod
    def __validate(cls, min_version: tuple, log_file: str, config_file: str) -> None:
        """

        :param log_file:
        :param config_file:
        :raise PythonVersionError
        :raise FileNotFoundError
        :raise PermissionError
        """
        # Check python version
        Validate.python_version(
            min_version,
            "Python version required >= {}".format(min_version)
        )

        Validate.is_file(
            log_file,
            "Invalid log configuration file '{}'.\n".format(log_file)
        )
        Validate.can_read(
            log_file,
            "You don't have read permission on '{}'".format(log_file)
        )

        Validate.is_file(
            config_file,
            "Invalid configuration file '{}'.\n".format(config_file)
        )
        Validate.can_read(
            config_file,
            "You don't have read permission on '{}'".format(config_file)
        )

    @staticmethod
    def start():
        # Get log file
        log_file = "{}/{}".format(Common.get_proj_root_path(), "res/conf/log.ini")
        # Get configuration file
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        else:
            config_file = "{}/{}".format(Common.get_proj_root_path(), "res/conf/conf.ini")

        # Validation
        try:
            Main.__validate((3, 7), log_file, config_file)
        except Exception as e:
            print("Error: " + str(e))
            exit(1)

        # Loading log's configuration file
        logging.config.fileConfig(fname=log_file)
        log = logging.getLogger()

        # Load configuration file
        config = Config.get_instance()
        config.load_from(config_file)

        log.info("Starting...")
        log.debug(config)

        # Start observing directory for strategy
        try:
            observer = MediaObserver(config.observing_timeout)
            observer.observe()
        except Exception as e:
            log.fatal("Error occurred: {}".format(e))

        log.info("Exiting.")
        logging.shutdown()


if __name__ == "__main__":
    Main().start()
