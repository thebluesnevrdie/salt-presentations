# -*- coding: utf-8 -*-
'''
Module for interacting with the Pimoroni InkyPhat

.. versionadded:: 2018.3.4

:codeauthor:    Cody Crawford <cody@saltstack.com>
:maturity:      new
:platform:      all
'''

# Import salt libs
import salt.utils

from PIL import Image, ImageFont, ImageDraw

try:
    from inky import InkyPHAT
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

__virtualname__ = 'inkyphat'

def __virtual__():
    if HAS_LIBS:
        return __virtualname__
    else:
        return False, 'The "{0}" module could not be loaded: ' \
                      '"inky" is not installed.'.format(__virtualname__)

inky_display = InkyPHAT("black")
inky_display.set_border(inky_display.WHITE)

def clear():
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)
    inky_display.set_image(img)
    inky_display.show()
    return True

def fill():
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), 1)
    draw = ImageDraw.Draw(img)
    inky_display.set_image(img)
    inky_display.show()
    return True

def draw(stack):
    '''
    Draw a stack of elements to the display, where elements are any of
    the following passed as a list:

    { 'type': 'image', 'coords': [35,45], 'file': '/path/to/image' },
    { 'type': 'text', 'coords': [14,12], 'content': 'Lorem Ipsum', 'file': '/path/to/font', 'size': 18 },
    { 'type': 'line', 'coords': [6,8,25,37] }
    '''
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)
    for element in stack:
	print element
        our_coords = tuple(element['coords'])
        print our_coords
        if element['type'] == 'image':
            the_image = Image.open(element['file'])
            img.paste(the_image, our_coords)
        elif element['type'] == 'text':
            our_font = ImageFont.truetype(element['file'], element['size'])
            draw.text(our_coords, element['content'], inky_display.BLACK, our_font)
        elif element['type'] == 'line':
            draw.line(our_coords,inky_display.BLACK)
        else:
            # Unrecognized element
            continue

    inky_display.set_image(img)
    inky_display.show()
    return True
