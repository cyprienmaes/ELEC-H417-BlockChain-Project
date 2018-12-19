#!/usr/bin/env python

"""
THIS IS A NODE MADE FOR TESTS IT'S NOT INTERACTIVE BUT ONLY A LISTENER. IT BEHAVES AS A
NORMAL NODE IN THE NETWORK.


"""

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
                #print(addr)
                data = conn.recv(self.BUFFER_SIZE)
                if data:
                    decriptedData = ast.literal_eval(data.decode('utf-8'))
                    try:
                        """
                        We want to know what kind of message we received
                        Here we consider it is a new block
                        """
                        
                        receivedBlock = decriptedData['Block']
                        if receivedBlock in self.blockchain.waiting_blocks:
                            pass


                        
                        else :
                            self.blockchain.putting_block(receivedBlock)
                            self.message = data
                            nodesMessage = Thread(target = node.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                            nodesMessage.start()
                    except KeyError:
                        try:
                            """
                            The message is not a new block but a response to a received block
                            If the block is rejected we drop everything and broadcast a message of rejection
                            If it is accepted we check if it is accepted by every neighbour if yes we ad it to the chain
                            and broadcast the info

                            """
    
                            receivedConfirmation = decriptedData['Confirmation']
                            if decriptedData['Conf block'] in blockchain.waiting_blocks:
                                if receivedConfirmation == 'block rejected':
                                    self.blockchain.waiting_blocks.clear()
                                    self.contactedIP.clear()
                                    self.message = data
                                    nodesMessage = Thread(target = node.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                                    nodesMessage.start()
                                elif receivedConfirmation == 'block accepted':
                                    self.contactedIP[addr] = receivedConfirmation
                                    if self.verifyIfAccepted():
                                        self.blockchain.chain.append(self.blockchain.waiting_blocks[0])
                                        self.blockchain.waiting_blocks.clear()
                                        self.message = data
                                        nodesMessage = Thread(target = node.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
                                        nodesMessage.start()
                                        
                                    else:
                                        continue
                                    
                        except KeyError:
                            pass
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
                while True:
                    try:
                        socketNodes.connect((neighbour, 5003))
                        socketNodes.send(self.message)
                        self.contactedIP[neighbour] = 'waiting'
                        break
                    except ConnectionRefusedError:
                        pass
            break

    def setMessage(self,block):
        message = str(block).encode('utf-8')
        return message

    def verifyIfAccepted():
        verified = True
        for contact in self.nextIP:
            if 'block accepted' == contactedIP[contact]:
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
    tran_op = 0

##    while True:
##        while (tran_op==0):
##            print("Do you want to make a transaction?")
##            transac_status = input("")
##            if transac_status =="yes":
##                #athentication = node.authenticate()
##                #if authenticate == b'ok'
##                print("How much money do you want to transfer?")
##                amount = input("")
##                if amount.isdigit():                
##                    if amount == 0:
##                        tran_op = 1
##                        print("Transaction Impossible - Amount Null")
##                        print(node.blockchain.last_block)
##                        
##                    else:                                       # insert proof of work here
##                        #blockchain.new_transaction(amount)
##                        """
##                        Here we create a new block that we broadcoast.
##                        """
##                        
##                        
##                        if (node.blockchain.chain == []):                  # ïf blockchain is empty, create genesis block
##                            #blockchain.create_genesis_block()
##                            nodesMessage = Thread(target = node.runNodesMessage) #Problem. We kill the last thread even if it didn't accomplished the task
##                            node.message = node.setMessage(node.blockchain.create_genesis_block(amount))
##                            nodesMessage.start()
##                        else:
##
##                            proof, time_proof = proof_of_work(node.blockchain.last_block())
##                            previous_hash = hashBlock(node.blockchain.last_block())
##                            #blockchain.new_block(blockchain.last_block['hash'])
##                            node.blockchain.new_block(amount, proof, time_proof, previous_hash)
##                        print("Transaction Validated")   
####                        timer.setTime(0)
####                        while (timer.getTime() < 30):
####                            if False:                                 # insert block incoming condition here
####                                blockchain.chain[-1] = []             # deletes created block if it recieves another block
####                        """append block"""
##                    
##                else:
##                    tran_op = 1;
##                    print("Transaction Impossible - Wrong Input")
##            elif transac_status =="no":
##                print("Ending Transaction")
##                tran_op = 1
##            else:
##                print("Transaction Impossible - Wrong Input")
##                tran_op = 1
##        tran_op = 0    
    
    
    
if __name__ == '__main__': main()




        
