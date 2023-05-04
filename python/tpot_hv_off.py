#!/usr/bin/env python3
import ctypes
import pathlib
import sys
import time

from tpot_hv_util import *

# usage
if len(sys.argv) == 1:
  print(
    'usage: \n'
    '  tpot_hv_on.py south|north|all|<detector names>|<channel names>\n'
    '\nwith\n'
    '  <detector names>: a list of detectors to turn off, e.g. NCOP SEW ...\n'
    '  <channel names> : a list of single channels to turn off, e.g. NCOP_D SEW_R1 ...')
  exit(0)

# get channel names
channel_dict = parse_arguments( sys.argv[1:] )

# ask for confirmation
print( 'this will turn off the following channels:' )
print_channels( channel_dict )
reply = input('confirm (y/n) ? ')
if reply != 'y' and reply != 'yes':
  exit(0)

# Load the shared library into ctypes
path = "/home/phnxrc/hpereira/lib"
libname = f"{path}/libtpot_hv_interface.so"
c_lib = ctypes.CDLL(libname)

# connect
answer = c_lib.connect_to_interface( b'10.20.34.154', b'admin', b'admin')
if answer == 0:
    print( "Unable to connect" )
    exit(1)

for det_name in sorted(channel_dict.keys()):
  print( f'processing {det_name}' )
  for ch_name in sorted(channel_dict[det_name] ):
    print( f'  {ch_name}' )
    c_lib.set_channel_on( bytes(ch_name,'ascii'),0 )
    time.sleep(1)
  print('')

#disconnect
c_lib.disconnect_from_interface()
