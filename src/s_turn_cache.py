# -*- coding:utf-8 -*-
"""
Created on Jun 2, 2011

@author: inesmeya
"""
from loa_game import WHITE

def get_or_set_init(the_dict,key, lazy_init_value, verbose=False):
    ''' 
    '''
    class MyNone():
        pass
    
    value = the_dict.get(key, MyNone)
    isNew = False
    if value == MyNone: 
        value = lazy_init_value()
        the_dict[key] = value
        isNew  = True
    
    if verbose:
        return value, isNew
    return value

class Statistics():
    
    def __init__(self):
        self.stats= {}
    
    def add(self,isNew, name):
        x = get_or_set_init(self.stats, name,lambda: [0,0])
        x[isNew] += 1
    
    def calc_hit_rate(self,a,b):
        r = float(a) / (a + b)
        return r
    
    def hit_rate(self):
        res = {}
        total_trues, total_falses = 0,0
        for name, (falses,trues) in self.stats.items():
            res[name] = self.calc_hit_rate(falses,trues), trues, falses
            total_trues += trues
            total_falses += falses
        
        if total_trues + total_falses == 0:
            res['total'] = 'empty statistics'
        else:
            res['total'] = self.calc_hit_rate(total_falses,total_trues)
        return res
    
            
class TurnCache():
    def __init__(self):
        self.checkers_left_table = {}
        self.statistics = Statistics()
        
    def get(self,current_state, func, *agrs):
        return self.get_cached_value(current_state, func, *agrs)
    
    def get_cached_value(self, current_state, func, *agrs):
        '''
        @param current_state: state of LinesOfActionState
        @param func: LinesOfActionState -> value
        '''
        turn_info = self._get_turn_info(current_state)
        func_value, isNew = get_or_set_init(  turn_info, func.__name__, 
                                              lambda: func(current_state,*agrs),
                                              verbose=True)
        
        self.statistics.add(isNew, func.__name__)        
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
        turn_info,isNew = get_or_set_init(turn_info_table, current_state, lambda: {},verbose=True  )
        self.statistics.add(isNew, 'states')
        return turn_info
    
class NoneTurnCache():
    ''' Dummy cache'''
    
    def __init__(self):
        self.statistics = Statistics()
    
    def get(self,current_state, func,*agrs):
        return self.get_cached_value(current_state, func,*agrs)    
    
    def get_cached_value(self, current_state, func,*agrs):
        '''
        @param current_state: state of LinesOfActionState
        @param func: LinesOfActionState -> value
        '''
        return func(current_state,*agrs)
    
    def clean_up_if_need(self, game_state, next_state):
        '''Removes all states that can't be reached 
           after capture of checker
        '''
        pass