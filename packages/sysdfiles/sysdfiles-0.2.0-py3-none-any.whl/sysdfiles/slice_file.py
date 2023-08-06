from .unit_file import UnitFile


# =============================================================================
# SliceFile
# =============================================================================
class SliceFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_resource_control_properties()
