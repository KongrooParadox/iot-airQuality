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

		# client.create_database(DBNAME)

		# print("Create retention policy")
		# client.create_retention_policy('one_day_only', '1d', 1, default=True)

		while(1):
			h, t, tvoc, co2 = sensor.main()

			# h = round(uniform(0, 100), 2)
			# t = round(uniform(10, 40), 2)
			# tvoc = round(uniform(125, 800), 0)
			# co2 = round(uniform(450, 2500), 0)

			# print('#### {:%d/%m/%Y %H:%M:%S} ####'.format(datetime.now()))
			# print('Température : {:.02f} °C'.format(t) )
			# print('Humidité : {:.02f} %'.format(h) )
			# print('CO2 (ppm) [450-2000] : %s' % co2)
			# print('TVOC (ppb) [125-600] : %s' % tvoc)
			# print('')

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

