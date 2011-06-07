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
from s_statistics import GTimeStatistics
from s_end_timer import EndTimer
from s_enums import ITERATIVE, NON_ITERATIVE

from s_weighted_evaluator import WeightedEvaluatorI
from s_eval_mass import CenterMassEvaluator
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams


agents = {}
a1 = AnytimeSmartAlphaBetaPrintAgentParams()
a1_params = {
  'caching':True,
  'init_max_depth': 4,
  'depth_delta':2,
  'use_iterative' : ITERATIVE,
  'evaluator' :  WeightedEvaluatorI(0.55, 0.3, 0.7, 0.25)       
}

a2 = AnytimeSmartAlphaBetaPrintAgentParams()
a2_params = {
  'caching':False,
  'init_max_depth': 3,
  'depth_delta':1,
  'use_iterative' : NON_ITERATIVE,
  'evaluator' : CenterMassEvaluator() 
            
}

a1.myinit(**a1_params)
a2.myinit(**a2_params)


ar = RandomAgent()
agents[ WHITE ] = ar
agents[ BLACK ] = a1

state = LinesOfActionState(6, 40)

try:
    winner = GameRunner(state, agents, 20.5 , 1).run()
    print 'Winner:', winner

except Exception, e:
    print e
    raise
finally:    
    print "a1", a1.turn_cache
    #print "cache time stat", times_stat
    print "time stat:", GTimeStatistics
    print EndTimer
