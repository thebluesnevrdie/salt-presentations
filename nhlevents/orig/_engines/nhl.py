# -*- coding: utf-8 -*-
'''
Send events from NHL live game feed
'''

# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals

import logging
import time
import traceback

import salt.utils.json
import salt.utils.event

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

# Define the module's virtual name
__virtualname__ = 'nhl'

def __virtual__():
    return True

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

def start(game_id, interval=3, tag='salt/engines/nhl'):
    '''
    Poll NHL API live feed for plays and fire events

    Example Config

    .. code-block:: yaml

        engines:
          - nhl:
              game_id: 2018020845

    The config above sets up an engine to poll for
    for plays in an NHL game and publish them to
    the Salt event bus.
    '''

    if __opts__.get('__role') == 'master':
        fire_master = salt.utils.event.get_master_event(
            __opts__,
            __opts__['sock_dir']).fire_event
    else:
        fire_master = None

    def fire(tag, msg):
        '''
        How to fire the event
        '''
        if fire_master:
            fire_master(msg, tag)
        else:
            __salt__['event.send'](tag, msg)

    
    url = 'https://statsapi.web.nhl.com'
    request = '{0}/api/v1/game/{1}/feed/live'.format(url, game_id)
    counter = 0
    
    while True:
        response = _make_request(request)
        plays = response['liveData']['plays']
        current_playno = plays['currentPlay']['about']['eventIdx']

        # TODO: if we start the engine mid-game or for a finished
        #       game, how do we handle it?
        
        if current_playno > counter:
            for i in range(counter, current_playno):
                play_data = {}
                play_data['eventId'] = plays['allPlays'][(i + 1)]['about']['eventIdx']
                play_data['description'] = plays['allPlays'][(i + 1)]['result']['description']
                play_data['event'] = plays['allPlays'][(i + 1)]['result']['event']
                play_data['period'] = plays['allPlays'][(i + 1)]['about']['period']
                play_data['periodTime'] = plays['allPlays'][(i + 1)]['about']['periodTime']
                event = plays['allPlays'][(i + 1)]['result']['eventTypeId']
                #log.debug('NHL play: {0} - {1}'.format(play_data['eventId'],play_data['description']))
                fire('{0}/{1}'.format(tag, event), play_data)
            counter = current_playno
        time.sleep(interval)
