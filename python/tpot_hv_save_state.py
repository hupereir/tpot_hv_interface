#!/usr/bin/env python3
import ctypes
import sys
import time
import json
import argparse

from tpot_hv_util import *

### write state data to file
def write_state( filename, data ):
  
  # open file
  f = open( filename, 'w' )

  # parse with JSON
  f.write(json.dumps(data,sort_keys=True,indent=2)) 
  
  f.close()
  return

def main():
	# parse arguments
	parser = argparse.ArgumentParser(
	  prog = 'tpot_hv_save_state',
	  description = 'save HV state to a file',
	  epilog = '')
	
	parser.add_argument(
	  'filename', 
	  help='the filename to which the HV state is saved')
	
	parser.add_argument('-f', '--force', action='store_true', help='do not ask for confirmation')
	args = parser.parse_args()
	
	# filename
	filename = args.filename
	print( f'this will save the HV state to {filename}' )
	if not args.force:
	  reply = input('confirm (y/n) ? ')
	  if reply != 'y' and reply != 'yes':
	    exit(0)
	
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
	
	# split by channel
	channels_raw = re.findall('\{.*?\}',status)
	
	channel_dict = dict()
	
	# loop over channels
	for channel_raw in channels_raw:
	
	  # parse json string
	  channel = json.loads(channel_raw)
	
	  # get channel name 
	  ch_name = channel["ch_name"]
	  if not channel_name_is_valid(ch_name):
	    continue
	
	  channel_info = dict((k, channel[k]) for k in ('i0set', 'v0set', 'rup', 'rdwn', 'trip'))
	  channel_dict[ch_name]=channel_info
	
	if filename:
	  write_state(filename,channel_dict)
	else:
	  print(json.dumps(channel_dict,sort_keys=True,indent=2))
	
	#disconnect
	c_lib.disconnect_from_interface()

if __name__ == '__main__':
  main()
