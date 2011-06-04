'''
Created on Jun 3, 2011

@author: inesmeya
'''
import unittest
from s_turn_cache import Statistics


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test__add(self):
        s = Statistics()
        s.add(True, 'a')
        s.add(True, 'a')
        s.add(True, 'a')
        s.add(True, 'a')
        s.add(False, 'a')
        s.add(False, 'a')
        
        s.add(False, 'b')
        s.add(False, 'b')
        
        self.assertEqual(s.stats['a'], [2,4])
        self.assertEqual(s.stats['b'], [2,0])
        
    def test__hit_rate(self):
        s = Statistics()
        s.add(True, 'a')
        s.add(True, 'a')
        s.add(True, 'a')
        s.add(True, 'a')
        s.add(False, 'a')
        s.add(False, 'a')
        
        s.add(False, 'b')
        s.add(False, 'b')
        
        self.assertEquals(s.hit_rate(),{'a':4.0/6,'b':0,'total':1.0/2})
        
        e = Statistics()
        
        self.assertEquals(e.hit_rate(),{'total' : 'empty statistics'})

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test__add']
    unittest.main()