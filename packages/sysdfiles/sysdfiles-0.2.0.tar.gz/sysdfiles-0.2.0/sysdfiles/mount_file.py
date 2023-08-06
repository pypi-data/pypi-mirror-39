from .unit_file import UnitFile


# =============================================================================
# MountFile
# =============================================================================
class MountFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_properties('mount',
                            [['directory_mode', 'fm'],
                             ['force_unmount', 'b'],
                             ['lazy_unmount', 'b'],
                             ['options', 'l', ','],
                             ['sloppy_options', 'b'],
                             ['timeout_sec', 'ns'],
                             ['type'],
                             ['what'],
                             ['where']])
        self.add_exec_properties()
        self.add_kill_properties()
        self.add_resource_control_properties()
