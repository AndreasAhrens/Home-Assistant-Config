# Setup of new installation of Home Assistant
This is a simple guide to setting up Home Assistant from scratch, with codes.
## Initial setup
``` shell
passwd

raspbian-config

cd /home/homeassistant/.homeassistant/
http://IP:8123/
```
Check if Home Assistant is up, takes a while first setup.

## Set up HA aliases
```shell
echo "alias hastart='sudo systemctl start home-assistant@homeassistant.service'" >> ~/.bash_profile
echo "alias hastop='sudo systemctl stop home-assistant@homeassistant.service'" >> ~/.bash_profile
echo "alias hastatus='sudo systemctl status -l home-assistant@homeassistant.service'" >> ~/.bash_profile
echo "alias halog='tail -f  /home/homeassistant/.homeassistant/home-assistant.log'" >> ~/.bash_profile
echo "alias hy='history'" >> ~/.bash_profile
source ~/.bash_profile 
```

## Git:
``` shell
sudo apt-get update && sudo apt-get upgrade
# sudo apt install git && sudo ssh-keygen -t rsa -b 4096 -C "andreas@ahrensit.se" && sudo cat /root/.ssh/id_rsa.pub
sudo apt install git && ssh-keygen -t rsa -b 4096 -C "andreas@ahrensit.se" && sudo cat /home/pi/.ssh/id_rsa.pub

sudo su -s /bin/bash homeassistant
source /srv/homeassistant/bin/activate
cat /home/homeassistant/.ssh/id_rsa.pub
cd /home/homeassistant/.homeassistant
sudo chown -hR homeassistant /home/homeassistant/.homeassistant

# sudo nano /root/.ssh/id_rsa.pub
# sudo tail /root/.ssh/id_rsa.pub
```
Put results of cat into a new deploy key on GitHub
The second deploy key is used for the homeassistant user.

``` shell
eval "$(ssh-agent -s)"

sudo systemctl stop home-assistant@homeassistant.service 
```
Remove all existing standard files, without this, we can't get the existing config
``` shell
cd /home/homeassistant/.homeassistant && sudo rm -rf /home/homeassistant/.homeassistant/*
sudo chmod -R g+w /home/homeassistant/.homeassistant/
```
Only works if you have done the ssh key generation without sudo above.
``` shell
git init && git remote add origin git@github.com:AndreasAhrens/Home-Assistant-Config.git && git fetch && git checkout -t origin/master

sudo hassbian-config install mosquitto && sudo hassbian-config install hue && sudo hassbian-config install samba 
```
While this is being installed:
``` shell
touch secrets.yaml && sudo chmod 755 secrets.yaml && sudo chown pi secrets.yaml && sudo nano secrets.yaml
```
Enter secrets.yaml that has been saved from before
``` shell
touch known_devices.yaml && sudo chmod 755 known_devices.yaml && sudo chown pi known_devices.yaml  && sudo nano known_devices.yaml
```
Same here, enter old config
``` shell

cd /etc/mosquitto/ && sudo cp mosquitto.conf mosquitto.conf.old && sudo rm -rf mosquitto.conf && sudo nano mosquitto.conf
```
Enter mosquitto config

``` shell
sudo systemctl restart mosquitto.service 
```
For troubleshooting
``` shell
sudo apt install htop wavemon
sudo apt-get install net-tools nmap
```

#### Possibly:
``` shell
# sudo hassbian-config install libcec 
```



## Tellstick:
``` shell
sudo hassbian-config install tellstick && sudo systemctl enable telldusd.service && sudo nano /etc/tellstick.conf
```
Enter predefined tellstick.conf
``` shell
sudo reboot now
```

## Install duckdns and letsencrypt:
https://community.home-assistant.io/t/guide-how-to-set-up-duckdns-ssl-and-chrome-push-notifications/9722
### Duck DNS
``` shell
sudo mkdir duckdns && cd duckdns && sudo touch duck.sh && sudo chmod 700 duck.sh && sudo mkdir /root/duckdns && sudo touch /root/duckdns/duck.log && sudo nano duck.sh
# sudo hassbian-config install duckdns
crontab -e
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
sudo touch duck.log && sudo chmod 777 duck.log && sudo ./duck.sh && cat duck.log
```

### Certbot
``` shell
cd ~ && mkdir certbot && cd certbot && wget https://dl.eff.org/certbot-auto && chmod a+x certbot-auto
```
New version, No warning:
``` shell
./certbot-auto certonly --standalone --preferred-challenges http-01 --email andreas@ahrensit.se -d eiolos.duckdns.org
sudo chmod -R 777 /etc/letsencrypt && sudo systemctl restart home-assistant@homeassistant.service
```
old version, still supported, but gives warning
``` shell
#./certbot-auto certonly --standalone --standalone-supported-challenges http-01 --email andreas@ahrensit.se -d eiolos.duckdns.org
```

## Homebridge:
Below manual install. Can also be installed via the Homebridge app automatically.
``` shell
sudo apt-get install nodejs npm
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install libavahi-compat-libdnssd-dev
sudo npm install -g --unsafe-perm homebridge
sudo npm install -g homebridge-homeassistant && sudo npm install -g homebridge-magichome && sudo npm install -g homebridge-mi-air-purifier miio && sudo npm install homebridge-server@latest -g
sudo nano ~/.homebridge/config.json
sudo nano /root/.homebridge/config.json
homebridge
```
https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi


### Run homebridge on boot
https://gist.github.com/johannrichard/0ad0de1feb6adb9eb61a/
``` shell
sudo nano /etc/default/homebridge
sudo nano /etc/systemd/system/homebridge.service
sudo useradd --system homebridge
sudo mkdir /var/lib/homebridge
sudo chown homebridge /var/lib/homebridge

sudo nano /var/lib/homebridge/config.json
journalctl -u homebridge
```

### Homebridge server:
https://www.npmjs.com/package/homebridge-server

### Fix homebridge problem:
Sometimes Homebridge stops working and is not shown in the Home app. The below code can sometimes solve it.
``` shell
sudo systemctl stop homebridge.service
sudo systemctl restart avahi-daemon
sudo systemctl start homebridge.service 
```


``` shell
sudo systemctl daemon-reload
sudo systemctl enable homebridge
sudo systemctl start homebridge
```

## FFMPEG
echo "deb http://ftp.debian.org/debian jessie-backports main" | sudo tee /etc/apt/sources.list
sudo apt-get update && sudo apt-get -t jessie-backports install ffmpeg
## Install MPD
``` shell
sudo apt-get install mpd mpc
sudo nano /etc/mpd.conf
audio_output {
        type            "alsa"
        name            "My ALSA Device"
        device          "hw:0,0"        # optional
        mixer_type      "software"      # optional
#       mixer_device    "default"       # optional
#       mixer_control   "PCM"           # optional
#       mixer_index     "0"             # optional
}
```

## MySQL:
``` shell 
sudo apt-get install mysql-server
```

``` shell 
mysql -u root -p
CREATE USER 'hassbian'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE hassbian;
GRANT ALL PRIVILEGES ON hassbian . * TO 'hassbian'@'localhost';
FLUSH PRIVILEGES;
exit;
```

``` shell 
sudo chown -R homeassistant /usr/local/lib/python3.4
sudo apt-get install libmysqlclient-dev
```

### Seems to work:
``` shell
sudo systemctl stop home-assistant@homeassistant.service
sudo su -s /bin/bash homeassistant
source /srv/homeassistant/bin/activate
pip3 install mysqlclient
exit
sudo systemctl start home-assistant@homeassistant.service
```

### Doesn't seem to work:
``` shell
#sudo -i
#su homeassistant
#cd /srv/homeassistant/homeassistant_venv/
#source bin/activate
#pip3 install mysqlclient
```

## Make a backup!
Now it's a good time to make a backup so you don't have to go through all of this again...

## Upgrade Home Assistant
``` shell
sudo hassbian-config uppgrade home-assistant
```
## Alternative, old way

``` shell
cd /home/pi/Downloads/
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

sudo systemctl restart telldusd.service
```
