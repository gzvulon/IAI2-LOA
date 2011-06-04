# -*- coding:utf-8 -*-
"""
Created on Jun 4, 2011

@author: inesmeya
"""
import time
from s_alpha_beta import INFINITY

class TimeStatisticsNone():
    
    def start_measure(self, f, name):
        pass
        
    def stop_measure(self):
        pass
            

class MeasureUnit():
    def __init__(self):
        self.times = 0
        self.average = 0.0
        self.min = +INFINITY
        self.max = -INFINITY
    
    def add_measurment(self, measurment):
        new_average =  (self.average * self.times + measurment) / (self.times + 1)
        self.average = new_average 
        

class TimeStatistics():
    
    def __init__(self):
        self.stats = {}
        self.stats.setdefault(MeasureUnit())
    
    def start_measure(self, name):
        self.name = name
        self.start = time.clock()

        
    def stop_measure(self):
        running_time = time.clock() - self.start
        self.stats[self.name] = running_time
        
        
        pass
    