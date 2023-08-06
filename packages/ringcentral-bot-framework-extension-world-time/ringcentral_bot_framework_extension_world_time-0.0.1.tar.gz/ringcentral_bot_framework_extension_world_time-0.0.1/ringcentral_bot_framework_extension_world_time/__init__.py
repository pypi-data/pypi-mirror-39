
import json
from datetime import datetime, timezone, timedelta

name = 'ringcentral_bot_framework_extension_world_time'

def botGotPostAddAction(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction
):
  """
  bot got group chat message: text
  bot extension could send some response
  return True when bot send message, otherwise return False
  """
  if not f'![:Person]({bot.id})' in text:
    return False

  if 'world time' in text:
    res = ''
    start = -12
    for i in range(27):
      h = i + start
      d = timedelta(hours=h)
      tz = timezone(d)
      t = tz.fromutc(datetime.utcnow().replace(tzinfo=tz))
      res = res + '\n' + t.strftime('%Z: %Y-%m-%d %H:%M:%S')
    bot.sendMessage(
      groupId,
      {
        'text': res
      }
    )
    return True
  else:
    return False