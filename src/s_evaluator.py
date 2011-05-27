# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""

class Evaluator():
    def evaluate(self, state, player, action =None, quad_table_ext=None):
        '''
        @param player: our player
        @param action: last action, from parent to this node
        @param quad_table_ext: aditional iterative information:
            dictionary? or struct with field for each evaluator
        Those can be None for eample at the beggining of the game
        
        @return: double between -1 and 1
        '''
        raise Exception("Not Implemented")
    
    