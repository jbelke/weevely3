from unittest import TestCase
from core.utilities import randstr
from testsuite import config
from generate import generate, save_generated
from core.loggers import stream_handler
from core.weexceptions import DevException
import subprocess
import logging
import tempfile
import hashlib
import os

class BaseTest(TestCase):

    @classmethod
    def _randomize_bd(cls):
        cls.password = randstr(10)
        password_hash = hashlib.md5(cls.password).hexdigest().lower()
        filename = '%s_%s.php' % (
            __name__, cls.password)
        cls.url = os.path.join(config.script_folder_url, filename)
        cls.path = os.path.join(config.script_folder, filename)

    @classmethod
    def setUpClass(cls):

        if config.debug:
            stream_handler.setLevel(logging.DEBUG)
        else:
            stream_handler.setLevel(logging.INFO)

        cls._randomize_bd()

        # Check `config.script_folder` permissions
        if (
            subprocess.check_output(
                config.cmd_env_stat_permissions_s % (config.script_folder),
                shell=True).strip()
            != config.script_folder_expected_perms
            ):
            raise DevException(
                "Error: give to the http user full permissions to the folder \'%s\'"
                % config.script_folder
            )

        obfuscated = generate(cls.password)

        tmp_handler, tmp_path = tempfile.mkstemp()
        save_generated(obfuscated, tmp_path)
        subprocess.check_call(
            config.cmd_env_move_s_s % (tmp_path, cls.path),
            shell=True)

        subprocess.check_call(
            config.cmd_env_chmod_s_s % ('777', cls.path),
            shell=True)

    @classmethod
    def tearDownClass(cls):

        # Check the agent presence, could be already deleted
        if os.path.isfile(cls.path):
            subprocess.check_call(
                config.cmd_env_remove_s % cls.path,
                shell=True
            )
