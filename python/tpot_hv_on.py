#!/usr/bin/env python3
import ctypes
import pathlib
import sys
import time

from tpot_util import *

if len(sys.argv) == 1:
  print(
    'usage: \n'
    '  tpot_hv_on.py south|north|<detector names>|<channel names>\n'
    '\nwith\n'
    '  <detector names>: a list of detectors to turn on, e.g. NCOP, SEW, ...\n'
    '  <channel names> : a list of single channels to turn on, e.g. NCOP_D, SEW_R1, ...')
  exit(0)

# get channel names
channel_dict = parse_arguments( sys.argv[1:] )

# Load the shared library into ctypes
path = "/home/phnxrc/hpereira/lib"
libname = f"{path}/libcaen_hv_interface.so"
c_lib = ctypes.CDLL(libname)

# connect
answer = c_lib.connect_to_interface( b'10.20.34.154', b'admin', b'admin')
if answer == 0:
    print( "Unable to connect" )
    exit

for det_name in sorted(channel_dict.keys()):
  print( f'processing {det_name}' )
  for ch_name in sorted(channel_dict[det_name] ):
    c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )
    time.sleep(1)

#disconnect
c_lib.disconnect_from_interface()
