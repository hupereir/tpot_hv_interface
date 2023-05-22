#!/usr/bin/env python3
import ctypes
import pathlib
import sys
import time
import json
import re
import os.path

from tpot_hv_util import *

### read trip data from log
def read_trip_data( filename ):
  
  if not os.path.isfile(filename):
    print(f'{filename} does not exist')
    return dict()

  # open file
  f = open( filename )

  # parse with JSON
  trip_data = json.load(f)
  
  f.close()
  return trip_data


### read trip data from log
def write_trip_data( filename, trip_data ):
  
  # open file
  f = open( filename, 'w' )

  # parse with JSON
  f.write(json.dumps(trip_data,indent=2)) 
  
  f.close()
  return

# Load trip data
trip_log_filename = '/home/phnxrc/hpereira/tpot_hv_interface/config/tpot_trips.json'
trip_data = read_trip_data( trip_log_filename )

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

# keep track of tripped channels
tripped_ch_names = set()

# split by channel
channels_raw = re.findall('\{.*?\}',status)

# loop over channels
for channel_raw in channels_raw:

  # parse json string
  channel = json.loads(channel_raw)

  # focus on tripped channels
  if channel['trip']:
    tripped_ch_names.add(channel['ch_name'])

# exit if not channels are tripped
if not tripped_ch_names:
  exit(0)

# loop over channels, increment trip counters
max_trip_count = 3
for ch_name in tripped_ch_names:
  print( f'processing {ch_name}')
  if ch_name in trip_data:

    # check how many times the channel triped
    trips = trip_data[ch_name]['trips']
    if trips >= max_trip_count:
      # max number of trips reached, turning channel off      
      print( f'{cha_name} number of trips is at maximum ({max_trip_count}). Turning the channel off' )  
      c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )
      c_lib.set_channel_off( bytes(ch_name,'ascii'),0 )
    else:   
      # increment number of trips, and recover channel
      trip_data[ch_name]['trips'] = trip_data[ch_name]['trips']+1
      c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )
  else:
    # increment number of trips, and recover channel
    trip_data[ch_name] ={'trips':1}
    c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )

  # store time of trip  
  trip_data[ch_name]['last_trip_time'] = int(time.time())

# write back
write_trip_data( trip_log_filename, trip_data )