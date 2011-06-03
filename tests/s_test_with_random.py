# -*- coding:utf-8 -*-
"""
Created on May 27, 2011

@author: inesmeya
"""
from s_agents import  DummyAgent, RandomAgent
from loa_game import WHITE, BLACK, LinesOfActionState
from game_runner import GameRunner
from alpha_beta import INFINITY
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams


agents = {}
a1 = AnytimeSmartAlphaBetaPrintAgentParams()
a1.myinit(caching=True,depth_delta=1)
a2 = AnytimeSmartAlphaBetaPrintAgentParams()
a2.myinit(caching=False,depth_delta=1)

ar = RandomAgent()
agents[ WHITE ] = a2
agents[ BLACK ] = a1

state = LinesOfActionState(8, 50)

winner = GameRunner(state, agents, 6.0 , 1).run()
print 'Winner:', winner


hit_rate1 = a1.alphaBeta.turn_cache.statistics.hit_rate()


print "a1",hit_rate1
