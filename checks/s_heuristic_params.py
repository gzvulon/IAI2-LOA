from s_enums import ITERATIVE
from s_weighted_evaluator import WeightedEvaluatorH
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams
from s_game_runner import GameTester
from random import Random
from s_agents import RandomAgent

def main():
    
    rand = Random()

    game_params_arr = []
    for i in range(0,20):
        board_size = rand.randint(5,15)
        turns = rand.randint(10,70)
        turn_time_limit = rand.randint(0.1,12)
        
        game_params_arr[i] = {
            'size' : board_size,
            'turns_left' : turns,
        
            'turn_time_limit' : turn_time_limit,
            'setup_time_limit' : 10.0
        }
    
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
      'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.05, 0.0)
                
    }
    a2 = AnytimeSmartAlphaBetaPrintAgentParams
    
    a3_params = {
      'caching':False,
      'init_max_depth': 2,
      'depth_delta':1,
      'use_iterative' : ITERATIVE,
      'evaluator' : WeightedEvaluatorH(0.4, 0.05, 0.1, 0.0)
                
    }
    a3 = AnytimeSmartAlphaBetaPrintAgentParams
    
    ar = RandomAgent
    
    tester = GameTester("Heuristic Params")
    for _ in range(0,50):
        tester.run_game_pair(a1,a1_params,ar,{},game_params_arr[rand.randint(0,10)])
        
    for _ in range(0,50):
        tester.run_game_pair(a2,a2_params,ar,{},game_params_arr[rand.randint(0,10)])
    

    for _ in range(0,50):
        tester.run_game_pair(a3,a3_params,ar,{},game_params_arr[rand.randint(0,10)])
    # number of wins    
    

# -------------------End of -------------------------
if __name__ == '__main__':
    main()

