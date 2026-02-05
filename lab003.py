from pyre import Pyre
from pyre import zhelper
import zmq
import uuid
import json
import lab_chat as lc

#imported everything from lab_chat.py to reduce confusion later on.


def get_username():
    username = input("Enter your username: ")
    username = username.strip()
    username = username.upper()
    return username

def get_group():
    group = input("Enter your group name: ")
    group = group.strip()
    group = group.upper()
    return group

def get_message():
    message = input("Message: ")
    message = message.strip()
    return message

username = get_username()
group = get_group()

#it breaks if I don't do this here, can't do in definitions. I'll let it be. I put it here when printing everything as a test.

def initializechat():
    node = Pyre(username)
    node.start()
    lc.join_group(node, group)
    channel = lc.get_channel(node, group)
    return channel

def startchat():
    channel = initializechat()

    while True:
        try:
            message = get_message()
            channel.send(message.encode('utf-8'))
        except (keyboardinterrupt, SystemExit):
            break
    channel.send("$$STOP".encode('utf-8'))
    print("Done")

initializechat()
startchat()

#So far, it asks for an initial message before connecting. I think that's fine because I know how it works, kind of.
