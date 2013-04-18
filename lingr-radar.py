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

try:
  growl = GrowlNotifier(
    applicationName="Lingr Radar",
    notifications=['message', 'presence', 'error'])
  growl.register()
  def notify(title, message, icon):
    growl.notify(
      noteType='message',
      title=title,
      description=message,
      icon=icon)
except:
  import pynotify
  import urllib
  import pygtk
  import gtk
  pynotify.init("Lingr Radar")
  def notify(title, message, icon):
    n = pynotify.Notification(title, message)
    if len(icon) > 0:
      f = urllib.urlopen(icon)
      data = f.read()
      pbl = gtk.gdk.PixbufLoader()
      pbl.write(data)
      pbuf = pbl.get_pixbuf()
      pbl.close()
      n.set_icon_from_pixbuf(pbuf)
    n.show()

lingr = pylingr.Lingr(config['email'], config['password'], config['api_key'])
stream = lingr.stream()
messageIds = collections.deque(maxlen = 5)

while True:
  try:
    e = stream.next()
  except KeyboardInterrupt:
    break
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
    icon = 'icon_url' in m and m['icon_url'] or ''
    notify(
      "%s@%s" % (m['nickname'], m['room']),
      m['text'].encode('utf-8'),
      icon)
