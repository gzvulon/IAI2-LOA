# -*- coding:utf-8 -*-
"""
Created on May 27, 2011

@author: inesmeya
"""
import st_import 

from s_agents import  DummyAgent, RandomAgent
from loa_game import WHITE, BLACK, LinesOfActionState
from game_runner import GameRunner
from alpha_beta import INFINITY
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams
from s_statistics import GTimeStatistics
from s_end_timer import EndTimer


agents = {}
a1 = AnytimeSmartAlphaBetaPrintAgentParams()
a1.myinit(caching=True,depth_delta=1)
a2 = AnytimeSmartAlphaBetaPrintAgentParams()
a2.myinit(caching=False,depth_delta=1)

ar = RandomAgent()
agents[ WHITE ] = a2
agents[ BLACK ] = a1

state = LinesOfActionState(8, 50)

try:
    winner = GameRunner(state, agents, 5.5 , 1).run()
    print 'Winner:', winner
except Exception as e:
    print e
    
    


hit_rate1 = a1.alphaBeta.turn_cache.statistics.hit_rate()
times_stat = a1.alphaBeta.turn_cache.time_statistics

print "a1", hit_rate1
print "cache time stat", times_stat
print "time stat:", GTimeStatistics
print EndTimer
