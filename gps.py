#!/usr/bin/python

import socket
import threading
import configparser
from ConnProcessor import ConnProcessor
from DbWrapper import DbWrapper

# read config
config = configparser.ConfigParser()
config.read("config.txt")

# start the server
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = config.get('server', 'host')
port = config.getint('server', 'port')
print("Starting server on {}:{}".format(host, port), flush=True)
s.bind((host, port))
s.listen(5)

# connect to the DB
db = DbWrapper(config['database'])

# start listening
while True:
    try:
        client, addr = s.accept()
    except KeyboardInterrupt:
        break

    thread = ConnProcessor(client, addr, db)
    thread.start()

# terminate threads
for t in threading.enumerate():
    if hasattr(t, 'should_terminate'):
        t.should_terminate = True

s.close()
print("\nBye!")
