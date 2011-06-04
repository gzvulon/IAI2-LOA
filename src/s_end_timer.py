# -*- coding:utf-8 -*-
"""
Created on Jun 3, 2011

@author: inesmeya
"""
import time

def checkTime(end_time, safe_delta=0):
    '''raises exception on timeout type: TimeOutException'''
    if(end_time - safe_delta < time.clock()):
        raise TimeOutException()
    
class TimeOutException(Exception):
    pass


class EndTimerClass():
    def set(self,end_time):
        self.end_time = end_time
    
    def check(self,safe_delta=0):
        checkTime(self.end_time,safe_delta)
        
EndTimer = EndTimerClass()



    