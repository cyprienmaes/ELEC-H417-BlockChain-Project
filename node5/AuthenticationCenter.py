#!/usr/bin/env python

import socket
import ast
import secrets
import hashlib

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
#s.listen(1)

users = [];


#conn, addr = s.accept()
#print ('Connection address:', addr)

#------METHODS----------

def encodeUser(info):
    users.append(ast.literal_eval(info.decode('utf-8')))  # Conversion from string to dict end appendint it to the list of users

def sendNonce():
    secrets.randbelow(100)

def checkUser(user):
    #userIndex = 0
    userInDataBase = {}
    #check = False
    for u in users:
        if user == u['Username']:
            #check = True
            userInDataBase = u
            break
    return userInDataBase



while 1:
    s.listen(1)
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)
    if not data:
        continue
    #if data != b'':
        #encodeUser(data)
    else:
        decriptedData = ast.literal_eval(data.decode('utf-8'))
        try :
            request = decriptedData['Request']
            user = checkUser(decriptedData['Username'])
            if user:
                if request == 'send nonce motherfucker':
                    nonce = secrets.randbelow(100)
                    conn.send(str(nonce).encode('utf-8'))
                    hashedUser = hashlib.sha256()
                    hashedUser.update(str(nonce).encode('utf-8'))
                    hashedUser.update(user['Password'])
                    authenticationHash = hashedUser.digest()  #or hexdigest for a more condensed for
                    receivedHash = conn.recv(BUFFER_SIZE)
                                        
                    if authenticationHash == receivedHash:
                        conn.send(b'ok')
                        continue
                    else :
                        conn.send(b'Hello Trudy')
                else:
                    print('Wrong request')
                    continue
            else:
                print('User not found in the database')
                continue
        except KeyError:
            try:
                decriptedData['Hash']
            except KeyError:
                try:
                    decriptedData['Password']
                    encodeUser(data)
                
                except:
                    pass
        
        
    #print ("received data:", data)
    #print(users[0]['Username'])
    #conn.send(str(secrets.randbelow(100)).encode('utf-8'))  # echo
      
conn.close()


