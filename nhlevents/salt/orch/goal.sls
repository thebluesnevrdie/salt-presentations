# -*- coding: utf-8; mode:yaml; tab-width:2; indent-tabs-mode:nil; -*-
# vim: syntax=yaml ts=2 sw=2 sts=2 et si ai

{% set info = salt.saltutil.cmd('hue', 'hue.lights') %}

Turn bulbs red:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        color: red

Flash all four bulbs:
  salt.function:
    - tgt: 'hue'
    - name: hue.alert
    - require:
      - salt: Turn bulbs red

Wait for 6 seconds:
  salt.function:
    - tgt: 'hue'
    - name: test.sleep
    - kwarg:
        length: 6
    - require:
      - salt: Flash all four bulbs
      
Stop Flashing bulbs:
  salt.function:
    - tgt: 'hue'
    - name: hue.alert
    - kwarg:
        'on': False
    - require:
      - salt: Wait for 6 seconds

{%- for bulb in ['1','2','3','4'] %}
Set Bulb {{ bulb }} Color:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        id: {{ bulb }}
        gamut: {{ info['hue']['ret'][bulb]['state']['xy'][0] }},{{ info['hue']['ret'][bulb]['state']['xy'][1] }}
    - require:
      - salt: Stop Flashing bulbs
{% endfor%}
