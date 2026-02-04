#!/usr/bin/env python3

#pretty sure this sets the language to python3 on Linux? That's what it looks like to me.

from pyre import Pyre
from pyre import zhelper
import zmq
import uuid
import json

#imports necessary modules. Pyre appears to be an input monitoring tool, zhelper helps with network functions
#ZeroMQ is a messaging library

def get_peer_node(username):
    n = Pyre(username)
    #n.set_header("CHAT_Header1","example header1")
    #n.set_header("CHAT_Header2","example header2")
    n.start()
    return n

#defines the function, uses pyre's username variable?


def join_group(node, group):
    node.join(group)
    print(f"Joined group: {group}")

#defines join_group with two variables: node and group


def chat_task(ctx, pipe, n, group):
    poller = zmq.Poller()
    poller.register(pipe, zmq.POLLIN)
    # print(n.socket())
    poller.register(n.socket(), zmq.POLLIN)
    # print(n.socket())

#defines chat_task
#uses poller which seems to watch for pipe and n.socket.

    while(True):
        items = dict(poller.poll())
        # print(n.socket(), items)
        if pipe in items and items[pipe] == zmq.POLLIN:
            message = pipe.recv()
            # message to quit
            if message.decode('utf-8') == "$$STOP":
                break
            print(f"YOU: {message.decode('utf-8')}")
            n.shouts(group, message.decode('utf-8'))
        else:
            cmds = n.recv()
            msg_type = cmds.pop(0).decode('utf-8')
            peer_id = uuid.UUID(bytes=cmds.pop(0))
            peer_username = cmds.pop(0).decode('utf-8')
            match msg_type:
                case "SHOUT":
                    intended_group = cmds.pop(0).decode('utf-8')
                    if intended_group == group:
                        # print(f"{peer_username}({peer_id}): {cmds}")
                        print(f"{peer_username}: {cmds.pop(0).decode('utf-8')}")
                case "ENTER":
                    headers = json.loads(cmds.pop(0).decode('utf-8'))
                    # print(f"NODE_MSG HEADERS: {headers}")
                    # for key in headers:
                    #    print("key = {0}, value = {1}".format(key, headers[key]))
                    # print( f"{peer_username}({peer_id}): is now connected." )
                    print( f"{peer_username}: is now connected." )
                case "JOIN":
                    #print( f"{peer_username}({peer_id}): joined {cmds.pop(0).decode('utf-8')}." )
                    print( f"{peer_username}: joined {cmds.pop( 0 ).decode( 'utf-8' )}." )
            # print(f"NODE_MSG CONT: {cmds}")
    n.stop()

#if it's able to poll these things, it connects and starts listening for other peers?
#Has pre-baked messages for connecting.

def get_channel(node, group):
    ctx = zmq.Context()
    return zhelper.zthread_fork(ctx, chat_task, n=node, group=group)

#defines get_channel and returns a few things, including chat_task. This appears to wrap up the code so it can run.

