# -*- coding:utf-8 -*-
"""
Created on May 27, 2011

@author: inesmeya
"""
from s_agents import  DummyAgent, RandomAgent
from loa_game import WHITE, BLACK, LinesOfActionState
from game_runner import GameRunner
from alpha_beta import INFINITY
from s_agents_itest import AlphaBetaPrintAgent, SmartAlphaBetaPrintAgent,\
    AnytimeSmartAlphaBetaPrintAgent


    
agents = {}
agents[ WHITE ] = AnytimeSmartAlphaBetaPrintAgent()
agents[ BLACK ] = RandomAgent()

state = LinesOfActionState(6, 50)

winner = GameRunner(state, agents, 1.0 , 1).run()
print 'Winner:', winner    