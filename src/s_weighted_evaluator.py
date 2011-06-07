# -*- coding:utf-8 -*-
"""
Created on Jun 7, 2011

@author: inesmeya
"""
from s_eval_mass import CenterMassEvaluator
from s_enums import QUAD_TABLE_TAG
from s_common_ops import other_player
from s_quad_evaluator import QuadEvaluator

class WeightedEvaluatorH():
    def __init__(self, wanted_mass, weight_before, weight_after, weight_enemy):
        '''
        @param weight_before: weight of euler
        '''
        self.wanted_mass = wanted_mass # center of mass, 
        #after this value we put weight_after on number of connected components
        self.weight_before = weight_before
        self.weight_after  = weight_after
        self.weight_enemy  = weight_enemy
        self.cm_eval = CenterMassEvaluator()
        self.quad_eval = QuadEvaluator()
    
    def evaluate(self, state, my_player, info_set):
        enemy = other_player(my_player)
        
        com_mine = self.cm_eval.evaluate(state, my_player, info_set)
        com_his = self.cm_eval.evaluate(state,enemy , info_set)
        
        euler_mine =  self.quad_eval.evaluate(state, my_player, info_set)
        euler_his = self.quad_eval.evaluate(state, enemy, info_set)
        
        if com_mine < self.wanted_mass:
            weight = self.weight_before
        else: 
            weight = self.weight_after
        
        h_mine = (1 - weight) * com_mine + weight * euler_mine
        h_his =  (1 - weight) * com_his + weight * euler_his
        h = (1 - self.weight_enemy) * h_mine + self.weight_enemy * h_his
        return h 


def apply_weight(w,first, second):
    return w * first + (1-w)*second

class WeightedEvaluatorI():
    def __init__(self, wanted_mass, weight_before, weight_after, weight_enemy):
        '''
        @param weight_before: weight of euler
        '''
        self.wanted_mass = wanted_mass # center of mass, 
        #after this value we put weight_after on number of connected components
        self.weight_before = weight_before
        self.weight_after  = weight_after
        self.weight_enemy  = weight_enemy
        self.cm_eval = CenterMassEvaluator()
        self.quad_eval = QuadEvaluator()
    
    def evaluate(self, state, my_player, info_set):
        enemy = other_player(my_player)
        
        com_mine = self.cm_eval.evaluate(state, my_player, info_set)
        com_his = self.cm_eval.evaluate(state,enemy , info_set)
        
        euler_mine =  self.quad_eval.evaluate(state, my_player, info_set)
        euler_his = self.quad_eval.evaluate(state, enemy, info_set)
        
        if com_mine < self.wanted_mass:
            weight = self.weight_before
        else: 
            weight = self.weight_after
        
        h_mine = apply_weight(weight,euler_mine, com_mine)
        h_his =  apply_weight(weight,1-euler_his, com_his)
        
        h = (1 - self.weight_enemy) * h_mine - self.weight_enemy * h_his
        return h 