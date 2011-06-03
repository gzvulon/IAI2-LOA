# -*- coding:utf-8 -*-
"""
Created on Jun 2, 2011

@author: inesmeya
"""
from loa_game import WHITE

def get_or_set_init(the_dict,key, lazy_init_value):
    '''
    '''
    value = the_dict.get(key, None)
    if not value : 
        value = lazy_init_value()
        the_dict[key] = value
    return value
        
            
class TurnCache():
    def __init__(self):
        self.checkers_left_table = {}
        
    def get(self,current_state, func):
        return self.get_cached_value(current_state, func)
    
    def get_cached_value(self, current_state, func):
        '''
        @param current_state: state of LinesOfActionState
        @param func: LinesOfActionState -> value
        '''
        turn_info = self._get_turn_info(current_state)
        func_value = get_or_set_init(  turn_info,func, lambda: func(current_state))
        return func_value
    
    def clean_up_if_need(self, game_state, next_state):
        '''Removes all states that can't be reached 
           after capture of checker
        '''
        (w,b) = (next_state.whites, next_state.blacks)

        if (game_state.whites, next_state.whites) == (w,b):
            return
        d = self.checkers_left_table
        
        player = game_state.getCurrentPlayer()

        if player == WHITE: # remove all (_,b+1)
            for i in range(w+1): 
                k = (i,b + 1)
                if d.has_key(k):
                    del d[k]
                    
        else: #player == BLACK: remove all (_,b+1)
            for i in range(b+1): 
                k = (w+1, i)
                if d.has_key(k):
                    del d[k]

            
    def _get_turn_info(self,current_state):
        checkers_left = (current_state.whites, current_state.blacks)
        turn_info_table = get_or_set_init(self.checkers_left_table,checkers_left, lambda: {} )
        turn_info = get_or_set_init(turn_info_table, current_state, lambda: {}  )
        return turn_info
    
class NoneTurnCache():
    ''' Dummy cache'''
    
    
    def get(self,current_state, func):
        return self.get_cached_value(current_state, func)    
    
    def get_cached_value(self, current_state, func):
        '''
        @param current_state: state of LinesOfActionState
        @param func: LinesOfActionState -> value
        '''
        return func(current_state)
    
    def clean_up_if_need(self, game_state, next_state):
        '''Removes all states that can't be reached 
           after capture of checker
        '''
        pass