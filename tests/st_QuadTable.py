'''
Created on May 27, 2011

@author: shizki
'''
import unittest
from quad_table import findQuadType, QuadTable


class Test(unittest.TestCase):

    def setUp(self):       
        self.board1 = ((' ', 'B'),('W', 'B'))
        self.board2 = (('W', 'B'),('B', 'B'))
        self.board3 = (('B', 'B'),('B', 'B'))
        self.board4 = (('B', 'W'),('W', 'B'))
        
        self.board5 = (('B', 'B', ' '),('W', 'W', 'B'),(' ', 'W', 'W'))
        self.quadTable1 = QuadTable(self.board5, 3, 'B')
        self.quadTable2 = QuadTable(self.board5, 3, 'W')
        
        self.board6 = ( (' ',' ',' ',' ',' ',' ',' ',' ',) , 
                        ('B',' ','B',' ',' ',' ',' ',' ',) , 
                        (' ','B',' ',' ','W',' ',' ',' ',) , 
                        (' ',' ',' ','W',' ','W',' ','B',) , 
                        (' ',' ','W',' ','W',' ',' ',' ',) , 
                        (' ','W',' ',' ','B',' ',' ',' ',) , 
                        (' ',' ',' ',' ',' ',' ',' ',' ',) , 
                        (' ',' ',' ',' ',' ',' ','W',' ',) )
        
        self.quadTable3 = QuadTable(self.board6, 8, 'B')
        self.quadTable4 = QuadTable(self.board6, 8, 'W')
        
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
        self.assertEqual('Q1', self.quadTable1.getQuadType(-1, -1))
        self.assertEqual('Q0', self.quadTable1.getQuadType(0, 1))
        self.assertEqual('Qd', self.quadTable1.getQuadType(1, 0))
        self.assertEqual('Q1', self.quadTable1.getQuadType(2, 1))
        self.assertEqual('Q2', self.quadTable1.getQuadType(0, 0))
        self.assertEqual('Q2', self.quadTable1.getQuadType(0, -1))
        
        self.assertEqual('Q1', self.quadTable2.getQuadType(-1, 0))
        self.assertEqual('Q2', self.quadTable2.getQuadType(0, 0))
        self.assertEqual('Q3', self.quadTable2.getQuadType(1, 1))
        self.assertEqual('Q2', self.quadTable2.getQuadType(1, 2))
        self.assertEqual('Q1', self.quadTable2.getQuadType(2, 2))
                
    def testEulerNumber(self):
        self.assertEqual(3, self.quadTable3.eulerNumber())
        self.assertEqual(1, self.quadTable4.eulerNumber())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()