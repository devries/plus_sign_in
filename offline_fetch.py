#!/usr/bin/env python

import json
import httplib2
import logging
import glob

from oauth2client.file import Storage

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

flist = glob.glob('credentials/*')

for fname in flist:
    storage = Storage(fname)
    credentials = storage.get()

    url = 'https://www.googleapis.com/plus/v1/people/me'
    h = httplib2.Http('cache')
    h = credentials.authorize(h)
    resp,content = h.request(url,'GET')
    info = json.loads(content)
    logging.info('%s: ID: %s',info['displayName'], info['id'])
