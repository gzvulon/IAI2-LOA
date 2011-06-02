'''
Created on Jun 2, 2011

@author: inesmeya
'''
import unittest
from s_turn_cache import get_or_set_init, TurnCache
from loa_game import LinesOfActionState


class Test(unittest.TestCase):


    def setUp(self):
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
        succs = o.get_cached_value(current_state, current_state.getSuccessors)
        self.assertEqual(succs,current_state.getSuccessors())
        
        for s in succs.values():
            o.get_cached_value(s, s.getSuccessors)
            
        t =  o.checkers_left_table.has_key((8,7))
        self.assertTrue(t)
        
        f =  o.checkers_left_table.has_key((7,8))
        self.assertFalse(f)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_or_set_init']
    unittest.main()