# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""
from s_evaluator import Evaluator
from loa_game import LinesOfActionState

class CenterMassEvaluator(Evaluator):
    
    
    
      def evaluate(self, state, action =None, quad_table_ext=None):
        '''
        @type state: loa_game.LinesOfActionState
        '''
        # calculate center of mass
        s = LinesOfActionState()
        s.blacks

    