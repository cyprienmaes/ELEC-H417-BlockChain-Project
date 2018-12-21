# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 15:51:19 2018

@author: Leonardo
"""

import time
import threading 
        
class timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sec = 0
        
    def run(self):
        while True:
            """
            print(self.sec) """
            time.sleep(1)
            self.sec += 1
        
    def getTime(self):
        return self.sec
    
    def setTime(self, clock):
        self.sec = clock