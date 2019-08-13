# The MIT License (MIT)
#
# Copyright (c) 2017 Dan Halbert
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
#

"""
`adafruit_hid.keyboard.Keyboard`
====================================================

* Author(s): Scott Shawcroft, Dan Halbert
"""

import time
from micropython import const
import usb_hid

from .keycode import Keycode


class Keyboard:
    """Send HID keyboard reports."""

    # No more than _MAX_KEYPRESSES regular keys may be pressed at once.
    _MAX_KEYPRESSES = 6

    def __init__(self):
        """Create a Keyboard object that will send USB keyboard HID reports."""
        self.hid_keyboard = None
        for device in usb_hid.devices:
            if device.usage_page == 0x1 and device.usage == 0x06:
                self.hid_keyboard = device
                break
        if not self.hid_keyboard:
            raise IOError("Could not find an HID keyboard device.")

        # Reuse this bytearray to send keyboard reports.
        self.report = bytearray(8)

        # report[0] modifiers
        # report[1] unused
        # report[2:8] regular key presses

        # View onto byte 0 in report.
        self.report_modifier = memoryview(self.report)[0:1]

        # List of regular keys currently pressed.
        # View onto bytes 2-7 in report.
        self.report_keys = memoryview(self.report)[2:]

        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.release_all()
        except OSError:
            time.sleep(1)
            self.release_all()


    def press(self, *keycodes):
        """Send a report indicating that the given keys have been pressed.

        :param keycodes: Press these keycodes all at once.
        :raises ValueError: if more than six regular keys are pressed.

        Keycodes may be modifiers or regular keys.
        No more than six regular keys may be pressed simultaneously.

        Examples::

            from adafruit_hid.keycode import Keycode

            # Press ctrl-x.
            kbd.press(Keycode.LEFT_CONTROL, Keycode.X)

            # Or, more conveniently, use the CONTROL alias for LEFT_CONTROL:
            kbd.press(Keycode.CONTROL, Keycode.X)

            # Press a, b, c keys all at once.
            kbd.press(Keycode.A, Keycode.B, Keycode.C)
        """
        for keycode in keycodes:
            self._add_keycode_to_report(keycode)
        self.hid_keyboard.send_report(self.report)

    def release(self, *keycodes):
        """Send a USB HID report indicating that the given keys have been released.

        :param keycodes: Release these keycodes all at once.

        If a keycode to be released was not pressed, it is ignored.

        Example::

            # release SHIFT key
            kbd.release(Keycode.SHIFT)
        """
        for keycode in keycodes:
            self._remove_keycode_from_report(keycode)
        self.hid_keyboard.send_report(self.report)

    def release_all(self):
        """Release all pressed keys."""
        for i in range(8):
            self.report[i] = 0
        self.hid_keyboard.send_report(self.report)

    def send(self, *keycodes):
        """Press the given keycodes and then release all pressed keys.

        :param keycodes: keycodes to send together
        """
        self.press(*keycodes)
        self.release_all()

    def _add_keycode_to_report(self, keycode):
        """Add a single keycode to the USB HID report."""
        modifier = Keycode.modifier_bit(keycode)
        if modifier:
            # Set bit for this modifier.
            self.report_modifier[0] |= modifier
        else:
            # Don't press twice.
            # (I'd like to use 'not in self.report_keys' here, but that's not implemented.)
            for i in range(const(self._MAX_KEYPRESSES)):
                if self.report_keys[i] == keycode:
                    # Already pressed.
                    return
            # Put keycode in first empty slot.
            for i in range(const(self._MAX_KEYPRESSES)):
                if self.report_keys[i] == 0:
                    self.report_keys[i] = keycode
                    return
            # All slots are filled.
            raise ValueError("Trying to press more than six keys at once.")

    def _remove_keycode_from_report(self, keycode):
        """Remove a single keycode from the report."""
        modifier = Keycode.modifier_bit(keycode)
        if modifier:
            # Turn off the bit for this modifier.
            self.report_modifier[0] &= ~modifier
        else:
            # Check all the slots, just in case there's a duplicate. (There should not be.)
            for i in range(const(self._MAX_KEYPRESSES)):
                if self.report_keys[i] == keycode:
                    self.report_keys[i] = 0
