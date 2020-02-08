# -*- coding: utf-8; mode:yaml; tab-width:2; indent-tabs-mode:nil; -*-
# vim: syntax=yaml ts=2 sw=2 sts=2 et si ai

{% set info = salt.saltutil.cmd('hue', 'hue.lights') %}

Turn Bulb bulbs off:
  salt.function:
    - tgt: 'hue'
    - name: hue.switch
    - kwarg:
        id: 1,3
        'on': False

Turn Bulb bulbs on:
  salt.function:
    - tgt: 'hue'
    - name: hue.switch
    - kwarg:
        id: 1,3
        'on': True
    - require:
      - salt: Turn Bulb bulbs off

{%- for bulb in ['1','3'] %}
Set Bulb {{ bulb }} Brightness:
  salt.function:
    - tgt: 'hue'
    - name: hue.brightness
    - kwarg:
        id: {{ bulb }}
        value: {{ info['hue']['ret'][bulb]['state']['bri'] }}
    - require:
      - salt: Turn Bulb bulbs on
{% endfor%}
