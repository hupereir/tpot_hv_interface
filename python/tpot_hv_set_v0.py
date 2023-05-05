#!/usr/bin/env python3
import ctypes
import pathlib
import sys
import time

from tpot_hv_util import *

# usage
if len(sys.argv) < 3:
  print(
    'usage: \n'
    '  tpot_hv_set_v0.py <value> <channel names>\n'
    '\nwith\n'
    '  <value>          the value to assign to V0SET ...\n'
    '  <channel names>  a list of single channels to which V0SET is assigned, e.g. NCOP_D SEW_R1 ...')
  exit(0)

value = float(sys.argv[1]);
ch_names = sorted( set(sys.argv[2:]) )
print( f'tpot_hv_set_v0 - value: {value}' )
print( f'tpot_hv_set_v0 - channel names: {ch_names}' )

# Load the shared library into ctypes
path = "/home/phnxrc/hpereira/lib"
libname = f"{path}/libcaen_hv_interface.so"
c_lib = ctypes.CDLL(libname)

# connect
answer = c_lib.connect_to_interface( b'10.20.34.154', b'admin', b'admin')
if answer == 0:
    print( "Unable to connect" )
    exit

for ch_name in ch_names:
  if channel_name_is_valid( ch_name ): 
    c_lib.set_parameter_float( bytes(ch_name,'ascii'), b'V0Set', ctypes.c_float(value) )
    time.sleep(1)

#disconnect
c_lib.disconnect_from_interface()
