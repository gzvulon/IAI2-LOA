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
from s_game_runner import run_game

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
a3_params = {
  'caching':True,
  'init_max_depth': 2,
  'depth_delta':1,
  'use_iterative' : ITERATIVE,
  'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.01, 0.25)
            
}

game_params = {
    'size' : 10,
    'turns_left' : 50,

    'turn_time_limit' : 3.0,
    'setup_time_limit' : 1.0
}

a1 = AnytimeSmartAlphaBetaPrintAgentParams
a2 = RandomAgent

run_game(a1,a3_params,a2,{},game_params,"test")
# -------------------End of -------------------------


