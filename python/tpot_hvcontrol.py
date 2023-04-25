#!/bin/env python3

import json
import subprocess
import re

def readall( ip = '10.20.34.154', user = 'admin', password = 'admin' ):
    getter = ['/home/phnxrc/hpereira/CAEN/caen_hv_reader/build/caen_hv_reader',
              '--ip', ip,
              '--user', user,
              '--password', password ]
    answer = subprocess.run(getter, 
                            universal_newlines=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
    channels_raw = re.findall('\{.*\}',answer.stdout)

    # loop over channel lines and parse
    channels = []
    for channel_raw in channels_raw:
        channel = json.loads(channel_raw)
        channels.append(channel)

    return channels
