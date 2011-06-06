# -*- coding:utf-8 -*-
"""
Created on Jun 4, 2011

@author: inesmeya
"""
import time
import inspect
INFINITY = 1.0e400

class TimeStatisticsNone():
    
    def start_measure(self, f, name):
        pass
        
    def stop_measure(self):
        pass
    
    def restart_measure(self, name):
        pass
    
    def measure_lambda(self,f,name, *args):
        return f(*args)
    
    def measure_function(self,f,*args):
        return self.measure_lambda(f, f.__name__, *args)
    
class MeasureUnit():
    def __init__(self):
        self.times = 0
        self.average = 0.0
        self.min = +INFINITY
        self.max = -INFINITY
    
    def add_measurment(self, measurment):
        new_average =  (self.average * self.times + measurment) / (self.times + 1)
        self.average = new_average
        self.times += 1
        self.min = min(self.min,measurment)
        self.max = max(self.max,measurment)
        
    def start_measure(self):
        self.start = time.clock()

    def stop_measure(self):
        running_time = time.clock() - self.start    
        self.add_measurment(running_time)
        
    def __str__(self):
        return "avg={0}, max={1}, min={2}, times={3}\n".format(
            self.average, self.max, self.min, self.times)
    
    def __repr__(self):
        return self.__str__()

class TimeStatisticsClass():
    
    def __init__(self):
        self.stats = {}

    def start_measure(self, name):
        self.stats.setdefault(name,MeasureUnit()).start_measure()

    def stop_measure(self,name):
        self.stats[name].stop_measure()
        
#    def restart_measure(self, name):
#        ''' stops previous measurements and starts new '''
#        self.stop_measure()
#        self.start_measure(name)
    
    def measure_lambda(self,f,name, *args):
        self.start_measure(name)
        retval = f(*args)
        self.stop_measure(name)
        return retval
    
    def measure_function(self,f,*args):
        return self.measure_lambda(f, f.__name__, *args)
    
    def __str__(self):
        return str(self.stats)
    
    def __repr__(self):
        return self.__str__()


class NodeStatisticsClass():
        
GTimeStatistics = TimeStatisticsClass()    
    