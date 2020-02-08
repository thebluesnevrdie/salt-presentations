# -*- coding: utf-8; mode:yaml; tab-width:2; indent-tabs-mode:nil; -*-
# vim: syntax=yaml ts=2 sw=2 sts=2 et si ai

Turn bulb 1 on:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        id: 1
        color: red

Turn bulb 2 on:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        id: 2
        color: blue

Turn bulb 3 on:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        id: 3
        color: yellow

Turn bulb 4 on:
  salt.function:
    - tgt: 'hue'
    - name: hue.color
    - kwarg:
        id: 4
        color: purple
