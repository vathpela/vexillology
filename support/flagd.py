#!/usr/bin/python3

""" This reads from the powermate's input and runs programs as a result """

# pylint: disable=fixme

# XXX: this will eventually become a daemon in C

import errno
import os
import sys
import select
import evdev
import pyudev

class UdevMonitor:
    """ Listen for new devices """
    def __init__(self):
        super().__init__()
        self.ctx = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.ctx)
        self.monitor.filter_by('input')
        self.monitor.start()

    def fileno(self):
        """ return the fileno for select """
        return self.monitor.fileno()

    def new_devices(self):
        """ handle a new device """

        while True:
            device = self.monitor.poll(0)
            if not device:
                break
            if device['ACTION'] != 'add':
                continue
            if 'DEVNAME' not in device:
                continue
            if 'ID_USB_DRIVER' not in device:
                continue
            if 'DEVLINKS' not in device:
                continue
            if device['ID_USB_DRIVER'] == 'powermate':
                yield device

class PowerMate:
    """ Listen for an input event and do stuff """
    def __init__(self, name, left_cb=None, right_cb=None, button_cb=None):
        super().__init__()
        self.name = name
        self.device = evdev.InputDevice("/dev/%s" % (name,))
        self.last = None
        self.debug = False
        self.left_cb = left_cb
        self.right_cb = right_cb
        self.button_cb = button_cb
        print("new device %s" % (name,))

    def fileno(self):
        """ return the fileno for select """
        return self.device.fileno()

    def save_last(self, event):
        """ maintain our state """
        self.last = (event.code, event.type, event.value)

    def read(self):
        """ handle a new event """
        try:
            for event in self.device.read():
                self.handle_event(event)
        except OSError as e:
            if e.errno == errno.ENODEV:
                return True
            else:
                raise
        return False

    def left(self, event):
        """ what to do if it's left """
        if self.left_cb:
            self.left_cb(self, event)
        else:
            os.system("powermate %s left %s" % (self.name, event.value))

    def right(self, event):
        """ what to do if it's right """
        if self.right_cb:
            self.right_cb(self, event)
        else:
            os.system("powermate %s right %s" % (self.name, event.value))

    def button(self, event):
        """ what to do if it's button """
        if self.button_cb:
            self.button_cb(self, event)
        else:
            os.system("powermate %s button %s" % (self.name, event.value))

    def handle_event(self, event):
        """ handle one event """

        # skip null events, these are just noise
        if event.code == 0 and event.type == 0 and event.value == 0:
            return

        # if the current event matches the most recent event, skip
        #if event.type == self.last_type and \
        #   event.code == self.last_code and \
        #   event.value == self.last_value:
        if (event.code, event.type, event.value) == self.last:
            if self.debug:
                print("skipping %s event: type %s code %s value %s" % (
                    self.name, event.type, event.code, event.value))
            return

        # take action
        if event.type == 2 and event.code == 7 and event.value != 0:
            # knob turned
            if event.value < 0:
                # left
                self.left(event)
            elif event.value > 0:
                # right
                self.right(event)
        elif event.type == 1 and event.code == 256:
            # pressed
            self.button(event)
        else:
            if self.debug:
                print("powermate %s event: type %s code %s value %s" % (
                    self.name, event.type, event.code, event.value))
        self.save_last(event)

class PowerMateDispatcher():
    """ A dispatcher for our devices """
    def __init__(self):
        super().__init__()
        self.powermates = {}
        self.udev = UdevMonitor()
        self.udev_fileno = self.udev.fileno()

        for dev in filter(lambda x: x.startswith("powermate"),
                          os.listdir("/dev/")):
            powermate = PowerMate(dev)
            self.powermates[powermate.fileno()] = powermate

    def new_powermate(self, device):
        """ This gets called when we get a new powermate """
        if not device:
            return
        for devlink in device['DEVLINKS'].split(' '):
            if devlink.startswith('/dev/powermate'):
                powermate = PowerMate(devlink[5:])
                self.powermates[powermate.fileno()] = powermate
                break

    @property
    def rlist(self):
        """ the rlist for select """
        return [k for k in self.powermates] + [self.udev_fileno]

    def run(self):
        """ this is our loop... """
        while self.powermates:
            r, _, _ = select.select(self.rlist, [], [])
            for fileno in r:
                if fileno == self.udev_fileno:
                    for device in self.udev.new_devices():
                        self.new_powermate(device)
                else:
                    powermate = self.powermates[fileno]
                    if powermate.read():
                        del self.powermates[fileno]

if __name__ == "__main__":
    dispatcher = PowerMateDispatcher()

    # If we can figure out how to add them on hotplug, we won't need this.
    if not dispatcher.powermates:
        sys.exit(0)

    dispatcher.run()
