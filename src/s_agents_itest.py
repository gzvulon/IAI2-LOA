# -*- coding:utf-8 -*-
"""
Created on May 27, 2011

@author: inesmeya
"""
from game_agent import GameAgent
from s_alpha_beta import AlphaBetaSearch, SmartAlphaBetaSearch,\
    AnyTimeSmartAlphaBeta
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
        action =  self.alphaBeta.search(game_state)
        return action
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.evaluator = CenterMassEvaluator()
        self.player = player
        self.alphaBeta = AlphaBetaSearch(self.player, 3, self.h)
        
 
class SmartAlphaBetaPrintAgent(GameAgent):

    def h(self,state,info_dict):
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
        action = self.alphaBeta.search(game_state,3)
        return action
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.evaluator = CenterMassEvaluator()
        self.player = player
        self.alphaBeta = SmartAlphaBetaSearch(self.player, 3, self.h)

# current
class AnytimeSmartAlphaBetaPrintAgent(GameAgent):

    
    def h(self,state,info_dict):
        r = winner_heuristics(state, self.player)
        if r == 0:
            r = self.evaluator.evaluate(state, self.player)
        return r
    
    def info_print(self,game_state):
        print "The heuristics of gaim state"
        print game_state
        r1,r2 = self.evaluator.evaluate2(game_state, self.player)
        r = r1 + r2
        print "r=", r, "    their:",r1, "    fix:",r2      

    
    def move(self, game_state):
      
        action, next_state = self.alphaBeta.search(game_state,3,self.turn_time_limit)
        return action
    
        #game_state.getS()[action]
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.evaluator = CenterMassEvaluator()
        self.player = player
        self.turn_time_limit = turn_time_limit
        
        self.alphaBeta = AnyTimeSmartAlphaBeta(self.player, 3, self.h, caching=True)
        
        
        
        
        
        
        
        
        