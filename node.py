# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 17:48:00 2018

@author: Leonardo
"""
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser



class Node:
        
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
    pass


host = Node()
print(host.description())
