# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""
from game_agent import GameAgent
from s_alpha_beta import AlphaBetaSearch
from s_heuristics import simple_heuristic

class AlphaBetaAgent(GameAgent):
    def move(self, game_state):
        return self.alphaBeta.search(game_state)
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.player = player
        u = lambda state: simple_heuristic(player)
        self.alphaBeta = AlphaBetaSearch(self.player, 3, u)