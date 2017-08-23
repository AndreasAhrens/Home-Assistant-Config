passwd

hassbian-config

cd /home/homeassistant/.homeassistant/


Git:
sudo apt-get update && upgrade
sudo apt install git

Tellstick:

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
