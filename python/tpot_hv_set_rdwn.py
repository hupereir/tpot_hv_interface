#!/usr/bin/env python3
import ctypes
import pathlib
import sys
import time

from tpot_hv_util import *

# usage
if len(sys.argv) < 3:
  print(
    'usage: \n'
    '  tpot_hv_set_rdwn.py <value> <channel names>\n'
    '\nwith\n'
    '  <value>          the value to assign to RDWN (V/s)\n'
    '  <channel names>  a list of single channels to which RDWN is assigned, e.g. NCOP_D SEW_R1 ...')
  exit(0)

# parse arguments
value = float(sys.argv[1]);
ch_names = sorted(filter_channel_names( sorted( set(sys.argv[2:]))))
if not ch_names:
  exit(0)

# ask for confirmation
print( f'this will set RDWN to {value}V/s for the following channels: {ch_names}' )
reply = input('confirm (y/n) ? ')
if reply != 'y' and reply != 'yes':
  exit(0)

# Load the shared library into ctypes
path = "/home/phnxrc/hpereira/lib"
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
  c_lib.set_parameter_float( bytes(ch_name,'ascii'), b'RDWn', ctypes.c_float(value) )
  time.sleep(1)

for ch_name in ch_names:
  result =  c_lib.get_parameter_float( bytes(ch_name,'ascii'), b'RDWn' )
  if result != value:
    print( f'{ch_name} setting failed. value: {value} readback: {result}' )

#disconnect
c_lib.disconnect_from_interface()
