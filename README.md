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
- [ ] Envoi MQTT depuis et vers InfluxDB
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

## Mosquitto

N.B : Commandes à exécuter en tant que super-user

### Installation
```
wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
apt-key add mosquitto-repo.gpg.key
cd /etc/apt/sources.list.d/
wget http://repo.mosquitto.org/debian/mosquitto-stretch.list
apt update -y
apt install -y mosquitto mosquitto-clients
```
### Configuration
```
echo "# Place your local configuration in /etc/mosquitto/conf.d/
#
# A full description of the configuration file is at
# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest topic

log_type error
log_type warning
log_type notice
log_type information

connection_messages true
log_timestamp true

include_dir /etc/mosquitto/conf.d" > /etc/mosquitto/mosquitto.conf
```

## Node-RED

Noeuds à installer :
- node-red-contrib-influxdb
- node-red-dashboard

### Dashboard local écran LCD

Voici le code à importer :
```
[{"id":"f1b87a58.25fd8","type":"tab","label":"Dashboard LCD","disabled":false,"info":"# Affichage LCD de la qualité de l'air au CERI\n\nOn va afficher les différentes variables qui nous intéressent :\n- Température (°C)\n- Humidité (%H)\n- Taux de CO2 (ppm)\n- TVOC (ppb)"},{"id":"4dadde3c.1d4658","type":"debug","z":"f1b87a58.25fd8","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":970,"y":100,"wires":[]},{"id":"e1e88f82.3a894","type":"influxdb in","z":"f1b87a58.25fd8","influxdb":"10575c76.e6486c","name":"Mesures capteurs","query":"","rawOutput":false,"precision":"","retentionPolicy":"","x":270,"y":220,"wires":[["a71d6d65.62aeb"]]},{"id":"623a8e1a.3eb1f","type":"inject","z":"f1b87a58.25fd8","name":"","topic":"","payload":"","payloadType":"date","repeat":"600","crontab":"","once":false,"onceDelay":"","x":110,"y":80,"wires":[["f01098e9.0d6818"]]},{"id":"f01098e9.0d6818","type":"function","z":"f1b87a58.25fd8","name":"Query","func":"msg.query=\"select * from mesures;\";\nreturn msg;","outputs":1,"noerr":0,"x":130,"y":160,"wires":[["e1e88f82.3a894"]]},{"id":"a71d6d65.62aeb","type":"function","z":"f1b87a58.25fd8","name":"getLast","func":"var len = msg.payload.length - 1;\nvar newMsg = { payload : msg.payload[len]};\nreturn newMsg;","outputs":1,"noerr":0,"x":380,"y":280,"wires":[["3a970446.11381c","576f3f9b.21a568","7f9cf6aa.4c2a48","91b5046e.d151b8","4dadde3c.1d4658"]]},{"id":"3a970446.11381c","type":"function","z":"f1b87a58.25fd8","name":"getTemp","func":"var o = {payload : msg.payload.temperature};\nreturn o;","outputs":1,"noerr":0,"x":700,"y":260,"wires":[["e74c161f.3d2188"]]},{"id":"576f3f9b.21a568","type":"function","z":"f1b87a58.25fd8","name":"getHum","func":"var o = {payload : msg.payload.humidite};\n\nreturn o;","outputs":1,"noerr":0,"x":700,"y":320,"wires":[["67251e18.032b68"]]},{"id":"7f9cf6aa.4c2a48","type":"function","z":"f1b87a58.25fd8","name":"getCo2","func":"var o = {payload : msg.payload.co2};\n\nreturn o;","outputs":1,"noerr":0,"x":700,"y":380,"wires":[["174862cd.b9fa0d"]]},{"id":"91b5046e.d151b8","type":"function","z":"f1b87a58.25fd8","name":"getTVOC","func":"var o = {payload : msg.payload.tvoc};\n\nreturn o;","outputs":1,"noerr":0,"x":700,"y":440,"wires":[["b48b9c13.4465c8"]]},{"id":"e74c161f.3d2188","type":"ui_gauge","z":"f1b87a58.25fd8","name":"","group":"9e7022ce.af158","order":1,"width":"6","height":"6","gtype":"wave","title":"Température","label":"°C","format":"{{value}}","min":0,"max":"40","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":930,"y":260,"wires":[]},{"id":"67251e18.032b68","type":"ui_gauge","z":"f1b87a58.25fd8","name":"","group":"9e7022ce.af158","order":2,"width":"6","height":"6","gtype":"donut","title":"Humidité","label":"%","format":"{{value}}","min":0,"max":"100","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":920,"y":320,"wires":[]},{"id":"174862cd.b9fa0d","type":"ui_gauge","z":"f1b87a58.25fd8","name":"","group":"6d7b0555.c020f4","order":1,"width":"6","height":"6","gtype":"gage","title":"CO2","label":"ppm","format":"{{value}}","min":0,"max":"2000","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":910,"y":380,"wires":[]},{"id":"b48b9c13.4465c8","type":"ui_gauge","z":"f1b87a58.25fd8","name":"","group":"6d7b0555.c020f4","order":2,"width":"6","height":"6","gtype":"donut","title":"TVOC","label":"ppb","format":"{{value}}","min":"125","max":"1000","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":910,"y":440,"wires":[]},{"id":"10575c76.e6486c","type":"influxdb","z":"","hostname":"127.0.0.1","port":"8086","protocol":"http","database":"iot","name":"Mesures Capteurs","usetls":false,"tls":""},{"id":"9e7022ce.af158","type":"ui_group","z":"","name":"Gauche","tab":"13078b5.573d675","order":1,"disp":false,"width":"6","collapse":false},{"id":"6d7b0555.c020f4","type":"ui_group","z":"","name":"Droite","tab":"13078b5.573d675","order":3,"disp":false,"width":"6","collapse":false},{"id":"13078b5.573d675","type":"ui_tab","z":"","name":"Qualité de l'air au CERI","icon":"dashboard"}]
```

Une fois que le flow est deployé on peut y accéder à l'URL locale suivante :

`http://<ADRESSE_PI>:1880/ui/`

### Envoi de données capteurs vers broker MQTT

```
[{"id":"8498aae6.9dc318","type":"tab","label":"Sensors to MQTT","disabled":true,"info":""},{"id":"2af2f5da.6ab7c2","type":"i2c in","z":"8498aae6.9dc318","name":"","address":"","command":"1","count":"1","x":630,"y":280,"wires":[["b7ef02c8.1d10f"]]},{"id":"3a25452d.593caa","type":"i2c scan","z":"8498aae6.9dc318","x":420,"y":240,"wires":[["a433ba34.1a9ed"],["2af2f5da.6ab7c2"]]},{"id":"a433ba34.1a9ed","type":"debug","z":"8498aae6.9dc318","name":"i2c devices","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":700,"y":160,"wires":[]},{"id":"90177261.c2d7d","type":"inject","z":"8498aae6.9dc318","name":"","topic":"","payload":"","payloadType":"date","repeat":"","crontab":"","once":false,"onceDelay":0.1,"x":200,"y":240,"wires":[["3a25452d.593caa"]]},{"id":"11a04664.e152fa","type":"debug","z":"8498aae6.9dc318","name":"check_before","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":1000,"y":400,"wires":[]},{"id":"7e9da7a3.e80bf8","type":"mqtt out","z":"8498aae6.9dc318","name":"","topic":"mesures","qos":"0","retain":"false","broker":"70398119.e1fed8","x":1220,"y":280,"wires":[]},{"id":"88819625.4dab08","type":"function","z":"8498aae6.9dc318","name":"sendData","func":"\nreturn msg;","outputs":1,"noerr":0,"x":1040,"y":280,"wires":[["aebc9f28.50cf5","7e9da7a3.e80bf8"]]},{"id":"b7ef02c8.1d10f","type":"function","z":"8498aae6.9dc318","name":"prepareData","func":"\nreturn msg;","outputs":1,"noerr":0,"x":810,"y":280,"wires":[["11a04664.e152fa","88819625.4dab08"]]},{"id":"e3344d75.d36728","type":"rpi-gpio in","z":"8498aae6.9dc318","name":"","pin":"tri","intype":"tri","debounce":"25","read":true,"x":570,"y":380,"wires":[["b7ef02c8.1d10f","ac1f4048.02a638"]]},{"id":"aebc9f28.50cf5","type":"debug","z":"8498aae6.9dc318","name":"check_after","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":1210,"y":400,"wires":[]},{"id":"ac1f4048.02a638","type":"debug","z":"8498aae6.9dc318","name":"gpio_output","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":730,"y":460,"wires":[]},{"id":"70398119.e1fed8","type":"mqtt-broker","z":"","name":"Mosquitto","broker":"localhost","port":"1883","clientid":"","usetls":false,"compatmode":true,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","closeTopic":"","closeQos":"0","closePayload":"","willTopic":"","willQos":"0","willPayload":""}]
```

### Envoi de données vers InfluxDB

```
[{"id":"c559291c.a3fb98","type":"tab","label":"MQTT to InfluxDB","disabled":false,"info":""},{"id":"ecf7eed5.6e4058","type":"mqtt in","z":"c559291c.a3fb98","name":"","topic":"mesures","qos":"2","broker":"70398119.e1fed8","x":170,"y":220,"wires":[["86b56590.048818","cb9efc45.b6ef38"]]},{"id":"cb9efc45.b6ef38","type":"debug","z":"c559291c.a3fb98","name":"mqtt_output","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":470,"y":360,"wires":[]},{"id":"9b3b3bdf.412348","type":"debug","z":"c559291c.a3fb98","name":"DB_output","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":890,"y":160,"wires":[]},{"id":"86b56590.048818","type":"function","z":"c559291c.a3fb98","name":"prepareQuery","func":"\nreturn msg;","outputs":1,"noerr":0,"x":530,"y":240,"wires":[["be821d9d.87bc7","9b3b3bdf.412348"]]},{"id":"be821d9d.87bc7","type":"influxdb out","z":"c559291c.a3fb98","influxdb":"10575c76.e6486c","name":"InfluxDB","measurement":"mesures","precision":"","retentionPolicy":"","x":940,"y":300,"wires":[]},{"id":"70398119.e1fed8","type":"mqtt-broker","z":"","name":"Mosquitto","broker":"localhost","port":"1883","clientid":"","usetls":false,"compatmode":true,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","closeTopic":"","closeQos":"0","closePayload":"","willTopic":"","willQos":"0","willPayload":""},{"id":"10575c76.e6486c","type":"influxdb","z":"","hostname":"127.0.0.1","port":"8086","protocol":"http","database":"iot","name":"Mesures Capteurs","usetls":false,"tls":""}]
```

## Sources :
- [pigpio](http://abyz.me.uk/rpi/pigpio/python.html)
- [Tuto InfluxDB & Grafana](https://bentek.fr/influxdb-grafana-raspberry-pi/)
- [i2c](https://raspberrypi.stackexchange.com/questions/79091/smbus-i2c-sensor-returns-fixed-data)
- [Mosquitto](https://bentek.fr/mosquitto-node-red-raspberry-pi/)
- [Doc InfluxDB](https://docs.influxdata.com/influxdb/v1.7/introduction/getting-started/)
- [InfluxDB Python](https://github.com/influxdata/influxdb-python/)
