# LabelPush
## Simple lightweight label printing app

- License: MIT License
- Author: Matteljay
- Language: Python (>= 3.5)
- Homepage: https://github.com/Matteljay


## Screenshots

![](screenshots/01_welcome.png)
![](screenshots/02_hello_serif.png)
![](screenshots/03_hello_double_bold.png)
![](screenshots/04_settings.png)


## Introduction

LabelPush is a simple lightweight label printing application written in Python.
It is built to be fast and simple to use. The CUPS printing system is used.
Please make sure the printer is correctly installed with all correct
settings such as label/paper size. This link should take you to your local
settings: [CUPS-localhost](http://localhost:631/printers/)


## Installation

Package dependencies are kept to a minimum. The proper installation guides
for your system can be found via these links:

- [Kivy](https://kivy.org/doc/stable/installation/installation.html) & [Pillow](https://python-pillow.org/)
Version 1.10.1 with SDL2 window provider are required! (NOT 1.9 with PyGame).
An updated Python Imaging Library is always recommended with a graphical Python program. And definitely required for LabelPush.

- [pip3](https://github.com/pypa/pip) & [setuptools](https://github.com/pypa/setuptools)
These are Python 3 installation tools. Universally useful!

- [CUPS](https://www.cups.org/)
Printer server for macOS and other UNIX-like operating systems.

### Debian Linux

For most up-to-date Debian based systems like Ubuntu Linux and Linux Mint this should work *as root*:

    add-apt-repository ppa:kivy-team/kivy
    apt-get install python3-kivy python3-pip python3-setuptools
    pip3 install --upgrade pillow labelpush

### Arch Linux

For the more up-to-date Arch Linux (Manjaro) simply run *as root*:

    pacman -S python-kivy python-pillow python-pip python-setuptools
    pip3 install labelpush


## How to launch

When finished, the shortcut icon can be found from your menu-bar in the **Office** category.
If the icon does not show up, you may need to restart your desktop.
Alternatively, open your graphical user terminal and type **labelpush.py**


## For developers, hackers and testers

Other ways to install are explained below. The above dependencies are still required!
Only use the info below if you know what you are doing.

### Option 1

You can install from tar.gz or the GitHub master tree.
First, download and extract the archive from the [releases](https://github.com/Matteljay/labelpush/releases) page.
Then run from within the extracted folder:

    sudo pip3 install .

### Option 2

Alternatively, you can run it without installing to the root
filesystem. Again, extract the downloaded archive. Then run:

    pip3 install --user -r requirements.txt
    ./labelpush.py


## More platforms

### Other UNIX

Other flavors of Linux are untested but there is no reason for them
not to work. Slackware, Gentoo, openSUSE, Fedora, Red Hat, Mandriva, CentOS,...

### Android, iPhone and Windows

These platforms probably won't work as they feature different printer
software (no CUPS). If a strong desire exists, find a way to
motivate me :-)


## Contact info & donations

See the [contact](CONTACT.md) file on GitHub.


