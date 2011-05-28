# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: szvulon
"""
from game_agent import GameAgent
from s_alpha_beta import AlphaBetaSearch
from loa_game import SpinAction, Direction, DIRECTIONS, MoveAction
from s_heuristics import make_simple_heuristic

class AlphaBetaAgent(GameAgent):
    def move(self, game_state):
        return self.alphaBeta.search(game_state)
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.player = player
        h = make_simple_heuristic(player)
        self.alphaBeta = AlphaBetaSearch(self.player, 3, h)
        
class InteractiveAgent(GameAgent):
    class StopGameException(Exception):
        pass
    
    def move(self, game_state):
        res_action = None
        # ask and parse user move until its legal or stop
        while res_action not in game_state.getSuccessors().keys():
            if res_action != None:
                print "Invalid move"
            try:
                res_action = self.the_move(game_state)
            except ValueError:
                print "Incorrect input"
        return res_action
    
    def the_move(self, game_state):
        print game_state
        inp = raw_input(self.player + ' turn. Enter <row col action> (action is N/NE/E/SE/S/SW/W/NW/SPIN): or STOP\n')
        # option to exit
        if inp.find("STOP") > -1:
            raise self.StopGameException("User stopped the game")
        
        row, col, action = inp.split()
        row = int(row)
        col = int(col)
        action = action.upper()
        res  = []
        if(action == 'SPIN'):
            res  = SpinAction(row, col)
        else:
            direction_idx = DIRECTIONS.index(Direction(action, (0, 0))) #@UndefinedVariable
            res  = MoveAction(row, col, DIRECTIONS[direction_idx])
        return res 
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.player = player

class DummyAgent(GameAgent):
    def move(self, game_state):
        for action in game_state.getSuccessors().keys():
            return action
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        return
    

class SmartAlphaBetaAgent(GameAgent):
    def move(self, game_state):
        return self.alphaBeta.search(game_state)
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.player = player
        h = make_simple_heuristic(player)
        self.alphaBeta = AlphaBetaSearch(self.player, 3, h)
