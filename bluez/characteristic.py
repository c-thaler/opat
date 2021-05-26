import dbus
from .constants import *


class Characteristic:

    IFACE = 'org.bluez.GattCharacteristic1'

    def __init__(self, bus, path):
        self.path = path
        self.obj = bus.get_object(BLUEZ_SERVICE_NAME, path)

        self.device_methods = dbus.Interface(self.obj, self.IFACE)
        self.device_props = dbus.Interface(self.obj, dbus.PROPERTIES_IFACE)

    def get_uuid(self):
        return self.device_props.Get(self.IFACE, 'UUID')

    def write_value(self, data):
        options = {'type': 'reliable'}
        message = data
        self.device_methods.WriteValue(dbus.Array(message), dbus.Dictionary(options))

    def read_value(self):
        return self.device_methods.ReadValue(dbus.Dictionary({}))


