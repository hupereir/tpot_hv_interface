#!/usr/bin/env python3
import ctypes
import sys
import time
import argparse

from tpot_hv_util import *

def main():

  # usage
  # parse arguments
  parser = argparse.ArgumentParser(
    prog = 'tpot_hv_set_trip.py',
    epilog = '')
  
  parser.add_argument(
    'value', 
    type=float,
    help='the value to assign to TRIP')
  
  parser.add_argument(
    'channels', 
    type=str,
    help='a list of channels to which TRIP is assigned, e.g. NCOP_D SEW_R1...',
    nargs='+' )
  args = parser.parse_args()
 
  # parse arguments
  value = float(args.value);
  ch_names = sorted(filter_channel_names( sorted( set(args.channels))))
  if not ch_names:
    exit(0)
  
  # ask for confirmation
  print( f'this will set TRIP to {value}s for the following channels: {ch_names}' )
  reply = input('confirm (y/n) ? ')
  if reply != 'y' and reply != 'yes':
    exit(0)
  
  # Load the shared library into ctypes
  path = "/home/phnxrc/operations/TPOT/lib"
  libname = f"{path}/libtpot_hv_interface.so"
  c_lib = ctypes.CDLL(libname)
  c_lib.get_parameter_float.restype = ctypes.c_float
  
  # connect
  answer = c_lib.connect_to_interface( b'10.20.34.154', b'admin', b'admin')
  if answer == 0:
    print( "Unable to connect" )
    exit
  
  for ch_name in ch_names:
    print( f'processing {ch_name}' )
    c_lib.set_parameter_float( bytes(ch_name,'ascii'), b'Trip', ctypes.c_float(value) )
    time.sleep(0.1)
  
  for ch_name in ch_names:
    result =  c_lib.get_parameter_float( bytes(ch_name,'ascii'), b'Trip' )
    if result != value:
      print( f'{ch_name} setting failed. value: {value} readback: {result}' )
  
  #disconnect
  c_lib.disconnect_from_interface()

if __name__ == '__main__':
  main()
