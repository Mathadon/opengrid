# -*- coding: utf-8 -*-
"""
Script to extract all minute sensor data from the flukso server through the 
flukso api.


Created on Mon Dec 30 04:24:28 2013 by Roel De Coninck
"""

import os, sys
import inspect


script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# add the path to opengrid to sys.path
sys.path.append(os.path.join(script_dir, os.pardir, os.pardir))
from opengrid.library.houseprint import Houseprint
from opengrid.library import fluksoapi
from opengrid.library.storetimeseriesdata import TimeSeriesData

# script settings ############################################################
extract_all = True
save_all = True

##############################################################################

hp = Houseprint()
all_sensordata = hp.get_all_fluksosensors()
print('Sensor data fetched')

i=0
if extract_all:
    print('Writing files:')
    for flukso_id in all_sensordata.keys():
        for sensor_id, s in all_sensordata[flukso_id].items():
            # sensor_id is 1-6, s is {}
            if s is not None and s:
                # determine the type of the measurement to set the unit                
                t = s['Type'].lower()
                if t.startswith('ele'):
                    unit = 'watt'
                else:
                    unit = 'lperday'
                # pull the data from the flukso server
                r = fluksoapi.pull_api(sensor=s['Sensor'], token=s['Token'],
                                       unit=unit)
                if save_all:
                    tsd=TimeSeriesData(sensor=s['Sensor'], token=s['Token'],unit=unit)
                    tsd.storeTimeSeriesData(newdata=r.json())
                    # storeTimeSeriesData(r.json(), s['Sensor'], s['Token'], unit)
                    fluksoapi.save2csv(r, csvpath=None, fileNamePrefix=s['Sensor'])
                    i=i+1
                    print('.'),
                    sys.stdout.flush()
    print('done')
print str(i) + " sensor data files saved"
            