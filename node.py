#!/usr/bin/env python

import socket
import hashlib
import ast

#--------GLOBAL VARIABLES----------------

TCP_IP = '127.0.0.1'  # my IP 164.15.244.54
TCP_PORT = 5005
BUFFER_SIZE = 1024
#MESSAGE = b"Hello, World!"
Password = b'Dricot'
MESSAGE = str({'Username':'mat','Password':Password}).encode('utf-8')
data = ''



#-------------METHODS-------------------

def connect(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(message)
    data = s.recv(BUFFER_SIZE)
    print ("received data:", data)
    s.close()

def authenticate():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    message = request = str({'Username':'mat','Request': 'send nonce motherfucker'}).encode('utf-8')
    s.send(message)
    data = s.recv(BUFFER_SIZE)
    #print ("received data:", data)
    hashedMessage = hashlib.sha256()
    hashedMessage.update(data)
    hashedMessage.update(Password)
    myHash = hashedMessage.digest()  #or hexdigest for a more condensed form
    s.send(myHash)
    data = s.recv(BUFFER_SIZE)
    print ("received authentication:", data)
    s.close()
    return data


def requestNonce():
    #request = b"('mat','send nonce motherfucker')"
    request = str({'Username':'mat','Request': 'send nonce motherfucker'}).encode('utf-8')
    connect(request)

def sendMessage(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(message)
    s.close()


sendMessage(MESSAGE)

#userAnswer = input('Send request? ')



active = True

while active:
    userAnswer = input("Write 'a' to athenticate or 'l' to logout")
    if userAnswer == 'a':
        authenticate()
        #print(authenticate())
    elif userAnswer == 'l':
        active = False
    else:
        print('Wrong command')
        pass
    
    

#print ("received data:", data)


    
