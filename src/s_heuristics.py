# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""

def simple_heuristic(player):
    '''
    @param player: player 

    @return: heuristics functions for provided player
    @type return: fn: state -> double in range [-1;1]
    '''
    def the_heuristic(state):
        winner = state.getWinner()
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1
    
    return the_heuristic