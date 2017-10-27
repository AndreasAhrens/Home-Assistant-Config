# Home Assistant Config
My Home Assistant configuration, feel free to copy any config files you want. 
## Installation
Fork repo  
If you want to replace all current files (you might need to remove all existing files):  
1. git init
2. git remote add origin PATH/TO/REPO
3. git fetch
4. git checkout -t origin/master
## Usage
Use with [Home Assistant](https://home-assistant.io)
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
## License
MIT Licence

## System
- [Philips Hue](http://www2.meethue.com/)
- [IKEA Trådfri](http://www.ikea.com/se/sv/catalog/categories/departments/lighting/36812/)
- [Telldus Tellstick Duo](http://telldus.com/se/produkt/tellstick-duo/)
- Multiple [NodeMCUs](http://www.nodemcu.com/index_en.html)
- [Verisure](https://www.verisure.se/) (Alarm system, various sensors)
- [Xiaomi Gateway](https://www.gearbest.com/alarm-systems/pp_345588.html)
- [Xiaomi Smart human body sensor](https://www.gearbest.com/smart-light-bulb/pp_257678.html)
- [Xiaomi Door/Window sensor](https://www.gearbest.com/smart-light-bulb/pp_257677.html)
- Xiaomi Switches ([old](https://www.gearbest.com/smart-light-bulb/pp_257679.html?wid=21) and [new](https://www.gearbest.com/alarm-systems/pp_610095.html))
- [Xiaomi Cube](https://www.gearbest.com/living-appliances/pp_364494.html)
- [Xiaomi Temperature and Humidity sensors](https://www.gearbest.com/living-appliances/pp_344665.html)
- [Xiaomi Air Purifier 2](https://www.gearbest.com/home-smart-improvements/pp_268522.html)
- [Xiaomi plant sensors](https://www.gearbest.com/other-garden-supplies/pp_373947.html?wid=37)
- Xiaomi plugs ([Wifi](https://www.gearbest.com/power-strips/pp_341431.html) and [Zigbee](https://www.gearbest.com/living-appliances/pp_344666.html))
- 2 * [Xiaomi router 3](https://www.gearbest.com/wireless-routers/pp_497233.html) working as access points
- [Draytek Router](https://www.draytek.com/en/products/products-a-z/router.all/vigor2925-series/)
- [NetGear 24 port switches](https://www.cnet.com/products/netgear-prosafe-fsm726-managed-switch-switch-24-ports-managed-desktop-series/specs/)
- [Digoo cameras](https://www.banggood.com/Digoo-DG-M1Q-960P-2_8mm-Wireless-Mini-WIFI-Night-Vision-Smart-Home-Security-IP-Camera-Onvif-Monitor-p-1123595.html?rmmds=search)
- [Custom built rollers](https://github.com/DevvAndreas/D1-boards/tree/master/D1_Covers_Buttons_IR_DHT)
- [Custom built mailbox automation](https://github.com/DevvAndreas/Mailbox-Automation)
- Apple TV 3 and 2 (4K incoming)
- [Chromecast Audios](https://store.google.com/product/chromecast_audio)
- [Chromecast Ultra](https://store.google.com/product/chromecast_ultra)
- [Amazon Echo Dot](https://www.amazon.com/All-New-Amazon-Echo-Dot-Add-Alexa-To-Any-Room/dp/B01DFKC2SO)
- [Dark Sky Weather](https://home-assistant.io/components/sensor.darksky/)
- [InfluxDB](https://www.influxdata.com/)
- [Grafana](https://grafana.com/)
- [Pi Hole](https://pi-hole.net/)
- [Octo Print](http://octoprint.org/download/)
- Several [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) to run everything
- [Homebridge](https://github.com/nfarina/homebridge)
- [Mosquitto MQTT server](http://mosquitto.org/)
- [ARILUX AL-LC01 LED controllers](https://www.banggood.com/ARILUX-AL-LC01-Super-Mini-LED-WIFI-Smart-RGB-Controller-For-RGB-LED-Strip-Light-DC-9-12V-p-1058603.html?rmmds=search)
- [Blitzwolf Vacuum](https://www.banggood.com/BlitzWolf-BW-XRC600-Ultrasonic-Smart-Robot-Vacuum-Cleaner-with-1200pa-3350mAH-UV-APP-Wifi-Control-p-1078757.html?rmmds=search)
- [Husqvarna Automower 420](http://www.husqvarna.com/se/produkter/robotgrasklippare/automower-420/967622421/) with connect

## Goal of automation
I would like to automate the home to such a degree that everything just works and we understand our home completely without intervention. That includes understanding intentions and behaviour and adjusting to it. We are far from the end goal, but a pretty good way along at least. The bedroom is fully automated when it comes to lights, fan and rollers, we never have to manually adjust it anymore. The livingroom is rather close to perfectly automated. 

My vision of an automated home is one that adapts to the inhabitants, not the other way around. The lights should be the right level for the actions taken and the time of day, the home should clean itself when nobody is around to hear the vacuum, rollers should be down when changing clothes or sleeping and up during the day. The lawn should be cut when children are not out to play. The car should be started, removed from the garage and warmed up when someone is ready to leave. 

Somethings are still dreams or just too expensive to accomplish at the moment, such as a washer and dryer that loads, starts and unloads by themselves. Getting a little bit closer to the dream every month is my goal though. I usually build or automate at least a few things per month. 

## Automations

### Alarm system
- Say good night when alarm is turned on
- Set bedroom lights to bright or low depending on time and close bedroom rollers
- Play music in the kitchen when alarm is turned off from home mode

### Fan automation
- Turn on fan in bedroom and livingroom if the temperature is too high. Only if alarm is off or in home mode (bedroom).
- Turn off fans if temperature is lower again

### Stairs
- Turn on lights in stairs (leds under each step) when movement in upper or lower hallway and sun is down
- Turn off lights in stairs when no movement for 3 minutes
- Turn on light when sun goes down
- Turn off light when sun rises

### Dining room
- Turn on light in cabinets if movement
- Turn off light in cabinets if no movement for 10 minutes
- Turn on aquarium in the morning and turn off in the evening

### Kitchen
- Turn on light (led strip) over cabinets if movement. Will be complemented with strips under cabinets as well. Turn off if no movement for 10 minutes
- Turn on kitchen over cabinet lights when sun goes down

### Livingroom
- Turn on ceiling light and wall light if movement and sun is down
- Turn off ceiling light and wall light if no movement for 10 minutes
- Turn on lights/turn off lights and set brightness if Xiaomi double wall switch is pressed single or double
- Turn on or off ceiling fan if both buttons on Xiaomi double wall switch is pressed twice
- Turn on or off tv bench if both buttons on Xiaomi double wall switch is pressed once
- Set Livingroom to tv mode if something is playing on the Apple TV
- Turn on lights if door is opened and it's dark
- Turn on lights a bit before sun goes down or illumination is too low


### Mailbox
- Turn on light inside when hatch is opened and increase number of deposits by one, turn off light when closed
- Turn on light inside when door is opened and set number of deposits to zero, turn off light when closed
- Turn on light outside when it's evening and turn off when it's morning
- Notify in app and email when mail arrives, also via TTS

### Plants
- Water plants if humidity is too low automatically
TODO: set up individual watering, possibly with automatic adding of nutrition to water when nutrition is too low

### Bedroom
- Turn on light if movement, alarm is off and the light is not on already
- Morning TTS played over Chromecast when button is pressed or bedside light is turned on in the morning (automated via alarm on phone). This contains traffic, weather, time and so on.
- Turn off lights gradually in the evening and then turn off completely

### Outside
- Turn on entrace lights on sunset, movement, door bell ring or door open
- Turn on driveway light on sunset and turn off on sun rise

### Movement
- Notify (TTS and app) if I leave work with travel time
- Notify (TTS and app) if I stopped at one of the most common stores we shop at. My wife or kids can add things to shopping list via Echo Dot
- Notify (TTS and app) if my daughter arrives at or leaves school
- Turn on driveway light if I get close, then turn off a while after I get home



