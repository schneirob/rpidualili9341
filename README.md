You have a small project, where one small display just isn't enough, but you do
not want to use the HDMI port (e.g. for reasons of form factor). Then it is
possible to connect two small displays to the SPI bus that is located on the
GPIO bar of the Raspberry Pi.

The following Raspbery Pi was used for this experiment:

| Hardware	| BCM2835  |
| Revision	| a020d3   |
| Model         | 3B+      |
| Revision      | 1.3      |
| RAM           | 1GB      |
| Manufacturer  | Sony UK  |


Additionally some cheap SPI displays with ili9341 chipset, cables, ... the
usual.


# pin-layout

| pin	| gpio	| name	|
| :---: | :---: | ----- |
| 1	| 	| 3.3V	|
| 6	| 	| GND	|
| 11	| 17	| (SPI1_CE1)	|
| 12	| 18	| (SPI1_CE0)	|
| 13	| 27	| SPI1_LED / SPI0_LED	|
| 18	| 24	| SPI0_DC	|
| 19	| 10	| SPI0_MOSI	|
| 21	| 9	| SPI0_MISO	|
| 22	| 25	| SPI0_RESET	|
| 23	| 11	| SPI0_SCLK	|
| 24	| 8	| SPI0_CE0	|
| 26	| 7	| (SPI0_CE1)	|
| 33	| 13	| SPI1_RESET	|
| 35	| 19	| SPI1_MISO	|
| 36	| 16	| SPI1_CE2	|
| 37	| 26	| SPI1_DC	|
| 38	| 20	| SPI1_MOSI	|
| 40	| 21	| SPI1_SCLK	|

() - not connected, but not usable for other applications


# dtoverlay

~~~bash
sudo dtc -I dts -O dtb -o /boot/overlays/rpi-displa0.dtbo dts/rpi-displa0.dts 
~~~

~~~
dtparam=spi=on
dtoverlay=spi1-3cs
...
dtoverlay=rpi-displa0
dtparam=rotate=90
...
~~~


# test

reboot before continuation

~~~bash
sudo modprobe fbtft_device name=rpi-display gpios=reset:13,dc:26,led:28 rotate=90 cs=2 busnum=1
~~~

led:28 - you need to name some GPIO, but it is hardwired to 27 used by both displays.

~~~bash
con2fbmap 1 1
con2fbmap 1 2
con2fbmap 1 0

sudo fbset -fb /dev/fb1 -i
sudo fbset -fb /dev/fb2 -i
~~~

convert your favorite 320x240 image to RGB565 and pipe it to the framebuffer

~~~bash
convert test.png -flip -type truecolor -define bmp:subtype=RGB565 test.bmp

tail --bytes 153600 test.bmp > /dev/fb1
tail --bytes 153600 test.bmp > /dev/fb2
~~~

configure what you require in /etc/rc.local, mine looks like this

~~~bash
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

modprobe fbtft_device name=rpi-display gpios=reset:13,dc:26,led:28 rotate=270 cs=2 busnum=1

con2fbmap 1 1

exit 0
~~~

Lets get an X-system running, python3 going ...

~~~bash
sudo apt-get install xinit python3 python3-pygame python3-rpi.gpio
~~~

~~~bash
sudo FRAMEBUFFER=/dev/fb1 xinit /usr/bin/python3 /home/pi/rpidualili9341/ui/simpleclock.py
~~~

With simpleclock I was able to reach 45 fps on /dev/fb1 and 30 fps on /dev/fb2. Currently I have no explenation for this except maybe signaling problems in the cabeling. 

# references

Thanks to everyone that did cover this topic ahead of me and made this
information available for me to collect and combine.


+ https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=194423
+ https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=193722&p=1217930#p1217930
+ https://stamm-wilbrandt.de/en/forum/rpi-displa0.dts
+ https://elinux.org/RPi_SPI
+ http://www.netzmafia.de/skripten/hardware/RasPi/RasPi_SPI.html
+ https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md
+ https://www.xgadget.de/anleitung/2-2-spi-display-ili9341-am-raspberry-betreiben/
