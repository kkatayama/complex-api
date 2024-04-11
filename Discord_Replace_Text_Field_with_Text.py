# coding: utf-8
from capstone_api import DiscordAPI
from rich import print
import time


d = DiscordAPI(config_path="secure_api", config_file="capstone.ini")
for msg in d.getChannelMessages(channel_id=1227661011373527040):
    if 'Text Field' in msg["content"]:
        print(msg["content"])
        msg["content"] = msg["content"].replace('Text Field', 'Text')
        msg["message_id"] = msg["id"]
        d.editMessage(**msg)
        time.sleep(2)
        
