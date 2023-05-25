#!/usr/bin/env python3
import ctypes
import sys
import time
import json
import re
import argparse
import os.path
import datetime

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

def init_mask_file():
  det_names_south = {'SEP', 'SEZ', 'SCOP', 'SCOZ', 'SCIP', 'SCIZ', 'SWP', 'SWZ'}
  det_names_north = {'NEP', 'NEZ', 'NCOP', 'NCOZ', 'NCIP', 'NCIZ', 'NWP', 'NWZ'}
  det_names_all = det_names_south | det_names_north
  suffixes = {'_R1', '_R2', '_R3', '_R4', '_D' }

  mask = {}
  for det in det_names_all:
    for suf in suffixes:
      detector_name = det + suf
      mask[detector_name] = False
  with open("/home/phnxrc/hpereira/tpot_hv_interface/config/tpot_mask.json", "w") as f:
    json.dump(mask, f, indent=2, sort_keys=True)

def main():
  
  parser = argparse.ArgumentParser(
                      prog = 'tpot_hv_recover_trips',
                      description = 'Recovers tripped channel in TPOT',
                      epilog = '')
  parser.add_argument('-f', '--force', action='store_true', help='do not ask for confirmation')
  args = parser.parse_args()

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
  print( f'this will recover the following tripped channels: {tripped_ch_names}' )
  if not args.force:
    reply = input('confirm (y/n) ? ')
    if reply != 'y' and reply != 'yes':
      exit(0)

  # loop over channels, increment trip counters
  for ch_name in tripped_ch_names:
    if ch_name in trip_data:
      # Increment the absolute numebr of trips
      trip_data[ch_name]['trips_abs'] += 1
      # Check how recent the last trip was
      last_trip = datetime.datetime.fromtimestamp(trip_data[ch_name]['last_trip_time'])
      current_time = datetime.datetime.now()
      if current_time - last_trip < datetime.timedelta(hours=1):
        # increment number of trips, and recover channel
        trip_data[ch_name]['trips_rel'] = trip_data[ch_name]['trips_rel']+1
      else:
        # if it has been longer than 1 hour, reset the trip counter
        trip_data[ch_name]['trips_rel'] = 1
    else:
      # increment number of trips, and recover channel
      trip_data[ch_name] ={'trips_rel':1, 'trips_abs':1}

    # store time of trip  
    trip_data[ch_name]['last_trip_time'] = int(time.time())

    # recover
    max_trip_count = 3
    trips = trip_data[ch_name]['trips_rel']
    if trips > max_trip_count:
      # max number of trips reached, turning channel off      
      print( f'{ch_name}: number of trips is at maximum ({max_trip_count}). Turning the channel off' )  
      c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )
      time.sleep(0.2)
      c_lib.set_channel_on( bytes(ch_name,'ascii'),0 )
      
      # Updating mask file
      masked_data = None
      with open("/home/phnxrc/hpereira/tpot_hv_interface/config/tpot_mask.json", "r") as f:
        masked_data = json.load(f)
      masked_data[ch_name] = True
      with open("/home/phnxrc/hpereira/tpot_hv_interface/config/tpot_mask.json", "w") as f:
        json.dump(masked_data, f, indent=2, sort_keys=True)

    else:   
      # increment number of trips, and recover channel
      print( f'{ch_name}: recovering trip' )  
      c_lib.set_channel_on( bytes(ch_name,'ascii'),0 )
      time.sleep(0.2)
      c_lib.set_channel_on( bytes(ch_name,'ascii'),1 )
    time.sleep(0.1)

  # write to file
  write_trip_data( trip_log_filename, trip_data )

if __name__ == '__main__':
  main()
