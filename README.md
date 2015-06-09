Copyright (c) 2015 BEEVC - Electronic Systems This file is part of BEESOFT software: 
you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
BEESOFT is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with BEESOFT. If not, see <http://www.gnu.org/licenses/>.

## Changelog ##

## v1.0.0 ##

*Printer Info screen is now updated with:
    * Printer Model Name
*WiFi config wifi.conf file in USB disk
*New Images
*New Display size and resolution
*Updated BEECODE List
*Shutdown Button in Settings
*Over-The-Air Updates
*Bug Fixes

## v0.2  ##

Printer Info screen is now updated with:
    * Printer satus
    * Printer firmware version
    * BeeConnect Version
    * Ethernet address
    * Wireless SSID
    * Wireless IP

### v0.1 ###

* Printer status update
* Print finish notification screen
* Images for movement and mantainance actions

## BEEConnect 1.0.0 ##

BEEConnect creates a small interface to control you BeeTheFirst 3D Printer. <br/>
BEEConnect grants you access to mantainance operations directly on the touch screen. <br/>
BEEConnect allows you to run custom gcodes on your BTF Printer, using USB Mass storage devices to transfer the code directly to the pritner. <br/>

https://github.com/beeverycreative/beeconnect


## Working on ##

* New Features


## Setup ##

### Requirements ###

* Raspberry Pi running Raspbian
* LCD Touch Dispaly with XPT2046 + ILI9341 controllers
* Python 3.4
* PyGame



### Reccommended Install ###
We recommend you to install BEEConnect by burning the Available Image into a SD card. <br/>
To burn the image follow these steps: <br/>

*   Download the .img file. <br/>
*   Insert a 8GB+ SD card in your SD card reader. <br/>
*   Follow instructions on how to burn the .img. (http://www.raspberrypi.org/documentation/installation/installing-images/) <br/>

However if you wish to install it on an existing raspbian image read section "Installing BEEConnect in an existing Raspbian Image" and follow the instructions. <br/>

## Update ##

To update, open a ssh session with using the username "pi" and the default password "1234":

    * In Windows use putty (or similar)
    * In Osx or Linux, open terminal and type "ssh pi@IP_ADDRESS", or "ssh pi@HOSTNAME.local"

In the ssh session console type:

        cd
        cd beeconnect
        sudo git pull
        sudo python3 setup.py install
        
        
## Installing BEEConnect in an existing Raspbian Image ##

### Install Bonjour/Zeroconf ###

        cd
        sudo apt-get update
        sudo apt-get install libnss-mdns

### Install Adafruit PiTFT ###

        cd
        wget http://adafru.it/pitftsh
        mv pitftsh pitft.sh
        chmod +x pitft.sh
        sudo ./pitft.sh -t 28c -r 

When asked if you want show console on the screen type "n" and press enter. Same thing fot the shuthdown option on button 23.

### Instal USB automount ### 

        sudo apt-get install usbmount
        
### Install PyGame ###

        cd
        sudo apt-get install mercurial
        hg clone https://bitbucket.org/pygame/pygame
        cd pygame

        sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev 
        sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev

        python3 setup.py build
        sudo python3 setup.py install
        
### Install PyUSB ###

        cd
        git clone https://github.com/walac/pyusb.git git/pyusb
        cd git/pyusb
        sudo python3 setup.py install
        
### BEEConnect ###

        cd
        git clone https://github.com/beeverycreative/beeconnect.git
        cd beeconnect/
        sudo python3 setup.py install
        
### Python Modules ###

        sudo apt-get install python3-pip
        sudo pip-3.2 install netifaces
        
        sudo reboot