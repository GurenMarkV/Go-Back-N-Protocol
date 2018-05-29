# Project 1: Implementation of Go-Back-N Protocol
# Group Member: Daksh Patel         ID: 104 030 031
# Group Member: Nyasha Kapfumvuti	ID: 104 121 166
# Date: Mar 30th, 2018

import socket #Sockets are the endpoints of a bidirectional communications channel. Channel types include TCP and UDP
import json #lightweight data interchange format inspired by JavaScript object literal syntax
import math #math functions
import numpy as np  # np is an alias pointing to numpy. importing as np helps keep away any conflict due to namespaces
import time #date time 

# GBN variables 
baseN           = 1
seqNum          = 1
nextPcktNumber  = 1
windowSize      = 10
numOfPackets    = 20
window          = []    #Arrays
packets         = []
unAcked         = []
Acked           = []
client_address = ('localhost', 10000)
server_address = ('localhost', 10000)
clientSocket    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET four-tuple (host, port, flowinfo, scopeid) is used
# SOCK_STREAM type of communications between the two endpoints
clientSocket.connect(server_address)
sending         = False
receiving       = True
lossRate        = 5 # .2 is one in 5 


# Generate a list of binary values for checksum demonstration : # seq nummber, acked, data
def prepPackets(numOfPackets): 
    for x in range(0, numOfPackets, 1):     
        packet = str(x)
        packets.append(packet)
    for x in range(0, len(packets), 1):
        print(packets[x])
        pass
    print('Done making ', numOfPackets, ' packets. Ready to start sending...')

# Send new and unAcked packets that are in the window
def sendData(baseN):
    window = []                                             # empty window
    while len(window) < windowSize:
        for x in unAcked:                                   # Add any unAcked packets to window for re-sending
            window.append(x)
            print('unacked package added', x)              
        if len(window) < windowSize:                        # Add new packets if there is room left in the window
            for x in range(baseN, (windowSize+baseN), 1):   # New packets fit current window location
                window.append(packets[x])
    for x in range(0, len(window),1):                       # send packet one at a time
        message = window[x]
        print('sending seq number: ', message)              #sequence num will increase with acks
        clientSocket.send(message.encode())
        print('listening')
        data, server = clientSocket.recvfrom(1024)
        newPack = int(data)
        Acked.append(newPack)
        baseN += 1
        print('attempted')
        print('back: ,', int(newPack))

# Continually receive acknowledgements and update containers 
def receiveData():
    print('receiving data')
    modifiedMessage = clientSocket.recvfrom(1024)
    print(modifiedMessage)
    clientSocket.close()
     

# Delay Timer to simulate GBN timeout
def timeOut(seconds):
    start = time.time()
    time.clock()    
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        print('Timeout! BaseN = ', baseN, ', Window Size: ', windowSize, ', Acked: ', Acked, ) 
        time.sleep(1) 

        sendData(baseN)


def main():   
    prepPackets(numOfPackets)
    timeOut(5)

main()

