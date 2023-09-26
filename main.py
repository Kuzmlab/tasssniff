import json
import asyncio

from datetime import datetime

import sql
from sql import *
import time

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (
    PeerChannel
)

api_id = 14375045
api_hash = '6c5cc6923aee8b712470371dab57c03c'

api_hash = str(api_hash)

phone = 79939766199
username = 'Kuzmlab'

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

# client = TelegramClient('session_name',
#                     api_id,
#                     api_hash,
#                     )
async def main(phone):
    await client.start()
    entity = await client.get_entity('t.me/+Dvp0lz6innBlMmJi')
    name_ch = '@TerminalTASSBot'


    while True:
        file = open('lastID.txt', 'r')
        str_min_id = file.read()
        file.close()
        min_id = int(str_min_id)
        offset_id = 0
        limit = 100
        all_messages = []
        total_messages = 0
        total_count_limit = 10000
        #print('scan ', name_ch, 'min_id:', min_id)

        while True:
            try:
                history = await client(GetHistoryRequest(peer=name_ch, offset_id=offset_id, offset_date=None,
                                                         add_offset=0, limit=limit, max_id=0, min_id=min_id, hash=0))
                if not history.messages:
                    break
                messages = history.messages
                for message in messages:
                    all_messages.append(message.to_dict())
                offset_id = messages[len(messages) - 1].id
                total_messages = len(all_messages)
                if total_count_limit != 0 and total_messages >= total_count_limit:
                    break
            except:
                print("scan ", name_ch, " error!")
                break

        msgs_sql = []
        #   insert msg in sql
        for message in all_messages:
            if (message['_'] == 'Message') and len(message['message']) > 0:
                await client.send_message(entity=entity, message=message['message'])

        #print(name_ch, ' scanned msgs: ', total_messages)
        min_id = min_id + total_messages
        file = open('lastID.txt', 'w')
        file.write(str(min_id))
        file.close()
        time.sleep(1)
with client:
    client.loop.run_until_complete(main(phone))

        #print('finish')