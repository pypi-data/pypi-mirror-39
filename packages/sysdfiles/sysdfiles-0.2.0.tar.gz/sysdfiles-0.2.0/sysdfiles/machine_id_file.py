from .value_file import ValueFile


# =============================================================================
# MachineIdFile
# =============================================================================
class MachineIdFile(ValueFile):

    MACHINE_ID_FILE = '/etc/machine-id'

    def __init__(self, file_name=MACHINE_ID_FILE):
        ValueFile.__init__(self, file_name)
