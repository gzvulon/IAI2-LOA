# -*- coding:utf-8 -*-
"""
Created on Jun 2, 2011

@author: inesmeya
"""

def get_or_set_init(the_dict,key, lazy_init_value):
        value = the_dict.get(key, None)
        if not value : 
            value = lazy_init_value()
            the_dict[key] = value
        return value
        
            
class TurnCache():
    def __init__(self):
        self.checkers_left_table = {}
        
    def get_cached_value(self, current_state, func):
        turn_info = self._get_turn_info(current_state)
        func_value = get_or_set_init(  turn_info,func,func)
        return func_value
            
    def _get_turn_info(self,current_state):
        checkers_left = (current_state.whites, current_state.blacks)
        turn_info_table = get_or_set_init(self.checkers_left_table,checkers_left, lambda: {} )
        turn_info = get_or_set_init(turn_info_table, current_state, lambda: {}  )
        return turn_info
    