# -*- coding:utf-8 -*-
"""
Created on May 27, 2011

@author: inesmeya
"""
from s_agents import  DummyAgent
from loa_game import WHITE, BLACK, LinesOfActionState
from game_runner import GameRunner
from alpha_beta import INFINITY
from s_agents_itest import AlphaBetaPrintAgent


    
agents = {}
agents[WHITE] = AlphaBetaPrintAgent()
agents[ BLACK ] = DummyAgent()

state = LinesOfActionState(6, 50)

winner = GameRunner(state, agents, INFINITY, 1).run()
print 'Winner:', winner    