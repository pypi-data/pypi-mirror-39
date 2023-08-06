
class Port:

    def __init__(self):
        self.name = None
        self.dn = None
        self.parent_dn = None
        self._handle = None
        self.admin_state = None
        self.max_speed = None
        self.oper_speed = None
        self.oper_state = None
        self.port_id = None
        self.peer_dn = None
        self.peer_port_id = None
        self.peer_slot_id = None

    def pop_base_params(self, port_data):
        self.name = port_data.name
        self.dn = port_data.dn
        self.parent_dn = port_data._ManagedObject__parent_dn
        self._handle = port_data._handle
        self.peer_dn = port_data.peer_dn
        self.admin_state = port_data.admin_state
        if getattr(port_data, 'max_speed', ''):
            self.max_speed = port_data.max_speed
        self.oper_speed = port_data.oper_speed
        self.oper_state = port_data.oper_state
        self.port_id = port_data.port_id
        if getattr(port_data, 'peer_port_id', ''):
            self.peer_port_id = port_data.peer_port_id
        if getattr(port_data, 'peer_slot_id', ''):
            self.peer_slot_id = port_data.peer_slot_id


class EthPortStat(Port):

    class EtherLoss:

        def __init__(self, data):
            self.dn = data.dn
            self.rn = data.rn
            self.time_collected = data.time_collected
            self.intervals = data.intervals
            self.carrier_sense = data.carrier_sense
            self.carrier_sense_delta = data.carrier_sense_delta
            self.excess_collision = data.excess_collision
            self.excess_collision_delta = data.excess_collision_delta
            self.giants = data.giants
            self.giants_delta = data.giants_delta
            self.multi_collision = data.multi_collision
            self.multi_collision_delta = data.multi_collision_delta
            self.single_collision = data.single_collision
            self.single_collision_delta = data.single_collision_delta
            self.sqe_test = data.sqe_test
            self.sqe_test_delta = data.sqe_test_delta
            self.symbol = data.symbol
            self.symbol_delta = data.symbol_delta

    class EtherPause:

        def __init__(self, data):
            self.dn = data.dn
            self.rn = data.rn
            self.time_collected = data.time_collected
            self.intervals = data.intervals
            self.recv_pause = data.recv_pause
            self.recv_pause_delta = data.recv_pause_delta
            self.resets = data.resets
            self.resets_delta = data.resets_delta
            self.xmit_pause = data.xmit_pause
            self.xmit_pause_delta = data.xmit_pause_delta

    class EtherErr:

        def __init__(self, data):
            self.dn = data.dn
            self.rn = data.rn
            self.time_collected = data.time_collected
            self.intervals = data.intervals
            self.align = data.align
            self.align_delta = data.align_delta
            self.deferred_tx = data.deferred_tx
            self.deferred_tx_delta = data.deferred_tx_delta
            self.fcs = data.fcs
            self.fcs_delta = data.fcs_delta
            self.int_mac_rx = data.int_mac_rx
            self.int_mac_rx_delta = data.int_mac_rx_delta
            self.int_mac_tx = data.int_mac_tx
            self.int_mac_tx_delta = data.int_mac_tx_delta
            self.out_discard = data.out_discard
            self.out_discard_delta = data.out_discard_delta
            self.rcv = data.rcv
            self.rcv_delta = data.rcv_delta
            self.under_size = data.under_size
            self.under_size_delta = data.under_size_delta
            self.xmit = data.xmit
            self.xmit_delta = data.xmit_delta

    class EtherRx:

        def __init__(self, data):
            self.dn = data.dn
            self.rn = data.rn
            self.time_collected = data.time_collected
            self.intervals = data.intervals
            self.broadcast_packets = data.broadcast_packets
            self.broadcast_packets_delta = data.broadcast_packets_delta
            self.jumbo_packets = data.jumbo_packets
            self.jumbo_packets_delta = data.jumbo_packets_delta
            self.multicast_packets = data.multicast_packets
            self.multicast_packets_delta = data.multicast_packets_delta
            self.total_bytes = data.total_bytes
            self.total_bytes_delta = data.total_bytes_delta
            self.total_packets = data.total_packets
            self.total_packets_delta = data.total_packets_delta
            self.unicast_packets = data.unicast_packets
            self.unicast_packets_delta = data.unicast_packets_delta

    class EtherTx:

        def __init__(self, data):
            self.dn = data.dn
            self.rn = data.rn
            self.time_collected = data.time_collected
            self.intervals = data.intervals
            self.broadcast_packets = data.broadcast_packets
            self.broadcast_packets_delta = data.broadcast_packets_delta
            self.jumbo_packets = data.jumbo_packets
            self.jumbo_packets_delta = data.jumbo_packets_delta
            self.multicast_packets = data.multicast_packets
            self.multicast_packets_delta = data.multicast_packets_delta
            self.total_bytes = data.total_bytes
            self.total_bytes_delta = data.total_bytes_delta
            self.total_packets = data.total_packets
            self.total_packets_delta = data.total_packets_delta
            self.unicast_packets = data.unicast_packets
            self.unicast_packets_delta = data.unicast_packets_delta

    def __init__(self):
        super().__init__()
        self.dn = None
        self.rn = None
        self.EtherPauseStats = None
        self.EtherLossStats = None
        self.EtherErrStats = None
        self.EtherRxStats = None
        self.EtherTxStats = None

    def pause_stats(self, data):
        self.EtherPauseStats = self.EtherPause(data)

    def loss_stats(self, data):
        self.EtherLossStats = self.EtherLoss(data)

    def err_stats(self, data):
        self.EtherErrStats = self.EtherErr(data)

    def rx_stats(self, data):
        self.EtherRxStats = self.EtherRx(data)

    def tx_stats(self, data):
        self.EtherTxStats = self.EtherTx(data)


class FcPortStat(Port):

    class FcStat:
        def __init__(self, data):
            self.time_collected = data.time_collected
            self.bytes_rx = data.bytes_rx
            self.bytes_rx_delta = data.bytes_rx_delta
            self.bytes_tx = data.bytes_tx
            self.bytes_tx_delta = data.bytes_tx_delta
            self.packets_tx = data.packets_tx
            self.packets_tx_delta = data.packets_tx_delta
            self.packets_rx = data.packets_rx
            self.packets_rx_delta = data.packets_rx_delta

    class FcErrStat:
        def __init__(self, data):
            self.time_collected = data.time_collected
            self.crc_rx = data.crc_rx
            self.crc_rx_delta = data.crc_rx_delta
            self.discard_rx = data.discard_rx
            self.discard_rx_delta = data.discard_rx_delta
            self.discard_tx = data.discard_tx
            self.discard_tx_delta = data.discard_tx_delta
            self.link_failures = data.link_failures
            self.link_failures_delta = data.link_failures_delta
            self.rx = data.rx
            self.rx_delta = data.rx_delta
            self.signal_losses = data.signal_losses
            self.signal_losses_delta = data.signal_losses_delta
            self.sync_losses = data.sync_losses
            self.sync_losses_delta = data.sync_losses_delta
            self.too_long_rx = data.too_long_rx
            self.too_long_rx_delta = data.too_long_rx_delta
            self.too_short_rx = data.too_short_rx
            self.too_short_rx_delta = data.too_short_rx_delta
            self.tx = data.tx
            self.tx_delta = data.tx_delta

    def __init__(self):
        super().__init__()
        self.FcErrStats = None
        self.FcStats = None

    def err_stats(self, data):
        self.FcErrStats = self.FcErrStat(data)

    def stats(self, data):
        self.FcStats = self.FcStat(data)


class EthPortChannelStat(EthPortStat):
    pass


class FcPortChannelStat(FcPortStat):
    pass

