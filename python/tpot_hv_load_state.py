#!/usr/bin/env python3
import ctypes
import sys
import time
import json
import os.path

from tpot_hv_util import *

if len(sys.argv) < 2:
  print( 
    'usage: \n'
    '  tpot_hv_load_state.py <filename>\n')
  exit(0)

filename = sys.argv[1]

### read trip data from log
def read_data( filename ):
  
  if not os.path.isfile(filename):
    print(f'{filename} does not exist')
    exit(0)

  # open file
  f = open( filename )

  # parse with JSON
  channel_dict = json.load(f)
  
  f.close()
  return channel_dict

channel_dict = read_data(filename)

if not channel_dict:
  print( f'invalid state read from file {filename}' )
  exit(0)

# Load the shared library into ctypes
path = "/home/phnxrc/hpereira/lib"
libname = f"{path}/libtpot_hv_interface.so"
c_lib = ctypes.CDLL(libname)
c_lib.get_channel_status.restype = ctypes.c_char_p

# connect
answer = c_lib.connect_to_interface( b'10.20.34.154', b'admin', b'admin')
if answer == 0:
  print( "Unable to connect" )
  exit(1)

for ch_name in sorted(channel_dict.keys() ):
  print( f'processing {ch_name}' )
  channel_data=channel_dict[ch_name]
  c_lib.set_parameter_float( bytes(ch_name,'ascii'), b'I0Set', ctypes.c_float(channel_data['i0set']) )
  c_lib.set_parameter_float( bytes(ch_name,'ascii'), b'V0Set', ctypes.c_float(channel_data['v0set']) )
  c_lib.set_parameter_float( bytes(ch_name,'ascii'), b'RUp', ctypes.c_float(channel_data['rup']) )
  c_lib.set_parameter_float( bytes(ch_name,'ascii'), b'RDWn', ctypes.c_float(channel_data['rdwn']) )
  c_lib.set_parameter_float( bytes(ch_name,'ascii'), b'Trip', ctypes.c_float(channel_data['trip']) )
  time.sleep(0.1)

#disconnect
c_lib.disconnect_from_interface()
