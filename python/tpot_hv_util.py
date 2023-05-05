#!/usr/bin/env python3
# regular expressions
import re

# parse arguments
# accepted values are: 
# all, south, north, 
# detector name, e.g. NCOZ, SEP
# channel name, e.g. NCOZ_R1, SEP_D
#
# returns a dictionary of all selected channels, grouped by detector names
def parse_arguments( arguments ):

  # define default detector names
  det_names_south = {'SEP', 'SEZ', 'SCOP', 'SCOZ', 'SCIP', 'SCIZ', 'SWP', 'SWZ'}
  det_names_north = {'NEP', 'NEZ', 'NCOP', 'NCOZ', 'NCIP', 'NCIZ', 'NWP', 'NWZ'}
  det_names_all = det_names_south|det_names_north

  suffixes = {'_R1', '_R2', '_R3', '_R4', '_D' }

  # get all detector/single channel names
  det_names = set()
  for arg in arguments:
    if arg == 'south' :
      det_names.update(det_names_south)
    elif arg == 'north':
      det_names.update(det_names_north)
    elif arg == 'all':
      det_names.update(det_names_all)
    elif arg in det_names_all:
      det_names.add( arg )
    else :
      result = re.fullmatch( '(\w+)_(R[1-4]|D)',arg )
      if result and result.group(1)  in det_names_all:
        det_names.add( arg )
      else: 
        print( f'unknown argument: {arg}' )

  # build dictionary
  channel_dict = dict()
  for name in det_names:
    if name in det_names_all:
      channels = set()
      for suffix in suffixes:
        channels.add( name+suffix )
      channel_dict[name] = channels
    else:
      result = re.fullmatch( '(\w+)_(R[1-4]|D)',name )
      module = result.group(1)
      if module in channel_dict.keys():
        channel_dict[module].add(name)
      else:
        channel_dict[module]={name}

  return channel_dict

# print channels from dictionary
def print_channels( channel_dict ):
  for det_name in sorted(channel_dict.keys() ):
    print( f"  {det_name:4}: ", end = '' )
    for ch_name in sorted(channel_dict[det_name]):
      print( f" {ch_name:7} ", end = '' )
    print('')

# check if a channel name is valid
def channel_name_is_valid( channel_name ):
  return re.fullmatch( '(N|S)(CO|CI|E|W)(Z|P)_(R[1-4]|D)',channel_name )
