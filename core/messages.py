version = '3.0beta'

class generic:
    file_s_not_found = "File '%s' not found"
    error_creating_file_s_s = "Error creating file '%s': %s"
    error_missing_arguments = 'Some arguments are missing'
    error_loading_file_s_s = 'Error loading file \'%s\': %s'
    error_file_s_already_exists = 'Error file \'%s\' already exists'
    error_parsing_command_s = 'Error parsing command: %s'

class sessions:
    error_loading_sessions = 'Session can not be loaded'
    error_storing_s_not_found = 'Error storing argument in session, \'%s\' argument not found or can\'t be set.'
    connection_info = """<%!
import urlparse
%><%
if not host:
    urlparsed = urlparse.urlparse(url)
    if urlparsed and urlparsed.netloc:
        hostname = urlparsed.netloc
    else:
        hostname = 'undefined host'
else:
    hostname = host
%>${'%s@' % user if user else ''}${hostname}${':%s' % path if path and path != '.' else ''}"""

class channels:
    error_loading_channel_s = 'Error loading channel \'%s\''

class terminal:
    backdoor_unavailable = 'Backdoor communication failed: please check URL reachability and password'
    help_no_shell = """
The system shell interpreter `shell_sh` is not available in this session,
use the following commands to simulate a complete shell.
"""
    welcome_to_s = """
[+] weevely ${version}

[+] Target:\t${conn_info}
[+] Session:\t${path}

[+] Browse the filesystem or execute commands starts the connection
[+] to the target. Type :help for more information.
"""

class stegareferrer:
    error_generating_id = 'Error generating id, payload too long?'
    error_password_hash = 'Error generating trigger, please use another password'
    error_language_start_letter_s = 'Error, at least one language must start with the letter \'%s\''
    error_chunk_position_i_s = 'Error chunk position %i is not indexable, delete template \'%s\''


class vectors:
    wrong_target_type = 'Wrong target operating system type'
    wrong_arguments_type = 'Wrong formatting argument type, a dictionary is required'
    wrong_postprocessing_type = 'Wrong postprocessing argument type, a callable function is required'
    wrong_payload_type = 'Wrong payload argument type, a string or a list of strings is required'
    wrong_condition_type = 'Wrong condition argument type, a callable function is required'
    wrong_store_name_type = 'Wrong argument type, a string with an argument name is required'

class vectorlist:
    vector_s_triggers_an_exc = 'Vector \'%s\' execution triggers an exception'

class module:
    error_setting_arguments_s = 'Error setting arguments: %s'
    argument_s_must_be_a_vector  = 'Argument \'%s\' must be a vector name'
    error_module_missing_description = 'Error, module description is missing'
    error_module_exec_error_s = 'Error, module execution triggered error \'%s\''
    error_init_method_required = 'Error, the init() method definition is required in Modules'
    module_s_exec_terminated = 'Module \'%s\' execution terminated'
    module_s_inactive = 'Module \'%s\' is inactive, skipped'
    error_choices_s_s_empty = 'Choices for \'%s\' argument \'%s\' is empty. Please check if vectors are declared before arguments.'
    running_the_alias_s = 'Shell interpreter unavailable, running the alias \'%s\''
    vector_s_not_support_arg_s_s = 'Vector \'%s\' does not support argument \'%s\' set to \'%s\''

class module_file_cd:
    failed_directory_change_to_s = "Failed cd '%s': no such directory or permission denied"
    error_getting_ossep = "Error getting remote directory separator"

class module_file_ls:
    failed_list_file_in_directory_s = "Failed list file in directory '%s': no such directory or permission denied"
    failed_list_file_in_directory_s_unknown = "Failed list file in directory '%s': unknown error"

class module_file_download:
    failed_download_file = "File download failed, please check remote path and permissions"
    skipping_md5_check = "Skipping MD5 check, the file integrity can't be checked"

class module_file_upload:
    error_content_lpath_required = "Error, argument 'lpath' or 'content' is required"
    failed_upload_file = "File upload failed, please check remote path and permissions"
    failed_md5_check = "Failed MD5 check, the integrity check is wrong or not available"

class module_file_edit:
    unmodified_file = "File unmodified, skipping upload"

class module_file_touch:
    error_invalid_timestamp_format = "Error, invalid timestamp format"
    error_source_timestamp_required = "Error, source timestamp is required."
    failed_touch_file = "File touch failed, please check remote path and permissions"

class module_sql_console:
    check_credentials = "Check credentials and DB availability"
    no_data = "No data returned"
    missing_sql_trailer_s = 'Is the trailing comma missing at the end of the SQL statement \'%s\'?'

class module_sql_dump:
    sql_dump_failed_check_credentials = "SQL dump failed, check credentials and DB availability"
    sql_dump_saved_s = "SQL dump saved to '%s'"

class module_file_grep:
    failed_retrieve_info = "Failed retrieve file information, please check if the remote readable files exist"

class module_file_upload2web:
    failed_retrieve_info = "Failed retrieve web root information"
    failed_resolve_path = "Failed resolve path, please check remote path and permissions"
    error_s_not_under_webroot_s = "Error, \'%s\' is not under the web root folder \'%s\'"
    failed_search_writable_starting_s = "Failed search first writable folder starting from '%s'."

class module_shell_php:
    error_404_remote_backdoor = 'The remote backdoor request triggers an error 404, please verify its availability'
    error_500_executing = 'The remote script execution triggers an error 500, please verify script integrity and sent payload correctness'
    error_URLError_network = 'Network error, unable to connect to the remote backdoor'
    missing_php_trailer_s = 'Is the trailing comma missing at the end of the PHP code \'%s\'?'
    error_i_executing = 'The request triggers the error %i, please verify running code'

class module_net_ifconfig:
    error_no_s_execution_result = 'Error, no \'%s\' execution result'
    error_parsing_s_execution_result = 'Error parsing \'%s\' execution result'
    error_interpeting_s_execution_result_s = 'Error interpreting \'%s\' execution result: \'%s\''
    failed_retrieve_info = "Failed retrieve ifconfig information"

class module_backdoor_tcp:
    error_parsing_connect_s = 'Error parsing hostname, connect manually to the shell on port %s'
    error_connecting_to_s_s_s = 'Error connecting to %s:%s: %s'

class module_backdoor_reversetcp:
    error_binding_socket_s = 'Error binding socket: \'%s\''
    error_timeout = 'Timeout error'
    reverse_shell_connected = 'Reverse shell connected, insert commands. Append semi-colon help to get the commands accepted.'

class module_audit_phpconf:
    not_enabled = 'Not enabled'
    enabled = 'Enabled'
    error = 'Error getting information'
    basedir_unrestricted = 'Unrestricted'
    basedir_dot = 'Set to \'.\', bypassable'
    basedir_no_slash = 'No trailing \'/\', bypassable'
    user_win_admin = 'Check this is not an administrative user'
    user_nix_root = 'User \'root\' can be abused'
    feat_expose_php = 'PHP configuration information exposed'
    feat_file_uploads = 'File upload enabled'
    feat_register_globals = 'Insecure variable manipulation enabled'
    feat_display_errors = 'Information display on error enabled'
    feat_enable_dl = 'Function dl() can be used to bypass restrictions'
    feat_safe_mode = 'Safe mode restrictions enabled'
    feat_magic_quotes_gpc = 'Insecure SQL injection protection enabled'
    feat_allow_url_include = 'Insecure inclusion of remote resources enabled'
    feat_session_use_trans_sid = 'Session IDs insecurely passed via URL'
    class_splFileObject = 'Class splFileObject can be used to bypass restrictions'
    class_COM = 'Class COM can be used to bypass restrictions'
    class_Java = 'Class Java can be used to bypass restrictions'
    func_info = 'Configuration exposed'
    func_files = 'Filesystem manipulation'
    func_log = 'Log tampering'
    func_proc_execution = 'Process execution'
    func_proc_manipulation = 'Process manipulation'

class module_net_curl:
    empty_response = 'The response is empty, check URL availability'

class module_shell_sh:
    error_sh_remote_shell = 'Error loading Sh remote shell'

class generate:
    error_agent_template_s_s = 'Error with agent template \'%s\': %s'
    error_obfuscator_template_s_s = 'Error with obfuscator template \'%s\': %s'
    generated_backdoor_with_password_s_in_s_size_i = 'Generated backdoor with password \'%s\' in \'%s\' of %i byte size.'
