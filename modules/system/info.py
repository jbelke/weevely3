from core.vectors import PhpCode
from core.module import Module
from core import messages
import random


class Info(Module):

    """Collect system information."""

    def init(self):

        self.register_info(
            {
                'author': [
                    'Emilio Pinna'
                ],
                'license': 'GPLv3'
            }
        )

        self.register_vectors(
            [
            PhpCode("print(@$_SERVER['DOCUMENT_ROOT']);", 'document_root'),
            PhpCode("""
                $u=@posix_getpwuid(@posix_geteuid());
                if($u){
                    $u=$u['name'];
                } else {
                    $u=getenv('username');
                }
                print($u);
            """, 'whoami'),
            PhpCode("print(@gethostname());", 'hostname'),
            PhpCode("@print(getcwd());", 'cwd'),
            PhpCode("$v=@ini_get('open_basedir'); if($v) print($v);", 'open_basedir'),
            PhpCode("(@ini_get('safe_mode') && print(1)) || print(0);", 'safe_mode',
             postprocess = lambda x: True if x=='1' else False
            ),
            PhpCode("print(@$_SERVER['SCRIPT_NAME']);", 'script'),
            PhpCode("print(dirname(__FILE__));", 'script_folder'),
            PhpCode("print(@php_uname());", 'uname'),
            PhpCode("print(@php_uname('s'));", 'os'),
            PhpCode("print(@$_SERVER['REMOTE_ADDR']);", 'client_ip'),
            PhpCode('print(@ini_get("max_execution_time"));', 'max_execution_time',
             postprocess = lambda x: int(x)
            ),
            PhpCode('print(@$_SERVER["PHP_SELF"]);', 'php_self'),
            PhpCode('@print(DIRECTORY_SEPARATOR);', 'dir_sep'),
            PhpCode("""
                $v='';
                if(function_exists('phpversion')) {
                    $v=phpversion();
                } elseif(defined('PHP_VERSION')) {
                    $v=PHP_VERSION;
                } elseif(defined('PHP_VERSION_ID')) {
                    $v=PHP_VERSION_ID;
                }
                print($v);""", 'php_version')
            ]
        )

        self.register_arguments([
          { 'name' : '-info',
            'help' : 'Check give information',
            'choices' : self.vectors.get_names(),
            'nargs' : '+' }
        ])

    def run(self, args):

        return self.vectors.get_results(
            names = args.get('info', []),
            results_to_store = ('whoami', 'hostname', 'dir_sep', 'os')
        )
