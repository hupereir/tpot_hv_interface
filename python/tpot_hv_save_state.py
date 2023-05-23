#!/usr/bin/env python3
import ctypes
import pathlib
import sys
import time
import json
import re

from tpot_hv_util import *

print( 
  'usage: \n'
  '  tpot_hv_save_state.py <filename>\n')

if len(sys.argv) > 1:
  filename = sys.argv[1]
else:
  filename = ''

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

# read status for all channels
status = str(c_lib.get_channel_status())

# split by channel
channels_raw = re.findall('\{.*?\}',status)

channel_list = []

# loop over channels
for channel_raw in channels_raw:

  # parse json string
  channel = json.loads(channel_raw)

  # get channel name 
  ch_name = channel["ch_name"]
  if not channel_name_is_valid(ch_name):
    continue

  channel_list.add( channel )

### read trip data from log
def write_state( filename, trip_data ):
  
  # open file
  f = open( filename, 'w' )

  # parse with JSON
  f.write(json.dumps(trip_data,indent=2)) 
  
  f.close()
  return

write_state( filename, channel_list )

#disconnect
c_lib.disconnect_from_interface()
