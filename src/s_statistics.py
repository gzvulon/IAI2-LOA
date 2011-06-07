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
    

class MeasureUnitBase():
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
        

    def __str__(self):
        return "avg={%s}, max={%s}, min={%s}, times={%s}\n" % \
            (self.average, self.max, self.min, self.times)
    
    def __repr__(self):
        return self.__str__()


class MeasureUnit():
    def __init__(self):
        MeasureUnitBase.__init__(self)

    def start_measure(self):
        self.start = time.clock()

    def stop_measure(self):
        running_time = time.clock() - self.start    
        self.add_measurment(running_time)
        
        

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
    pass
        
GTimeStatistics = TimeStatisticsClass()






# ============================ Visiting statistics ============================


class DepthUnit():
    def __init__(self,maxdepth):
        self.maxdepth = maxdepth
        self.count = 0
        self.mesureunit = MeasureUnit()
        self.nodes = MeasureUnitBase()
    
    def start(self):
        self.mesureunit.start_measure()
                
    def add_one(self):
        self.count += 1
    
    def finish(self):
        self.mesureunit.stop_measure()
        self.nodes.add_measurment(self.count)
        
    def __str__(self):
        return "Times:" + str(self.mesureunit) + "\n" + \
               "Nodes:" + str(self.nodes)

        
class DepthList():
    
    def __init__(self,tag):
        self.__init__([])
        self.depths = {}
        self.tag = tag

    def add(self,maxdepth):
        depth_unit = self.depths.setdefault(maxdepth,DepthUnit(maxdepth))
        depth_unit.start()
        self.last = depth_unit
        
    def inc_last(self):
        self.last.add_one()
    
    def stop(self):
        self.finish_last()
        
    def get_statistics(self):
        str = self.tag + " Stats :\n"
        for depth, unit in sorted(self.depths.items()):
            str += "d:" + str(depth) + ". S=" + str(unit)
        return str
    
    def __str__(self):
        return self.get_statistics()
        
    def __repr__(self):
        return self.__str__()


class VisitsStatistics():
    
    def __init__(self):
        self.stats = {}
        
    def start_monitor(self,tag , maxdepth):
        self.stats.setdefault(tag,DepthList(tag)).add(maxdepth)
        pass
    
    def visit_node(self, tag):
        self.stats[tag].inc_last()
        
    def stop_monitor(self, tag, maxdepth):
        self.stats[tag].stop()
        
    def get_statistics(self):
        str = " VisitsStatistics :\n"
        for tag, dl in self.stats.items():
            str += "d:" + str(tag) + ". DepthList=" + str(dl)
        return str
    
    def __str__(self):
        return self.get_statistics()
        
    def __repr__(self):
        return self.__str__()        
