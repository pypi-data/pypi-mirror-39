from .unit_file import UnitFile


# =============================================================================
# DeviceFile
# =============================================================================
class DeviceFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
