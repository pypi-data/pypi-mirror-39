from .unit_file import UnitFile


# =============================================================================
# ScopeFile
# =============================================================================
class ScopeFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_resource_control_properties()
