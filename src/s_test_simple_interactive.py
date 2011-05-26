# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""
from s_agents import AlphaBetaAgent
from s_agents import InteractiveAgent
from loa_game import WHITE, BLACK, LinesOfActionState
from game_runner import GameRunner
from alpha_beta import INFINITY


agents = {}
agents[WHITE] = AlphaBetaAgent()
agents[BLACK] = InteractiveAgent()

state = LinesOfActionState(6, 50)

winner = GameRunner(state, agents, INFINITY, 1).run()
print 'Winner:', winner
