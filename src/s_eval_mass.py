# -*- coding:utf-8 -*-
"""
Created on May 26, 2011

@author: inesmeya
"""
from s_evaluator import Evaluator, UpdatableTable
from loa_game import WHITE, BLACK, EMPTY
import sys
from s_end_timer import EndTimer
from s_statistics import TimeStatisticsClass, GTimeStatistics


def initialize(board):
        # {WHITE : [(x,y),(x1,y1),...], BLACK : [(x,y),(x1,y1),...]}
        EndTimer.check(name="cm_a")
        coord_repr = state_to_coord_repr(board)
        # central of mass dict {WHITE : (x,y) , BLACK : [(x,y),(x1,y1),...]}
        cm_dict ={}
        EndTimer.check(name="cm_b")
        cm_dict[WHITE] = center_of_mass_from_coord_list(coord_repr[WHITE])
        EndTimer.check(name="cm_c")
        cm_dict[BLACK] = center_of_mass_from_coord_list(coord_repr[BLACK])
        res = CenterMassTable(coord_repr,cm_dict)
        return res

def state_to_coord_repr(board):
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
    for row in board:
        x = 0
        for cell in row:
            if cell != EMPTY:
                res[cell].append((x,y))
            x += 1
        y+=1
    return res

def center_of_mass_from_coord_list(coord_list):
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

class CenterMassTable(UpdatableTable):
    
    def update(self,state, action, new_state):
        ''' state + action => new_state
        @param action:  
        '''
        raise NotImplementedError()
    
    def __init__(self,coord_repr,cm_dict):
        self.coord_repr = coord_repr
        self.cm_dict = cm_dict
        

class CenterMassEvaluator(Evaluator):
    
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
        
        EndTimer.check(name="cm_d")
        dsum = sum(dists)
        dmin = min(dists)
        
        EndTimer.check(name="cm_e")
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
        
        cmt = initialize(state.board)
        cmt.coord_repr
        EndTimer.check(name="cm_f")
        
        my_coord_list = cmt.coord_repr[player]
        cm = cmt.cm_dict[player]
        
        EndTimer.check(name="cm_g")
        
        GTimeStatistics.start_measure("sum_of_min_distances_ext2")
        rsmd = self.sum_of_min_distances_ext2(cm,my_coord_list)
        GTimeStatistics.stop_measure("sum_of_min_distances_ext2")
        
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
        #TODO: no end_time

    