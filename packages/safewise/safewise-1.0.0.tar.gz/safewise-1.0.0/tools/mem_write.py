#!/usr/bin/env python3
from safewiselib.debuglink import DebugLink
from safewiselib.client import SafeWISEClient
from safewiselib.transport import enumerate_devices
import binascii
import sys


def main():
    # List all debuggable SafeWISEs
    devices = [device for device in enumerate_devices() if hasattr(device, 'find_debug')]

    # Check whether we found any
    if len(devices) == 0:
        print('No SafeWISE found')
        return

    # Use first connected device
    transport = devices[0]
    debug_transport = devices[0].find_debug()

    # Creates object for manipulating SafeWISE
    client = SafeWISEClient(transport)
    debug = DebugLink(debug_transport)

    debug.memory_write(int(sys.argv[1], 16), binascii.unhexlify(sys.argv[2]), flash=True)
    client.close()


if __name__ == '__main__':
    main()
