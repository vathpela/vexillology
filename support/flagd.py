#!/usr/bin/python

# XXX: this will eventually become a daemon in C

import os
import asyncore
import evdev

class InputDeviceDispatcher(asyncore.file_dispatcher):
    def __init__(self, device):
        self.device = device
        self.last_code = 0
        self.last_type = 0
        self.last_value = 0
        asyncore.file_dispatcher.__init__(self, device)

    def save_last(self, event):
        self.last_code = event.code
        self.last_type = event.type
        self.last_value = event.value

    def recv(self, ign=None):
        return self.device.read()

    def handle_read(self):
        for event in self.recv():
            # skip null events, these are just noise
            if event.code == 0 and event.type == 0 and event.value == 0:
                continue

            # if the current event matches the most recent event, skip
            if event.code == self.last_code and event.type == self.last_type and event.value == self.last_value:
                continue

            # take action
            if event.type == 2 and event.code == 7:
                # knob turned
                if event.value == -1L:
                    # left
                    os.system("/home/dcantrel/bin/flag-open")
                    self.save_last(event)
                elif event.value == 1L:
                    # right
                    os.system("/home/dcantrel/bin/flag-dnd")
                    self.save_last(event)
            elif event.type == 1 and event.code == 256 and event.value == 1L:
                # pressed
                os.system("/home/dcantrel/bin/flag-away")
                self.save_last(event)

if __name__ == "__main__":
    powermate = evdev.InputDevice('/dev/powermate')
    InputDeviceDispatcher(powermate)
    asyncore.loop()
