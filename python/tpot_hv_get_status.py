#!/usr/bin/env python3
import ctypes
import sys
import time
import json
import re
import argparse

from tpot_hv_util import *

def main():
  # parse arguments
  parser = argparse.ArgumentParser(
    prog = 'tpot_hv_get_status',
    description = 'print HV status for selected channels',
    epilog = '')
  
  parser.add_argument(
    'channels', 
    help='a list of channels from which the status will be printed, e.g. NCOP SEW, or individual channels, e.g  NCOP_D SEW_R1, or south|north|all',
    nargs='+' )
  args = parser.parse_args()
  
  # get channel names
  channel_dict = parse_arguments( args.channels )
  
  # store selected channels
  selected_channels = set()
  for det_name in sorted(channel_dict.keys()):
    for ch_name in sorted(channel_dict[det_name] ):
      selected_channels.add(ch_name)
      
  if not selected_channels:
    exit(0)

  # Load the shared library into ctypes
  path = "/home/phnxrc/operations/TPOT/lib"
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

  # counters
  count_total = 0
  count_good = 0

  # loop over channels

  print( 'slot_id ch_id ch_name   v0set  i0set  rup rdwn trip    vmon    imon  status' )

  for channel_raw in channels_raw:

    # parse json string
    channel = json.loads(channel_raw)

    # get channel name 
    ch_name = channel["ch_name"]
    if not ch_name in selected_channels: 
      continue  

    if channel_name_is_resist(ch_name):
      count_total = count_total+1
      if channel['v0set'] >= 399 and channel['status'] == 1:
        count_good = count_good+1

    print( '%5i '
           '%5i   '
           '%7s  '
           '%6.2f '
           '%6.2f '
           '%4.0f '
           '%4.0f '
           '%4.0f  '
           '%6.2f '
           '%7.3f '
           '%6s '
           % (channel['slot_id'],
              channel['ch_id'],
              channel['ch_name'],
              channel['v0set'],
              channel['i0set'],
              channel['rup'],
              channel['rdwn'],
              channel['trip'],
              channel['vmon'],
              channel['imon'],
              channel['status_Hex'] ) )

  if count_total : 
    print( f'\ntotal: {count_total} good: {count_good} ratio: %.3f%%' %(100.*count_good/count_total) )

  #disconnect
  c_lib.disconnect_from_interface()

if __name__ == '__main__':
  main()
