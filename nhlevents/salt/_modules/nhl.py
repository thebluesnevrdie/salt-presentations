# -*- coding: utf-8 -*-
'''
Module for interacting with the NHL API

:codeauthor:    Cody Crawford <cody@saltstack.com>
:maturity:      new
:platform:      all

'''

# Import salt libs
import salt.utils
import datetime

__virtualname__ = 'nhl'

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


def games(game_state='Live',date=None):
    '''
    Request schedule of games for a given date

    game_state
        One of Live, Preview, or Final

    date
        Formatted as YYYY-MM-DD. Defaults to current date.

    '''

    if not date:
        today = datetime.datetime.now()
        date = today.strftime('%Y-%m-%d')

    url = "https://statsapi.web.nhl.com/api/v1/schedule"
    request = '{0}?date={1}'.format(url,date)
    response = _make_request(request)
    ret = {}

    for game in response['dates'][0]['games']:
        if game['status']['abstractGameState'] == game_state:
            ret[game['gamePk']] = {}
            ret[game['gamePk']]['away'] = game['teams']['away']['team']['name'].encode('utf8', 'replace')
            ret[game['gamePk']]['home'] = game['teams']['home']['team']['name'].encode('utf8', 'replace')
            ret[game['gamePk']]['venue'] = game['venue']['name']
    return ret
