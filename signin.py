#!/usr/bin/env python

import json
import bottle
import httplib2
import random
import string
import logging
import os

from beaker.middleware import SessionMiddleware

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.file import Storage

# We'll do some logging, I like to include time stamps so I can compare these times
# with any diagnostics on my browser console.
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

# The quickstart documents recommend placing a state key in the AJAX request which
# will match a state in the user session to avoid forgery by a malicous user. I
# configure beaker to use a session middleware here.
session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './data',
        'session.auto': True
        }

app = SessionMiddleware(bottle.app(), session_opts)

# I store the client ID, and secret in the client_secrets file. Here I read the client_id
# which the javascript of my page needs.
f = open('client_secrets.json','r')
client_secrets = json.load(f)
f.close()
client_id = client_secrets['web']['client_id']

if not os.path.exists('credentials'):
    os.makedirs('credentials')

@bottle.route('/')
def index():
    # I serve the template page with my client id and the state key, which I also save
    # in the session data.
    session = bottle.request.environ.get('beaker.session')
    state = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in range(32))
    session['state']=state
    session.save()
    return bottle.template('index',state=state,client_id=client_id)

@bottle.route('/connect', method='POST')
def connect():
    session = bottle.request.environ.get('beaker.session')
    state = bottle.request.query.state
    session_state = session['state']
    code = bottle.request.body.read()

    logging.debug('State: %s',state)
    logging.debug('Session State: %s',session_state)
    logging.debug('Code: %s',code)

    if state != session_state:
        return {'info':'Session/Web Page call missmatch. Forgery attempt?'}

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json',scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return {'info':'Something Went Wrong in the Flow Exchange'}

    url = 'https://www.googleapis.com/plus/v1/people/me'
    h = httplib2.Http('cache')
    h = credentials.authorize(h)
    resp,content = h.request(url,'GET')
    f = open('my_info.json','w')
    f.write(content)
    f.close()
    result = json.loads(content)
    if credentials.refresh_token:
        logging.debug('Saving new credentials because they have a refresh token.')
        gplus_id = result['id']
        storage = Storage('credentials/%s'%gplus_id)
        storage.put(credentials)
    else:
        logging.debug('No refresh token, not saving these credentials.')

    return {'info':'<p>You are:<br/><img src="%s"/><br/>%s</p>'%(result['image']['url'],result['displayName'])}

@bottle.route('/staticjs')
def staticjs():
    # In order to compare the performance of the server side calls, I adaped the pure
    # client-side javascript quick start to perform the same functions, but in this
    # case my server saves no data regarding the user.
    return bottle.template('jsindex',client_id=client_id)

bottle.debug(True)
bottle.run(app=app,host='localhost',port=9021)
