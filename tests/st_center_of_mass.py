'''
Created on May 27, 2011

@author: inesmeya
'''
import unittest
from s_eval_mass import CenterMassEvaluator
from loa_game import LinesOfActionState, WHITE, BLACK


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_state_to_coord_repr(self):
        ev = CenterMassEvaluator()
        state  = LinesOfActionState(6, 50)
        chord_repr_of_state = ev.state_to_coord_repr(state)
        #print 
        #print chord_repr_of_state
        #print state
        #ev.evaluate(state, player, action, quad_table_ext)
        expected = {'B': [(0, 1), (5, 1), (0, 2), (5, 2), (0, 3), (5, 3), (0, 4), (5, 4)], 'W': [(1, 0), (2, 0), (3, 0), (4, 0), (1, 5), (2, 5), (3, 5), (4, 5)]}
        
        def test(player):
            self.assertEqual(len(chord_repr_of_state[player]), len(expected[player]))
            for xy in  chord_repr_of_state[player]:
                self.assertTrue( xy in expected[player])
        test(WHITE)
        test(BLACK)
        #~~~
    
    def test_center_of_mass_from_coord_list(self):
        ev = CenterMassEvaluator()
        l = [(0,0),(1,0),(2,0), 
             (0,1),      (2,1), 
             (0,2),(1,2),(2,2)]
        cx,cy = ev.center_of_mass_from_coord_list(l)
        self.assertEquals((cx,cy),(1,1))
        #~~~    
    
    def test_sum_of_min_distances_ext2(self):
        ev = CenterMassEvaluator()
        l = [(0,0),(1,0),(3,0), 
             (0,1),      (2,1), 
             (0,2),(1,2),(4,4)]
        cm = ev.center_of_mass_from_coord_list(l)
        r = ev.sum_of_min_distances_ext2(cm, l)
        #print r
    
    
    def lists(self):
        lls = [
               [(0,0),(3,0),(6,0), 
                (0,3),      (6,3), 
                (0,6),(3,6),(6,6)],
                
                [(0,0),(1,0),(2,0), 
                 (0,1),      (2,1), 
                 (0,2),(1,2),(2,2)],

               [(0,0),(1,0),(2,0), 
                (0,1),      (2,1), 
                (0,2),(1,2),(2,3)],               

               [(0,0),(1,0),(2,0), 
                (0,1),      (2,1), 
                (0,2),(1,2),(4,4)],
                
               [(0,0),(1,0),(3,0), 
                (0,1),      (2,1), 
                (0,2),(1,2),(4,4)],
               
                [(0,0),(1,0),(3,0), 
                     (2,1), 
                (0,2),(1,2),(4,4)],
                
                [(0,0),(1,0),(3,0), 
                (0,1),      (2,1), 
                (0,2),(1,2),(4,4)],
                                              
               ]
        return lls
    
    
    def do_i(self,l,ev):

        cm = ev.center_of_mass_from_coord_list(l)
        r = ev.sum_of_min_distances_ext2(cm, l)
        smart_sum, smart_sum_count, dsum, dmin_sum, dmin, dmin_count = r

        r1 = ev.min_sum_res(smart_sum_count, smart_sum)
        r2 = ev.min_sum_fix(dmin, dmin_count, len(l))  
        print r1+r2, "  ",r1,r2
             
    def test_evaluate(self):
        ev = CenterMassEvaluator()
        print
        for the_l in self.lists():
            self.do_i(the_l,ev)     
        
        
        
        #self.assertEquals((cx,cy),(1,1))
        #~~~         
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()