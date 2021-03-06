#!/usr/bin/python3

import argparse
import sys

import transport
from bluez import Adapter
from http_p100 import HttpTransport, RequestSetDeviceInfo

TAPO_WRITE_CHAR_NAME = 'service000c/char0010'
TAPO_READ_CHAR_NAME = 'service000c/char000d'
TAPO_SERVICE_UUID = '8641'

def create_transport(device):
    char_write = device.get_characteristic(TAPO_WRITE_CHAR_NAME)
    char_read = device.get_characteristic(TAPO_READ_CHAR_NAME)
    return transport.Transport(char_read, char_write)


def scan(args, adapter):
    print('Scanning...')
    adapter.discover(5)
    devices = adapter.get_devices_by_uuid(TAPO_SERVICE_UUID)

    if len(devices) == 0:
        print("No devices found.")
        return

    print('Found:')
    for d in devices:
        print('\t' + d.get_address())


def info(args, adapter):
    device = adapter.get_device_by_addr(args.baddr)
    device.connect()
    t = create_transport(device)

    req = transport.RequestQuickSetup()
    resp = t.request(req)

    print('Type: ' + resp.get_type())
    print('Model: ' + resp.get_model())

    print('Components:')
    for c in resp.get_components():
        print('\t' + c['id'].ljust(16) + ' v' + str(c['ver_code']))

    device.disconnect()


def wifi_scan(args, adapter):
    device = adapter.get_device_by_addr(args.baddr)
    device.connect()
    t = create_transport(device)

    req = transport.RequestWifiScanInfo()
    resp = t.request(req)

    ap_list = resp.get_ap_list()
    index = resp.get_next_index()
    while not resp.is_complete():
        req = transport.RequestWifiScanInfo(index)
        resp = t.request(req)
        ap_list += resp.get_ap_list()
        index = resp.get_next_index()

    print('SSID'.ljust(32) + 'Key type'.ljust(16) + 'Signal level')
    for w in ap_list:
        print(w['ssid'].ljust(32) + w['key_type'].ljust(16) + str(w['signal_level']))

    device.disconnect()


def wifi_set(args, adapter):
    device = adapter.get_device_by_addr(args.baddr)
    device.connect()
    t = create_transport(device)

    req = transport.RequestSetQsInfo(wifi_ssid=args.ssid, wifi_key=args.key,
                                     web_user=args.email, web_password=args.password)
    resp = t.request(req)

    if resp.has_error():
        print('Setting WIFI failed.')
        return

    print(resp.get_result())

    device.disconnect()


def switch(args, adapter):
    t = HttpTransport(args.ipaddr, args.email, args.password)

    if args.onoff == 'on':
        enable = True
    elif args.onoff == 'off':
        enable = False
    else:
        print(f'Argument onoff must be \'on\' or \'off\' but was \'{args.onoff}\'.')
        return -1

    req = RequestSetDeviceInfo(enable)
    t.request(req)


def print_usage(parser: argparse.ArgumentParser):
    parser.print_usage()


def main():
    parser = argparse.ArgumentParser(description='Setup Tapo smart devices via bluetooth.')
    subparsers = parser.add_subparsers(help='Available commands')

    parser_scan = subparsers.add_parser('scan', help='scan for devices')
    parser_scan.set_defaults(func=scan)

    parser_info = subparsers.add_parser('info', help='info for device')
    parser_info.add_argument('baddr', type=str, help='BT address of device')
    parser_info.set_defaults(func=info)

    parser_wifi_scan = subparsers.add_parser('wifi_scan', help='scan WiFis')
    parser_wifi_scan.add_argument('baddr', type=str, help='BT address of device')
    parser_wifi_scan.set_defaults(func=wifi_scan)

    parser_wifi_set = subparsers.add_parser('wifi_setup', help='wifi settings')
    parser_wifi_set.add_argument('baddr', type=str, help='BT address of device')
    parser_wifi_set.add_argument('ssid', type=str, help='SSID of the WiFi network')
    parser_wifi_set.add_argument('key', type=str, help='Key of the WiFi network (!SENT UNENCRYPTED!)')
    parser_wifi_set.add_argument('email', type=str, default='edcrfv@edcujm.com', help='email')
    parser_wifi_set.add_argument('password', type=str, default='Passw0rd', help='password')
    parser_wifi_set.set_defaults(func=wifi_set)

    parser_switch = subparsers.add_parser('switch', help='Turn the plug on or off')
    parser_switch.add_argument('ipaddr', type=str, help='IP address of device')
    parser_switch.add_argument('email', type=str, help='email')
    parser_switch.add_argument('password', type=str, help='password')
    parser_switch.add_argument('onoff', type=str, help='Must be \'on\' or \'off\'.')
    parser_switch.set_defaults(func=switch)

    if len(sys.argv) == 1:
        print_usage(parser)
        exit(-1)

    args = parser.parse_args()

    adapter = Adapter()
    adapter.set_power(1)

    args.func(args, adapter)

    adapter.set_power(0)


main()
