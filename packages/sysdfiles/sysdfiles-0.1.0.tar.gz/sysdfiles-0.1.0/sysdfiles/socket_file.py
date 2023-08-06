from .unit_file import UnitFile


# =============================================================================
# SocketFile
# =============================================================================
class SocketFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_properties('socket',
                            [['accept', 'b'],
                             ['backlog', 'i'],
                             ['bind_ipv6_only'],
                             ['bind_to_device'],
                             ['broadcast', 'b'],
                             ['defer_accept_sec', 'ns'],
                             ['directory_mode', 'fm'],
                             ['exec_start_post', 'l', '', 1],
                             ['exec_start_pre', 'l', '', 1],
                             ['exec_stop_post', 'l', '', 1],
                             ['exec_stop_pre', 'l', '', 1],
                             ['file_descriptor_name'],
                             ['free_bind', 'b'],
                             ['ip_tos', 'i'],
                             ['ip_ttl', 'i'],
                             ['keep_alive', 'b'],
                             ['keep_alive_interval_sec', 'ns'],
                             ['keep_alive_probes', 'i'],
                             ['keep_alive_time_sec', 'ns'],
                             ['listen_datagram', 'l', '', 1],
                             ['listen_fifo'],
                             ['listen_message_queue'],
                             ['listen_netlink'],
                             ['listen_sequential_packet', 'l', '', 1],
                             ['listen_special'],
                             ['listen_stream', 'l', '', 1],
                             ['listen_usb_function'],
                             ['mark', 'i'],
                             ['max_connections', 'i'],
                             ['max_connections_per_source', 'i'],
                             ['message_queue_max_messages', 'i'],
                             ['message_queue_message_size', 'i'],
                             ['no_delay', 'b'],
                             ['pass_credentials', 'b'],
                             ['pass_security', 'b'],
                             ['pipe_size', 'nb'],
                             ['priority', 'i'],
                             ['receive_buffer', 'nb'],
                             ['remove_on_stop', 'b'],
                             ['reuse_port', 'b'],
                             ['se_linux_context_from_net', 'b'],
                             ['send_buffer', 'nb'],
                             ['service'],
                             ['smack_label'],
                             ['smack_label_ip_in'],
                             ['smack_label_ip_out'],
                             ['socket_group'],
                             ['socket_mode', 'fm'],
                             ['socket_protocol'],
                             ['socket_user'],
                             ['symlinks', 'l', '', 1],
                             ['tcp_congestion'],
                             ['timeout_sec', 'ns'],
                             ['transparent', 'b'],
                             ['trigger_limit_burst', 'i'],
                             ['trigger_limit_interval_sec', 'ns'],
                             ['writable', 'b']])
        self.add_exec_properties()
        self.add_kill_properties()
        self.add_resource_control_properties()
