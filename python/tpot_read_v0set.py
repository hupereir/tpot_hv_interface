#!/usr/bin/env python3
import ctypes

# Load the shared library into ctypes
libname = "/home/hpereira/sphenix/src/CAEN/caen_hv_reader/install/lib/libcaen_hv_interface.so"
c_lib = ctypes.CDLL(libname)

answer = c_lib.connect_to_interface()
print( f"answer: {answer}" )

slot=0
channel=0
answer = c_lib.get_v0set(slot,channel)
