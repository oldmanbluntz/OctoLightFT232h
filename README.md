Forked from gigibu5/OctoLight

This is a fully functioning proof of concept plugin to get the adafruit FT232H USB breakout board working in OctoPrint to get GPIO functionality on desktops running OctoPrint, since most desktops don't have native GPIO anymore, since serial/parallel ports left the commonplace with Motherboards. This should work on a Raspberry pi as well, and on Windows, as long as adafruit-blinka/libusb/pyftdi are installed and working on those platforms. It is a cheaper option than an add in card for the desktop. Plus, with the current shortage of, and increased price of, Raspberry Pi's, people who decide to use an x86/x64 platform to run OctoPrint can benefit from GPIO to control extra functions.

https://www.adafruit.com/product/2264 (link to the FT232H USB breakout board)

To get it working in Ubuntu (as i have yet gotten to fully test it on a rpi or on Windows), Install octoprint on Ubuntu following these directions, but stop when you go to start octoprint, or to make the service for Automating Octoprint Startup:

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

"sudo systemctl enable octoprint" to enable it on startup
"sudo systemctl start/stop octoprint" to start/stop the service.

you will now have Octoprint installed on Ubuntu, you will have the libusb/pyftdi/adafruit-blinka dependencies installed, you will have the environment variable set for all users, and you will have octoprint starting as a service on bootup of Ubuntu. You will now be able to install this plugin, and turn an LED or a relay to run more leds on and off using a desktop computer with an Adafruit FT232H breakout board. They have 12 digital GPIO pins, and can do SPI or I2C.

https://www.adafruit.com/product/2264
