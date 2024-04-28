

import socket
import bson
import logging

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
state = {}
connections = {}

def send_state(addr):
    msg = state
    sock.sendto(bson.dumps(msg), addr)
    return



def user_update(update: dict, state: dict, addr):
    username = update["user"]
    if username not in state:
        # Global state
        state[username] = {
            "x": 0,
            "y": 0
        }
        # Add this user's address to the connections dictionary
        connections[username] = addr
    else:
        user = state[username]
    if "x" in update or "y" in update:
        user["x"] += update["x"]
        user["y"] += update["y"]
    
    return user

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    try:
        update = bson.loads(data)
    except:
        print("invalid bson, no actions to be taken")
        continue
    try:
        user = user_update(update, state, addr)
    except Exception as e:
        logging.exception(f"User update failed")
    
    send_state(addr)
    print(f"{state=}")