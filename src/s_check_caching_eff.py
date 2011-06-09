from s_enums import ITERATIVE
from s_weighted_evaluator import WeightedEvaluatorH
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams
from s_game_runner import GameTester

TURNS_LIST = [20,60,80]

def main():
    tester = GameTester("Caching Effectiveness",same_agents=False)
    
    a1_params = {
      'caching':True,
      'init_max_depth': 2,
      'depth_delta':1,
      'use_iterative' : ITERATIVE,
      'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.05, 0.25)
    }
    a1 = AnytimeSmartAlphaBetaPrintAgentParams

    a2_params = {
      'caching':False,
      'init_max_depth': 2,
      'depth_delta':1,
      'use_iterative' : ITERATIVE,
      'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.05, 0.25)
    }
    a2 = AnytimeSmartAlphaBetaPrintAgentParams
    
    
    for turns in TURNS_LIST:
        game_params = {
            'size' : 8,
            'turns_left' : turns,
        
            'turn_time_limit' :  10.0,
            'setup_time_limit' : 5.0
        }
        tester.run_game_pair(a1,a1_params,a2,a2_params,game_params)

    print tester.result()
    tester.save_result()

# -------------------End of -------------------------
if __name__ == '__main__':
    main()

