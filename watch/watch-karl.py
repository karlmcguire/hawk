#!/usr/bin/env python3

import sys
from telethon import TelegramClient, events, sync, functions, types

api_id = sys.argv[1]
api_hash = sys.argv[2]

client = TelegramClient("data", api_id, api_hash)
client.start()

chan = client.get_entity(
        list(filter(
            lambda e: e.name == "Crypto Family Pumps", 
            client.get_dialogs()
        )
    )[0]
)

for message in client.iter_messages(chan, search = "Next message"):
    print(message.message)
    print(message.id)
    print("\n")

