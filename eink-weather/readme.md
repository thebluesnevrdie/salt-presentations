
![Pi Zero with Inky pHAT](https://secure.meetupstatic.com/photos/event/2/5/b/9/highres_477729657.jpeg)

# An introduction to extending SaltStack with custom modules

## Summary
We will show how easy it is to create and drop in custom components in SaltStack. Specifically, we will create a custom grain, execution, and state module and tie them together on our demo endpoint.

## Details

This is a talk about creating custom modules in SaltStack, with the goal of building a mini weather dashboard using an eInk display on a Raspberry Pi.

Below is the parts list if you want to try this out yourself:.

 * [Pimoroni Inky pHAT - eInk Display - Black/White](https://www.adafruit.com/product/3934)
 * [USB OTG Host Cable - MicroB OTG male to A female](https://www.adafruit.com/product/1099)
 * [Mini HDMI Plug to Standard HDMI Jack Adapter](https://www.adafruit.com/product/2819)
 * Raspberry Pi Zero WH (with Wifi, Bluetooth, and headers) from [Adafruit](https://www.adafruit.com/product/3708) or [PiShop](https://www.pishop.us/product/raspberry-pi-zero-wireless-wh-pre-soldered-header/)
 * [Generic USB 2.0 to Rj-45 Ethernet Adapter](https://www.amazon.com/gp/product/B003DR070U/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
 * [Enokay Power Supply for Raspberry Pi 5V 2.5A Micro USB Charger Adapter with On Off Switch](https://www.amazon.com/gp/product/B01MZX466R/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
 * [Samsung 32GB 95MB/s (U1) MicroSD EVO Select Memory Card](https://www.amazon.com/gp/product/B06XWN9Q99/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)

At the time of this writing, the above parts totaled approximately $67 without shipping.

**Note:** make sure you use a power supply with adequate amperage, or you will get random reboots and/or SD card corruption. The Zero has pretty low consumption, so the power supply above (even with the display) should be more than enough. See the [power requirements for different models](https://www.raspberrypi.org/documentation/faqs/#pi-power) in the table.

Use the following steps to prep the Raspberry Pi Zero as used in the talk:

1. Download the [Raspian installer image](https://fastapi.tiangolo.com/features/) (if you're not sure, get the "Raspbian Buster Lite" image)
1. Follow the [installation instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) to prepare your SD card.
1. Boot your Pi Zero with the SD card. Along with lots of other messages, you should see `Started LSB: Resize the rom filesystem to fill partition.`
1. Login as the user `pi` with the default password of `raspberry`. Once you're in, you can change the `pi` user's password with the `passwd` command.
1. Run the built-in configuration tool by typing `sudo raspi-config`
1. Update Locale:
   1. Move to item `4 Localisation Options`, and hit Enter.
   1. Select the first entry, `I1 Change Locale`
   1. Scroll down to `en_GB.UTF-8 UTF-8` and unselect it using the spacebar.
   1. Continue to scroll down to `en_US.UTF-8 UTF-8` and select it using the spacebar.
   1. Use the tab key to move to `<Ok>`, and hit Enter.
   1. When prompted for "Default locale for the system environment" choose `C.UTF-8`, then use the tab key to move to `<Ok>`, and hit Enter again.
1. Update Keyboard Layout:
   1. Move to item `4 Localisation Options`, and hit Enter.
   1. Select the third entry, `I3 Change Keyboard Layout`
   1. Select `Generic 104-key PC`, then for "Keyboard Layout" select "Other", scroll down and select "English (US)", then scroll up and select "English (US)" again.
   1. On the screen to select "Key to function as AltGr", choose either `The default for the keyboard layout` or `No AltGr key`
   1. On the screen to select "Compose key", choose `No compose key`
1. **Optional** - Enable the SSH server:
   1. Move to item `5 Interfacing Options`, and hit Enter.
   1. Select `P2 SSH` and choose `<Yes>` to enable the SSH server. Choose `<Ok>` to return to the main menu.
1. **Optional** - Configure wireless networking:
   1. Move to item `2 Network Options`, and hit Enter.
   1. Select `N2 Wi-fi` and choose your country if prompted.
   1. Enter your wirelss access point community name when prompted to `Please enter SSID`
   1. Enter your access point password when prompted to `Please enter passphrase.`
1. Use the tab key to move to `<Finish>`, and hit Enter.
1. Install the Salt Minion:
   1. Add the SaltStack repository key: `wget -O - https://repo.saltstack.com/py3/debian/10/armhf/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -`
   1. Add the SaltStack package repo: `sudo sh -c "echo 'deb http://repo.saltstack.com/py3/debian/10/armhf/latest buster main' > /etc/apt/sources.list.d/saltstack.list"`
   1. Update the list of packages available: `sudo apt-get update`
   1. Install the Salt Minion package: `sudo apt -y install salt-minion`
1. Install [Git](https://git-scm.com/) command-line tool: `sudo apt -y install git`
1. Clone this repo: `git clone https://github.com/thebluesnevrdie/salt-presentations.git`
1. Move Salt States and modules into place: `sudo cp -rv ./salt-presentations/eink-weather/salt /srv`
