This is a talk about creating custom modules in SaltStack, with the goal of building a mini weather dashboard using an eInk display on a Raspberry Pi.

![Pi Zero with Inky pHAT](https://secure.meetupstatic.com/photos/event/2/5/b/9/highres_477729657.jpeg)

Below is the parts list if you want to try this out yourself:.

 * [Pimoroni Inky pHAT - eInk Display - Black/White](https://www.adafruit.com/product/3934)
 * [USB OTG Host Cable - MicroB OTG male to A female](https://www.adafruit.com/product/1099)
 * [Mini HDMI Plug to Standard HDMI Jack Adapter](https://www.adafruit.com/product/2819)
 * Raspberry Pi Zero WH (with Wifi, Bluetooth, and headers) from [Adafruit](https://www.adafruit.com/product/3708) or [PiShop](https://www.pishop.us/product/raspberry-pi-zero-wireless-wh-pre-soldered-header/)
 * [Generic USB 2.0 to Rj-45 Ethernet Adapter](https://www.amazon.com/gp/product/B003DR070U/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
 * [Enokay Power Supply for Raspberry Pi 5V 2.5A Micro USB Charger Adapter with On Off Switch](https://www.amazon.com/gp/product/B01MZX466R/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
 * [Samsung 32GB 95MB/s (U1) MicroSD EVO Select Memory Card](https://www.amazon.com/gp/product/B06XWN9Q99/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)

At the time of this writing, the above parts totaled approximately $67 without shipping.

**Note:** make sure you use a power supply with adequate amperage, or you will get SD card corruption. The Zero has pretty low consumption, so the power supply above (even with the display) should be more than enough. See the [power requirements for different models](https://www.raspberrypi.org/documentation/faqs/#pi-power) in the table here.


