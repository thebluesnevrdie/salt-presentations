# -*- coding: utf-8 -*-
'''
Module for interacting with the Pimoroni InkyPhat

:codeauthor:    Cody Crawford <cody@saltstack.com>
:maturity:      new
:platform:      all

Example:

.. code-block:: yaml

    show_current_weather:
      inkyphat.weather:
        - image_dir: '/etc/salt/inkyphat/icons'
        - font_file: '/etc/salt/inkyphat/fonts/SourceSansPro-Regular.ttf'
        - celsius: True
        - location: False

'''
from __future__ import absolute_import, print_function, unicode_literals
import datetime

# Import Salt Libs
import salt

def __virtual__():
    return 'inkyphat'

def _to_celsius(temp):
    return (temp - 32) * 0.5556

def weather(name, image_dir, font_file, celsius=False, location=True):
    '''
    Updates the inkyphat display to a current weather forecast including an icon

    name
        The name has no functional value and is only used as a tracking reference

    image_dir
        Directory containing the icon images corresponding to weather conditions

    font_file
        Full path to the font to be used (coordinates work with SourceSansPro-Regular best

    celsius
        Optional: boolean - use celsius instead of the default of Fahrenheit

    location
        Optional: boolean - display the location (default) or summary info

    '''
    ret = {'name': name,
           'changes': {},
           'result': False,
           'comment': ''}

    display_stack = []
    temp_font_size = 36
    temp_coords = (105, 4)
    line_coords = (105,50,200,50)
    location_font_size = 16
    city_coords = (105, 54)
    region_coords = (105, 69)

    latitude = __grains__['geo']['latitude']
    longitude = __grains__['geo']['longitude']
    forecast = __salt__['darksky.forecast']([latitude, longitude])
    image_path = '{0}/{1}.png'.format(image_dir,forecast['currently']['icon'])
    summary = forecast['currently']['summary']

    if celsius:
        temp = _to_celsius(forecast['currently']['temperature'])
        display_temp = '{0:.1f}\260 C'.format(temp)
    else:
        temp = forecast['currently']['temperature']
        display_temp = '{0:.1f}\260 F'.format(temp)
    
    if location:
        city = __grains__['geo']['city']
        region = __grains__['geo']['region_name']
    else:
        summary = forecast['currently']['summary']

    display_stack.append({'type': 'image', 'coords': (2,2), 'file': image_path})
    display_stack.append({'type': 'text', 'coords': temp_coords, 'content': display_temp, 'file': font_file, 'size': temp_font_size })
    display_stack.append({'type': 'line', 'coords': line_coords})

    if location:
        display_stack.append({'type': 'text', 'coords': city_coords, 'content': city, 'file': font_file, 'size': location_font_size })
        display_stack.append({'type': 'text', 'coords': region_coords, 'content': region, 'file': font_file, 'size': location_font_size })
        ret['changes']['location'] = '{0}, {1}'.format(city, region)
    else:
        display_stack.append({'type': 'text', 'coords': city_coords, 'content': summary, 'file': font_file, 'size': location_font_size })
        ret['changes']['summary'] = summary

    __salt__['inkyphat.draw'](display_stack)

    ret['result'] = True
    ret['changes']['temperature'] = display_temp
    return ret
