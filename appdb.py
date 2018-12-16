#!/usr/bin/env python
import time
import subprocess
from random import uniform
from datetime import datetime
from influxdb import InfluxDBClient
import sensor

DELAY = 900 # 15 minutes entre les saisies
HOST = 'localhost'
DBNAME = 'iot'
USER = 'pi'
PWD = 'raspberry'

def main():
	try:
		client = InfluxDBClient(HOST, 8086, USER, PWD, DBNAME)

		while(1):
			h, t, tvoc, co2 = sensor.main()

			maintenant = datetime.now()
			iot = [
			        {
			            "measurement": "mesures",
			            "time": maintenant,
			            "fields": {
			                "temperature": t,
			                "humidite":h,
			                "co2":co2,
			                "tvoc":tvoc
			            }
			        }
			    ]	
			print("Ajout données : {}".format(iot))
			client.write_points(iot, retention_policy='one_day_only')
			time.sleep(DELAY)

	finally:
			print("\nExiting script ***appdb.py***")

if __name__ == '__main__':
	main()

