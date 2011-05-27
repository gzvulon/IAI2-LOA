# -*- coding:utf-8 -*-
"""
Created on May 27, 2011

@author: inesmeya
"""
from game_agent import GameAgent
from s_alpha_beta import AlphaBetaSearch
from s_heuristics import winner_heuristics
from s_eval_mass import CenterMassEvaluator

class AlphaBetaPrintAgent(GameAgent):

    def h(self,state):
        r = winner_heuristics(state, self.player)
        if r == 0:
            r = self.evaluator.evaluate(state, self.player)
        return r
    
    def move(self, game_state):
        print "The heuristics of gaim state"
        print game_state
        r1,r2 = self.evaluator.evaluate2(game_state, self.player)
        r = r1 + r2
        print "r=", r, "    their:",r1, "    fix:",r2        
        return self.alphaBeta.search(game_state)
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.evaluator = CenterMassEvaluator()
        self.player = player
        self.alphaBeta = AlphaBetaSearch(self.player, 3, self.h)
        
        