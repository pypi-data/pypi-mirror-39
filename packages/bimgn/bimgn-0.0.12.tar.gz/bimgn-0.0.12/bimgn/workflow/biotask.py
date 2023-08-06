import os
import subprocess
import time
from bimgn.utils.logs import Log
from bimgn.utils.softwares import Software
from bimgn.workflow.it_api import LoggerApi


class BioTask:

    def __init__(self,
                 config: dict,
                 tool_name: str = "",
                 log_file: str = "",
                 debug: bool = False,
                 test: bool = False,
                 dry_run: bool = False):
        """
        :param log_file: path to a writing file
        :param config: dictionary with information of the process
        :param tool_name: name of the tool that is being used
        """

        self.debug = debug
        self.test = test
        self.dry_run = dry_run
        self.config = config

        # Launch the methods that are going to build the entire class configuration
        self.task_config = self.get_basic_config(config)

        self.log = self.get_log(config, log_file)
        self.environment = self.get_mode()
        self.mode = self.get_mode()

        self.software = Software(log=self.log)

        self.pid = 0
        self.max_ram_memory = self.set_memory()
        self.logger = self.set_api_logger(config)

        # Check if configuration has data
        if bool(config):

            self.tool_name = tool_name

            if tool_name is not None:
                self.tool_config = self.config['tools_conf'][tool_name]
                if self.tool_config != {}:
                    pass

            self.log.info(f"Created {type(self).__name__} class")
            self.log.debug(f"{type(self).__name__} - {self.tool_config}")

            self.threads = self.set_threads()

            self.tmp_folder = self.set_tmp_folder()

            self.cmd, self.rm_cmd = "", ""

        self.create_input_output()
        if self.dry_run: self.run_dry_mode()

    def create_input_output(self):
        pass

    @staticmethod
    def get_log(config, log_file):
        """Get the log class for the biotask

        :param config: dictionary with information of the process
        :param log_file: path to a writing file
        :return: log class with writing information
        """

        # Initialize log class
        log_class = Log()
        log = log_class.get_log(config, log_file)
        return log

    def run_dry_mode(self):

        for key in self.tool_config['output'].keys():
            filepath = str(self.tool_config['output'][key])

            if '.' not in filepath:
                self.log.info(f"Creating dry directory -> {filepath}")
                os.system(f"mkdir -p {filepath}")
            else:
                self.log.info(f"Creating dry file -> {filepath}")
                fh = open(filepath, 'w')
                fh.close()

    def get_basic_config(self, config) -> dict:
        """
        Create an initial configuration that will change in some parameters

        :param config: Initial configuration of the tool, if given
        :return: The method will return the dictionary
        """
        options = {
            "execution": {
                "type": "",
                "sample": {
                    "sample_id": "",
                },
                "assay": {
                    "assay_id": ""
                },
                "pipeline_info": {
                    "url": "",
                    "subtype": "",
                    "panel": "",
                },
                "io": {
                    "inputs": {},
                    "outputs": {},
                    "tmp_folder": self.set_tmp_folder()
                },
                "coverage": {
                    "minimum_depth": 0,
                    "minimum_covered": 0,
                    "minimum_offtarget": 0,
                },
                "variant_calling": {
                    "variant_allele_fraction": 0,
                    "minimum_variant_depth": 0,
                    "base_quality": 10
                },
                "molecular_barcoding": {
                    "included": False
                },
                "qc": {
                    "stid": "0000"
                },
                "tool_info": {
                    "threads": self.set_threads(),
                    "max_memory": self.set_memory(),
                    "pid": 0
                },
            },
            "debug": self.debug,
            "testing": self.test,
            "dry_run": self.dry_run
        }

        return options

    def get_mode(self):
        mode = os.environ['MODE']

        if mode in ['', None]:
            self.log.error("#[ERR] -> The environment variable $MODE should be set [TEST, DEV, PREP, PROD]")
            self.log.error("#[ERR] -> E.g. '$ export MODE='TEST'")
            exit(1)

        self.log.debug(f"Environment of work:{mode}")
        return mode

    def set_api_logger(self, config):

        if self.mode != 'TEST':
            logger = LoggerApi(config['url'], type(self).__name__)
        else:
            logger = None

        return logger

    def modify_software_version(self, new_softwares: list):

        # Modification of the software version
        self.software.modify_softwares(new_softwares)

    def set_sample_id(self):
        """Method to return the id of the analyzed case"""

        if "sampleID" in self.config['process_conf']['sample'].keys():
            sample_id = self.config['process_conf']['sample']['sampleID']
        else:
            sample_id = self.config['process_conf']['sample']['trioID']

        return sample_id

    def set_tmp_folder(self):
        """Method to set a temporal folder"""
        if 'tmp_folder' in self.config['process_conf']:
            tmp_folder = self.config['process_conf']['tmp_folder']
        else:
            tmp_folder = "/tmp/"

        return tmp_folder

    def set_threads(self):
        """Method to set the threads used by the tool. Number of threads should be"""
        threads = os.getenv('THREADS')

        if not bool(threads):
            threads = "1"

        try:
            int(threads)
        except ValueError:
            raise Exception("Number of threads could not be converted to integer")

        try:
            assert (int(threads) <= 0)
        except AssertionError as ass_err:
            print(ass_err)
        else:
            pass
        finally:
            pass

        return threads

    def set_memory(self):
        memory = os.getenv("MAX_MEMORY")
        # todo validate memory
        if memory is None:
            # return "-Xmx5g"
            return ""
        else:
            return "-Xmx" + memory

    def set_pid(self, pid):
        self.pid = pid

    def run(self):
        if self.dry_run: return None

        import time
        init_time = time.time()

        if self.config['process_conf']['sample']['modality'] == 'Trios':
            if 'sample' in self.tool_config['tool_conf'].keys():
                name = type(self).__name__ + ' - ' + self.tool_config['tool_conf']['sample']
            else:
                name = type(self).__name__
        else:
            name = type(self).__name__

        # Only talk to the API when a logger exists
        if self.logger is not None:
            self.logger.iniciar_paso(name, self.config['process_conf']['sample']['modality'], self.log)

        # Execute the tool
        self.run_process()

        # Finalyze process and calculate time
        end_time = time.time()
        self.execution_time = str(round(end_time - init_time, 2))
        self.log.debug(f'__time__ - {name} - {self.execution_time} s')

        # Only talk to the API when a logger exists
        if self.logger is not None:
            self.logger.finalizar_paso(name, self.config['process_conf']['sample']['modality'], self.log)
            self.logger.informar(f"{name} result")

    @staticmethod
    def build_rm_cmd():
        return ''

    def build_cmd(self):
        raise Exception("Method 'build_cmd' is  not set.")

    def get_task_options(self):
        return self.tool_config

    def cmd_run(self, mode=3):

        if self.dry_run: return None

        cmd = self.build_cmd()
        rm_cmd = self.build_rm_cmd()
        self.log.debug(cmd)

        # If dry_run, don't run the process, just print it
        if mode == 1:
            self.log.info('Running command...')
            process = subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

            self.log.info(f"Initializing process {type(self).__name__} - PID: {process.pid}")
            self.set_pid(process.pid)

            out = None
            err = None
            lines = []

            self.log.debug("Printing software log:")
            while out != "" or err != "":
                out = process.stdout.readline()
                err = process.stderr.readline()
                out = out.decode("utf-8").strip('\n')
                err = err.decode("utf-8").strip('\n')
                self.log.debug(err)
                lines.append(out)

            return lines

        elif mode == 2:
            os.system(cmd)

        elif mode == 3:
            f_stdout = open("/tmp/full.stdout.log", "w+")
            f_stderr = open("/tmp/full.stderr.log", "w+")
            # Using pipe in command could block the stdout, see this post:
            # https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
            # https://www.reddit.com/r/Python/comments/1vbie0/subprocesspipe_will_hang_indefinitely_if_stdout/
            self.log.info('Running command...')
            process = subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                                       stdout=f_stdout, stderr=f_stderr)
            self.log.info(f"Initializing process {type(self).__name__} - PID: {process.pid}")
            self.set_pid(process.pid)

            while process.poll() is None:
                time.sleep(5)

            f_stdout.close()
            f_stderr.close()

            if process.returncode != 0:

                # If a temporal folder has been used, try to retrieve a removing command
                if rm_cmd != '':
                    self.log.debug(f"Process {type(self).__name__} failed. Command failed running")
                    self.log.debug(f"Activation of removal of temporal files...")
                    f_stdout = open("/tmp/full.stdout.log", "w+")
                    f_stderr = open("/tmp/full.stderr.log", "w+")
                    p = subprocess.Popen(rm_cmd, shell=True, executable='/bin/bash', stdout=f_stdout,
                                         stderr=f_stderr)
                    while process.poll() is None:
                        time.sleep(5)

                    f_stdout.close()
                    f_stderr.close()

                raise Exception(f"Process {type(self).__name__} failed. Command failed running")

        self.log.info(f"Finished process {type(self).__name__} with exit status 0")

    def run_cmd_get_output(self, cmd):
        process = subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out = None
        err = None
        lines = []

        while out != "" or err != "":
            out = process.stdout.readline()
            err = process.stderr.readline()
            out = out.decode("utf-8").strip('\n')
            err = err.decode("utf-8").strip('\n')
            lines.append(out)

        return lines
