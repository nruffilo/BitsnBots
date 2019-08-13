# The MIT License (MIT)
#
# Copyright (c) 2018 Carter Nelson for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`ads1015`
====================================================

CircuitPython driver for ADS1015 ADCs.

* Author(s): Carter Nelson
"""
import struct
from .ads1x15 import ADS1x15

# Data sample rates
_ADS1015_CONFIG_DR = {
    128:   0x0000,
    250:   0x0020,
    490:   0x0040,
    920:   0x0060,
    1600:  0x0080,
    2400:  0x00A0,
    3300:  0x00C0
}

# Pins
P0 = 0
P1 = 1
P2 = 2
P3 = 3

class ADS1015(ADS1x15):
    """Class for the ADS1015 12 bit ADC."""

    @property
    def bits(self):
        """The ADC bit resolution."""
        return 12

    @property
    def rates(self):
        """Possible data rate settings."""
        r = list(_ADS1015_CONFIG_DR.keys())
        r.sort()
        return r

    @property
    def rate_config(self):
        """Rate configuration masks."""
        return _ADS1015_CONFIG_DR

    def _data_rate_default(self):
        return 1600

    def _conversion_value(self, raw_adc):
        raw_adc = raw_adc.to_bytes(2, "big")
        value = struct.unpack(">h", raw_adc)[0]
        return value >> 4
