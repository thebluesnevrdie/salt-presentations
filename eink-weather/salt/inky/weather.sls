# -*- coding: utf-8; mode:yaml; tab-width:2; indent-tabs-mode:nil; -*-
# vim: syntax=yaml ts=2 sw=2 sts=2 et si ai

push_inky_icons_and_fonts:
  file.recurse:
    - name: /etc/salt/inkyphat
    - source: salt://inky/files/
    - makedirs: True

show_current_weather:
  inkyphat.weather:
    - celsius: True
    - location: False
    - image_dir: '/etc/salt/inkyphat/icons'
    - font_file: '/etc/salt/inkyphat/fonts/SourceSansPro-Regular.ttf'
    - require:
      - file: push_inky_icons_and_fonts
