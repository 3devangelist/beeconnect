import usb.core
import usb.util
import sys
import os
import time

READ_TIMEOUT = 1000
DEFAULT_READ_LENGTH = 512

# send a message and read the response
def dispatch(message):
    time.sleep(0.001)
    ep_out.write(message)
    time.sleep(0.009)
    ret = ep_in.read(DEFAULT_READ_LENGTH, READ_TIMEOUT)
    sret = ''.join([chr(x) for x in ret])
    return sret

# find our device
dev = usb.core.find(idVendor=0xffff, idProduct=0x014e)

# was it found? no, try the other device
if dev is None:
    dev = usb.core.find(idVendor=0x29c9, idProduct=0x001)
elif dev is None:
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
    # match the first in endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)


# Verify that the end points exist
assert ep_out is not None
assert ep_in is not None

firmware = sys.argv[1]

assert firmware is not None

fileName, fileExtension = os.path.splitext(firmware)

print "Prepareing to flash device with firmware:{0}.".format(firmware)

file_size = os.path.getsize(firmware)

print "Filesize:{0}".format(file_size)

#Set firmware version string
version = "0.0.0"
ret = dispatch("M114 A{0}\n".format(version))


print ret
message = "M650 A{0}\n".format(file_size)
ret = dispatch(message)
print ret
assert ('ok' in ret) is True

#check for bootloader

print("Flashing"),
with open(firmware, 'rb') as f:
    while True:
        buf = f.read(64)
        
        if not buf: break
        
        ep_out.write(buf)
        ret = []
        while (len(ret) != len(buf)):
            ret += ep_in.read(len(buf), READ_TIMEOUT)
    
        assert (''.join([chr(x) for x in ret]) in buf)
        sys.stdout.write('.')
        sys.stdout.flush()
        #ret = dispatch(buf)
        #print buf.len
        #print(ret==buf)

print ("Flash completed")



dev.reset()






