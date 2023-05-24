#!/usr/bin/env python3
import ctypes
import sys
import time
import json
import re
import argparse
import os.path

from tpot_hv_util import *

parser = argparse.ArgumentParser(
                    prog = 'tpot_hv_recover_trips',
                    description = 'Recovers tripped channel in TPOT',
                    epilog = '')
parser.add_argument('-f', '--force', action='store_true')

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

  ch_name = channel['ch_name']
  if not channel_name_is_valid( ch_name ):
    continue
  trip = bool(channel['status']&(1<<9))
  if trip:
    tripped_ch_names.add(ch_name)

# exit if not channels are tripped
if not tripped_ch_names:
  print( 'no tripped channels found' )
  exit(0)


# ask for confirmation
if not arg.force:
  print( f'this will recover the following tripped channels: {tripped_ch_names}' )
  reply = input('confirm (y/n) ? ')
  if reply != 'y' and reply != 'yes':
    exit(0)

# loop over channels, increment trip counters
for ch_name in tripped_ch_names:
  if ch_name in trip_data:
    # increment number of trips, and recover channel
    trip_data[ch_name]['trips'] = trip_data[ch_name]['trips']+1
  else:
    # increment number of trips, and recover channel
    trip_data[ch_name] ={'trips':1}

  # store time of trip  
  trip_data[ch_name]['last_trip_time'] = int(time.time())

  # recover
  max_trip_count = 20
  trips = trip_data[ch_name]['trips']
  if trips > max_trip_count:
    # max number of trips reached, turning channel off      
    print( f'{cha_name}: number of trips is at maximum ({max_trip_count}). Turning the channel off' )  
    c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )
    c_lib.set_channel_off( bytes(ch_name,'ascii'),0 )
  else:   
    # increment number of trips, and recover channel
    print( f'{ch_name}: recovering trip' )  
    trip_data[ch_name]['trips'] = trip_data[ch_name]['trips']+1
    c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )
  time.sleep(0.1)

# write to file
write_trip_data( trip_log_filename, trip_data )
