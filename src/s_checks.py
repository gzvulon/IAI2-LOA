from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams


'''------- With caching VS Without caching ---------''' 
from loa_game import WHITE, BLACK, LinesOfActionState
from s_weighted_evaluator import WeightedEvaluatorH
from s_enums import ITERATIVE
from game_runner import GameRunner
from s_eval_mass import CenterMassEvaluator

agents = {}
a1 = AnytimeSmartAlphaBetaPrintAgentParams()
a1_params = {
  'caching':True,
  'init_max_depth': 2,
  'depth_delta':1,
  'use_iterative' : ITERATIVE,
  'evaluator' :  WeightedEvaluatorH(0.55, 0.3, 0.7, 0.25)
}

a2 = AnytimeSmartAlphaBetaPrintAgentParams()
a2_params = {
  'caching':True,
  'init_max_depth': 2,
  'depth_delta':1,
  'use_iterative' : ITERATIVE,
  'evaluator' : WeightedEvaluatorH(0.55, 0.3, 0.7, 0.25)
}

a1.myinit(**a1_params)
a2.myinit(**a2_params)

agents[ WHITE ] = a1
agents[ BLACK ] = a2

for size in [50, 80]:
    state = LinesOfActionState(15, size)
    
    try:
        winner = GameRunner(state, agents, 3.0 , 1).run()
        print 'Winner:', winner
    
    except Exception, e:
        print e
        raise
    finally:    
        pass
