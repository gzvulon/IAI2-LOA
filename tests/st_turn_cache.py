'''
Created on Jun 2, 2011

@author: inesmeya
'''
import unittest
from s_turn_cache import get_or_set_init, TurnCache
from loa_game import LinesOfActionState


class Test(unittest.TestCase):


    def setUp(self):
        print
        pass


    def tearDown(self):
        pass


    def test__get_or_set_init(self):
        d = {}
        #init test
        r = get_or_set_init(d,3,lambda: 1)
        self.assertEqual(r,1)
        self.assertEqual(d[3],1)
        # resolve test
        r = get_or_set_init(d,3,lambda: 5)
        self.assertEqual(r,1)
        self.assertEqual(d[3],1)
        
    def test__get_or_set_init_dict(self):
        d = {}
        #init test
        a = get_or_set_init(d,'a',lambda: {})
        b = get_or_set_init(d,'b',lambda: {})
        a[1] = 1
        b[1] = 2
        self.assertNotEqual(a[1],b[1])
        
    def test__get_cached_value(self):
        o = TurnCache()
        
        current_state = LinesOfActionState(6, 50)
        succs = o.get_cached_value(current_state, LinesOfActionState.getSuccessors)
        self.assertEqual(succs,current_state.getSuccessors())
        
        for s in succs.values():
            o.get_cached_value(s, LinesOfActionState.getSuccessors)
            
        t =  o.checkers_left_table.has_key((8,7))
        self.assertTrue(t)
        
        f =  o.checkers_left_table.has_key((7,8))
        self.assertFalse(f)

    def test__clean_up_if_need(self):
        o = TurnCache()
        
        current_state = LinesOfActionState(6, 50)
        succs = o.get_cached_value(current_state, LinesOfActionState.getSuccessors)
        self.assertEqual(succs,current_state.getSuccessors())        
        for s in succs.values():
            o.get_cached_value(s, LinesOfActionState.getSuccessors)
            
        ns = filter(lambda s: s.blacks == 7, succs.values() )[0]
        
        self.assertEquals(o.checkers_left_table.keys(),[(8, 8), (8, 7)])
        o.clean_up_if_need(current_state, ns)
        self.assertEquals(o.checkers_left_table.keys(),[ (8, 7)])
            
    def test__get_winner(self):
        state = LinesOfActionState(6, 50)
        o = TurnCache()
        o.get(state, LinesOfActionState.getWinner)
        o.get(state, LinesOfActionState.getWinner)
        self.assertEqual(o.statistics.hit_rate(), 
        {'getWinner': (0.5, 1, 1), 'total': 0.5})
        
    def test__get_multiple_params(self):
        state = LinesOfActionState(6, 50)
        o = TurnCache()
        
        def fun(istate, p):
            print self.assertEqual(p, 23)
        
        o.get(state, fun, 23)
    
    def test__get_variants(self): 
        current_state = LinesOfActionState(6, 50)
        o = TurnCache()
        v = o.get_variants(current_state, 'getWinner', current_state.getWinner, [])
        v = o.get_variants(current_state, 'getWinner', current_state.getWinner, []) 
         
         (, LinesOfActionState.getWinner)
        o.get(state, LinesOfActionState.getWinner)
        self.assertEqual(o.statistics.hit_rate(), 
        {'getWinner': (0.5, 1, 1), 'total': 0.5})       
       
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_or_set_init']
    unittest.main()