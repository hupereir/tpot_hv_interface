#!/usr/bin/env python3
import ctypes
import sys
import time
import json

from tpot_hv_util import *

print( 
  'usage: \n'
  '  tpot_hv_save_state.py [filename]\n')

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

channel_dict = dict()

# loop over channels
for channel_raw in channels_raw:

  # parse json string
  channel = json.loads(channel_raw)

  # get channel name 
  ch_name = channel["ch_name"]
  if not channel_name_is_valid(ch_name):
    continue

  channel_info = dict((k, channel[k]) for k in ('i0set', 'v0set', 'rup', 'rdwn', 'trip'))
  channel_dict[ch_name]=channel_info

### read trip data from log
def write_state( filename, data ):
  
  # open file
  f = open( filename, 'w' )

  # parse with JSON
  f.write(json.dumps(data,sort_keys=True,indent=2)) 
  
  f.close()
  return

if filename:
  write_state(filename,channel_dict)
else:
  print(json.dumps(channel_dict,sort_keys=True,indent=2))

#disconnect
c_lib.disconnect_from_interface()
