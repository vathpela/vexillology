#!/usr/bin/python

""" This reads from the powermate's input and runs programs as a result """

# pylint: disable=fixme

# XXX: this will eventually become a daemon in C

import os
import asyncore
import evdev

class InputDeviceDispatcher(asyncore.file_dispatcher):
    """ Listen for an input event and do stuff """
    def __init__(self, name, device):
        self.name = name
        self.device = device
        self.last_code = 0
        self.last_type = 0
        self.last_value = 0
        asyncore.file_dispatcher.__init__(self, device)

    def save_last(self, event):
        """ maintain our state """
        self.last_code = event.code
        self.last_type = event.type
        self.last_value = event.value

    def recv(self, _=None):
        """ receive from the device """
        return self.device.read()

    def handle_read(self):
        for event in self.recv():
            # skip null events, these are just noise
            if event.code == 0 and event.type == 0 and event.value == 0:
                continue

            # if the current event matches the most recent event, skip
            if event.code == self.last_code and \
               event.type == self.last_type and \
               event.value == self.last_value:
                continue

            # take action
            if event.type == 2 and event.code == 7:
                # knob turned
                if event.value == -1:
                    # left
                    os.system("powermate %s left" % (self.name,))
                    self.save_last(event)
                elif event.value == 1:
                    # right
                    os.system("powermate %s right" % (self.name,))
                    self.save_last(event)
            elif event.type == 1 and event.code == 256:
                # pressed
                os.system("powermate %s button %s" % (self.name, event.value))
                self.save_last(event)

if __name__ == "__main__":
    for dev in filter(lambda x: x.startswith("powermate"), os.listdir("/dev/")):
        powermate = evdev.InputDevice("/dev/%s" % (dev,))
        InputDeviceDispatcher(dev, powermate)
    asyncore.loop()
