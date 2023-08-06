import sys
import commands
import subprocess
import socket
import os

from os import path
from cpbox.app.appconfig import appconfig
from cpbox.tool import utils
from cpbox.tool import datatypes
from cpbox.tool import file
from cpbox.tool import logger
from signal import signal, SIGPIPE, SIG_DFL

class DevOpsApp:

    class Error(Exception):
        """
        DevOpsApp Error
        """
        pass

    def __getattr__(self, name):
        if name == 'hostname':
            import traceback
            self.want_logger('devops').warning('Access hostname: %s', ''.join(traceback.format_stack()))
            return self.hostname_short

    def want_logger(self, app_name=None):
        syslog_ng_server = os.environ['PUPPY_SYSLOG_NG_SERVER'] if 'PUPPY_SYSLOG_NG_SERVER' in os.environ else None
        logger.make_logger(app_name, self.log_level, syslog_ng_server, True)
        return logger.getLogger(app_name)

    def __init__(self, app_name, log_level='info', exit_on_error=True):
        appconfig.init(app_name)
        self.log_level = log_level
        self.exit_on_error = exit_on_error
        self.env = os.environ['PUPPY_ENV'] if 'PUPPY_ENV' in os.environ else 'dev'
        self.logger = self.want_logger(app_name)

        hostname = socket.gethostname()
        self.hostname_fqdn = hostname
        self.hostname_short = hostname.split('.', 1)[0]

        self.root_dir = path.dirname(path.realpath(sys.argv[0]))
        self.roles_dir = self.root_dir + '/roles'
        app_root_dir = self.roles_dir + '/' + app_name

        self.app_config_dir =  app_root_dir + '/config'
        self.app_templates_dir =  app_root_dir + '/templates'
        self.app_scripts_dir =  app_root_dir + '/scripts'

        self.app_storage_dir = '/opt/data/' + app_name
        self.app_persitent_storage_dir = self.app_storage_dir + '/persistent'
        self.app_runtime_storage_dir = self.app_storage_dir + '/runtime'
        self.app_logs_dir = self.app_runtime_storage_dir + '/logs'

        self._ensure_dir_and_write_permision()

        self.file_lock = None

    def run_cmd_ret(self, cmd):
        return self.run_cmd(cmd)[1]

    def run_cmd(self, cmd):
        self.logger.info('run_cmd: %s', cmd)
        ret = commands.getstatusoutput(cmd)
        return ret

    def shell_run(self, cmd, keep_pipeline=True, exit_on_error=True, dry_run=False):
        if datatypes.is_list_or_tuple(cmd):
            cmd = '\n' + ';\n'.join(cmd)

        self.logger.info('shell_run: %s', cmd)
        if dry_run:
            return 0
        ret = 0
        if keep_pipeline:
            # https://stackoverflow.com/questions/10479825/python-subprocess-call-broken-pipe
            ret = subprocess.call(cmd, shell=True, preexec_fn=lambda: signal(SIGPIPE, SIG_DFL))
        else:
            ret = subprocess.call(cmd, shell=True)
        if ret != 0 and self.exit_on_error and exit_on_error:
            sys.exit(ret)
        return ret

    def _ensure_dir_and_write_permision(self):
        file.ensure_dir(self.app_storage_dir)
        file.ensure_dir(self.app_persitent_storage_dir)
        file.ensure_dir(self.app_runtime_storage_dir)
        file.ensure_dir(self.app_logs_dir)

    def _check_lock(self):
        filepath = self.app_runtime_storage_dir + '/locks/' + file.compute_lock_filepath(sys.argv)
        file_lock = file.obtain_lock(filepath)
        if file_lock is None:
            pid = 0
            with open(filepath, 'r') as f:
                pid = f.read()
            self.logger.warning('lock file exists, pid: %s => %s', pid, filepath)
            sys.exit(1)
        else:
            self.file_lock = file_lock
