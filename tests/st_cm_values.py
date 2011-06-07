# -*- coding:utf-8 -*-
"""
Created on Jun 7, 2011

@author: inesmeya
"""

import unittest
from s_quad_table import QuadTable
from loa_game import MoveAction, Direction, LinesOfActionState, SpinAction,\
    WHITE, BLACK
from s_common_ops import findQuadType, calcMoveDist
from s_eval_mass import CenterMassEvaluator
from s_weighted_evaluator import WeightedEvaluatorI
from s_enums import QUAD_TABLE_TAG

class Test(unittest.TestCase):

    def setUp(self):      
        print 
        self.board1 = ((' ', 'B'),
                       ('W', 'B'))
       
        self.board2 = (('W', 'B'),
                       ('B', 'B'))
        
        self.board3 = (('B', 'B'),
                       ('B', 'B'))
        
        self.board4 = (('B', 'W'),
                       ('W', 'B'))
        
        self.board5 = (('B', 'B', ' '),
                       ('W', 'W', 'B'),
                       (' ', 'W', 'W'))
        
        self.quadTable1 = QuadTable(self.board5, 3)
        
        self.move1 = MoveAction(3, 3, Direction("W", (0, -1)))
        self.move2 = MoveAction(2, 4, Direction("SW", (1, -1)))   
        self.move3 = MoveAction(6, 0, Direction("E", (0, 1)))
        
        self.board6 = ( (' ',' ',' ',' ',' ',' ',' ',' ',) , 
                        ('B',' ','B',' ',' ',' ',' ',' ',) , 
                        (' ','B',' ',' ','W',' ',' ',' ',) , 
                        (' ',' ',' ','W',' ','W',' ','B',) , 
                        (' ',' ','W',' ','W',' ',' ',' ',) , 
                        (' ','W',' ',' ','B',' ',' ',' ',) , 
                        (' ',' ',' ',' ',' ',' ',' ',' ',) , 
                        (' ',' ',' ',' ',' ',' ','W',' ',) )
        
        self.state3 = LinesOfActionState(8, 50, self.board6, 6, 6)
        
        self.board7 = ( (' ','W','W','W','W','W','W',' ',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        (' ','W','W','W','W','W','W',' ',) )
  
        self.quadTable3 = QuadTable(self.board7, 8)
        self.state3 = LinesOfActionState(8, 50, self.board7, 6, 6)
        
        self.board8 = ( (' ','W','W','W','W','W','W',' ',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        (' ',' ','B',' ',' ',' ',' ','B',) , 
                        (' ','W','W','W','W','W','W',' ',) )
  
        self.quadTable4 = QuadTable(self.board8, 8)
        self.move4 = MoveAction(6, 0, Direction("E", (0, 1)))
        self.state4 = LinesOfActionState(8, 50, self.board8, 6, 6)

        self.board9 = ( (' ','W',' ','W','W','W','W',' ',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('W',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        (' ',' ','B',' ',' ',' ',' ','B',) , 
                        (' ','W','W','W','W','W','W',' ',) )
  
        self.quadTable5 = QuadTable(self.board9, 8)
        self.move5 = MoveAction(0, 2, Direction("SW", (1, -1)))
        self.state5 = LinesOfActionState(8, 50, self.board9, 6, 6)

        self.board10 = (   (' ', 'W', 'W', 'W', 'W', 'W', 'W', ' '),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', 'B', 'B', ' ', ' ', ' ', ' ', 'B'),
                           (' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B'),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', 'W', 'W', 'W', 'W', 'W', 'W', ' '))
       
        self.quadTable6 = QuadTable(self.board10, 8)
        self.spin6 = SpinAction(6, 0)
        self.state6 = LinesOfActionState(8, 50, self.board10, 6, 6)
        
        self.board11 = (   (' ', 'W', 'W', 'W', 'W', 'W', 'W', ' '),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', 'B', 'B', ' ', ' ', ' ', ' ', 'B'),
                           (' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B'),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B'),
                           ('W', ' ', 'W', 'W', 'W', 'W', 'W', ' '))
       
        self.quadTable7 = QuadTable(self.board11, 8)
        self.spin7 = SpinAction(3, 1)
        self.state7 = LinesOfActionState(8, 50, self.board11, 6, 6)

        self.board12 = (   (' ', 'W', 'W', 'W', 'W', 'W', 'W', ' '),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B'),
                           (' ', 'B', 'B', ' ', ' ', ' ', ' ', 'B'),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B'),
                           ('W', ' ', 'W', 'W', 'W', 'W', 'W', ' '))
       
        self.quadTable8 = QuadTable(self.board12, 8)
        self.state8 = LinesOfActionState(8, 50, self.board12, 6, 6)
    
    def tearDown(self):
        pass
    
    def test_cm(self):
        
        states = [self.__dict__["state" + str(i)] for i in range(3,9) ]
        ev = WeightedEvaluatorI(0.55, 0.3, 0.7, 0.25)
        
        
        
        for state in states:
            print state
            qt = QuadTable(state.board, state.size, initialize=True)
            w = ev.evaluate(state, WHITE,{QUAD_TABLE_TAG:qt})
            b = ev.evaluate(state, BLACK,{QUAD_TABLE_TAG:qt})  
            
            print "w=",w
            print "b=",b

        
        
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()