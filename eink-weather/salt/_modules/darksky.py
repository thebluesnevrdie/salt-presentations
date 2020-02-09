# -*- coding: utf-8 -*-
'''
Module for interacting with the DarkSky weather API

.. versionadded:: 2018.3.4

:codeauthor:    Cody Crawford <cody@saltstack.com>
:maturity:      new
:platform:      all

:configuration: This module requires an API key for the DarkSky service
    passed as an argument, or a configuration profile to be configured
    in the minion config, minion pillar, or master config.
    The module will use the 'darksky' key by default, if defined.

    For example:

    .. code-block:: yaml

        darksky:
          api_key: e72413d2cbd14b2fee7d5915e4c48e9d

'''

# Import salt libs
import salt.utils

__virtualname__ = 'darksky'

def __virtual__():
    return __virtualname__

def _make_request(url):
    our_req = salt.utils.http.query(
        url,
        status=200,
        method='GET',
        header_render=False,
        header='Content-Type: application/json',
        persist_session=False,
        verify_ssl=False
    )
    return salt.utils.json.loads(our_req['body'])


def forecast(coords, sections=['currently'], profile='darksky', api_key=None):
    '''
    Request forecast data for a specific location

    coords
        A two element list of Latitude, Longitude

    sections
        Optional: list of sections of forecast to include
        Available sections are currently, minutely, hourly, daily, alerts, flags
        Default is 'currently' section only.

    profile
        Configuration profile used to define the API key for the developer account at DarkSky.
        Default is 'darksky'.

    api_key
        API key for the developer account at DarkSky (if not defined as a config option)

    CLI Example:

    .. code-block:: bash

        salt 'minion01' darksky.forecast '["40.422563", "-111.883563"]' sections=['daily']

    '''

    if not api_key:
        profile = __salt__['config.option'](profile)
        if profile:
            api_key = profile.get('api_key', None)

    if not api_key:
        return False, 'An API key is required to access the DarkSky service. ' \
                      'See https://darksky.net/dev'
    
    url = "https://api.darksky.net/forecast/" 
    request = '{0}{1}/{2},{3}'.format(url, api_key, coords[0], coords[1])
    
    response = _make_request(request)

    ret = {}
    for section in sections:
        # if there is no data for a section, the DarkSky API will just omit it
        ret[section] = response.get(section, None)
    return ret
