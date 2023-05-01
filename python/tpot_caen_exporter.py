#!/usr/bin/env python3

import argparse
from flask import Response, Flask, request, render_template_string
import prometheus_client
from prometheus_client import CollectorRegistry, Gauge, Info, Counter, Summary
import re
import socket
import time
from threading import Lock

from tpot_hvcontrol import *

parser = argparse.ArgumentParser(
    prog='status',
    description='Prometheus Data Exporter for sPHENIX TPOT HV module',
    epilog='')
parser.add_argument('-p', '--port', default=5100,  help='Webservice port')
parser.add_argument('-l', '--limit', default=2,
                    help='Scrubbing time throttling limit in seconds')
args = parser.parse_args()

throttling_limit = float(args.limit)
print(f"Throttling request to no less than {throttling_limit} seconds")

# initialization
metric_prefix = 'sphenix_tpot_hv'
label_host = {}

registry = CollectorRegistry()
metrics = {}

# Host prints
print(f"Host name:        {socket.gethostname()}")
label_host[f"hostname"] = socket.gethostname()

request_counter = Counter(f"{metric_prefix}_request_counter", 'Requests processed',
                          list(label_host.keys()) + ['status'], registry=registry)
request_time = Summary(f"{metric_prefix}_requests_processing_seconds", "Inprogress HTTP requests",
                       list(label_host.keys()), registry=registry)

# map detector name to detector index
detector_map = {
    'NEP':0, 'NEZ':1, 'NCIP':2,  'NCIZ':3,  'NCOP':4,  'NCOZ':5,  'NWP':6,  'NWZ':7,
    'SEP':8, 'SEZ':9, 'SCIP':10, 'SCIZ':11, 'SCOP':12, 'SCOZ':13, 'SWP':14, 'SWZ':15,
}

# define channel properties and json equivalent
property_map = {
    'v0set': {'metric':'v0set', 'comment':'request voltage (V)', 'json':'v0set' },
    'vmon': {'metric':'vmon', 'comment':'measured voltage (V)', 'json':'vmon' },
    'imon': {'metric':'imon', 'comment':'measured current (uA)', 'json':'imon' },
    'status': {'metric':'status', 'comment':'channel status (bit pattern)', 'json':'status' },
    'trip': {'metric':'trip', 'comment':'channel trip (boolean)', 'json':'trip' }
}

properties = list(property_map.keys())

# hv channel information
def hv_channel_information(verbose=False):
    channels = readall()

    channel_label={}

    # loop over channels
    for channel in channels:

        # skip unnamed channels
        ch_name = channel["ch_name"]
        if ch_name.startswith('CHANNEL'):
            continue

        # parse detector name
        p = re.search('(\S+)_',ch_name)
        det_name = p.group(1)
        det_id = detector_map[det_name]

        # create channel labels
        channel_label['slot_id']=channel["slot_id"]
        channel_label['ch_id']=channel["ch_id"]
        channel_label['det_name']=det_name
        channel_label['det_id']=det_id
        channel_label['ch_name']=ch_name

        # loop over properties and store
        for property in properties:
            metric_name = property_map[property]['metric']
            json_name = property_map[property]['json']
            value = channel[json_name]
            if metric_name not in metrics:
                comment = property_map[property]['comment']
                metrics[metric_name] = Gauge(f"{metric_prefix}_{metric_name}", comment, list(channel_label.keys()), registry=registry)
            metrics[metric_name].labels(**channel_label).set(value)

        # special channel_on property, from status
        if 'ch_on' not in metrics:
            metrics['ch_on'] = Gauge(f"{metric_prefix}_ch_on", 'channel ON (boolean)', list(channel_label.keys()), registry=registry)
        metrics['ch_on'].labels(**channel_label).set((channel["status"]&1)==1)

# web service
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
<h1>Prometheus Data Exporter for sPHENIX TPOT HV Module and Utilies</h1>
<p>Fetch metrics at <a href="./metrics">./metrics</a>.</p>
""")

requests_metrics_lock = Lock()

@app.route("/metrics")
# @request_time.labels(**label_host).time() # did not work under python3.7
def requests_metrics():

    request_counter.labels(status='incoming', **label_host).inc()

    with requests_metrics_lock:

        start_time = time.time()

        try:
            if (time.time() - requests_metrics.lastcall < throttling_limit):
                print('requests_metrics: Time litmit throttled....')
                request_counter.labels(status='throttled', **label_host).inc()
            else:
                # refresh all readings
                # clear metrics
                for key, metric in metrics.items():
                    metric.clear()

                # read all channel information
                hv_channel_information()

                requests_metrics.lastcall = time.time()
                request_counter.labels(status='updated', **label_host).inc()

        except Exception as e:
            print(f'requests_metrics: caught {type(e)}: {e}')
            request_counter.labels(status='failed', **label_host).inc()

        request_time.labels(**label_host).observe(time.time() - start_time)

    return Response(prometheus_client.generate_latest(registry), mimetype="text/plain")

requests_metrics.lastcall = time.time()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=args.port)
