import socket
from time import time, sleep
import json


id = 1
for _ in range(1):
    timestamp = time()
    data_to_send = {
        "id": id,
        "timestamp": int(timestamp * 1e9),
        "event": "start_experiment",
        "value": '1',
    }
    event = json.dumps(data_to_send).encode("utf-8")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(event, ("239.128.35.86", 7891))
    sleep(1)

stims = ['cat', 'cat', 'dog', 'horse', 'mouse', 'mouse', 'mouse', 'key', 'key', 'camel']
for stim in stims:
    id += 1
    timestamp = time()
    data_to_send = {
        "id": id,
        "timestamp": int(timestamp * 1e9),
        "event": "event_stim",
        "value": stim,
    }
    event = json.dumps(data_to_send).encode("utf-8")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(event, ("239.128.35.86", 7891))
    sleep(.500)

id += 1
timestamp = time()
data_to_send = {
    "id": id,
    "timestamp": int(timestamp * 1e9),
    "event": "end_experiment",
    "value": '0',
}
event = json.dumps(data_to_send).encode("utf-8")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(event, ("239.128.35.86", 7891))
