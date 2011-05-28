# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""
from s_evaluator import Evaluator
from loa_game import WHITE, BLACK, EMPTY
import sys

class CenterMassEvaluator(Evaluator):
    
    def state_to_coord_repr(self,state):
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
        return res
        
    
    def center_of_mass_from_coord_list(self,coord_list):
        ''' calculate center of mass from coord_list
        @param coord_list: [(x,y),(x,y),...]
                  (x,y) = coordinates of checker
        @return: (x,y) of center mass
        '''
        X,Y = 0,0
        n = len(coord_list)
        for (x,y) in coord_list:
            X += x
            Y += y
        cx,cy = X/n,Y/n
        return (cx,cy)
        
    
    def distance(self,(x1,y1),(x2,y2)):
        h = abs(y1-y2)
        w = abs(x1-x2)
        res = max(h,w)
        return res 
        
    def sum_of_distances_ext(self,cm,coord_list):
        ''' Calculates sum_of distances - sum of minimal distances
        @param cm:  (cx,cy) - center of mass
        @param coord_list: [(x,y),...] - list of coordinates
        @return: sum of distances ext,sum of distances, sum of minimal distances
        '''
        dsum = 0
        dmin = sys.maxint
        min_count = 1 
        for p in coord_list: 
            d = self.distance(p,cm)
            dsum += d
            if d < dmin:
                dmin = d
                min_count = 1
            else:
                min_count+=1
        dmin_sum = dmin*min_count
        res = dsum - dmin_sum  
        return res, dsum, dmin_sum    
            
    
    def sum_of_min_distances_ext2(self,cm,coord_list):
        dists = map(lambda p: self.distance(cm,p), coord_list)
        dsum = sum(dists)
        dmin = min(dists)
        dmin_count = dists.count(dmin)
        dmin_sum = dmin * dmin_count
        smart_sum = dsum - dmin_sum
        smart_sum_count = len(coord_list) - dmin_count
        return smart_sum, smart_sum_count, dsum, dmin_sum, dmin, dmin_count
        
    
    def min_sum_fix(self,dmin, nmin, n):
        ''' fixes '''
        if dmin == 0:return 0.0
        res = 0.5*(1.0 / dmin)*(float(nmin)/n)
        return res 
            
            
    def min_sum_res(self,smart_sum_count,smart_sum):
        if smart_sum_count == 0: 
            res = 0.5
        else:  
            average = float(smart_sum) / smart_sum_count
            res = 1.0 / average
        return res
    
    def evaluate2(self, state, player, action =None, quad_table_ext=None):
        '''
        @type state: loa_game.LinesOfActionState
        '''
        coord_repr = self.state_to_coord_repr(state)
        
        my_coord_list = coord_repr[player]
        cm = self.center_of_mass_from_coord_list(my_coord_list)
        rsmd = self.sum_of_min_distances_ext2(cm,my_coord_list)
        smart_sum, smart_sum_count, dsum, dmin_sum, dmin, dmin_count = rsmd
        r1 = self.min_sum_res(smart_sum_count, smart_sum)
        r2 = self.min_sum_fix(dmin, dmin_count, len(my_coord_list))
        return r1, r2
        
    def evaluate(self, state, player, action =None, quad_table_ext=None):
        '''
        @type state: loa_game.LinesOfActionState
        '''
        r1, r2 = self.evaluate2(state, player, action, quad_table_ext)
        return r1 + r2
          
        

        
        
        
        
        
        # calculate center of mass
        

    