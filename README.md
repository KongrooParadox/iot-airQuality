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
- [X] Commenter le code existant
- [X] Envoi MQTT depuis et vers InfluxDB
- [X] Envoi de données au réseau TTN(TheThingsNetwork)
- [ ] Développer interface locale
- [ ] Tester qualité lien LoRa
- [ ] Localisation ?
- [ ] Réglage seuil limite polluants
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
- node-red-contrib-ttn
- node-red-contrib-pythonshell

### Application AirQuality

Voici le code à importer :

```
[{"id":"ad235098.4bc578","type":"tab","label":"Application AirQuality","disabled":false,"info":"# Affichage LCD de la qualité de l'air au CERI\n\nOn va afficher les différentes variables qui nous intéressent :\n- Température (°C)\n- Humidité (%H)\n- Taux de CO2 (ppm)\n- TVOC (ppb)"},{"id":"77f2c7dd.d179c8","type":"inject","z":"ad235098.4bc578","name":"Envoi toutes les 10 minutes","topic":"","payload":"","payloadType":"date","repeat":"600","crontab":"","once":false,"onceDelay":"","x":180,"y":60,"wires":[["39f24209.28338e"]]},{"id":"e693f374.224e28","type":"ui_gauge","z":"ad235098.4bc578","name":"","group":"cb41940a.4a6198","order":1,"width":"6","height":"6","gtype":"wave","title":"Température","label":"°C","format":"{{value}}","min":0,"max":"40","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":850,"y":260,"wires":[]},{"id":"7e054c5d.21af0c","type":"ui_gauge","z":"ad235098.4bc578","name":"","group":"cb41940a.4a6198","order":2,"width":"6","height":"6","gtype":"donut","title":"Humidité","label":"%","format":"{{value}}","min":0,"max":"100","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":840,"y":300,"wires":[]},{"id":"daa24ad0.84251","type":"ui_gauge","z":"ad235098.4bc578","name":"","group":"f053cf5a.d35e9","order":1,"width":"6","height":"6","gtype":"gage","title":"CO2","label":"ppm","format":"{{value}}","min":0,"max":"2000","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":830,"y":380,"wires":[]},{"id":"6c8a8d74.2a70fc","type":"ui_gauge","z":"ad235098.4bc578","name":"","group":"f053cf5a.d35e9","order":2,"width":"6","height":"6","gtype":"donut","title":"TVOC","label":"ppb","format":"{{value}}","min":"125","max":"1000","colors":["#00b500","#e6e600","#ca3838"],"seg1":"","seg2":"","x":830,"y":340,"wires":[]},{"id":"39f24209.28338e","type":"pythonshell in","z":"ad235098.4bc578","name":"Script Capteur","pyfile":"/home/pi/iot-airQuality/sensor.py","virtualenv":"","continuous":false,"stdInData":false,"x":220,"y":200,"wires":[["832630b2.ce64f","d085fe05.3008f","6ef66dd9.889344","21f6011f.70df1e"]]},{"id":"832630b2.ce64f","type":"function","z":"ad235098.4bc578","name":"prepareDataForTTN","func":"var m = msg.payload.split(';');\nif(m.length !== 1) { // On n'envoie pas de message si tableau de données est vide\n    var humidite = parseFloat(m[0]);\n    var temperature = parseFloat(m[1]);\n    var tvoc = parseFloat(m[2]);\n    var co2 = parseFloat(m[3]);\n    \n    var o = {payload : \n        {temperature : temperature, \n        humidite : humidite,\n        tvoc : tvoc,\n        co2 : co2}\n        };\n    return o;\n}","outputs":1,"noerr":0,"x":540,"y":160,"wires":[["4e25573d.401e9","ff25883.58b0078"]]},{"id":"4e25573d.401e9","type":"debug","z":"ad235098.4bc578","name":"TTN_output","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":830,"y":60,"wires":[]},{"id":"ff25883.58b0078","type":"ttn downlink","z":"ad235098.4bc578","name":"TTN","app":"242fc4ed.262274","dev_id":"temp-hum-sensor-4","port":"","confirmed":false,"schedule":"replace","x":810,"y":100,"wires":[]},{"id":"21f6011f.70df1e","type":"function","z":"ad235098.4bc578","name":"prepareDataForLCD","func":"var m = msg.payload.split(';');\nif(m.length !== 1) { // On n'envoie pas de message si notre tableau de données est vide\n    var humidite = parseFloat(m[0]);\n    var temperature = parseFloat(m[1]);\n    var tvoc = parseFloat(m[2]);\n    var co2 = parseFloat(m[3]);\n    \n    var o1 = {payload : temperature};\n    var o2 = {payload : humidite};\n    var o3 = {payload : tvoc};\n    var o4 = {payload : co2};\n    if ((temperature !== null) && (humidite !== null) && (humidite !== null) && (co2 !== null))\n    return [o1, o2, o3, o4];\n}","outputs":4,"noerr":0,"x":540,"y":260,"wires":[["e693f374.224e28"],["7e054c5d.21af0c"],["6c8a8d74.2a70fc"],["daa24ad0.84251"]]},{"id":"d085fe05.3008f","type":"debug","z":"ad235098.4bc578","name":"python_output","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":520,"y":120,"wires":[]},{"id":"402bb67f.02d37","type":"influxdb out","z":"ad235098.4bc578","influxdb":"10575c76.e6486c","name":"InfluxDB","measurement":"mesures","precision":"","retentionPolicy":"","x":840,"y":200,"wires":[]},{"id":"6ef66dd9.889344","type":"function","z":"ad235098.4bc578","name":"prepareDataForDB","func":"var m = msg.payload.split(';');\nif(m.length !== 1) { // On n'envoie pas de message si notre tableau de données est vide\n    var humidite = parseFloat(m[0]);\n    var temperature = parseFloat(m[1]);\n    var tvoc = parseFloat(m[2]);\n    var co2 = parseFloat(m[3]);\n    msg.payload = [{\n        \"temperature\": temperature,\n        \"humidite\":humidite,\n\t\t\"co2\":co2,\n\t\t\"tvoc\":tvoc\n        }];\n    return msg;\n}","outputs":1,"noerr":0,"x":530,"y":200,"wires":[["402bb67f.02d37","ec58d5a1.1baab8"]]},{"id":"ec58d5a1.1baab8","type":"debug","z":"ad235098.4bc578","name":"DB_output","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","x":850,"y":160,"wires":[]},{"id":"6c8fad4d.d151bc","type":"pythonshell in","z":"ad235098.4bc578","name":"Script Capteur","pyfile":"/home/pi/iot-airQuality/sensor.py","virtualenv":"","continuous":false,"stdInData":false,"x":220,"y":260,"wires":[["21f6011f.70df1e","6ef66dd9.889344"]]},{"id":"b16185d3.eb36b","type":"inject","z":"ad235098.4bc578","name":"On demand","topic":"","payload":"","payloadType":"date","repeat":"","crontab":"","once":false,"onceDelay":0.1,"x":130,"y":360,"wires":[["6c8fad4d.d151bc"]]},{"id":"cb41940a.4a6198","type":"ui_group","z":"","name":"Gauche","tab":"247ce936.31617e","disp":false,"width":"6","collapse":false},{"id":"f053cf5a.d35e9","type":"ui_group","z":"","name":"Droite","tab":"247ce936.31617e","disp":false,"width":"6","collapse":false},{"id":"242fc4ed.262274","type":"ttn app","z":"","appId":"tp2-temp-hum","accessKey":"ttn-account-v2.dp_bYW19zX7W3Rq_QH5kF8LDRNkdKdVl2JGJYbgBtqk","discovery":"discovery.thethingsnetwork.org:1900"},{"id":"10575c76.e6486c","type":"influxdb","z":"","hostname":"127.0.0.1","port":"8086","protocol":"http","database":"iot","name":"Mesures Capteurs","usetls":false,"tls":""},{"id":"247ce936.31617e","type":"ui_tab","z":"","name":"Qualité de l'air au CERI","icon":"dashboard"}]
```

## Grafana

### Installation

N.B : Commandes à exécuter en tant que super-user

```
apt-get install apt-transport-https curl
curl https://bintray.com/user/downloadSubjectPublicKey?username=bintray | apt-key add -
echo "deb https://dl.bintray.com/fg2it/deb stretch main" | tee -a /etc/apt/sources.list.d/grafana.list
apt-get update
apt-get install grafana
```

## Sources :
- [pigpio](http://abyz.me.uk/rpi/pigpio/python.html)
- [Tuto InfluxDB & Grafana](https://bentek.fr/influxdb-grafana-raspberry-pi/)
- [i2c](https://raspberrypi.stackexchange.com/questions/79091/smbus-i2c-sensor-returns-fixed-data)
- [Mosquitto](https://bentek.fr/mosquitto-node-red-raspberry-pi/)
- [Doc InfluxDB](https://docs.influxdata.com/influxdb/v1.7/introduction/getting-started/)
- [InfluxDB Python](https://github.com/influxdata/influxdb-python/)
