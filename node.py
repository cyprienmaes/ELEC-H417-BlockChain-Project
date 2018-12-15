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
    #pass

    #Timer
    #Timer listener
    #Timer compare
    #Timer send

    # runTimer is a thread which runs the timer and sand it over a upd socket
    def runTimer(self):
        while self.sec <= 60:
            print(self.sec)
            self.sendTimer()
            time.sleep(1)
            self.sec+=1
            if self.sec >60:
                self.sec = 0

    def sendTimer(self):
        timerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #timerSocket.bind((self.nextIP1, self.TCP_PORT_BROAD))
        #timerSocket.send(str({'time':self.sec}).encode('utf-8'))
        timerSocket.sendto(str({'time':self.sec}).encode('utf-8'), (self.nextIP1, 5004))
        timerSocket.close()

    def runlistenToNodes(self):
        """
        This function runs as a thread. It is responsible for listening to the neighboring nodes
        """
        
        neighbour1socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbour1socket.connect((self.nextIP1, 5003))
        
    def runNodesListener(self):
        """
        This function runs as a thread. It is responsible for listening to the neighboring nodes
        """
        
        socketNodes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketNodes.bind((self.ip_address, 5003))
        while True:
            socketNodes.listen(1)
            #print("fuck you")
            conn, addr = socketNodes.accept()
            data = conn.recv(self.BUFFER_SIZE)
            if data:
                print(data)
            else: pass

    def runSend
            

    
    def runAuthenticationCenterCom(self):
        """ fonction run as a thread it's reposible for the communication with
        the authentication center
        """
        
        while True:
            #userAnswer = input("Write 't' for transaction or 'l' to logout")
            #usersAction(userAnswer)
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



    def __init__(self):
        config=ConfigParser()
        config.read('settings.ini')
        self.ip_address=config.get('node','ip_address')
        self.username=config.get('node','username')
        self.server_address=config.get('registration','ip_address')
        self.nextIP1=config.get('neigbours','IP_1')
        self.nextIP2=config.get('neigbours','IP_2')

        #authenticationCenterCom = Thread(target = self.runAuthenticationCenterCom)
        nodeListener = Thread(target = self.runNodesListener())
        #timer = Thread(target = self.runTimer)
        #authenticationCenterCom.setDaemon(True)
        nodeListener.setDaemon(True)
        #timer.setDaemon(True)
        #authenticationCenterCom.start()
        nodeListener.start()
        #timer.start()

def main():

    node = Node()   
    #MESSAGE = str({'Username':node.username,'Password':node.Password}).encode('utf-8')
    #node.sendMessage(MESSAGE)

##    authenticationCenterCom = Thread(target = node.runAuthenticationCenterCom())
##    authenticationCenterCom.setDaemon(True)
##    authenticationCenterCom.start()

    
    
    
if __name__ == '__main__': main()

    #print ("received data:", data)



        
