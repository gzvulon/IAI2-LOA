from s_enums import ITERATIVE
from s_weighted_evaluator import WeightedEvaluatorH
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams
from s_game_runner import GameTester

def main():
    tester = GameTester("Caching Nodes Explored")
    
    game_params = {
        'size' : 10,
        'turns_left' : 80,
    
        'turn_time_limit' : 20.0,
        'setup_time_limit' : 5.0
    }
    
    for init_depth in [1,2,3,4,5]:
        a1_params = {
          'caching':True,
          'init_max_depth': init_depth,
          'depth_delta':100,
          'use_iterative' : ITERATIVE,
          'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.05, 0.25)
                    
        }
        a1 = AnytimeSmartAlphaBetaPrintAgentParams
    
        a2_params = {
          'caching':False,
          'init_max_depth': init_depth,
          'depth_delta':1,
          'use_iterative' : ITERATIVE,
          'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.05, 0.25)
                    
        }
        a2 = AnytimeSmartAlphaBetaPrintAgentParams
        tester.run_game_pair(a1,a1_params,a2,a2_params,game_params)
        # check hit rate
        # number of node / times

# -------------------End of -------------------------
if __name__ == '__main__':
    main()

