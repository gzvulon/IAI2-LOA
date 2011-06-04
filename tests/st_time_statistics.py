'''
Created on Jun 4, 2011

@author: inesmeya
'''
import unittest
from s_statistics import TimeStatisticsClass
from s_eval_mass import CenterMassEvaluator
from loa_game import LinesOfActionState, WHITE


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test__all(self):
        stat = TimeStatisticsClass()
        ev = CenterMassEvaluator()
        state  = LinesOfActionState(100, 50)
        
        stat.restart_measure("f")
        ev.evaluate(state, WHITE, 10)
        stat.restart_measure("f")
        
        stat.stop_measure()
        print stat.stats
        pass
    
    def test__measure_function(self):
        stat = TimeStatisticsClass()
        ev = CenterMassEvaluator()
        root_state  = LinesOfActionState(15, 50)
        
        def f(the_state):
            ev.evaluate( the_state, WHITE, 10)
        
        for ss in root_state.getSuccessors().values():
            stat.measure_function(f,ss)
        
        print stat.stats
        pass        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test__all']
    unittest.main()