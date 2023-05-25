#!/usr/bin/env python3
import ctypes
import sys
import time
import argparse

from tpot_hv_util import *

def main():
  # parse arguments
  parser = argparse.ArgumentParser(
    prog = 'tpot_hv_off',
    description = 'Turns off TPOT',
    epilog = '')
  
  parser.add_argument(
    'channels', 
     help='a list of detectors to turn on, e.g. NCOP SEW, or individual channels, e.g  NCOP_D SEW_R1, or south|north|all',
     nargs='+' )
  
  parser.add_argument('-f', '--force', action='store_true', help='do not ask for confirmation')
  args = parser.parse_args()
  
  # get channel names
  channel_dict = parse_arguments( args.channels )
  
  # ask for confirmation
  print( 'this will turn off the following channels:' )
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
      print( f'  {ch_name}' )
      c_lib.set_channel_on( bytes(ch_name,'ascii'),0 )
      time.sleep(0.1)
    print('')
  
  #disconnect
  c_lib.disconnect_from_interface()

if __name__ == '__main__':
  main()
