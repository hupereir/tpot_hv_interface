#!/usr/bin/env python3
import ctypes
import pathlib

# Load the shared library into ctypes
libname = "libcaen_hv_interface.so"
c_lib = ctypes.CDLL(libname)

# connect
answer = c_lib.connect_to_interface( b'10.20.34.154', b'admin', b'admin')
if answer == 0:
    print( "Unable to connect" )
    exit

c_lib.get_v0set.restype = ctypes.c_float

c_lib.set_v0set(b'NEZ_R1', ctypes.c_float(100.0))
answer = c_lib.get_v0set(b'NEZ_R1')
print( f"answer: {answer}" )

#disconnect
c_lib.disconnect_from_interface()
