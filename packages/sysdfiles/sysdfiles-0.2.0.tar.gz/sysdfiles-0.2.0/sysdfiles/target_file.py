from .unit_file import UnitFile


# =============================================================================
# TargetFile
# =============================================================================
class TargetFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
