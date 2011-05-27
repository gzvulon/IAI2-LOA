# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""
from s_eval_mass import CenterMassEvaluator



def winner_heuristics(state,player):
        winner = state.getWinner()
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1

def make_simple_heuristic(player):
    '''
    @param player: player 

    @return: heuristics functions for provided player
    @type return: fn: state -> double in range [-1.0;1.0]
    '''
    def the_heuristic(state):
        return winner_heuristics(player,state)

    return the_heuristic    