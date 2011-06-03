# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""

class Evaluator():
    def evaluate(self, state, player, end_time,action =None, info_set=None):
        '''
        @param player: our player
        @param action: last action, from parent to this node
        @param quad_table_ext: aditional iterative information:
            dictionary? or struct with field for each evaluator
        Those can be  None for eample at the beggining of the game
        
        @return: double between -1 and 1
        '''
        raise Exception("Not Implemented")


class UpdatableTable():    
    def update(self,state, action, new_state):
        ''' state + action => new_state
        @param action:  
        
        '''
    # def __init__(self,state)
    
        
    
    