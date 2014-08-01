BEECONNECT by ![www.beeverycreative.com](https://www.beeverycreative.com/client/skins/images/logo.png "Logo Title Text 1")
===============================

The BEETHEFIRST 3D printer was built around the [r2c2](http://www.3dprinting-r2c2.com/) electronic board and is a RepRap printer at heart.
However we are using a usb communication protocol that makes it harde to use with most 3d printing software.

Our goals are:
* To make the BEETF more compatible overall and allowing users to enjoy their favourite 3d printing software or customize their slicer settings;
* To ensure compatibility for the best 3D printing projects;
* To develop a steping stone for open-source colaboration.
* Also to develop wifi/lan connectivity for the BEETHEFIRST 3d print;

The first of the projects that we will ensure 100% compatibility is the [Octoprint](http://octoprint.org/) an amazing responsive web interface for controlling your 3D printer that runs on the [Raspberry Pi](http://www.raspberrypi.org/). 


Version History
===============

* BECONNECT v0.1 (this is where we are right now)
  * BEETF Communication api using [pyUSB](https://github.com/walac/pyusb/)
  * USB command line interface into the BEETF
  * linux-driver and intructions; 
  * Octoprint compatibility using PyUsb to launch the BEETF in serial COM mode.

* BECONNECT v1.0 (next step)
  * multi-system user-friendly installations
  * Complete, ready-to-user, Raspberry Pi Kit optimized for the BEETF

* BECONNECT v2.0 (somewhere over the rainbow)
  * we are not sure, what lies ahead ;)


Setup on RPI from scratch
=========================
We found that the easiest way to setup Octprint on your Raspberry Pi is to use [OctoPi](https://github.com/guysoft/OctoPi) 
> A Raspberry Pi distribution for 3d printers. It includes the OctoPrint host software for 3d printers out of the box and mjpg-streamer with rapicam support for live viewing of prints and timelapse video creation.

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



Requirements
------------

- PyUsb 1.0
- Python >= 2.7or >= 3.3


Resources
------------

[g-codes implemented](https://github.com/beeverycreative/beeconnect/blob/develop/beetf/gcode.md)

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/rui-teixeira/beetf/blob/master/LICENSE>`_ file for more details.
