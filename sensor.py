# -*- coding: utf-8 -*
#!/usr/bin/env python
import time
import pigpio
import subprocess
import Adafruit_DHT as dht
from datetime import datetime


def init():
	#print('############################################\n\tRunning sensor.py\n############################################')
	# On démarre le daemon pigpiod pour pouvoir accéder aux données de notre capteur GPIO
	start_command = 'sudo pigpiod'
	# Permet d'éxécuter la commande bash ci-dessus
	subprocess.call(start_command.split())
	time.sleep(1)	 

def close():
	# On ferme le daemon pigpiod pour économiser de l'énergie
	stop_command = 'sudo killall pigpiod'
	# Permet d'éxécuter la commande bash ci-dessus
	subprocess.call(stop_command.split())
	#print('\n############################################\n\tExiting sensor.py\n############################################')

def main():
	try:
		init()
		pi = pigpio.pi()
		if not pi.connected:
			print('Erreur au démarrage de pigpiod')
			init()
 
		air = pi.i2c_open(1, 0x5a)
		c, d = pi.i2c_read_device(air, 9)
		h,t = dht.read_retry(dht.DHT22, 8)
		h = round(h, 2)
		t = round(t, 2)
		tvoc = d[7] * 256 + d[8]
		co2 = d[0] * 256 + d[1] 
		# if(co2 > 2500):
		# 	print('Attention taux de CO2 dangereux !!!')
		# if(tvoc > 700):
		# 	print('Attention taux TVOC dangereux!!!')

		# print('#### {:%d/%m/%Y %H:%M:%S} ####'.format(datetime.now()))
		# print('Température : {:.02f} °C'.format(t) )
		# print('Humidité : {:.02f} %'.format(h) )
		# print('CO2 (ppm) [450-2000] : %s' % co2)
		# print('TVOC (ppb) [125-600] : %s' % tvoc)
		# print('')
		# int(past_date.strftime('%s'))

	finally:
		try:
			pi.i2c_close(air)
			pi.stop()
			close()
			output = ''
			output += str(h) + ';' + str(t) + ';'+ str(tvoc) + ';' + str(co2)
			print(output)
			return h, t, tvoc, co2
		except:
			close()

if __name__ == '__main__':
	main()
