from .unit_file import UnitFile


# =============================================================================
# ServiceFile
# =============================================================================
class ServiceFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_properties('service',
                            [['bus_name'],
                             ['exec_reload', 'l', '', 1],
                             ['exec_start', 'l', '', 1],
                             ['exec_start_post', 'l', '', 1],
                             ['exec_start_pre', 'l', '', 1],
                             ['exec_stop', 'l', '', 1],
                             ['exec_stop_post', 'l', '', 1],
                             ['file_descriptor_store_max', 'i'],
                             ['guess_main_pid', 'b'],
                             ['non_blocking', 'b'],
                             ['notify_access'],
                             ['permissions_start_only', 'b'],
                             ['pid_file'],
                             ['remain_after_exit', 'b'],
                             ['restart'],
                             ['restart_force_exit_status', 'l'],
                             ['restart_prevent_exit_status', 'l'],
                             ['restart_sec', 'ns'],
                             ['root_directory_start_only', 'b'],
                             ['runtime_max_sec', 'ns'],
                             ['sockets', 'l', ' ', 3],
                             ['success_exit_status', 'l'],
                             ['timeout_sec', 'ns'],
                             ['timeout_start_sec', 'ns'],
                             ['timeout_stop_sec', 'ns'],
                             ['type'],
                             ['usb_function_descriptors'],
                             ['usb_function_strings'],
                             ['watchdog_sec', 'ns']])
        self.add_exec_properties()
        self.add_kill_properties()
        self.add_resource_control_properties()
