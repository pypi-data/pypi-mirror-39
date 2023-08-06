from .value_file import ValueFile


# =============================================================================
# HostnameFile
# =============================================================================
class HostnameFile(ValueFile):

    HOSTNAME_FILE = '/etc/hostname'

    def __init__(self, file_name=HOSTNAME_FILE):
        ValueFile.__init__(self, file_name)
