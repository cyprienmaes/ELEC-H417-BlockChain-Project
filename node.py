#!/usr/bin/env python

import socket
import hashlib
import ast

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

class Node:

    #--------GLOBAL VARIABLES----------------

    TCP_IP = '127.0.0.1'  # my IP 164.15.244.54
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    #MESSAGE = b"Hello, World!"
    Password = b'Dricot'
    
    data = ''

    #-------------METHODS-------------------

    def __init__(self):
        config=ConfigParser()
        config.read('settings.ini')
        self.ip_address=config.get('node','ip_address')
        self.username=config.get('node','username')
        self.server_address=config.get('registration','ip_address')
        self.nextIP1=config.get('neigbours','IP_1')
        self.nextIP2=config.get('neigbours','IP_2')
        
    def description(self):
        return '{} IP is {} and it is connected to the server at {}. Its neighbours are {} and {}' . format(self.username,self.ip_address,self.server_address,self.nextIP1,self.nextIP2)        
    #pass
    

    def connect(message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(message)
        data = s.recv(BUFFER_SIZE)
        print ("received data:", data)
        s.close()

    def authenticate(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server_address, self.TCP_PORT))
        message = str({'Username':self.username,'Request': 'send nonce motherfucker'}).encode('utf-8')
        s.send(message)
        data = s.recv(self.BUFFER_SIZE)
        #print ("received data:", data)
        hashedMessage = hashlib.sha256()
        hashedMessage.update(data)
        hashedMessage.update(self.Password)
        myHash = hashedMessage.digest()  #or hexdigest for a more condensed form
        s.send(myHash)
        data = s.recv(self.BUFFER_SIZE)
        print ("received authentication:", data)
        s.close()
        return data


    def requestNonce():
        #request = b"('mat','send nonce motherfucker')"
        request = str({'Username':self.username,'Request': 'send nonce motherfucker'}).encode('utf-8')
        connect(request)

    def sendMessage(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.server_address, self.TCP_PORT)
        s.connect((self.server_address, self.TCP_PORT))
        s.send(message)
        s.close()


def main():

    node = Node()   
    MESSAGE = str({'Username':node.username,'Password':node.Password}).encode('utf-8')
    node.sendMessage(MESSAGE)

    active = True

    while active:
        userAnswer = input("Write 'a' to athenticate or 'l' to logout")
        if userAnswer == 'a':
            node.authenticate()
        elif userAnswer == 'l':
            active = False
        else:
            print('Wrong command')
            pass
    
    
if __name__ == '__main__': main()

    #print ("received data:", data)



        
