'''
Created on 5/10/2011

@author: andrew
'''
import time

class Session(object):
    def __init__(self, interface):
        self.interface = interface
        self.begintime = time.time()