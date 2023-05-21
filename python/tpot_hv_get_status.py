#!/usr/bin/env python3
import ctypes
import pathlib
import sys
import time
import json
import re

from tpot_hv_util import *

# usage
if len(sys.argv) == 1:
  print(
    'usage: \n'
    '  tpot_hv_get_status.py south|north|all|<detector names>|<channel names>\n'
    '\nwith\n'
    '  <detector names>: a list of detectors for which to get the status, e.g. NCOP SEW ...\n'
    '  <channel names> : a list of single channels to turn on, e.g. NCOP_D SEW_R1 ...')
  exit(0)

# get channel names
channel_dict = parse_arguments( sys.argv[1:] )

# store selected channels
selected_channels = set()
for det_name in sorted(channel_dict.keys()):
  print( f'processing {det_name}' )
  for ch_name in sorted(channel_dict[det_name] ):
    selected_channels.add(ch_name)

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

status = str(c_lib.get_channel_status())

# split by channel
channels_raw = re.findall('\{.*?\}',status)

for channel_raw in channels_raw:

  # parse json string
  channel = json.loads(channel_raw)

  # get channel name 
  ch_name = channel["ch_name"]
  if not ch_name in selected_channels: 
    continue  

  print( '{ "slot_id": %2i, '
         '"ch_id": %2i, '
         '"ch_name": "%7s", '
         '"v0set": %6.2f, '
         '"vmon": %6.2f, '
         '"imon": %7.3f, '
         '"status": "%5s", '
         '"trip": %i }'
         % (channel['slot_id'],channel['ch_id'],
            channel['ch_name'],
            channel['v0set'],channel['vmon'],channel['imon'],
            channel['status_Hex'], channel['trip']))

#disconnect
c_lib.disconnect_from_interface()
