#!/usr/bin/env python
import time
import pigpio
import subprocess
import Adafruit_DHT as dht
from datetime import datetime

# Executer ce script en tant que super user


def init():
	global pi 
	pi = pigpio.pi()
	if not pi.connected:
		print('Erreur : démarrage de pigpiod')
		start = 'pigpiod'
		subprocess.check_call(start.split())
		#exit()

	global air 
	air = pi.i2c_open(1, 0x5a)


def run(sleep_time):
	global air
	while(1):
		c, d = pi.i2c_read_device(air, 9)
		h,t = dht.read_retry(dht.DHT22, 8)

		tvoc = d[7] * 256 + d[8]
		co2 = (d[0] * 256) + d[1] 
		if(co2 > 2500):
			print('Attention taux de CO2 dangereux !!!')
		if(tvoc > 700):
			print('Attention taux TVOC dangereux!!!')
		
		print('#### {:%d/%m/%Y %H:%M:%S} ####'.format(datetime.now()))
		print('Température : {:.02f} °C'.format(t) )
		print('Humidité : {:.02f} %'.format(h) )
		print('CO2 (ppm) [450-2000] : %s' % co2)
		print('TVOC (ppb) [125-600] : %s' % tvoc)
		print('')
		time.sleep(sleep_time)


def close():
	global pi, air
	pi.i2c_close(air)
	pi.stop()


def main():
	init()
	run(10)
	close()

if __name__ == '__main__':
	main()