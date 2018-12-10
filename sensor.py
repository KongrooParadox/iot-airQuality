#!/usr/bin/env python
import time
import pigpio
import subprocess
import Adafruit_DHT as dht
from datetime import datetime
from influxdb import InfluxDBClient
from datetime import datetime
 

DELAY = 10
HOST = 'localhost'
DBNAME = 'iot'
USER = 'pi'
PWD = 'raspberry'

def init():
	print('############################################\n\tRunning sensor.py\n############################################')
	start_command = 'sudo pigpiod'
	subprocess.call(start_command.split())
	time.sleep(1)	 

def close():
	stop_command = 'sudo killall pigpiod'
	subprocess.call(stop_command.split())
	print('\n############################################\n\tExiting sensor.py\n############################################')

def main():
	try:
		init()
		pi = pigpio.pi()
		if not pi.connected:
			print('Erreur au démarrage de pigpiod')
			init()
 
		air = pi.i2c_open(1, 0x5a)

		client = InfluxDBClient(HOST, 8086, USER, PWD, DBNAME)

		client.create_database(DBNAME)

		print("Create retention policy")
		client.create_retention_policy('one_day_only', '1d', 1, default=True)

		while(1):
			c, d = pi.i2c_read_device(air, 9)
			h,t = dht.read_retry(dht.DHT22, 8)

			tvoc = d[7] * 256 + d[8]
			co2 = (d[0] * 256) + d[1] 
			if(co2 > 2500):
				print('Attention taux de CO2 dangereux !!!')
			if(tvoc > 700):
				print('Attention taux TVOC dangereux!!!')
			
			# print('#### {:%d/%m/%Y %H:%M:%S} ####'.format(datetime.now()))
			# print('Température : {:.02f} °C'.format(t) )
			# print('Humidité : {:.02f} %'.format(h) )
			# print('CO2 (ppm) [450-2000] : %s' % co2)
			# print('TVOC (ppb) [125-600] : %s' % tvoc)
			# print('')

			# int(past_date.strftime('%s'))
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
			print("Write points #: {0}".format(iot))
			client.write_points(iot, retention_policy='one_day_only')
			time.sleep(DELAY)

	finally:
		try:
			pi.i2c_close(air)
			pi.stop()
			close()
			print("Drop database: {}".format(DBNAME))
			client.drop_database(DBNAME)
		except:
			close()

if __name__ == '__main__':
	main()