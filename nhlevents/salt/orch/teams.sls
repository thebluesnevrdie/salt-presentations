# -*- coding: utf-8; mode:yaml; tab-width:2; indent-tabs-mode:nil; -*-
# vim: syntax=yaml ts=2 sw=2 sts=2 et si ai

{% set game = salt['pillar.get']('game') %}
{% set teamcolors = salt.saltutil.runner('cache.pillar',tgt='hue') %}
{% set colors = teamcolors['hue']['teams'][game] %}

{% for bulb, color in colors.iteritems() %}
Set Bulb {{ bulb }} to {{ color }}:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        id: {{ bulb }}
        color: {{ color }}

{% if color == 'white' %}
{% set bright = 150 %}
{% else %}
{% set bright = 255 %}
{% endif %}

Set Bulb {{ bulb }} Brightness:
  salt.function:
    - tgt: 'hue'
    - name: hue.brightness
    - kwarg:
        id: {{ bulb }}
        value: {{ bright }}
    - require:
      - salt: Set Bulb {{ bulb }} to {{ color }}
{% endfor %}
