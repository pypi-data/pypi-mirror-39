
import queue
from pyucs.logging.handler import Logger
from influxdb import InfluxDBClient


LOGGERS = Logger(log_file='/var/log/ucs_influx.log', error_log_file='/var/log/ucs_influx_err.log')


class InfluxDB:

    def __init__(self, influxq, host='127.0.0.1', port=8186, username='anonymous', password='anonymous',
                 database='perf_stats', timeout=5, retries=3):

        self.in_q = influxq
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__database = database
        self.__timeout = timeout
        self.__retries = retries
        self.client = self.__create_influx_client()
        self.logger = LOGGERS.get_logger('InfluxDB')

        try:
            self._run()
        except BaseException as e:
            self.logger.exception('Exception: {}, \n Args: {}'.format(e, e.args))

    def __create_influx_client(self):
        return InfluxDBClient(host=self.__host,
                              port=self.__port,
                              username=self.__username,
                              password=self.__password,
                              database=self.__database,
                              timeout=self.__timeout,
                              retries=self.__retries
                              )

    def _run(self):
        logger = LOGGERS.get_logger('InfluxDB')
        logger.info('InfluxDB process Started')
        while True:
            try:
                json_data = self.in_q.get_nowait()
                if json_data:
                    try:
                        logger.info('Sending stats: {}'.format(json_data))
                        self.client.write_points(points=[json_data],
                                                 time_precision='s',
                                                 protocol='json'
                                                 )
                    except BaseException as e:
                        # Writing to InfluxDB was unsuccessful. For now let's just try to resend
                        logger.error('Failed to Send influx data {}'.format(json_data))
                        logger.info('Retry Sending stats: {}'.format(json_data))
                        self.logger.exception('Exception: {}, \n Args: {}'.format(e, e.args))
                        self.client.write_points(points=json_data,
                                                 time_precision='s',
                                                 protocol='json'
                                                 )
                        pass
            except queue.Empty:
                pass

        logger.info('InfluxDB process Stopped')
