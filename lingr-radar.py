import time
import pylingr
from gntp.notifier import GrowlNotifier
from pit import Pit

config = Pit.get(
  'lingr.com', {
    'require':{
      'email': 'email for lingr.com',
      'password': 'password for lingr.com'
    }
  }
)

growl = GrowlNotifier(
  applicationName="Lingr Radar",
  notifications=['message', 'presence', 'error'],
)
growl.register()

lingr = pylingr.Lingr(config['email'], config['password'])
stream = lingr.stream()
while True:
  try:
    e = stream.next()
  except:
    time.sleep(30)
    stream = lingr.stream()
    continue

  if 'message' in e.keys():
    m = e['message']
    i = 'icon_url' in m and m['icon_url'] or ''
    growl.notify(
      noteType='message',
      title="%s@%s" % (m['nickname'], m['room']),
      description=m['text'],
      icon=i,
    )
