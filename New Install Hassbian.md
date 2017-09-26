#Setup of new installation of Home Assistant
This is a simple guide to setting up Home Assistant from scratch, with codes.
##Initial setup
```passwd

hassbian-config

cd /home/homeassistant/.homeassistant/```


##Git:
```sudo apt-get update && sudo apt-get upgrade
sudo apt install git && sudo ssh-keygen -t rsa -b 4096 -C "aa@devv.it" && sudo cat /root/.ssh/id_rsa.pub
(sudo nano /root/.ssh/id_rsa.pub)
(sudo tail /root/.ssh/id_rsa.pub)

eval "$(ssh-agent -s)"

sudo systemctl stop home-assistant@homeassistant.service 
cd /home/homeassistant/.homeassistant && sudo rm -rf /home/homeassistant/.homeassistant/*
sudo chmod -R g+w /home/homeassistant/.homeassistant/
git init && git remote add origin git@github.com:DevvAndreas/Home-Assistant-Config.git && git fetch && git checkout -t origin/master



sudo hassbian-config install mosquitto && sudo hassbian-config install hue && sudo hassbian-config install samba 

cd /etc/mosquitto/
sudo cp mosquitto.conf mosquitto.conf.old && sudo rm -rf mosquitto.conf && sudo nano mosquitto.conf
sudo systemctl restart mosquitto.service ```

####Possibly:
```sudo hassbian-config install libcec```

```sudo apt install htop wavemon```

##Tellstick:
```sudo hassbian-config install tellstick && sudo systemctl enable telldusd.service && sudo nano /etc/tellstick.conf
sudo reboot now```

##Install duckdns and letsencrypt:
https://community.home-assistant.io/t/guide-how-to-set-up-duckdns-ssl-and-chrome-push-notifications/9722
```mkdir duckdns
cd duckdns
nano duck.sh
chmod 700 duck.sh
crontab -e
./duck.sh
cat duck.log```

```mkdir certbot
cd certbot
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
(./certbot-auto certonly --standalone --preferred-challenges http-01 --email andreas@ahrensit.se -d eiolos.duckdns.org)
./certbot-auto certonly --standalone --standalone-supported-challenges http-01 --email andreas@ahrensit.se -d eiolos.duckdns.org

sudo chmod -R 777 /etc/letsencrypt```

##Homebridge:
```sudo apt-get install nodejs npm
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install libavahi-compat-libdnssd-dev
sudo npm install -g --unsafe-perm homebridge
sudo npm install -g homebridge-homeassistant && sudo npm install -g homebridge-magichome && sudo npm install -g homebridge-mi-air-purifier miio && sudo npm install homebridge-server@latest -g
sudo nano ~/.homebridge/config.json
homebridge```
https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi

###Run homebridge on boot
https://gist.github.com/johannrichard/0ad0de1feb6adb9eb61a/
```sudo nano /etc/default/homebridge
sudo nano /etc/systemd/system/homebridge.service
sudo useradd --system homebridge
sudo mkdir /var/lib/homebridge
sudo chown homebridge /var/lib/homebridge

sudo nano /var/lib/homebridge/config.json
journalctl -u homebridge```

###Homebridge server:
https://www.npmjs.com/package/homebridge-server

###Fix homebridge problem:
```sudo systemctl stop homebridge.service
sudo systemctl restart avahi-daemon
sudo systemctl start homebridge.service ```



```sudo systemctl daemon-reload
sudo systemctl enable homebridge
sudo systemctl start homebridge```

##Install MPD
```sudo apt-get install mpd mpc
sudo nano /etc/mpd.conf
audio_output {
        type            "alsa"
        name            "My ALSA Device"
        device          "hw:0,0"        # optional
        mixer_type      "software"      # optional
#       mixer_device    "default"       # optional
#       mixer_control   "PCM"           # optional
#       mixer_index     "0"             # optional
}```

##MySQL:
```sudo apt-get install mysql-server```

```mysql -u root -p
CREATE USER 'hassbian'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE hassbian;
GRANT ALL PRIVILEGES ON hassbian . * TO 'hassbian'@'localhost';
FLUSH PRIVILEGES;
exit;```

```sudo chown -R homeassistant /usr/local/lib/python3.4
sudo apt-get install libmysqlclient-dev```

###Seems to work:
```sudo systemctl stop home-assistant@homeassistant.service
sudo su -s /bin/bash homeassistant
source /srv/homeassistant/bin/activate
pip3 install mysqlclient
exit
sudo systemctl start home-assistant@homeassistant.service```

###Doesn't seem to work:
```sudo -i
su homeassistant
cd /srv/homeassistant/homeassistant_venv/
source bin/activate
pip3 install mysqlclient```

##Alternative, old way

```cd /home/pi/Downloads/
wget http://download.telldus.se/TellStick/Software/telldus-core/telldus-core-2.1.2.tar.gz
sudo apt-get install libftdi1 libftdi-dev libconfuse0 libconfuse-dev cmake
cd /usr/src
sudo tar xzf ~/Downloads/telldus-core-2.1.2.tar.gz
cd telldus-core-2.1.2
sudo apt-get install doxygen
sudo wget http://developer.telldus.com/export/4342bbaa1dcd90011b66e8c1540db6ba904877fe/telldus-core/Doxyfile.in
sudo cmake .
sudo make
sudo make install
sudo ldconfig
sudo nano /lib/systemd/system/telldusd.service

[Unit]
Description=Tellstick service daemon
After=multi-user.target

[Service]
Type=forking
ExecStart=/usr/local/sbin/telldusd

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl start telldusd.service
systemctl status telldusd.service
sudo systemctl enable telldusd.service

sudo nano /etc/tellstick.conf

sudo systemctl restart telldusd.service```
