from .unit_file import UnitFile


# =============================================================================
# SwapFile
# =============================================================================
class SwapFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_properties('swap',
                            [['options'],
                             ['priority', 'i'],
                             ['timeout_sec', 'ns'],
                             ['what']])
        self.add_exec_properties()
        self.add_kill_properties()
        self.add_resource_control_properties()
