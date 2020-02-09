# -*- coding: utf-8 -*-
'''
Grain data set via geoip info lookup from KeyCDN

:codeauthor:    Cody Crawford <cody@saltstack.com>
:maturity:      new
:platform:      all
'''

# Import salt libs
import salt.utils

def geo_grains():
    url = "https://tools.keycdn.com/geo.json"
    
    request = salt.utils.http.query(
        url,
        status=200,
        method='POST',
        header_render=False,
        header='Content-Type: application/json',
        persist_session=False,
        verify_ssl=False
    )

    response = salt.utils.json.loads(request['body'])
    return response['data']
