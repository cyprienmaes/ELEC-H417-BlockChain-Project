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
        socketNodes.bind((self.ip_address, 5003))

        while True:
            socketNodes.listen(1)
            socketNodes.settimeout(1)
            try :
                conn, addr1 = socketNodes.accept()
                #print(addr)
                data = conn.recv(self.BUFFER_SIZE)
                if data:
                    decriptedData = ast.literal_eval(data.decode('utf-8'))
                    addr = decriptedData[0]
                    try:
                        """
                        We want to know what kind of message we received
                        Here we consider it is a new block
                        """
                        
                        receivedBlock = decriptedData[1]['Block']
                        #print(receivedBlock)
                        if self.blockchain.chain == []:
                            self.arrivingBlock(decriptedData[1], addr, receivedBlock)                 

                        else:
                            #print('lalala')
                            if receivedBlock['previous_hash'] == self.blockchain.last_block['hash']:
                               self.arrivingBlock(decriptedData[1], addr, receivedBlock)
                            else:
                                self.message = self.setMessage((self.ip_address,{'Confirmation':'block rejected'}))
                                nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                                nodesMessage.setDaemon(True)
                                nodesMessage.start()
                               
                        
                    except KeyError:
                        try:
                            """
                            The message is not a new block but a response to a received block
                            If the block is rejected we drop everything and broadcast a message of rejection
                            If it is accepted we check if it is accepted by every neighbour if yes we ad it to the chain
                            and broadcast the info
                            """
                            if self.blockchain.waiting_blocks != []:
                                receivedConfirmation = decriptedData[1]['Confirmation']
                            
                                if receivedConfirmation == 'block rejected':
                                    self.blockchain.waiting_blocks.clear()
                                    self.contactedIP.clear()
                                    self.message = self.setMessage((self.ip_address,decriptedData[1]))
                                    nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                                    nodesMessage.setDaemon(True)
                                    nodesMessage.start()
                                elif receivedConfirmation == 'All my neighbours ok':
                                    #print('r u ok?')
                                    if addr in self.neighboursOk:
                                        pass
                                    else:
                                        self.neighboursOk.append(addr)
                                        if self.verifyConfirmed(self.neighboursOk):
                                            #print(self.blockchain.waiting_blocks)
                                            if self.blockchain.waiting_blocks != []:
                                                self.blockchain.chain.append(self.blockchain.waiting_blocks[0])
                                                print(self.blockchain.chain)
                                                self.blockchain.waiting_blocks.clear()
                                                self.neighboursOk.clear()
                                                self.confirmed.clear()
                                                #self.message = self.setMessage((self.ip_address,{'Confirmation': 'All my neighbours ok'}))
                                                #nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                                                #nodesMessage.setDaemon(True)
                                                #nodesMessage.start()
                                    
                                
                                elif receivedConfirmation == 'block accepted':
                                    self.contactedIP[addr] = receivedConfirmation
                                    if self.verifyIfAccepted():
                                        #print(self.blockchain.waiting_blocks)
                                        self.blockchain.chain.append(self.blockchain.waiting_blocks[0])
                                        #print(self.blockchain.chain)
                                        self.blockchain.waiting_blocks.clear()
                                        self.message = self.setMessage((self.ip_address,decriptedData[1]))
                                        nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                                        nodesMessage.setDaemon(True)
                                        nodesMessage.start()
                                        
                                    else:
                                        continue
                                    
                            else:
                                continue
                        except KeyError:
                            continue
                else:
                    continue
            except socket.timeout:
                pass

           
    def runNodesMessage(self):
        """
        Function sending infomrmations to other nodes
        """
        while True:
            for neighbour in self.nextIP:
                socketNodes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                while True:
                    try:
                        socketNodes.connect((neighbour, 5003))
                        socketNodes.send(self.message)
                        #print(b'sending'+self.message)
                        self.contactedIP[neighbour] = 'waiting'
                        break
                    except TimeoutError:
                        pass
                    except ConnectionRefusedError:
                        pass
                socketNodes.close()
            break

    

    def setMessage(self,block):
        message = str(block).encode('utf-8')
        return message
##
##    def arrivingBlock(self,data, addr, receivedBlock):
##        """
##        Looks if the received block is in the waiting list. If yes we
##        check if the address is already recorded. If no it is added to the waiting list
##        and broadcasted.
##        """
##        
##        if self.blockchain.waiting_blocks == []:
##            self.blockchain.putting_block(receivedBlock)
##            self.message = data
##            nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
##            nodesMessage.setDaemon(True)
##            nodesMessage.start()
##        else:
##            if receivedBlock in self.blockchain.waiting_blocks:
##                if addr not in self.confirmed:
##                    self.confirmed.append(addr)
##                    if self.verifyConfirmed(self.confirmed):
##                        self.message = setMessage({'Conf block': 'All my neighbours ok'})
##                        nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
##                        nodesMessage.setDaemon(True)
##                        self.blockchain.chain.append()
##                        nodesMessage.start()
##                        self.confirmed.clear()
                        
    def arrivingBlock(self,data, addr, receivedBlock):
        """
        Looks if the received block is in the waiting list. If yes we
        check if the address is already recorded. If no it is added to the waiting list
        and broadcasted.
        """
        
        if self.blockchain.waiting_blocks == []:
            #self.confirmed.clear()
            self.neighboursOk.clear()
            self.confirmed.append(addr)
            self.blockchain.putting_block(receivedBlock)

            self.message = self.setMessage((self.ip_address,data))
            nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
            nodesMessage.setDaemon(True)
            nodesMessage.start()
            nodesMessage.join()
            
            if self.verifyConfirmed(self.confirmed):
                #print('conf')
                #print(receivedBlock)
                self.message = self.setMessage((self.ip_address,{'Confirmation': 'All my neighbours ok'}))
                nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                nodesMessage.setDaemon(True)
                nodesMessage.start()
                nodesMessage.join()
                self.confirmed.clear()
##            else: 
##                self.message = self.setMessage((self.ip_address,data))
##                nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
##                nodesMessage.setDaemon(True)
##                nodesMessage.start()
        else:
            if receivedBlock in self.blockchain.waiting_blocks:
                if addr not in self.confirmed:
                    self.confirmed.append(addr)
                    if self.verifyConfirmed(self.confirmed):
                        self.message = self.setMessage((self.ip_address,{'Confirmation': 'All my neighbours ok'}))
                        nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                        nodesMessage.setDaemon(True)
                        nodesMessage.start()
                        nodesMessage.join()
                        self.confirmed.clear()
            else:
                self.blockchain.putting_block(receivedBlock)
                self.blockchain.waiting_blocks = [self.blockchain.compare_blocks()]
                self.message = self.setMessage((self.ip_address,{'Block': self.blockchain.waiting_blocks[0]}))
                nodesMessage = Thread(target = self.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                nodesMessage.setDaemon(True)
                nodesMessage.start()
                nodesMessage.join()
                           
        

    def verifyIfAccepted(self):
        verified = True
        for contact in self.nextIP:
            if 'block accepted' == contactedIP[contact]:
                verified = True
            else:
                verified = False
                break
        return verified

        
    
    def verifyConfirmed(self,listOfPeople):
        verified = True
        for addr in self.nextIP:
            
            if addr in listOfPeople:
                verified = True
            else:
                verified = False
                break
        return verified
            
            
        

    
    def runAuthenticationCenterCom(self):
        """ fonction run as a thread it's responsible for the communication with
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
        self.nextIP = []   # list of the neighbours' IP addresses
        i = 0
        for neighbour in items:
            self.nextIP.append(neighbour[1])
            i+=1
        self.message = b''
        self.blockchain = Blockchain()
        self.contactedIP = {}
        self.confirmed = []
        self.neighboursOk = []


def main():

    node = Node()   
    #MESSAGE = str({'Username':node.username,'Password':node.Password}).encode('utf-8')
    #node.sendMessage(MESSAGE)

    #blockchain = Blockchain()

    #authenticationCenterCom = Thread(target = self.runAuthenticationCenterCom)
    
    nodeListener = Thread(target = node.runNodesListener)        
    #nodesMessage = Thread(target = node.runNodesMessage)
    #authenticationCenterCom.setDaemon(True)
    #nodeListener.setDaemon(True)
    #nodesMessage.setDaemon(True)
    #authenticationCenterCom.start()
    
    
    nodeListener.start()
    #nodesMessage.start()
    #print('ok')
    #timer.start()
    
    
    
if __name__ == '__main__': main()




        
