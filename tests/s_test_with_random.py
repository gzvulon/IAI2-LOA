# -*- coding:utf-8 -*-
"""
Created on May 27, 2011

@author: inesmeya
"""
import st_import 

from s_agents import   RandomAgent
from game_runner import GameRunner
from s_enums import ITERATIVE, NON_ITERATIVE

from s_weighted_evaluator import WeightedEvaluatorI, WeightedEvaluatorH
from s_eval_mass import CenterMassEvaluator
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams
from s_game_runner import GameTester


'''
a1_params = {
  'caching':True,
  'init_max_depth': 4,
  'depth_delta':2,
  'use_iterative' : ITERATIVE,
  'evaluator' :  WeightedEvaluatorI(0.55, 0.3, 0.7, 0.25)       
}

a2_params = {
  'caching':True,
  'init_max_depth': 2,
  'depth_delta':1,
  'use_iterative' : ITERATIVE,
  'evaluator' : CenterMassEvaluator() 
            
}
'''

# -------------------Example -------------------------

def main():
    a3_params = {
      'caching':True,
      'init_max_depth': 2,
      'depth_delta':1,
      'use_iterative' : ITERATIVE,
      'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.01, 0.25)
                
    }
        
    tester = GameTester("My Test Name")
    a1 = AnytimeSmartAlphaBetaPrintAgentParams
    a2 = RandomAgent
    
    for size in [15]:
        game_params = {
            'size' : size,
            'turns_left' : 20,
        
            'turn_time_limit' : 10.0,
            'setup_time_limit' : 1.0
        }
        tester.run_game_pair(a1,a3_params,a2,{},game_params)
    

# -------------------End of -------------------------
if __name__ == '__main__':
    main()

