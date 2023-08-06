import queue
from datetime import datetime
from pyucs.logging.handler import Logger
from pyucs.statsd.portstats import EthPortStat, EthPortChannelStat, FcPortStat, FcPortChannelStat
from ucsmsdk.mometa.adaptor.AdaptorVnicStats import AdaptorVnicStats
from ucsmsdk.mometa.sw.SwSystemStatsHist import SwSystemStatsHist
from ucsmsdk.mometa.storage.StorageItem import StorageItem


LOGGERS = Logger(log_file='/var/log/ucs_parser.log', error_log_file='/var/log/ucs_parser_err.log')


class Parser:

    def __init__(self, statsq, influxq):
        self.in_q = statsq
        self.out_q = influxq

        self._run()

    def _run(self):
        """
        This is the background process payload. Constantly looking in the statsq
        queue to be able to parse the data to json.
        :return: None
        """
        # establish the logger
        logger = LOGGERS.get_logger('Parser')
        logger.info('Parser process Started')
        # running as a background process and should be in an infinite loop
        while True:
            try:
                # get the next item in the queue
                data = self.in_q.get_nowait()
                # send the raw data to be parsed into a dict format
                influx_series = self._parse_data(data)

                if influx_series:
                    # since the influxdb process is using queues and is also a background
                    # process lets parse the array of dicts down to single entries into the queue
                    # to be processed by influx
                    for i in influx_series:
                        logger.info('Parsed JSON data: {}'.format(i.__str__()))
                        # store the json data into the influx queue
                        self.out_q.put_nowait(i)
            except queue.Empty:
                # keep looping waiting for the queue not to be empty

                #   code reviewer...this is a test to see if you actually reviewed the code
                #     did you see this comment? If so you might win a prize, let me know!
                pass
        logger.info('Parser process Stopped')

    def _parse_data(self, data):
        """
        this function prepares the data to be sent to _format_json
        :param data:
        :return:
        """
        json_series = []

        logger = LOGGERS.get_logger('Parser_data_parser')
        try:
            if isinstance(data, FcPortChannelStat):
                json_series.append(self._prep_fc_port(data, 'fcportchannel'))
            if isinstance(data, EthPortChannelStat):
                json_series.append(self._prep_ether_port(data, 'ethportchannel'))
            if isinstance(data, EthPortStat):
                json_series.append(self._prep_ether_port(data, 'eth'))
            if isinstance(data, FcPortStat):
                json_series.append(self._prep_fc_port(data, 'fc'))
            if isinstance(data, StorageItem):
                json_series.append(self._prep_system_storage(data))
            if isinstance(data, AdaptorVnicStats) and data.dn.find('host-fc-') >= 0:
                json_series.append(self._prep_vhba(data))
            if isinstance(data, AdaptorVnicStats) and data.dn.find('host-eth-') >= 0:
                json_series.append(self._prep_vnic(data))
            if isinstance(data, SwSystemStatsHist):
                json_series.append(self._prep_fabric_kernel(data))

            return json_series
        except BaseException as e:
            logger.error('Parsing error: \nUcs: {} \nDevice: {}\nParent: {}'.format(data._handle.ucs,
                                                                                    data.dn,
                                                                                    data._ManagedObject__parent_dn))
            logger.exception('Exception: {}, \n Args: {}'.format(e, e.args))

    def _prep_ether_port(self, data, port_type):
        """
        :param data:
        :param port_type: Valid types are eth, ethportchannel
        :return: json_series
        """
        if not (port_type == 'eth' or port_type == 'ethportchannel'):
            raise TypeError("Parameter 'port_type' expected value 'eth' "
                            "or 'ethportchannel' but got '{}'".format(port_type))

        json_series = []

        # get the chassis dn
        chassis = data.peer_dn
        chassis_iom = data.peer_slot_id
        chassis_iom_port = data.peer_port_id
        fabric = data.dn.split('/')[1]

        # pair down the stats down to the relevant stats to be collected.
        # the raw data is an object with properties containing the metric data
        metrics = ['network.eth.tx.rate', 'network.eth.rx.rate', 'network.eth.pause.recv',
                   'network.eth.pause.resets', 'network.eth.pause.xmit', 'network.eth.err.xmit',
                   'network.eth.err.recv', 'network.eth.link.speed']
        tags = {
            'fabric': fabric,
            'port': data.port_id,
            'port_type': port_type,
            'max_speed': data.max_speed,
            'chassis': chassis,
            'chassis_iom': chassis_iom,
            'chassis_iom_port': chassis_iom_port,
            'ucs': data._handle.ucs,
        }
        json_series = (self._format_json(rawdata=data,
                                         measurement='network',
                                         metrics=metrics,
                                         tags=tags,
                                         _value_func=Parser._get_eth_port_value
                                         ))
        return json_series

    def _prep_fc_port(self, data, port_type):
        """
        :param data:
        :param port_type: Valid types are fc, fcportchannel
        :return: json_series
        """
        if not (port_type == 'fc' or port_type == 'fcportchannel'):
            raise TypeError("Parameter 'port_type' expected value 'fc' "
                            "or 'fcportchannel' but got '{}'".format(port_type))

        json_series = []

        # get the chassis dn
        chassis = data.peer_dn
        chassis_iom = data.peer_slot_id
        chassis_iom_port = data.peer_port_id
        fabric = data.dn.split('/')[1]

        # pair down the stats down to the relevant stats to be collected.
        # the raw data is an object with properties containing the metric data
        metrics = ['network.fc.tx.rate', 'network.fc.rx.rate', 'network.fc.err.rx.crc',
                   'network.fc.err.rx.discard', 'network.fc.err.rx', 'network.fc.err.rx.too_long',
                   'network.fc.err.rx.too_short', 'network.fc.err.tx', 'network.fc.err.signal_losses',
                   'network.fc.err.link.failure', 'network.fc.link.speed']
        tags = {
            'fabric': fabric,
            'port': data.port_id,
            'port_type': port_type,
            'max_speed': data.max_speed,
            'chassis': chassis,
            'chassis_iom': chassis_iom,
            'chassis_iom_port': chassis_iom_port,
            'ucs': data._handle.ucs,

        }
        json_series = (self._format_json(rawdata=data,
                                         measurement='network',
                                         metrics=metrics,
                                         tags=tags,
                                         _value_func=Parser._get_fc_port_value
                                         ))
        return json_series

    def _prep_system_storage(self, data):
        json_series = []

        # pair down the stats down to the relevant stats to be collected.
        # the raw data is an object with properties containing the metric data
        metrics = ['storage.size.mb', 'storage.used.percent', 'storage.used.mb',
                   'storage.free.percent', 'storage.free.mb']

        # data will be a list of StorageItems (partitions) from both Fabric Interconnects
        tags = {
            'partition': data.name,
            'fabric': data._ManagedObject__parent_dn,
            'storage_dn': data.dn,
            'ucs': data._handle.ucs,
        }
        json_series = (self._format_json(rawdata=data,
                                         measurement='storage',
                                         metrics=metrics,
                                         tags=tags,
                                         _value_func=Parser._get_storage_value
                                         ))
        return json_series

    def _prep_vnic(self, data):
        json_series = []

        parent_type = data.dn.split('/')[1]
        if parent_type.find('rack-unit-') >= 0:
            # get the rack dn
            pn_dn = "{}/{}".format(data.dn.split('/')[0],
                                   data.dn.split('/')[1]
                                   )
        else:
            # get the chassis/blade dn
            pn_dn = "{}/{}/{}".format(data.dn.split('/')[0],
                                      data.dn.split('/')[1],
                                      data.dn.split('/')[2]
                                      )

        # get the chassis dn
        chassis = "{}/{}".format(data.dn.split('/')[0],
                                 data.dn.split('/')[1]
                                 )

        # map the service profile to this stat
        service_profile = [s for s in data._handle.LsServer if s.pn_dn == pn_dn][0]
        # pair down the stats down to the relevant stats to be collected.
        # the raw data is an object with properties containing the metric data
        metrics = ['network.vnic.tx.rate', 'network.vnic.rx.rate', 'network.vnic.tx.drop',
                   'network.vnic.rx.drop', 'network.vnic.tx.error', 'network.vnic.rx.error']
        tags = {
            'parent': service_profile.name,
            'equipment_dn': pn_dn,
            'chassis': chassis,
            'ucs': data._handle.ucs,
            'device': data._ManagedObject__parent_dn.split('/')[
                len(data._ManagedObject__parent_dn.split('/')) - 1],
        }
        json_series = (self._format_json(rawdata=data,
                                         measurement='network',
                                         metrics=metrics,
                                         tags=tags,
                                         _value_func=Parser._get_vnic_value
                                         ))
        return json_series

    def _prep_vhba(self, data):
        logger = LOGGERS.get_logger('_prep_vhba')
        json_series = []
        parent_type = data.dn.split('/')[1]
        if parent_type.find('rack-unit-') >= 0:
            # get the rack dn
            pn_dn = "{}/{}".format(data.dn.split('/')[0],
                                   data.dn.split('/')[1]
                                   )
        else:
            # get the chassis/blade dn
            pn_dn = "{}/{}/{}".format(data.dn.split('/')[0],
                                      data.dn.split('/')[1],
                                      data.dn.split('/')[2]
                                      )

        # get the chassis dn
        chassis = "{}/{}".format(data.dn.split('/')[0],
                                 data.dn.split('/')[1]
                                 )

        # map the service profile to this stat
        service_profile = [s for s in data._handle.LsServer if s.pn_dn == pn_dn][0]
        # pair down the stats down to the relevant stats to be collected.
        # the raw data is an object with properties containing the metric data
        metrics = ['network.vhba.tx.rate', 'network.vhba.rx.rate', 'network.vhba.tx.drop',
                   'network.vhba.rx.drop', 'network.vhba.tx.error', 'network.vhba.rx.error']
        tags = {
            'parent': service_profile.name,
            'equipment_dn': pn_dn,
            'chassis': chassis,
            'ucs': data._handle.ucs,
            'device': data._ManagedObject__parent_dn.split('/')[
                len(data._ManagedObject__parent_dn.split('/')) - 1],
        }
        json_series = (self._format_json(rawdata=data,
                                         measurement='network',
                                         metrics=metrics,
                                         tags=tags,
                                         _value_func=Parser._get_vhba_value
                                         ))
        return json_series

    def _prep_fabric_kernel(self, data):
        json_series = []

        # pair down the stats down to the relevant stats to be collected.
        # the raw data is an object with properties containing the metric data
        metrics = ['systat.kernel.mem.free.mb', 'systat.kernel.mem.free.percent', 'systat.kernel.mem.total.mb',
                   'systat.kernel.mem.used.percent', 'systat.kernel.mem.used.mb', 'systat.cpu.load',
                   'systat.system.memory.total.mb', 'systat.system.memory.cached.mb']

        # data will be a list of StorageItems (partitions) from both Fabric Interconnects
        tags = {
            'fabric': "{}/{}".format(data.dn.split('/')[0], data.dn.split('/')[1]),
            'ucs': data._handle.ucs,
        }
        json_series = (self._format_json(rawdata=data,
                                         measurement='systat',
                                         metrics=metrics,
                                         tags=tags,
                                         _value_func=Parser._get_systat_value
                                         ))
        return json_series

    @staticmethod
    def _format_json(rawdata, measurement, metrics, tags, _value_func):
        if not isinstance(tags, dict):
            raise TypeError("Parameter 'tags' expected type dict but recieved type '{}'".format(type(tags)))

        logger = LOGGERS.get_logger('Parser _format_json')
        time_collected = getattr(rawdata, 'time_collected', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f'))
        collected_time = datetime.strptime(time_collected, '%Y-%m-%dT%H:%M:%S.%f')
        collected_time = datetime.utcfromtimestamp(collected_time.timestamp())
        influx_time = collected_time.__str__()
        json_data = {
            'time': influx_time,
            'measurement': measurement,
            'fields': {},
            'tags': tags,
        }
        for m in metrics:
            field_value = _value_func(m, rawdata)
            json_data['fields'].update({
                '{}'.format(m.replace(measurement, '')).lstrip('.'): field_value
            })
        return json_data

    @staticmethod
    def _get_vnic_value(metric, data):
        """
        function that returns the data from the managed object
        :param metric:
        :param data:
        :return:
        """
        if metric == 'network.vnic.tx.rate':
            # convert to Gbps
            return float(((float(data.bytes_tx_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.vnic.rx.rate':
            # convert to Gbps
            return float(((float(data.bytes_rx_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.vnic.rx.drop':
            return float(data.dropped_rx_delta)
        elif metric == 'network.vnic.tx.drop':
            return float(data.dropped_tx_delta)
        elif metric == 'network.vnic.rx.error':
            return float(data.errors_rx_delta)
        elif metric == 'network.vnic.tx.error':
            return float(data.errors_tx_delta)
        else:
            return None

    @staticmethod
    def _get_vhba_value(metric, data):
        """
        function that returns the data from the managed object
        :param metric:
        :param data:
        :return:
        """
        if metric == 'network.vhba.tx.rate':
            # convert to Gbps
            return float(((float(data.bytes_tx_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.vhba.rx.rate':
            # convert to Gbps
            return float(((float(data.bytes_rx_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.vhba.rx.drop':
            return float(data.dropped_rx_delta)
        elif metric == 'network.vhba.tx.drop':
            return float(data.dropped_tx_delta)
        elif metric == 'network.vhba.rx.error':
            return float(data.errors_rx_delta)
        elif metric == 'network.vhba.tx.error':
            return float(data.errors_tx_delta)
        else:
            return None

    @staticmethod
    def _get_storage_value(metric, data):
        """
        function that returns the data from the managed object
        :param metric:
        :param data:
        :return:
        """
        # Wonderful Cisco likes to use numbers and strings such as 'empty' and 'nothing' instead of 0
        # so let's test for this condition and make the number 0
        size = data.size
        used = data.used
        try:
            float(size)
        except ValueError:
            size = 0
        try:
            float(used)
        except ValueError:
            used = 0

        if metric == 'storage.used.mb':
            return float(size) * (float(used) / 100)
        elif metric == 'storage.used.percent':
            return float(used)
        elif metric == 'storage.free.mb':
            return float(size) - (float(size) * (float(used) / 100))
        elif metric == 'storage.free.percent':
            return 100 - float(used)
        elif metric == 'storage.size.mb':
            return float(size)
        else:
            return None

    @staticmethod
    def _get_fc_port_value(metric, data):
        """
        function that returns the data from the managed object
        :param metric:
        :param data:
        :return:
        """
        if metric == 'network.fc.tx.rate':
            return float(((float(data.FcStats.bytes_tx_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.fc.rx.rate':
            return float(((float(data.FcStats.bytes_rx_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.fc.err.rx.crc':
            return float(data.FcErrStats.crc_rx_delta)
        elif metric == 'network.fc.err.rx.discard':
            return float(data.FcErrStats.discard_rx_delta)
        elif metric == 'network.fc.err.rx':
            return float(data.FcErrStats.rx_delta)
        elif metric == 'network.fc.err.signal_losses':
            return float(data.FcErrStats.signal_losses_delta)
        elif metric == 'network.fc.err.link.failure':
            return float(data.FcErrStats.link_failures_delta)
        elif metric == 'network.fc.link.speed':
            return float(data.oper_speed.replace('gbps', ''))
        elif metric == 'network.fc.err.rx.too_short':
            return float(data.FcErrStats.too_short_rx_delta)
        elif metric == 'network.fc.err.rx.too_long':
            return float(data.FcErrStats.too_long_rx_delta)
        elif metric == 'network.fc.err.tx':
            return float(data.FcErrStats.tx_delta)
        else:
            return None

    @staticmethod
    def _get_eth_port_value(metric, data):
        """
        function that returns the data from the managed object
        :param metric:
        :param data:
        :return:
        """
        if metric == 'network.eth.tx.rate':
            # convert to Gbps
            return float(((float(data.EtherTxStats.total_bytes_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.eth.rx.rate':
            # convert to Gbps
            return float(((float(data.EtherRxStats.total_bytes_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.eth.pause.recv':
            return float(data.EtherPauseStats.recv_pause_delta)
        elif metric == 'network.eth.pause.resets':
            return float(data.EtherPauseStats.resets_delta)
        elif metric == 'network.eth.pause.xmit':
            return float(data.EtherPauseStats.xmit_pause_delta)
        elif metric == 'network.eth.err.xmit':
            return float(data.EtherErrStats.xmit_delta)
        elif metric == 'network.eth.err.recv':
            return float(data.EtherErrStats.xmit_delta)
        elif metric == 'network.eth.link.speed':
            return float(data.oper_speed.replace('gbps', ''))
        else:
            return None

    @staticmethod
    def _get_systat_value(metric, data):
        """
        function that returns the data from the managed object
        :param metric:
        :param data:
        :return:
        """

        if metric == 'systat.kernel.mem.free.mb':
            return float(data.kernel_mem_free)
        elif metric == 'systat.kernel.mem.free.percent':
            return ((float(data.kernel_mem_total) - float(data.kernel_mem_free)) / float(data.kernel_mem_free))*100
        elif metric == 'systat.kernel.mem.total.mb':
            return float(data.kernel_mem_total)
        elif metric == 'systat.kernel.mem.used.percent':
            return (float(data.kernel_mem_free) / float(data.kernel_mem_total)) * 100
        elif metric == 'systat.kernel.mem.used.mb':
            return float(data.kernel_mem_total) - float(data.kernel_mem_free)
        elif metric == 'systat.cpu.load':
            return float(data.load)
        elif metric == 'systat.system.memory.total.mb':
            return float(data.mem_available)
        elif metric == 'systat.system.memory.cached.mb':
            return float(data.mem_cached)
        else:
            return None
