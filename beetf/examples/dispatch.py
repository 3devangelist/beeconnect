import usb.core
import usb.util
import sys

READ_TIMEOUT = 1000
DEFAULT_READ_LENGTH = 512

# find our device
dev = usb.core.find(idVendor=0xffff, idProduct=0x014e)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep_out = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)


ep_in = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert ep_out is not None
assert ep_in is not None


message = "M300\n"

print sys.argv
if sys.argv[1]:
    message = sys.argv[1] + '\n'

# write the data
ep_out.write(message)


ret = ep_in.read(DEFAULT_READ_LENGTH, READ_TIMEOUT)
sret = ''.join([chr(x) for x in ret])
print sret

dev.reset()






