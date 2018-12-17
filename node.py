#!/usr/bin/env python

import socket
import hashlib
import ast
from threading import Thread
import time
#import Blockchain
from Blockchain import Blockchain


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

class Node:

    #--------GLOBAL VARIABLES----------------

    #TCP_IP = '127.0.0.1'  # my IP 164.15.244.54
    TCP_PORT = 5005        # port number used for the TCP authentication center connection
    TCP_PORT_BROAD = 5004  # testing for broadcoast 
    BUFFER_SIZE = 1024     # size of the receiveng buffer -- we can adapt it to the lenght
                           # of our messages witch will speed up the transition
    #MESSAGE = b"Hello, World!"
    Password = b'Dricot'   # users password
    sec = 0                # counter but I think it's gonna be useless
    data = ''

    #-------------METHODS-------------------

    
  

        
    def description(self):
        return '{} IP is {} and it is connected to the server at {}. Its neighbours are {} and {}' . format(self.username,self.ip_address,self.server_address,self.nextIP1,self.nextIP2)        
        
        
    def runNodesListener(self):
        """
        This function runs as a thread. It is responsible for listening to the neighboring nodes
        """
        
        socketNodes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketNodes.bind((self.ip_address, 5002))

        while True:
            socketNodes.listen(1)
            #print("fuck you")
            socketNodes.settimeout(1)
            try :
                conn, addr = socketNodes.accept()
                print(addr)
                data = conn.recv(self.BUFFER_SIZE)
                if data:
                    print(data)
                else:
                    continue
            except socket.timeout:
                pass

            #print("fuck you")


    def runNodesMessage(self):
        """
        Function sending infomrmations to other nodes
        """
        while True:
            for neighbour in self.nextIP:
                socketNodes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    socketNodes.connect((neighbour, 5003))
                    socketNodes.send(b'message')
                    socketNodes.close()
                except ConnectionRefusedError:
                    pass
                

    
    def runAuthenticationCenterCom(self):
        """ fonction run as a thread it's reposible for the communication with
        the authentication center
        """
        
        while True:
            answer = input("Write 't' for transaction or 'l' to logout")
            if answer == 't':
                authen = self.authenticate()
                if authen == b'ok':
                    blockchain = Blockchain()
                    value = input("Write the value of the transaction: ")
                    blockchain.new_transaction(value)
            elif answer == 'l':
                break
            else:
                print('Wrong command')
                pass

    def usersAction(answer):
        if answer == 't':
            authen = self.authenticate()
            if authen == b'ok':
                blockchain = Blockchain()
                value = input("Write the value of the transaction: ")
                blockchain.new_transaction(value)
##        elif answer == 'l':
##            
##        else:
##            print('Wrong command')
##            pass


    def authenticate(self):
        """
        Fonction which authenticates the user at the authentication center
        """

        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server_address, self.TCP_PORT))
        message = str({'Username':self.username,'Request': 'send nonce motherfucker'}).encode('utf-8') # User's request of nonce
        s.send(message)
        data = s.recv(self.BUFFER_SIZE)
        hashedMessage = hashlib.sha256()
        hashedMessage.update(data)
        hashedMessage.update(self.Password)  # The received nonce and the password are concatenated and hashed
        myHash = hashedMessage.digest()  #or hexdigest for a more condensed form
        s.send(myHash)
        data = s.recv(self.BUFFER_SIZE)
        print ("received authentication:", data) # Response of the authentication center
        s.close()
        return data


   

    def sendMessage(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.server_address, self.TCP_PORT)
        s.connect((self.server_address, self.TCP_PORT))
        s.send(message)
        s.close()



    def __init__(self):
        """
        Constructor of the node
        """
        
        config=ConfigParser()
        config.read('settings.ini')
        self.ip_address=config.get('node','ip_address')
        self.username=config.get('node','username')
        self.server_address=config.get('registration','ip_address')
        items = config.items('neigbours')
        print(items)
        self.nextIP = []   # list of the neighbours' IP addresses
        i = 0
        for neighbour in items:
            self.nextIP.append(neighbour[1])
            i+=1

        self.blockchain = Blockchain()

        #authenticationCenterCom = Thread(target = self.runAuthenticationCenterCom)
        
        nodeListener = Thread(target = self.runNodesListener)        
        nodesMessage = Thread(target = self.runNodesMessage)
        #timer = Thread(target = self.runTimer)
        #authenticationCenterCom.setDaemon(True)
        #nodeListener.setDaemon(True)
        #nodesMessage.setDaemon(True)
        #timer.setDaemon(True)
        #authenticationCenterCom.start()
        
        
        nodeListener.start()
        nodesMessage.start()
        #print('ok')
        #timer.start()

def main():

    node = Node()   
    #MESSAGE = str({'Username':node.username,'Password':node.Password}).encode('utf-8')
    #node.sendMessage(MESSAGE)
    
    
    
if __name__ == '__main__': main()




        
