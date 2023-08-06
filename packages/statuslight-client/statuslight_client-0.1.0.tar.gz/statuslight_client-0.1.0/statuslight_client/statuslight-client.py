#!/usr/bin/env python3
import serial
# Bit 7-5: command
# noqa: E221
LIGHT_INTENSITY = (0x1 << 5)
LIGHT_BLINK     = (0x2 << 5)
LIGHT_PULSE     = (0x3 << 5)
MESSAGE_LINE_1  = (0x4 << 5)
MESSAGE_LINE_2  = (0x5 << 5)

# Bit 4-0: data
RED    = 0x1
YELLOW = 0x2
GREEN  = 0x4

CMD_MASK  = 0xE0
DATA_MASK = 0x1F


def make_command_package(light, command, data):
    return (command | light) << 8 | data


class Statuslight(object):
    def __init__(self, port="/dev/ttyUSB1", baudrate=9600, timeout=1):
        self.conn = serial.Serial(port=port,
                                  baudrate=baudrate,
                                  timeout=timeout)

    def clear(self):
        for light in [RED, YELLOW, GREEN]:
            self.send_command(make_command_package(light, LIGHT_PULSE, 0))
            self.send_command(make_command_package(light, LIGHT_BLINK, 0))
            self.send_command(make_command_package(light, LIGHT_INTENSITY, 0))

    def send_command(self, cmd):
        self.conn.write(cmd.to_bytes(2, 'big'))

    def set_intensity(self, light, intensity):
        self.send_command(make_command_package(light,
                                               LIGHT_INTENSITY,
                                               intensity))

    def set_blink(self, light, period):
        self.send_command(make_command_package(light, LIGHT_BLINK, period))

    def set_pulse(self, light, period):
        self.send_command(make_command_package(light, LIGHT_PULSE, period))
