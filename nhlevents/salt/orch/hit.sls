# -*- coding: utf-8; mode:yaml; tab-width:2; indent-tabs-mode:nil; -*-
# vim: syntax=yaml ts=2 sw=2 sts=2 et si ai

{% set info = salt.saltutil.cmd('hue', 'hue.lights') %}

Turn Bulb bulbs red:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        id: 1,3
        color: red

{%- for bulb in ['1','3'] %}
Set Bulb {{ bulb }} Color:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        id: {{ bulb }}
        gamut: {{ info['hue']['ret'][bulb]['state']['xy'][0] }},{{ info['hue']['ret'][bulb]['state']['xy'][1] }}
    - require:
      - salt: Turn Bulb bulbs red
{% endfor%}
