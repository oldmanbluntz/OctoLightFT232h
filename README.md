Just a test to get this plugin to work with CircuitPython's digitalio instead of RPI.GPIO

Forked from Gigibu5/OctoLight

It is currently working. 

To get it working, Install octoprint on Ubuntu following these directions, but stop when you go to start octoprint, or to make the service for Automating Octoprint Startup:

https://www.illuminated3d.com/2020/06/05/setting-up-octoprint-on-ubuntu-20-04-with-python-3/

Before making the service files, install libusb, pyftdi, and adafruit-blinka following these instructions. You will be installing all of this while you have the venv active from installing octoprint:

https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/linux

After you get this installed, you will need to edit your /etc/environment file, as to set the "BLINKA_FT232H" environment variable. Use the text editor of your choice and add this line to the last line of the file (for example "sudo nano /etc/environment", add the line, ctrl O to save, then ctrl X to exit):

BLINKA_FT232H=1

The next step is to create the service but to use systemd/systemctl to create it. Create a file at "/etc/systemd/system/octoprint.service", and put the following code in it, making sure to update the user and the path parts of the file if you didn't install octoprint at the default user "pi": (for example "sudo nano /etc/systemd/system/octoprint.service", paste the following code, press ctrl O to save, then ctrl X to exit)

[Unit]
Description=Octoprint Server
After=network.target
[Service]
Type=simple
Restart=always
RestartSec=10
User=pi
ExecStart=/home/pi/OctoPrint/venv/bin/octoprint serve --port=5000
Environment=BLINKA_FT232H=1
[Install]
WantedBy=multi-user.target

save that file with CTRL X, then run this command:

"sudo chmod 777 /etc/systemd/system/octoprint.service"

and finally run

"sudo systemctl enable octoprint"

you will now have Octoprint installed on Ubuntu, you will have the libusb/pyftdi/adafruit-blinka dependencies installed, you will have the environment variable set for all users, and you will have octoprint starting as a service on bootup of Ubuntu. You will now be able to install this plugin, and turn an LED or a relay to run more leds on and off using a desktop computer with an Adafruit FT232H breakout board. They have 12 digital GPIO pins, and can do SPI or I2C.

https://www.adafruit.com/product/2264
