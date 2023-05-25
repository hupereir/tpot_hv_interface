#!/usr/bin/env python3
import ctypes
import sys
import time
import argparse
import os.path
import json

from tpot_hv_util import *

### read masked channels from file
def read_mask( filename ):
  
  if not os.path.isfile(filename):
    print(f'{filename} does not exist')
    return {}

  # open file
  f = open( filename )

  # parse with JSON
  masked_channels = json.load(f)
  
  f.close()
  return masked_channels

def main():
  # parse arguments
  parser = argparse.ArgumentParser(
    prog = 'tpot_hv_on',
    description = 'Turns on TPOT',
    epilog = '')
  
  parser.add_argument(
    'channels', 
     help='a list of detectors to turn on, e.g. NCOP SEW, or individual channels, e.g  NCOP_D SEW_R1, or south|north|all',
     nargs='+' )
  
  parser.add_argument('-m', '--mask', type=str, required=False, metavar='filename', help='masks channels as read from input file')
  parser.add_argument('-f', '--force', action='store_true', help='do not ask for confirmation')
  args = parser.parse_args()
  
  if args.mask:
    print( f'will not turn on channels found in {args.mask}' )
    masked_channels = read_mask(args.mask)
  else:
    masked_channels = {}
  
  # get channel names
  channel_dict = parse_arguments( args.channels )
  if not channel_dict:
    exit(0)
  
  # ask for confirmation
  print( 'this will turn on the following channels:' )
  print_channels( channel_dict )
  if not args.force:
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
      if ch_name in masked_channels.keys() and masked_channels[ch_name]:
        print( f'  {ch_name} is masked' )
      else:
        print( f'  {ch_name}' )
        c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )
        time.sleep(0.1)
    print('')
  
  #disconnect
  c_lib.disconnect_from_interface()

if __name__ == '__main__':
  main()
