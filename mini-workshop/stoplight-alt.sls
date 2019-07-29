# -*- coding: utf-8; mode:yaml; tab-width:2; indent-tabs-mode:nil; -*-
# vim: syntax=yaml ts=2 sw=2 sts=2 et si ai

{% set minions = salt.saltutil.runner('cache.grains',tgt='*') %}

{% for node, grains in minions|dictsort %}
{% if grains['os_family'] == 'RedHat' %}
{% set web_path = '/usr/share/nginx' %}
{% elif grains['os_family'] == 'Debian' %}
{% set web_path = '/var/www' %}
{% endif %}

update_stoplight_to_yellow_on_{{ node }}:
  salt.function:
    - name: file.touch
    - tgt: {{ node }}
    - arg:
      - {{ web_path }}/html/maintenance.html

stoplight_timer_for_yellow_on_{{ node }}:
  salt.function:
    - tgt: {{ node }}
    - name: test.sleep
    - kwarg:
        length: 2
    - require:
      - salt: update_stoplight_to_yellow_on_{{ node }}
{% endfor %}

{% for node, grains in minions|dictsort %}
update_stoplight_to_green_on_{{ node }}:
  salt.state:
    - tgt: {{ node }}
    - sls: go-green
{% endfor %}

{% for node, grains in minions|dictsort %}
{% if grains['os_family'] == 'RedHat' %}
{% set web_path = '/usr/share/nginx' %}
{% elif grains['os_family'] == 'Debian' %}
{% set web_path = '/var/www' %}
{% endif %}
update_stoplight_to_red_on_{{ node }}:
  salt.function:
    - name: file.remove
    - tgt: {{ node }}
    - arg:
      - {{ web_path }}/html/test.html
    - require:
      - salt: update_stoplight_to_green_on_{{ node }}

stoplight_timer_for_red_on_{{ node }}:
  salt.function:
    - tgt: {{ node }}
    - name: test.sleep
    - kwarg:
        length: 2
    - require:
      - salt: update_stoplight_to_red_on_{{ node }}
{% endfor %}
