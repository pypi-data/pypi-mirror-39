"""
Unofficial library to read single shot data from
DXS-100 Daxis Data Acquisition Device
"""
from __future__ import division, print_function
import json
import socket
import struct
import logging


def i16(data: bytes, pos=0)-> int:
    """unpack signed 16 bit from position in byte array"""
    return struct.unpack('!h', data[pos:pos + 2])[0]


def u16(data: bytes, pos=0)-> int:
    """unsigned 16 bit int"""
    return struct.unpack('!h', data[pos:pos + 2])[0]


def u32(data: bytes, pos=0)-> int:
    """unsigned 32 bit int"""
    return struct.unpack('!L', data[pos:pos + 4])[0]


def f64(data: bytes, pos=0)-> float:
    """unsigned double float"""
    return struct.unpack('!d', data[pos: pos + 8])[0]


def chars(data: bytes, pos, length)-> str:
    """null padded string"""
    return data[pos:pos + length].strip(b'\0').decode('utf-8')


class _DaxusChannel:
    def __init__(self, daxus, channel_num):
        self.span_steps = 60000
        self.connection = daxus
        self.channel_num = channel_num
        # send query packet
        self.connection.send(0x80000100, [4, channel_num])
        data = self.connection.get(32)
        self.channel_id = u32(data, 8)
        self.slot_num = u32(data, 16)
        # query chanel
        self.connection.send(0x80000104, [4, channel_num])
        data = self.connection.get(28)
        self.span_top = f64(data, 8)
        self.span_bottom = f64(data, 16)
        self.attenuation_code = u32(data, 24)
        self.connection.send(0x8000010c, [4, channel_num])
        data = self.connection.get(284)
        self.units = chars(data, 28, 20)
        self.label = chars(data, 156, 40)

    def __repr__(self):
        return json.dumps({
            'channel_label': self.label,
            'channel_num': self.channel_num,
            'channel_id': self.channel_id,
            'slot_num': self.slot_num,
            'span_top': self.span_top,
            'span_bottom': self.span_bottom,
            'attenuation_code': self.attenuation_code,
            'units': self.units
        })

    @property
    def gain(self):
        return (self.span_top - self.span_bottom) / self.span_steps

    @property
    def center(self):
        return (self.span_top - self.span_bottom) / 2

    def scaled_value(self, raw_value):
        return self.gain * raw_value + self.center


class Daxus:
    def __init__(self, ip: str, port=2864):
        """

        :param ip:
        :param port:
        """
        """
        """
        self.logger = logging.getLogger(__name__)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = 1
        self.connection.settimeout(self.timeout)
        self.connection.connect((ip, port))

        self.flush()
        self.heartbeat()
        self.set_mode('realtime')
        self.flush()
        self.name, self.channel_max, _ = self.get_config()
        self.channels = []
        self.flush()
        for c in range(1, self.channel_max + 1):
            _ = _DaxusChannel(self, c)
            self.channels.append(_)
            print(_)

    def get(self, size=448):
        # time.sleep(.09)
        data = b''
        while len(data) < size:
            data += self.connection.recv(size)
        # if len(data) > 0:
        #     self.logger.debug(f"received {len(data)} # {data}.")

        return data

    def flush(self):
        self.connection.settimeout(0)
        try:
            _ = self.connection.recv(1024)
        except BlockingIOError:
            pass  # no data avaliable
        else:
            if len(_) > 0:
                print(f'flushed {len(_)}')
        self.connection.settimeout(self.timeout)

    def set_mode(self, mode: str):
        """0 for real time, 1 for scope"""
        mode = {'realtime': 0, 'scope': 1}[mode]
        if mode != 0:
            raise NotImplementedError
        self.send(0x9, [0x4, mode])
        # no response

    def get_measurements(self):
        # request acquisition.
        self.send(0x80000014)
        data = self.get(10)
        payload_len = u32(data, 4) - 2
        num_chan = min(u16(data, 2), len(self.channels))
        data = self.get(payload_len)
        measurements = {}
        self.logger.debug(f'sample received channels:{num_chan}'
                          f' payload{payload_len} len{len(data)}')

        for chan in range(num_chan):
            pos = chan * 2
            raw_value = i16(data, pos)
            measurements[self.channels[chan].label] =\
                self.channels[chan].scaled_value(raw_value)
        return measurements

    def get_config(self):
        self.send(0x80000001)  # request system status, including name
        data = self.get(448)
        assert len(data) == 448
        name = data[24:24 + 32].strip(b'\0').decode('utf-8')
        wave = u32(data, 12)
        channels = u32(data, 16)
        self.logger.debug(f'config {name} {wave} {channels}')
        return name, wave, channels

    def heartbeat(self):
        """Send a 4 byte heartbeat packet to determine link state."""
        self.send(0x80000010)
        self.get(12)

    def send(self, type_, arguments=(0,)):
        """send packet type, and arguments as 32 bit unsigned numbers."""
        self.connection.send(
            struct.pack("!L" + "L" * len(arguments), type_, *arguments)
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print("closed Daxus socket")


def test_daxus():
    logging.basicConfig(level=logging.DEBUG)
    with Daxus('127.0.0.1', 2864) as d:
        d.set_mode('realtime')
        for i in range(3):
            logging.info(d.get_measurements())
    print("complete")
