import time

import dbus
from .device import Device
from .constants import *


def find_adapter(bus):
    """
    Returns the first object that the bluez service has that has a GattManager1 interface
    """
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'), DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if GATT_MANAGER_IFACE in props.keys():
            return o

    return None


class Adapter:

    IFACE = 'org.bluez.Adapter1'

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.adapter = find_adapter(self.bus)

        if not self.adapter:
            print("GattManager1 interface not found.")
            return

        self.obj = self.bus.get_object(BLUEZ_SERVICE_NAME, self.adapter)

        self.adapter_props = dbus.Interface(self.obj,
                                            dbus.PROPERTIES_IFACE)

        self.adapter_methods = dbus.Interface(self.obj,
                                              self.IFACE)

    def get_address(self):
        return self.adapter_props.Get(self.IFACE, 'Address')

    # on = 0 - Power off
    # on = 1 - Power on
    def set_power(self, on):
        self.adapter_props.Set(self.IFACE, 'Powered', dbus.Boolean(on))

    def get_devices(self):
        man_obj = self.bus.get_object(BLUEZ_SERVICE_NAME, '/')
        manager = dbus.Interface(man_obj, 'org.freedesktop.DBus.ObjectManager')
        data = manager.GetManagedObjects()

        result = []
        for path in data.keys():
            interfaces = data[path]
            for interface in interfaces.keys():
                if interface == "org.bluez.Device1":
                    result.append(path)

        return result

    # Only show devices that implement a service with given UUID.
    def get_devices_by_uuid(self, uuid: str):
        devs = self.get_devices()

        result = []
        for path in devs:
            dev = Device(self.bus, path)
            uuids = dev.get_uuids()
            if '0000' + uuid + '-0000-1000-8000-00805f9b34fb' in uuids:
                result.append(dev)
        return result

    # Get the device with a given address.
    def get_device_by_addr(self, addr: str):
        devs = self.get_devices()

        result = None
        for path in devs:
            dev = Device(self.bus, path)
            a = dev.get_address()
            if addr == a:
                result = dev
        return result

    def get_device(self, path):
        return Device(self.bus, path)

    def start_discovery(self):
        self.adapter_methods.StartDiscovery()

    def stop_discovery(self):
        self.adapter_methods.StopDiscovery()

    # time out in seconds
    def discover(self, timeout):
        self.start_discovery()
        time.sleep(timeout)
        self.stop_discovery()
