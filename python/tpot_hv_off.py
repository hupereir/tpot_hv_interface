#!/usr/bin/env python3
import ctypes
import pathlib
import sys
import time

# define default detector names
det_names_south = ['SEP', 'SEZ', 'SCOP', 'SCOZ', 'SCIP', 'SCIZ', 'SWP', 'SWZ']
det_names_north = ['NEP', 'NEZ', 'NCOP', 'NCOZ', 'NCIP', 'NCIZ', 'NWP', 'NWZ']
det_names_all = det_names_south+det_names_north

# parse arguments
det_names = set();
for i, arg in enumerate(sys.argv):
  if i == 0:
    continue
  if arg == 'south' :
    for name in det_names_south:
      det_names.add(name)
  elif arg == 'north':
    for name in det_names_north:
      det_names.add( name )
  elif arg == 'all':
    for name in det_names_all:
      det_names.add( name )
  elif arg in det_names_all:
    det_names.add( arg )
  else :
    print( f'unknown argument: {arg}' )

# Load the shared library into ctypes
path = "/home/phnxrc/hpereira/lib"
libname = f"{path}/libcaen_hv_interface.so"
c_lib = ctypes.CDLL(libname)

# connect
answer = c_lib.connect_to_interface( b'10.20.34.154', b'admin', b'admin')
if answer == 0:
    print( "Unable to connect" )
    exit

# define channel suffix
suffixes = ['_R1', '_R2', '_R3', '_R4', '_D' ]
for name in det_names:
  for suffix in suffixes:
    ch_name = name + suffix
    c_lib.set_channel_on( bytes(ch_name,'ascii'), 0 )
    time.sleep(1)

#disconnect
c_lib.disconnect_from_interface()
