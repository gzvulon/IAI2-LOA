# -*- coding:utf-8 -*-
"""
Created on Jun 3, 2011

@author: inesmeya
"""
import time
import inspect

def whosdaddy():
    return inspect.stack()[2][3]

def checkTime(end_time, safe_delta=0):
    '''raises exception on timeout type: TimeOutException'''
    if(end_time - safe_delta < time.clock()):
        raise TimeOutException()
    
class TimeOutException(Exception):
    pass


class EndTimerClass():
    def __init__(self):
        self.end_time = None
        
        self.last_name =("noname",-1)
        self.prev_name =("noname",-1)
    
    def set(self,end_time):
        self.end_time = end_time
    
    def check(self,safe_delta=0, name="not set"):
        if self.end_time == None: return
        self.save_name( name)
        checkTime(self.end_time,safe_delta)
    
    def save_name(self,name):
        self.prev_name = self.last_name
        self.last_name = (name, self.end_time - time.clock())

    def __str__(self):
        return str((self.prev_name,self.last_name))
    
    def __repr__(self):
        return self.__str__()        
        
#EndTimer = EndTimerClassExt() 
EndTimer = EndTimerClass()



    