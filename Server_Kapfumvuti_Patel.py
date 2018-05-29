# Project 1: Implementation of Go-Back-N Protocol
# Group Member: Daksh Patel         ID: 104 030 031
# Group Member: Nyasha Kapfumvuti	ID: 104 121 166
# Date: Mar 30th, 2018

import socket 
import numpy
import time
import json
from random import randint

acked           = []  # acknowledged packets
unAcked         = []  # unacknowledged  packets
ticker          = 0   # 0.2 loss rate = 1/5 packets get "lost" => placed in unAcked
lostItem        = 5   # every 5th item gets placed in unacked
returnVals      = []  # array of values to be returned as acks/unacks
timer           = time.localtime
packets         = []
packet          = ''
server_address = ('localhost', 10000)
serverSocket    = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(server_address)
serverSocket.listen(1)
print('The server is ready to receive') 

while True:
    print('waiting for a connection')
    connection, client_address = serverSocket.accept() 
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(1024) # data arrives as a string. Need to convert this back to an array
            newPack = int(data)
            if(randint(0,5) == 5):
                print('packet was lost/corrupted')
                connection.sendto(str(newPack).encode(), server_address)
            else:
                if newPack not in acked:
                    acked.append(newPack)
                print('recieved sequence # ', str(newPack), ' successfully. Sending ack')
                connection.sendto(str(newPack).encode(), server_address)
                print('sent')
            ticker += 1 # loss rate leads to every nth item getting lost
            
            if data:
                # send acknowledgement
                # connection.sendto(str(newPack).encode(), server_address)
                print('')
            else:
                break
    finally:
        connection.close()
        print(acked)
