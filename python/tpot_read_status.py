#!/usr/bin/env python3
import ctypes
import pathlib
import re

# Load the shared library into ctypes
libname = "libcaen_hv_interface.so"
c_lib = ctypes.CDLL(libname)

# connect
answer = c_lib.connect_to_interface( b'10.20.34.154', b'admin', b'admin')
if answer == 0:
    print( "Unable to connect" )
    exit

c_lib.get_channel_status.restype = ctypes.c_char_p
status = str(c_lib.get_channel_status())
# print( f"status: {status}" )

channels_raw = re.findall('\{.*?\}',status)
print( f"channels: {channels_raw}" )

#disconnect
c_lib.disconnect_from_interface()
