# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""
from s_evaluator import Evaluator
from loa_game import LinesOfActionState, WHITE, BLACK, EMPTY

class CenterMassEvaluator(Evaluator):
    
    def board_to_coord_repr(self,state):
        ''' Converts board matrix to two lists with checkers coordinates
        @param state.board: (row1,row2,...,rowN)
                      rowX = (EMPTY,WHITE,BLACK,..,<CELL_N>)
        @param state.size:  board width (== height)
        @return: {WHITE : white_coord_list, BLACK :black_coord_list}
                  X_coord_list = [(x,y),(x,y),...]
                  (x,y) = coordinates of checker
        '''
        res = {WHITE : [], BLACK : []}
        y = 0
        for row in state.board:
            x = 0
            for cell in row:
                if cell != EMPTY:
                    res[cell].append((x,y))
                x += 1
            y+=1
        
                    
                
    
    def center_of_mass_from_coord_list(self,board,size):
        '''
        @param board: [row1,row2,...,rowN]
                      rowX = (EMPTY,WHITE,BLACK,..,<CELL_N>)
        @param size:  board width (== height)
        @return: 
        '''
        
        
    
    def evaluate(self, state, action =None, quad_table_ext=None):
        '''
        @type state: loa_game.LinesOfActionState
        '''
        # calculate center of mass
        s = LinesOfActionState()
        s.blacks

    