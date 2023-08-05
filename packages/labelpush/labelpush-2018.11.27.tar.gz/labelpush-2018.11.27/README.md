# LabelPush - Lightweight label printing app

- License: MIT License
- Author: Matteljay
- Language: Python (>= 3.5)
- Homepage: https://github.com/Matteljay

## Screenshots

![](screenshots/01_welcome.png)
![](screenshots/02_hello_serif.png)
![](screenshots/03_hello_double_bold.png)
![](screenshots/04_settings.png)

## Getting started

LabelPush is a lightweight label printing application written in Python.
It is built to be fast and simple to use. The CUPS printing system is
used. So make sure the printer is correctly installed with all default
settings such as label size. This link should take you to your local
settings: [CUPS-localhost](http://localhost:631/printers/)

## Installation

Two libraries, the Kivy cross-platform GUI and Pillow imaging library
are required for LabelPush. Arch Linux (Manjaro) is very up-to-date,
installation will be very quick. This will be briefly explained below.

Unfortunately most Debian-based systems like Linux Mint and Ubuntu Linux
do not have the required up-to-date versions of these libraries.

However the requirements can be compiled and installed via the Python
package management system 'pip'. To be able to compile, install at least
these system packages via apt-get or the Synaptic Package Manager:

    sudo apt-get install python3-pip python3-dev python3-setuptools \
    libgl1-mesa-dev xclip

### Option 1

Now, get a copy of LabelPush. The 'whl' file from the
[releases-page](https://github.com/Matteljay/labelpush/releases) is
the easiest to work with. It does not require extracting, simply run:

    sudo pip3 install /path/to/file.whl

All of the requirements should now get downloaded, compiled and
automatically installed. This can take a while. When finished, the
shortcut can be found from your menu-bar in the 'Office' category.
If the icon does not show up, you may need to restart your desktop.

### Option 2

Alternatively, you can install from tar.gz or the GitHub master tree.
First, extract the archive. Then run from within the extracted folder:

    sudo pip3 install .

### Option 3

Alternatively, you can run it without installing to the root
filesystem. Again, extract the downloaded archive. Then run:

    pip3 install --user -r requirements.txt
    ./labelpush.py

### Arch Linux

Now, let's have a look at Arch Linux. Install these packages:

    sudo pacman -S python-kivy python-pillow python-setuptools cython

You can now choose from the 3 methods above, they will execute much
faster as no compilations are required:

    sudo pip3 install /path/to/file.whl
    sudo pip3 install .
    ./labelpush.py


## Development version

Optionally, you can use git:

    git clone git://github.com/Matteljay/labelpush.git
    cd labelpush

This should install dependencies:

    pip3 install --user -r requirements.txt


## Other platforms


### Linux distributions

This application should work on other up-to-date flavors of Linux like
Slackware, Gentoo, openSUSE, Fedora, Red Hat, Mandriva, CentOS,...

FreeBSD (TrueOS) and macOS are Linux based but are also untested.


### Windows

Although Python and the required libraries are cross-platform, this
application will not work on Windows due to the big difference in
printer software (no CUPS). If a strong desire exists, find a way to
motivate me :-)


## Contact info & Donations

See [contact](CONTACT.md) file.


