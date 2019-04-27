=pin-layout=

pin	gpio	name
1		3.3V
6		GND
11	17	(SPI1_CE1)
12	18	(SPI1_CE0)
13	27	SPI1_LED / SPI0_LED
18	24	SPI0_DC
19	10	SPI0_MOSI
21	9	SPI0_MISO
22	25	SPI0_RESET
23	11	SPI0_SCLK
24	8	SPI0_CE0
26	7	(SPI0_CE1)
33	13	SPI1_RESET
35	19	SPI1_MISO
36	16	SPI1_CE2
37	26	SPI1_DC
38	20	SPI1_MOSI
40	21	SPI1_SCLK

() - not connected, but not usable for other applications


=dtoverlay=

'''
sudo dtc -I dts -O dtb -o /boot/overlays/rpi-displa0.dtbo dts/rpi-displa0.dts 
'''

'''
dtparam=spi=on
dtoverlay=spi1-3cs
...
dtoverlay=rpi-displa0
dtparam=rotate=90
...
'''


=test=

reboot

'''
sudo modprobe fbtft_device name=rpi-display gpios=reset:13,dc:26,led:28 rotate=90 cs=2 busnum=1
'''

led:28 - you need to name some GPIO, but it is hardwired to 27 used by both displays.

'''
con2fbmap 1 1
con2fbmap 1 2
con2fbmap 1 0
'''


=references=

+ https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=194423
+ https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=193722&p=1217930#p1217930
+ https://stamm-wilbrandt.de/en/forum/rpi-displa0.dts
+ https://elinux.org/RPi_SPI
+ http://www.netzmafia.de/skripten/hardware/RasPi/RasPi_SPI.html
+ https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md
+ https://www.xgadget.de/anleitung/2-2-spi-display-ili9341-am-raspberry-betreiben/


