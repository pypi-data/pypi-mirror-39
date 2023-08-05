import logging
import coloredlogs
import graypy
import os


class Log:

    def __init__(self):
        self.mode = os.environ['MODE']

    @staticmethod
    def set_mode(args):
        if args.d is True:
            mode = 'Debug'
        else:
            mode = 'Production'

        return mode

    def get_log(self, config: dict, log_file=""):

        # Initial variables
        message = False
        failed_file = False

        # If there is a config dictionary, check the log files
        if bool(config):
            log = self.set_log(type(self).__name__, config['log_files'])
            log.debug(f"Logging into {config['log_files'][0]}")
            return log

        # If not, write to simple file or to stream on stdout
        else:
            # Check if log_file has a value
            if bool(log_file):

                message = ""

                # Check if instance is string
                if not isinstance(log_file, str):
                    message = f"<log_file> variable should be a string instance, not {type(log_file)}"
                    failed_file = True

                # If the folder does not exists, just check the value to true
                if not failed_file and not os.path.exists(os.path.dirname(log_file)):
                    message = f"Output folder to write the log file does not exists ({os.path.dirname(log_file)})"
                    failed_file = True

                # If everything has been ok, write to a file
                if not failed_file:
                    log = self.set_log(type(self).__name__, [log_file])
                    log.info(f"Logging into {log_file}")
                    return log

            # Create a logging stream if no file is found
            log = self.set_log(type(self).__name__)
            log.debug(f"No logging file found, logging into stream")

            if failed_file is True:
                log.warn(message)

        return log

    @staticmethod
    def set_log(name, dirs: list = list()):

        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)

        if len(dirs) > 0:
            for d in dirs:
                # create a file handler
                handler = logging.FileHandler(d)
                handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)

                log.addHandler(handler)
                level = "INFO"

        else:
            # create a file handler
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            log.addHandler(handler)
            level = "DEBUG"

        # Create stream handler
        coloredlogs.install(level=level, logger=log)

        log_ip = os.getenv('LOGIP')
        if log_ip is not None:
            handler_gp = graypy.GELFHandler(log_ip, 12201)
            log.addHandler(handler_gp)

        return log
