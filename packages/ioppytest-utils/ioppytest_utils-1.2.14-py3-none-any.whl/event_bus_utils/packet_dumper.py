#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import signal
from datetime import datetime

import pika

# use this as main and also lib:
try:
    from messages import *
    from pure_pcapy import Dumper, Pkthdr, DLT_RAW, DLT_IEEE802_15_4_NOFCS
    from event_bus_utils.rmq_handler import RabbitMQHandler, JsonFormatter
except:
    from .messages import *
    from .pure_pcapy import Dumper, Pkthdr, DLT_RAW, DLT_IEEE802_15_4_NOFCS
    from .event_bus_utils.rmq_handler import RabbitMQHandler, JsonFormatter

try:
    # For Python 3.0 and later
    from urllib.parse import urlparse
except ImportError:
    # Fall back to Python 2
    from urlparse import urlparse

logger = logging.getLogger(__name__)

VERSION = '0.1.1'
ALLOWED_DATA_LINK_TYPES = (DLT_IEEE802_15_4_NOFCS, DLT_RAW)


def launch_amqp_data_to_pcap_dumper(dump_dir, log_level, filename, dlt, amqp_url, amqp_exchange, topics):
    def signal_int_handler(self, frame):
        if pcap_dumper is not None:
            pcap_dumper.stop()

    signal.signal(signal.SIGINT, signal_int_handler)

    # init pcap_dumper
    pcap_dumper = AmqpDataPacketDumper(
        dump_dir=dump_dir,
        log_level=log_level,
        filename=filename,
        dlt=dlt,
        topics=topics,
        amqp_url=amqp_url,
        amqp_exchange=amqp_exchange,
    )

    # start pcap_dumper
    pcap_dumper.run()

    return pcap_dumper


class AmqpDataPacketDumper:
    """
    Sniffs data.serial and dumps into pcap file (assumes that frames are DLT_IEEE802_15_4)
    Sniffs data.tun and dumps into pcap file (assumes that frames are DLT_RAW)

    about pcap header:
        ts_sec: the date and time when this packet was captured. This value is in seconds since January 1,
            1970 00:00:00 GMT; this is also known as a UN*X time_t. You can use the ANSI C time() function
            from time.h to get this value, but you might use a more optimized way to get this timestamp value.
            If this timestamp isn't based on GMT (UTC), use thiszone from the global header for adjustments.

        ts_usec: in regular pcap files, the microseconds when this packet was captured, as an offset to ts_sec.
            In nanosecond-resolution files, this is, instead, the nanoseconds when the packet was captured, as
            an offset to ts_sec
            /!\ Beware: this value shouldn't reach 1 second (in regular pcap files 1 000 000;
            in nanosecond-resolution files, 1 000 000 000); in this case ts_sec must be increased instead!

        incl_len: the number of bytes of packet data actually captured and saved in the file. This value should
            never become larger than orig_len or the snaplen value of the global header.

        orig_len: the length of the packet as it appeared on the network when it was captured. If incl_len and
            orig_len differ, the actually saved packet size was limited by snaplen.
    """
    # fixme deprecate old rkey fromats
    DEFAULT_TOPICS = ['#.fromAgent.#', 'fromAgent.#']
    DEFAULT_DUMP_DIR = "tmp"
    DEFAULT_LOG_LEVEL = 10  # 10-> debug
    DEFAULT_FILENAME = "DLT_RAW.pcap"

    QUANTITY_MESSAGES_PER_PCAP = 1000

    def dumper_init(self):
        # delete tmp pcap file (the one with ~)
        full_path_temp_pcap_file = os.path.join(self.dump_dir, self.pcap_filename_wr)
        # delete previous pcap file
        full_path_pcap_file = os.path.join(self.dump_dir, self.pcap_filename)

        for f in [full_path_pcap_file, full_path_temp_pcap_file]:
            if os.path.exists(f):
                if os.path.isfile(f):
                    os.remove(f)

        self.pcap_dumper = Dumper(
            filename=os.path.join(self.dump_dir, self.pcap_filename_wr),
            snaplen=2000,
            network=self.dlt
        )

        # copy filename.pcap~ to filename.pcap, so we have a pcap file in the dir since the bagging, even if it's empty
        shutil.copyfile(
            os.path.join(self.dump_dir, self.pcap_filename_wr),
            os.path.join(self.dump_dir, self.pcap_filename)
        )

    def __init__(self,
                 dump_dir=DEFAULT_DUMP_DIR,
                 log_level=DEFAULT_LOG_LEVEL,
                 filename=DEFAULT_FILENAME,
                 dlt=DLT_RAW,
                 topics=DEFAULT_TOPICS,
                 amqp_url=None,
                 amqp_exchange=None,
                 ):

        assert dlt in ALLOWED_DATA_LINK_TYPES, 'not accepted dlt %s' % dlt

        self.COMPONENT_ID = 'capture_dumper_%s' % str(uuid.uuid4())[:8]  # uuid in case several dumpers listening to bus
        self.dlt = dlt
        self.messages_dumped = 0

        if amqp_url and amqp_exchange:
            self.url = amqp_url
            self.exchange = amqp_exchange
        else:
            self.url = os.environ.get('AMQP_URL')
            self.exchange = os.environ.get('AMQP_EXCHANGE')

        self.pcap_filename = filename
        self.pcap_filename_wr = self.pcap_filename + "~"

        self.dump_dir = dump_dir
        if not os.path.exists(self.dump_dir):
            os.makedirs(self.dump_dir)

        # pcap dumpers
        self.pcap_dumper = None
        self.dumper_init()

        # AMQP stuff
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))  # queues & default exchange declaration
        self.channel = self.connection.channel()

        self.data_queue_name = '%s::packet.sniffed.raw' % self.COMPONENT_ID
        self.channel.queue_declare(queue=self.data_queue_name,
                                   auto_delete=True,
                                   arguments={'x-max-length': 1000}
                                   )

        # create my own logger (to avoid file description errors)
        self.logger = logging.getLogger(self.COMPONENT_ID)

        # AMQP log handler with f-interop's json formatter
        rabbitmq_handler = RabbitMQHandler(self.url, self.COMPONENT_ID)
        json_formatter = JsonFormatter()
        rabbitmq_handler.setFormatter(json_formatter)

        self.logger.addHandler(rabbitmq_handler)
        self.logger.setLevel(log_level)

        # subscribe to data plane channels
        self.topics = topics
        for t in self.topics:
            self.channel.queue_bind(exchange=self.exchange,
                                    queue=self.data_queue_name,
                                    routing_key=t)

        # subscribe to channel where the terminate session message is published
        self.channel.queue_bind(exchange=self.exchange,
                                queue=self.data_queue_name,
                                routing_key=MsgTestingToolTerminate.routing_key)

        # publish Hello message in bus
        msg = MsgTestingToolComponentReady(
            component=self.COMPONENT_ID,
            description="%s READY to start test suite." % self.COMPONENT_ID

        )
        self.channel.basic_publish(
            body=msg.to_json(),
            routing_key=msg.routing_key,
            exchange=self.exchange,
            properties=pika.BasicProperties(
                content_type='application/json',
            )
        )

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=self.data_queue_name)

    def dump_packet(self, message):
        try:
            t = time.time()
            t_s = int(t)
            t_u_delta = int((t - t_s) * 1000000)
            if 'serial' in message.interface_name:
                self.logger.info(
                    'Dumping packet found in %s interface of %s bytes' % (message.interface_name, len(message.data))
                )
                raw_packet = bytes(message.data)
                packet_slip = bytes(message.data_slip)

                # lets build pcap header for packet
                pcap_packet_header = Pkthdr(
                    ts_sec=t_s,
                    ts_usec=t_u_delta,
                    incl_len=len(raw_packet),
                    orig_len=len(raw_packet),
                )

                self.pcap_dumper.dump(pcap_packet_header, raw_packet)

                self.messages_dumped += 1

                # copy filename.pcap~ to filename.pcap
                shutil.copyfile(
                    os.path.join(self.dump_dir, self.pcap_filename_wr),
                    os.path.join(self.dump_dir, self.pcap_filename)
                )

            elif 'tun' in message.interface_name:
                self.logger.info(
                    'Dumping packet found in %s interface of %s bytes' % (message.interface_name, len(message.data))
                )
                raw_packet = bytes(message.data)

                # lets build pcap header for packet
                pcap_packet_header = Pkthdr(
                    ts_sec=t_s,
                    ts_usec=t_u_delta,
                    incl_len=len(raw_packet),
                    orig_len=len(raw_packet),
                )

                self.pcap_dumper.dump(pcap_packet_header, raw_packet)

                self.messages_dumped += 1

                # copy filename.pcap~ to filename.pcap
                shutil.copyfile(
                    os.path.join(self.dump_dir, self.pcap_filename_wr),
                    os.path.join(self.dump_dir, self.pcap_filename)
                )

            else:
                self.logger.info('Raw packet not dumped to pcap: ' + repr(message))
                return

        except Exception as e:
            self.logger.error(e)

        logging.info("Messages dumped : " + str(self.messages_dumped))

    def dumps_rotate(self):
        self.logger.warning(self.pcap_filename)
        full_path = os.path.join(self.dump_dir, self.pcap_filename)
        if os.path.isfile(full_path):
            self.logger.info('rotating file dump: %s' % full_path)
            self.logger.info(full_path)
            self.logger.info(full_path)
            self.logger.info(
                os.path.join(self.dump_dir, datetime.now().strftime('%Y%m%d_%H%M%S_') + self.pcap_filename))
            self.logger.info(self.pcap_filename)
            shutil.copyfile(
                full_path,
                os.path.join(self.dump_dir, datetime.now().strftime('%Y%m%d_%H%M%S_') + self.pcap_filename)
            )

    def stop(self):
        self.logger.info("Stopping %s..." % self.COMPONENT_ID)
        self.channel.queue_delete(self.data_queue_name)
        self.channel.stop_consuming()
        self.connection.close()

    def on_request(self, ch, method, props, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)

        try:

            m = Message.load_from_pika(method, props, body)
            self.logger.info('got event: %s' % type(m))

            if isinstance(m, MsgTestingToolTerminate):
                ch.stop_consuming()
                self.logger.info('%s got terminate signal. Terminating...' % self.COMPONENT_ID)
                self.stop()

            elif isinstance(m, MsgSniffingStop):
                ch.stop_consuming()
                self.logger.info('%s got capture stop singal. Stopping...' % self.COMPONENT_ID)
                self.stop()

            elif isinstance(m, MsgPacketSniffedRaw):

                self.dump_packet(m)

                try:  # rotate files each X messages dumped
                    if self.messages_dumped != 0 and self.messages_dumped % self.QUANTITY_MESSAGES_PER_PCAP == 0:
                        self.dumps_rotate()
                        self.dumper_init()

                except Exception as e:
                    self.logger.error(e)

            else:
                self.logger.info('drop amqp message: ' + repr(m))

        except NonCompliantMessageFormatError as e:
            err_msg = """
            * * * * * * API VALIDATION ERROR * * * * * * * 
            AMQP MESSAGE LIBRARY COULD PROCESS JSON MESSAGE
            * * * * * * * * * * * * * * * * * * * * * * * *
            """
            self.logger.error(err_msg)
            self.logger.error(e)
            # raise NonCompliantMessageFormatError("AMQP MESSAGE LIBRARY COULD PROCESS JSON MESSAGE")

        except Exception as e:
            self.logger.error(e)
            req_body_dict = json.loads(body.decode('utf-8'), object_pairs_hook=OrderedDict)
            self.logger.error("Message: %s, body: %s" % (json.dumps(req_body_dict), str(body)))

    def run(self):
        self.channel.start_consuming()


if __name__ == '__main__':
    dumper = AmqpDataPacketDumper()
    dumper.run()
