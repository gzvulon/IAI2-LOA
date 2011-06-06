'''
Created on May 27, 2011

@author: shizki
'''
import unittest
from s_quad_table import QuadTable
from loa_game import MoveAction, Direction, LinesOfActionState, SpinAction
from s_common_ops import findQuadType, calcMoveDist


class Test(unittest.TestCase):

    def setUp(self):       
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
        self.assertEqual(3, calcMoveDist(self.move1, self.quadTable2.board, self.quadTable2.size))
        self.assertEqual(4, calcMoveDist(self.move2, self.quadTable2.board, self.quadTable2.size))
        self.assertEqual(2, calcMoveDist(self.move3, self.quadTable3.board, self.quadTable3.size))


    def testMoveUpdate(self):
        u1 = self.quadTable3.update(self.state3, self.state4, self.move4)
        u2 = self.quadTable4.update(self.state4, self.state5, self.move5)
        
        self.assertNotEqual(self.quadTable3, u1)
        self.assertEqual(self.quadTable4, u1)

        self.assertNotEqual(self.quadTable4, u2)
        self.assertEqual(self.quadTable5, u2)


    def testSpinUpdate(self):
        u1 = self.quadTable6.update(self.state6, self.state7, self.spin6)
        u2 = self.quadTable7.update(self.state7, self.state8, self.spin7)
        
        self.assertNotEqual(self.quadTable6, u1)
        self.assertEqual(self.quadTable7, u1)

        self.assertNotEqual(self.quadTable7, u2)
        self.assertEqual(self.quadTable8, u2)
        
#        print "Before update:"
#        for y in range(-1, self.quadTable4.size):
#            for x in range(-1, self.quadTable4.size):
#                print self.quadTable7.black_quads[(x,y)], 
#            print
#        print
#
#        print "After update:"
#        for y in range(-1, self.quadTable4.size):
#            for x in range(-1, self.quadTable4.size):
#                print u2.black_quads[(x,y)], 
#            print
#        print
#        print "What it should be:"
#        for y in range(-1, self.quadTable5.size):
#            for x in range(-1, self.quadTable5.size):
#                print self.quadTable8.black_quads[(x,y)], 
#            print
        
    def testUpdateWithoutAction(self):
        u1 = self.quadTable3.updateWithoutAction(self.state3, self.state4)
        u2 = self.quadTable4.updateWithoutAction(self.state4, self.state5)
        
        self.assertNotEqual(self.quadTable3, u1)
        self.assertEqual(self.quadTable4, u1)

        self.assertNotEqual(self.quadTable4, u2)
        self.assertEqual(self.quadTable5, u2)
        
        u3 = self.quadTable6.updateWithoutAction(self.state6, self.state7)
        u4 = self.quadTable7.updateWithoutAction(self.state7, self.state8)
        
        self.assertNotEqual(self.quadTable6, u3)
        self.assertEqual(self.quadTable7, u3)

        self.assertNotEqual(self.quadTable7, u4)
        self.assertEqual(self.quadTable8, u4)       

def count_types(quadTable, player):
    count_types = {'Q0':0, 'Q1':0, 'Q2':0, 'Q3':0, 'Q4':0, 'Qd':0}
    for x in range(-1, quadTable.size):
        for y in range(-1, quadTable.size):
            count_types[quadTable.getQuadType(x, y, player)] += 1
    
    return count_types


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()