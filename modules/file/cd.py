from core.vectors import PhpCode
from core.module import Module
from core import messages
from core.loggers import log
import random


class Cd(Module):

    """Change current working directory."""

    aliases = [ 'cd' ]

    def init(self):

        self.register_info(
            {
                'author': [
                    'Emilio Pinna'
                ],
                'license': 'GPLv3'
            }
        )

        self.register_arguments([
          { 'name' : 'dir', 'help' : 'Target folder', 'default' : '.', 'nargs' : '?' }
        ])

    def run(self, args):

        chdir = '' if args['dir'] == '.' else "@chdir('%s')&&" % args['dir']
        folder = PhpCode("""${chdir}print(@getcwd());""", "chdir").run({ 'chdir' : chdir })

        if folder:
            # Store cwd used by other modules
            self._store_result('cwd', folder)
        else:
            log.warning(
                messages.module_file_cd.failed_directory_change_to_s %
                (args['dir']))

    def run_alias(self, line, cmd):

        # Run this alias independently from the shell_sh status
        return self.run_cmdline(line)
