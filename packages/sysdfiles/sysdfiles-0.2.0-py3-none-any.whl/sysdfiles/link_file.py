from .ini_file import IniFile


# =============================================================================
# LinkFile
# =============================================================================
class LinkFile(IniFile):

    def __init__(self, file_name=''):
        IniFile.__init__(self, file_name)
        self.add_properties('match',
                            [['architecture'],
                             ['driver', 'l'],
                             ['host'],
                             ['kernel_command_line'],
                             ['kernel_version'],
                             ['mac_address', 'l', ' ', 3],
                             ['original_name', 'l'],
                             ['path', 'l'],
                             ['type', 'l'],
                             ['virtualization']])
        self.add_properties('link',
                            [['alias'],
                             ['auto_negotiation', 'b'],
                             ['bits_per_second', 'bps'],
                             ['combine_channels', 'i'],
                             ['description'],
                             ['duplex'],
                             ['generic_receive_offload', 'b'],
                             ['generic_segmentation_offload', 'b'],
                             ['large_receive_offload', 'b'],
                             ['mac_address'],
                             ['mac_address_policy'],
                             ['mtu_bytes', 'nb'],
                             ['name'],
                             ['name_policy', 'l'],
                             ['other_channels', 'i'],
                             ['port'],
                             ['rx_channels', 'i'],
                             ['tcp_segmentation_offload', 'b'],
                             ['tcp6_segmentation_offload', 'b'],
                             ['tx_channels', 'i'],
                             ['wake_on_lan']])
