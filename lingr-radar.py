#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import pylingr
import collections
from gntp.notifier import GrowlNotifier
from pit import Pit

config = Pit.get(
  'lingr.com', {
    'require':{
      'email': 'email for lingr.com',
      'password': 'password for lingr.com',
      'api_key': 'api_key for lingr.com'
    }
  }
)

growl = GrowlNotifier(
  applicationName="Lingr Radar",
  notifications=['message', 'presence', 'error'],
)
growl.register()

lingr = pylingr.Lingr(config['email'], config['password'], config['api_key'])
stream = lingr.stream()
messageIds = collections.deque(maxlen = 5)

while True:
  try:
    e = stream.next()
  except:
    time.sleep(30)
    stream = lingr.stream()
    continue

  if 'message' in e.keys():
    m = e['message']
    mid = m['id']
    if mid in messageIds:
      continue
    messageIds.append(mid)
    i = 'icon_url' in m and m['icon_url'] or ''
    growl.notify(
      noteType='message',
      title="%s@%s" % (m['nickname'], m['room']),
      description=m['text'].encode('utf-8'),
      icon=i,
    )
