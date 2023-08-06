from .unit_file import UnitFile


# =============================================================================
# AutomountFile
# =============================================================================
class AutomountFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_properties('automount',
                            [['directory_mode', 'fm'],
                             ['timeout_idle_sec', 'ns'],
                             ['where']])
