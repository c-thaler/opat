import dbus
from .characteristic import Characteristic
from .constants import *


class Device:

    IFACE = 'org.bluez.Device1'

    def __init__(self, bus, path):
        self.path = path
        self.bus = bus
        self.obj = bus.get_object(BLUEZ_SERVICE_NAME, path)

        self.device_methods = dbus.Interface(self.obj, self.IFACE)
        self.device_props = dbus.Interface(self.obj, dbus.PROPERTIES_IFACE)

    def connect(self):
        self.device_methods.Connect()

    def disconnect(self):
        self.device_methods.Disconnect()

    def get_prop(self, prop_name):
        return self.device_props.Get(self.IFACE, prop_name)

    def get_address(self):
        return self.device_props.Get(self.IFACE, 'Address')

    def get_uuids(self):
        resp = self.device_props.Get(self.IFACE, 'UUIDs')
        return [str(s) for s in resp]

    def get_characteristic(self, path):
        return Characteristic(self.bus, self.path + '/' + path)

