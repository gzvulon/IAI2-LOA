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
    

class MeasureUnitBase(object):
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


class MeasureUnit(MeasureUnitBase):
    def __init__(self):
        super(MeasureUnit,self).__init__()

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
        self.depths = {}
        self.tag = tag

    def add(self,maxdepth):
        depth_unit = self.depths.setdefault(maxdepth,DepthUnit(maxdepth))
        depth_unit.start()
        self.last = depth_unit
        self.last_depth = maxdepth
        
    def inc_last(self):
        self.last.add_one()
    
    def stop(self):
        self.last.finish()
        
    def get_statistics(self):
        s = self.tag + " Stats :\n"
        for depth, unit in sorted(self.depths.items()):
            s += "Max depth:" + str(depth) + ".Stats:" + str(unit)
        return s
    
    def clear_last(self):
        del self.depths[self.last_depth]
    
    def __str__(self):
        return self.get_statistics()
        
    def __repr__(self):
        return self.__str__()


class VisitsStatisticsClass():
    
    def __init__(self,tag=None):
        self.stats = {}
        self.tag = tag
        
    def _getTag(self,tag):
        DEFAULT_TAG = "default"
        if not tag is None:
            return tag
        elif not self.tag is None:
            return self.tag
        return DEFAULT_TAG
    
    def start_monitor(self, maxdepth, tag=None):
        the_tag = self._getTag(tag)
        self.stats.setdefault(the_tag,DepthList(the_tag)).add(maxdepth)
        pass
    
    def visit_node(self, tag=None):
        the_tag = self._getTag(tag)
        self.stats[the_tag].inc_last()
        
    def stop_monitor(self, maxdepth, tag=None):
        the_tag = self._getTag(tag)
        self.stats[the_tag].stop()
        
    def get_statistics(self):
        s = " VisitsStatistics :\n"
        for tag, dl in self.stats.items():
            s += "d:" + str(tag) + ". DepthList=" + str(dl)
        return s
    
    def clear_monitor(self,tag=None):
        the_tag = self._getTag(tag)
        self.stats[the_tag].clear_last()
    
    def __str__(self):
        return self.get_statistics()
        
    def __repr__(self):
        return self.__str__()        
