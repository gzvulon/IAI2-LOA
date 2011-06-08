# -*- coding:utf-8 -*-
"""
Created on Jun 8, 2011

@author: inesmeya
"""
from s_end_timer import EndTimer
from s_statistics import GTimeStatistics

def print_results(agent):
    print "== Node statistics =="
    print agent.node_statistics
    print"== turn_cache =="
    print "a3", agent.turn_cache
    #print "cache time stat", times_stat
    print "time stat:", GTimeStatistics
    print EndTimer
    