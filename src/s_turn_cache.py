# -*- coding:utf-8 -*-
"""
Created on Jun 2, 2011

@author: inesmeya
"""
from loa_game import WHITE
from s_statistics import TimeStatisticsClass

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
    
    def __str__(self):
        return  "Hit rate:" + str(self.hit_rate())
    
    def __repr__(self):
        return self.__str__()
        
    
            
class TurnCache():
    def __init__(self):
        self.checkers_left_table = {}
        self.statistics = Statistics()
        self.time_statistics = TimeStatisticsClass()
    
    def get_wkt(self,current_state, key, fuck_key, func, *args):
        '''  get with key
        Using provided key instead of function name
        @param current_state: state of LinesOfActionState
        @param func: ()->value
        @param key: function name or other id
        '''
        def action():
            # return func(args*)
            return self.time_statistics.measure_lambda(func, fuck_key, *args)
        
        turn_info = self._get_turn_info(current_state)
        if turn_info.has_key(key):
            return turn_info[key]
        
        func_value, isNew = get_or_set_init(  turn_info, key, action, verbose=True)       
        self.statistics.add(isNew, key)
        return func_value
        
        
    def get_wk(self,current_state, key, fuck_key, func, *args):
        '''  get with key
        Using provided key instead of function name
        @param current_state: state of LinesOfActionState
        @param func: ()->value
        @param key: function name or other id
        '''
        def action():
            # return func(args*)
            return self.time_statistics.measure_lambda(func, key, *args)
        
        turn_info = self._get_turn_info(current_state)
        func_value, isNew = get_or_set_init(  turn_info, key, action, verbose=True)       
        self.statistics.add(isNew, key)
        return func_value
                
        return func_value         
    def get(self,current_state, func, *args):
        return self.get_wk(current_state, func.__name__, func.__name__,   lambda: func(current_state,*args) )
        #return self.get_cached_value(current_state, func, *agrs)
    
    def get_cached_value(self, current_state, func, *agrs):
        '''
        @param current_state: state of LinesOfActionState
        @param func: LinesOfActionState -> value
        '''
        def action():
            # return func(args*)
            return self.time_statistics.measure_function(func,current_state,*agrs)
        
        turn_info = self._get_turn_info(current_state)
        func_value, isNew = get_or_set_init(  turn_info, func.__name__, 
                                              action, verbose=True)
        
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
        turn_info = get_or_set_init(turn_info_table, current_state, lambda: {})
        return turn_info

    def __str__(self):
        res =  "Stat:" + str(self.statistics) + "\n"
        res += "TimeStat:" + str(self.time_statistics) + "\n"
        return res
    
    def __repr__(self):
        return self.__str__()
    
class NoneTurnCache():
    '''cache wich does nothing'''
    
    def __init__(self):
        self.statistics = Statistics()
        self.time_statistics = TimeStatisticsClass() #??
    
    def get_wk(self,current_state, key, func, *args):
        # todo: add time measurment
        return func(*args)   
    
    def get_cached_value(self, current_state, func,*agrs):
        '''
        @param current_state: state of LinesOfActionState
        @param func: LinesOfActionState -> value
        '''
        # todo: add time measurment
        return func(current_state,*agrs)    
    
    def get(self,current_state, func,*agrs):
        return self.get_cached_value(current_state, func, *agrs)    
    
    
    def get_wkt(self,current_state, key, fuck_key, func, *args):
        return self.get_wk(current_state, key, func, *args)
    
    def clean_up_if_need(self, game_state, next_state):
        '''Removes all states that can't be reached 
           after capture of checker
        '''
        pass
    
class TurnCacheCleanable():
    def __init__(self, max_num_of_states):
        self.active_checkers_left_table = {}
        self.passive_checkers_left_table = {}
        
        self.passive_size = 0
        self.max_passive_size = max_num_of_states /2
        self.statistics = Statistics()
        self.time_statistics = TimeStatisticsClass()
    
    def swap_and_empty(self):
        del self.active_checkers_left_table
        self.active_checkers_left_table = self.passive_checkers_left_table
        self.passive_checkers_left_table = {}
        self.passive_size = 0
            
    
    def _add_to_passive(self,current_state,turn_info):
        checkers_left = (current_state.whites, current_state.blacks)
        turn_info_table = get_or_set_init(self.passive_checkers_left_table,checkers_left, lambda: {} )
        turn_info_table[current_state ] = turn_info
        self.passive_size += 1
        if self.passive_size > self.max_passive_size:
            self.swap_and_empty()
    
    def get_wkt(self,current_state, key, fuck_key, func, *args):
        '''  get with key
        Using provided key instead of function name
        @param current_state: state of LinesOfActionState
        @param func: ()->value
        @param key: function name or other id
        '''
        def action():
            # return func(args*)
            return self.time_statistics.measure_lambda(func, fuck_key, *args)
        
        turn_info = self._get_turn_info(current_state)
        if turn_info.has_key(key):
            return turn_info[key]
        
        func_value, isNew = get_or_set_init(  turn_info, key, action, verbose=True)       
        self.statistics.add(isNew, key)
        return func_value
        
        
    def get_wk(self,current_state, key, fuck_key, func, *args):
        '''  get with key
        Using provided key instead of function name
        @param current_state: state of LinesOfActionState
        @param func: ()->value
        @param key: function name or other id
        '''
        def action():
            # return func(args*)
            return self.time_statistics.measure_lambda(func, key, *args)
        
        turn_info = self._get_turn_info(current_state)
        func_value, isNew = get_or_set_init(  turn_info, key, action, verbose=True)       
        self.statistics.add(isNew, key)
        return func_value
                
    def get(self,current_state, func, *args):
        return self.get_wk(current_state, func.__name__, func.__name__,   lambda: func(current_state,*args) )
        #return self.get_cached_value(current_state, func, *agrs)
    
    def get_cached_value(self, current_state, func, *agrs):
        '''
        @param current_state: state of LinesOfActionState
        @param func: LinesOfActionState -> value
        '''
        def action():
            # return func(args*)
            return self.time_statistics.measure_function(func,current_state,*agrs)
        
        turn_info = self._get_turn_info(current_state)
        func_value, isNew = get_or_set_init(  turn_info, func.__name__, 
                                              action, verbose=True)
        
        self.statistics.add(isNew, func.__name__)
                
        return func_value 


    def _clean_up(self, d, (w,b) ):
        for (kw,kb) in d.keys():
            if kw > w or kb > b:
                del d[(kw,kb)]

    def clean_up_if_need(self, game_state, next_state):
        '''Removes all states that can't be reached 
           after capture of checker
        '''
        (w,b) = (next_state.whites, next_state.blacks)

        if (game_state.whites, next_state.whites) == (w,b):
            return
        active  = self.active_checkers_left_table
        passive = self.passive_checkers_left_table
        
        self._clean_up(active,  (w, b))
        self._clean_up(passive, (w, b))
        
            
    def _get_turn_info(self,current_state):
        checkers_left = (current_state.whites, current_state.blacks)
        turn_info_table = get_or_set_init(self.active_checkers_left_table,checkers_left, lambda: {} )
        turn_info, isNew = get_or_set_init(turn_info_table, current_state, lambda: {},verbose=True)
        if isNew:
            self._add_to_passive(current_state, turn_info)
        return turn_info

    def __str__(self):
        res =  "Stat:" + str(self.statistics) + "\n"
        res += "TimeStat:" + str(self.time_statistics) + "\n"
        return res
    
    def __repr__(self):
        return self.__str__()
    
    def destroy_cache(self):
        del self.active_checkers_left_table
        del self.passive_checkers_left_table
    
    