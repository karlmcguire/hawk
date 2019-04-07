#!/usr/bin/env python3

import sys
from telethon import TelegramClient, events, sync, functions, types
from telethon.tl.functions.messages import GetHistoryRequest

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

#print(dir(client))

alert_msgs = set()


searches = ['min', 'coin is']

for searchterm in searches:
    for message in client.iter_messages(chan, search = searchterm, reverse=True):
        print("Post with '"+searchterm+"'")
        print(message.message.encode('utf-8'))
        print(message.id)
        print(message.date)

        alert_msgs.add(message.id)
        #print(dir(message))
        print("\n")

        #posts = client(GetHistoryRequest(peer=chan, min_id=message.id+1, max_id=message.id+50, offset_id=0, add_offset=0, hash=0, offset_date=None, limit=500))
        #posts = client(GetHistoryRequest(peer=chan, min_id=0, max_id=0, offset_id=0, add_offset=0, hash=0, offset_date=None, limit=50)) # some i get UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f680' in position 1003: character maps to <undefined>

        '''
        for m in posts.messages:
            print (m.id, m.message)
        print("Image post")
        image_post = posts.messages[-1]'''

        #for image_post in posts.messages: #[::-1]:


alert_msgs = sorted(list(alert_msgs))

print(alert_msgs)

images_msgs = []

posts = {}


for image_post in client.iter_messages(chan, reverse=True):
        posts[image_post.id] = image_post
        print("Potential Image post ID ", end="")
        print(image_post.id)
        if image_post.id in alert_msgs:
            looking = 1
        #print(image_post.message.encode('utf-8'))
        if not image_post.media == None:

            images_msgs.append(image_post.id)


print(alert_msgs)
print(images_msgs)

alert_c = [[e, "A"] for e in alert_msgs]
images_c = [[e, "I"] for e in images_msgs]


all_c = alert_c + images_c
all_c.sort()
looking = 0

fout=open('tgimages.csv', 'w')

for item in all_c:

    print("at", item[0], looking)
    
    if item[1] == "A":
        looking = 1

    elif item[1] == "I":
            if looking:
                looking = 0
                print("downloaded image post", item[0])
                client.download_media(posts[item[0]].media, "./tg/images/"+str(item[0]))
                fout.write(str(item[0])+","+str(posts[item[0]].date)+"\n")
            else:
                looking = 0
                print("downloaded image post backup", item[0])
                client.download_media(posts[item[0]].media, "./tg/images/others/"+str(item[0]))
            looking = 0

    else:
        print("Error")
