# Application IoT : Mesure de la Qualité de l'air au CERI

Technologie utilisée : __LoRa__

## Matériel
- Raspberry Pi 3 Model B
- Pi 3 Click Shield
- DHT22 Click
- Air quality 2 Click
- Ecran LCD
- Cablage, etc


## TODO

- [X] Installation et configuration Node-Red
- [X] Communication Bus I2C, GPIO
- [X] Communication SSH
- [X] Récupération données capteurs 
- [X] Installation et configuration base de données InfluxDB
- [X] Stocker data BDD InfluxDB
- [ ] Commenter le code existant
- [ ] Envoi de données au réseau TTN(TheThingsNetwork)
- [ ] Tester qualité lien LoRa
- [ ] Localisation ?
- [ ] Réglage seuil limite polluants
- [ ] Développer interface locale
- [ ] Développer interface à distance


## Outils utilisés
- [GitHub](https://github.com/KongrooParadox/iot-airQuality)
- [Framaboard](https://iot_app.framaboard.org)
- [GoogleDocs](https://docs.google.com/document/d/1oSpJuE5dsAaoRs45m0XVYFyhgwdIBXbI-T1pg3EFDO8/edit?usp=sharing)


## Récapitulatif des séances

### 5-12-19 Novembre
- Réception matériel
- Prise en main Raspberry, Node-Red
- Communication capteurs
- Définition d'outils collaboratifs

### 10 Décembre
- Création base de données InfluxDB
- Ajout de données des capteurs dans BDD (appdb.py)
- Redaction ébauche du rapport

## Edition de fichiers à distance avec SublimeText3

__Sur la Raspberry__

Installation rsub:
```
# wget -O /usr/local/bin/rsub \https://raw.github.com/aurora/rmate/master/rmate
# chmod a+x /usr/local/bin/rsub
```

__Sur machine locale__

1. Installation paquet rsub dans SublimeText3

Dans Sublime Text 3, ouvrir Package Manager (Ctrl-Shift-P sur Linux/Win, Cmd-Shift-P sur Mac, Install Package), chercher et installer __RemoteSubl__

2. Ouvrir terminal et éxecuter commande suivante :

`# ssh -R 52698:localhost:52698 pi@<ADDRESSE_PI>`

3. Un fois que vous êtes connectés en SSH, éxecuter la comande suivante sur la Raspberry :

`# rsub path_to_file/file.txt`

4. Le fichier va s'ouvrir automatiquement sur SublimeText

## Dashboard local sur Node-RED

Noeuds à installer :
- node-red-contrib-influxdb
- node-red-dashboard

Voici le flow à importer :
```
[{"id":"f1b87a58.25fd8","type":"tab","label":"Dashboard Application","disabled":false,"info":""},{"id":"4dadde3c.1d4658","type":"debug","z":"f1b87a58.25fd8","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":970,"y":80,"wires":[]},{"id":"e1e88f82.3a894","type":"influxdb in","z":"f1b87a58.25fd8","influxdb":"10575c76.e6486c","name":"Mesures capteurs","query":"","rawOutput":false,"precision":"","retentionPolicy":"","x":270,"y":220,"wires":[["a71d6d65.62aeb"]]},{"id":"623a8e1a.3eb1f","type":"inject","z":"f1b87a58.25fd8","name":"","topic":"","payload":"","payloadType":"date","repeat":"600","crontab":"","once":false,"onceDelay":"","x":110,"y":80,"wires":[["f01098e9.0d6818"]]},{"id":"f01098e9.0d6818","type":"function","z":"f1b87a58.25fd8","name":"Query","func":"msg.query=\"select * from mesures;\";\nreturn msg;","outputs":1,"noerr":0,"x":130,"y":160,"wires":[["e1e88f82.3a894"]]},{"id":"a71d6d65.62aeb","type":"function","z":"f1b87a58.25fd8","name":"getLast","func":"var len = msg.payload.length - 1;\nvar newMsg = { payload : msg.payload[len]};\nreturn newMsg;","outputs":1,"noerr":0,"x":380,"y":280,"wires":[["3a970446.11381c","576f3f9b.21a568","7f9cf6aa.4c2a48","91b5046e.d151b8","4dadde3c.1d4658"]]},{"id":"3a970446.11381c","type":"function","z":"f1b87a58.25fd8","name":"getTemp","func":"var o = {payload : msg.payload.temperature};\nreturn o;","outputs":1,"noerr":0,"x":700,"y":260,"wires":[["e74c161f.3d2188"]]},{"id":"576f3f9b.21a568","type":"function","z":"f1b87a58.25fd8","name":"getHum","func":"var o = {payload : msg.payload.humidite};\n\nreturn o;","outputs":1,"noerr":0,"x":700,"y":320,"wires":[["67251e18.032b68"]]},{"id":"7f9cf6aa.4c2a48","type":"function","z":"f1b87a58.25fd8","name":"getCo2","func":"var o = {payload : msg.payload.co2};\n\nreturn o;","outputs":1,"noerr":0,"x":700,"y":380,"wires":[["174862cd.b9fa0d"]]},{"id":"91b5046e.d151b8","type":"function","z":"f1b87a58.25fd8","name":"getTVOC","func":"var o = {payload : msg.payload.tvoc};\n\nreturn o;","outputs":1,"noerr":0,"x":700,"y":440,"wires":[["b48b9c13.4465c8"]]},{"id":"e74c161f.3d2188","type":"ui_gauge","z":"f1b87a58.25fd8","name":"","group":"9e7022ce.af158","order":1,"width":"6","height":"6","gtype":"wave","title":"Température","label":"°C","format":"{{value}}","min":0,"max":"40","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":930,"y":260,"wires":[]},{"id":"67251e18.032b68","type":"ui_gauge","z":"f1b87a58.25fd8","name":"","group":"9e7022ce.af158","order":2,"width":"6","height":"6","gtype":"donut","title":"Humidité","label":"%","format":"{{value}}","min":0,"max":"100","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":920,"y":320,"wires":[]},{"id":"174862cd.b9fa0d","type":"ui_gauge","z":"f1b87a58.25fd8","name":"","group":"6d7b0555.c020f4","order":1,"width":"6","height":"6","gtype":"gage","title":"CO2","label":"ppm","format":"{{value}}","min":0,"max":"2000","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":910,"y":380,"wires":[]},{"id":"b48b9c13.4465c8","type":"ui_gauge","z":"f1b87a58.25fd8","name":"","group":"6d7b0555.c020f4","order":2,"width":"6","height":"6","gtype":"donut","title":"TVOC","label":"ppb","format":"{{value}}","min":"125","max":"1000","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":910,"y":440,"wires":[]},{"id":"10575c76.e6486c","type":"influxdb","z":"","hostname":"127.0.0.1","port":"8086","protocol":"http","database":"iot","name":"Mesures Capteurs","usetls":false,"tls":""},{"id":"9e7022ce.af158","type":"ui_group","z":"","name":"Gauche","tab":"13078b5.573d675","order":1,"disp":false,"width":"6","collapse":false},{"id":"6d7b0555.c020f4","type":"ui_group","z":"","name":"Droite","tab":"13078b5.573d675","order":3,"disp":false,"width":"6","collapse":false},{"id":"13078b5.573d675","type":"ui_tab","z":"","name":"Qualité de l'air au CERI","icon":"dashboard"}]
```

Une fois que le flow est deployé on peut y accéder à l'URL locale suivante :
`http://<ADRESSE_PI>:1880/ui/`

## Sources :
- [pigpio](http://abyz.me.uk/rpi/pigpio/python.html)
- [Tuto InfluxDB & Grafana](https://bentek.fr/influxdb-grafana-raspberry-pi/)
- [i2c](https://raspberrypi.stackexchange.com/questions/79091/smbus-i2c-sensor-returns-fixed-data)
- [Mosquitto](https://bentek.fr/mosquitto-node-red-raspberry-pi/)
- [Doc InfluxDB](https://docs.influxdata.com/influxdb/v1.7/introduction/getting-started/)
- [InfluxDB Python](https://github.com/influxdata/influxdb-python/)
