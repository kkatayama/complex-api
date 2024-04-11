# coding: utf-8
from pathlib import Path
from capstone_api import DiscordAPI
from markdownify import markdownify
from rich import print, markdown
from rich.markup import escape
import re


COMPLEX_API_CATEGORY_ID = '1226569641883865119'
CONNECT_TO_FLUTTERFLOW_CHANNEL_ID = '1226569765896720499'

CAT_ID = int(COMPLEX_API_CATEGORY_ID)
CHAN_ID = int(CONNECT_TO_FLUTTERFLOW_CHANNEL_ID)


def getFlutterFlowHowToMessages(d):    
    messages2 = d.getChannelMessages(channel_id=CHAN_ID)
    messages1 = d.getChannelMessages(channel_id=CHAN_ID, before='04-08-2024 09:10:11')
    messages3 = d.getChannelMessages(channel_id=CHAN_ID, after='04-10-2024 09:10:11')
    msg_ids = []
    msgs = []
    for m in messages1 + messages2:
        if m["id"] not in msg_ids:
            msg_ids.append(m["id"])
            msgs.append(m)
    messages = sorted(msgs, key=lambda x: x['id'])
    return messages


def createChannel(d: DiscordAPI, name: str, category_id: int, allow: str = '1024', deny: str = '0'):
    path = f'/guilds/{d.GUILD_ID}/channels'
    payload = {
        'type': 0,
        'name': name,
        'parent_id': category_id,
        'permission_overwrites': [
            {'id': d.BOT_ID, 'type': 0, 'allow': '536804850935', 'deny': '0'},
        ]
    }
    return d.post(path, json=payload)


d = DiscordAPI(config_path="secure_api", config_file="capstone.ini")
messages = getFlutterFlowHowToMessages(d)
for m in messages:
    if (('** **\n\n```' in m["content"]) and ('\n```\n\n** **' in m["content"])):
        m = re.search(r'(?P<step>[0-9\.]+)\s{2}(?P<desc>[a-zA-Z0-9\:\.\ ]+)', m["content"]).groupdict()
        title = str(m["step"].strip('.') + '.' + m["desc"].strip(':')).replace('.', '-').replace(' ', '-').lower()
        print(title)
        
        CH = createChannel(d, name=title, category_id=CAT_ID)
        d.cloneMessage(msg=m, channel_id=CH["id"])
    else:
        d.cloneMessage(msg=m, channel_id=CH["id"])
        
