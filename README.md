BEECONNECT by ![www.beeverycreative.com](https://www.beeverycreative.com/client/skins/images/logo.png "Logo Title Text 1")
===============================

The BEETHEFIRST 3D printer was built around the [R2C2](http://www.3dprinting-r2c2.com/) electronic board and is a RepRap printer at heart (however we are using a custom usb communication protocol).

Our goals are:
* To make the BEETF more compatible overall and allowing users to enjoy their favourite 3D printing software or customize their slicer settings;
* To ensure compatibility for the best 3D printing projects;
* To develop a steping stone for open-source colaboration.
* Also to develop Wi-Fi/LAN connectivity for the BEETHEFIRST 3D print;

The first of the projects that we will ensure 100% compatibility is the [Octoprint](http://octoprint.org/) an amazing responsive web interface for controlling your 3D printer that runs on the [Raspberry Pi](http://www.raspberrypi.org/). 

You can follow and contact us for development on [BEECONNECT Google Groups page](https://groups.google.com/forum/#!forum/beeconnect).


Version History
===============

* BECONNECT v0.1 (this is where we are right now)
  * BEETF Communication API using [pyUSB](https://github.com/walac/pyusb/)
  * USB command line interface into the BEETF
  * linux-driver and intructions; 
  * Octoprint compatibility using PyUsb to launch the BEETF in serial COM mode.

* BECONNECT v1.0 (next step)
  * multi-system user-friendly installations
  * Complete, ready-to-user, Raspberry Pi Kit optimized for the BEETF

* BECONNECT v2.0 (somewhere over the rainbow)
  * we are not sure, what lies ahead ;)


Install image
=============
Following this steps you can install a prepared image of BEECONNECT. 
Download the image [here](https://www.beeverycreative.com/public/software/software/beeconnect_v01.dmg.zip).
[Follow this steps](https://github.com/raspberrypi/documentation/blob/master/installation/installing-images/README.md). Jump to "Writing an image to the SD card"

Setup on RPI from scratch
=========================
We found that the easiest way to setup Octprint on your Raspberry Pi is to use [OctoPi](https://github.com/guysoft/OctoPi) 
> A Raspberry Pi distribution for 3D printers. It includes the OctoPrint host software for 3D printers out of the box and mjpg-streamer with rapicam support for live viewing of prints and timelapse video creation.

OctoPi for the BEETF can easily be installed by downloading our pre-configured [image](ftp://beeverycreative.com) and following the steps described in [OctoPi](https://github.com/guysoft/OctoPi) 

1. unzip the image and dd it to an sd card like any other Raspberry Pi image
2. boot the pi and connect it to a lan or wifi network, like any other Rasbpian installation.
3. OctoPrint is located at `http://octopi.local <http://octopi.local>`_ and also at `https://octopi.local <https://octopi.local>`_. > Since the SSL certificate is self signed (and generated upon first boot), you will get a certificate warning at the latter location, please ignore it.
4. If a webcam was plugged in, MJPG-streamer is on port 8080. You can reach it at: `http://octopi.local:8080/?action=stream <octopi.local:8080/?action=stream>`_. It is also setup so that you can reach it under `http://octopi.local/webcam/?action=stream <octopi.local/webcam/?action=stream>`_ and SSL respectively.




Setup on existing OctoPi or Linux based system
==============================================

BEECONNECT tools can be installed by cloning this repository and installing them.

    git clone https://github.com/beeverycreative/beeconnect.git
    cd beeconnect
    sudo python setup.py install



Dependencies
------------

- PyUsb 1.0
- Python >= 2.7or >= 3.3


Documentation
------------

[g-codes implemented](https://github.com/beeverycreative/beeconnect/blob/develop/beetf/gcode.md)


Resources
------------
git ignore rules from (https://github.com/github/gitignore) under [MIT](https://github.com/github/gitignore/blob/master/LICENSE)

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/rui-teixeira/beetf/blob/master/LICENSE>`_ file for more details.
