# Application IoT : Mesure de la Qualité de l'air au CERI

Technologie utilisée : __LoRa__

Groupe : 
- ZAANOUNY Israa
- NANTY Guillaume


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
- [ ] Installation et configuration base de données InfluxDB
- [ ] Stocker data BDD InfluxDB
- [ ] Tester qualité lien LoRa
- [ ] Réglage seuil limite polluants
- [ ] Localisation
- [ ] Envoi de données au réseau TTN(TheThingsNetwork)
- [ ] Développer interface locale
- [ ] Développer interface à distance
- [ ] TBD


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


## Sources :
- [pigpio](http://abyz.me.uk/rpi/pigpio/python.htm)
- [InfluxDB & Grafana](https://bentek.fr/influxdb-grafana-raspberry-pi/)
- [i2c](https://raspberrypi.stackexchange.com/questions/79091/smbus-i2c-sensor-returns-fixed-data)
- [Mosquitto](https://bentek.fr/mosquitto-node-red-raspberry-pi/)
