'''
Created on May 27, 2011

@author: shizki
'''
import unittest
from s_quad_table import QuadTable, findQuadType, calcMoveDist
from loa_game import MoveAction, Direction


class Test(unittest.TestCase):

    def setUp(self):       
        self.board1 = ((' ', 'B'),('W', 'B'))
        self.board2 = (('W', 'B'),('B', 'B'))
        self.board3 = (('B', 'B'),('B', 'B'))
        self.board4 = (('B', 'W'),('W', 'B'))
        
        self.board5 = (('B', 'B', ' '),('W', 'W', 'B'),(' ', 'W', 'W'))
        self.quadTable1 = QuadTable(self.board5, 3)
        
        self.board6 = ( (' ',' ',' ',' ',' ',' ',' ',' ',) , 
                        ('B',' ','B',' ',' ',' ',' ',' ',) , 
                        (' ','B',' ',' ','W',' ',' ',' ',) , 
                        (' ',' ',' ','W',' ','W',' ','B',) , 
                        (' ',' ','W',' ','W',' ',' ',' ',) , 
                        (' ','W',' ',' ','B',' ',' ',' ',) , 
                        (' ',' ',' ',' ',' ',' ',' ',' ',) , 
                        (' ',' ',' ',' ',' ',' ','W',' ',) )
        
        self.quadTable2 = QuadTable(self.board6, 8)

        self.board7 = ( (' ','W','W','W','W','W','W',' ',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        (' ','W','W','W','W','W','W',' ',) )
  
        self.quadTable3 = QuadTable(self.board7, 8)
        
        self.board8 = ( (' ','W','W','W','W','W','W',' ',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        (' ',' ','B',' ',' ',' ',' ','B',) , 
                        (' ','W','W','W','W','W','W',' ',) )
  
        self.quadTable4 = QuadTable(self.board7, 8)

        self.board9 = ( (' ','W','W',' ','W','W','W',' ',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B','W',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        ('B',' ',' ',' ',' ',' ',' ','B',) , 
                        (' ',' ','B',' ',' ',' ',' ','B',) , 
                        (' ','W','W','W','W','W','W',' ',) )
  
        self.quadTable5 = QuadTable(self.board7, 8)

        self.board10 = (   (' ', 'W', 'W', 'W', 'W', 'W', 'W', ' '),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', 'B', 'B', ' ', ' ', ' ', ' ', 'B'),
                           (' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B'),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           ('B', ' ', ' ', ' ', ' ', ' ', ' ', 'B'),
                           (' ', 'W', 'W', 'W', 'W', 'W', 'W', ' '))
       
        self.quadTable6 = QuadTable(self.board10, 8)

       
    def tearDown(self):
        pass


    def testFindQuadType(self):
        self.assertEqual('Q1', findQuadType(0, 0, self.board1, 2, 'W'))
        self.assertEqual('Q2', findQuadType(0, 0, self.board1, 2, 'B'))
        self.assertEqual('Q1', findQuadType(0, 0, self.board2, 2, 'W'))
        self.assertEqual('Q3', findQuadType(0, 0, self.board2, 2, 'B'))
        self.assertEqual('Q0', findQuadType(0, 0, self.board3, 2, 'W'))
        self.assertEqual('Q4', findQuadType(0, 0, self.board3, 2, 'B'))
        self.assertEqual('Q1', findQuadType(-1, -1, self.board3, 2, 'B'))
        self.assertEqual('Q1', findQuadType(1, 1, self.board3, 2, 'B'))
        self.assertEqual('Q2', findQuadType(0, -1, self.board3, 2, 'B'))
        self.assertEqual('Qd', findQuadType(0, 0, self.board4, 2, 'W'))
        self.assertEqual('Qd', findQuadType(0, 0, self.board4, 2, 'B'))


    def testQuadBoardInit(self):
        self.assertEqual('Q1', self.quadTable1.getQuadType(-1, -1, 'B'))
        self.assertEqual('Q0', self.quadTable1.getQuadType(0, 1, 'B'))
        self.assertEqual('Qd', self.quadTable1.getQuadType(1, 0, 'B'))
        self.assertEqual('Q1', self.quadTable1.getQuadType(2, 1, 'B'))
        self.assertEqual('Q2', self.quadTable1.getQuadType(0, 0, 'B'))
        self.assertEqual('Q2', self.quadTable1.getQuadType(0, -1, 'B'))
        
        self.assertEqual('Q1', self.quadTable1.getQuadType(-1, 0, 'W'))
        self.assertEqual('Q2', self.quadTable1.getQuadType(0, 0, 'W'))
        self.assertEqual('Q3', self.quadTable1.getQuadType(1, 1, 'W'))
        self.assertEqual('Q2', self.quadTable1.getQuadType(1, 2, 'W'))
        self.assertEqual('Q1', self.quadTable1.getQuadType(2, 2, 'W'))
        
        count_types_w = count_types(self.quadTable3, 'W')
        count_types_b = count_types(self.quadTable3, 'B')
         
        self.assertEqual(count_types_w['Q0'], 53)
        self.assertEqual(count_types_w['Q1'], 8)
        self.assertEqual(count_types_w['Q2'], 20)
        self.assertEqual(count_types_w['Q3'], 0)
        self.assertEqual(count_types_w['Q4'], 0)
        self.assertEqual(count_types_w['Qd'], 0)
        
        self.assertEqual(count_types_b['Q0'], 53)
        self.assertEqual(count_types_b['Q1'], 8)
        self.assertEqual(count_types_b['Q2'], 20)
        self.assertEqual(count_types_b['Q3'], 0)
        self.assertEqual(count_types_b['Q4'], 0)
        self.assertEqual(count_types_b['Qd'], 0)
        
        count_types_w2 = count_types(self.quadTable6, 'W')
        count_types_b2 = count_types(self.quadTable6, 'B')
         
        self.assertEqual(count_types_w2['Q0'], 53)
        self.assertEqual(count_types_w2['Q1'], 8)
        self.assertEqual(count_types_w2['Q2'], 20)
        self.assertEqual(count_types_w2['Q3'], 0)
        self.assertEqual(count_types_w2['Q4'], 0)
        self.assertEqual(count_types_w2['Qd'], 0)
        
        self.assertEqual(count_types_b2['Q0'], 49)
        self.assertEqual(count_types_b2['Q1'], 17)
        self.assertEqual(count_types_b2['Q2'], 14)
        self.assertEqual(count_types_b2['Q3'], 1)
        self.assertEqual(count_types_b2['Q4'], 0)
        self.assertEqual(count_types_b2['Qd'], 0)
                    
    def testEulerNumber(self):
        self.assertEqual(3, self.quadTable2.eulerNumber('B'))
        self.assertEqual(1, self.quadTable2.eulerNumber('W'))

        
    def testCalcMoveDist(self):
        move1 = MoveAction(3, 3, Direction("W", (0, -1)))
        self.assertEqual(3, calcMoveDist(move1, self.quadTable2.board, self.quadTable2.size))
        move2 = MoveAction(2, 4, Direction("SW", (1, -1)))   
        self.assertEqual(4, calcMoveDist(move2, self.quadTable2.board, self.quadTable2.size))

    
    def testUpdate(self):
        move1 = MoveAction(6, 0, Direction("E", (0, 1)))
        self.assertEqual(3, self.quadTable2.calcMoveDist(move1))

def count_types(quadTable, player):
    count_types = {'Q0':0, 'Q1':0, 'Q2':0, 'Q3':0, 'Q4':0, 'Qd':0}
    for x in range(-1, quadTable.size):
        for y in range(-1, quadTable.size):
            count_types[quadTable.getQuadType(x, y, player)] += 1
    
    return count_types


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()