from s_enums import ITERATIVE
from s_weighted_evaluator import WeightedEvaluatorH
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams
from s_game_runner import GameTester
from random import Random
from s_agents import RandomAgent

def main():
    tester = GameTester("Heuristic Params")
    rand = Random()
    NUMBER_OF_GAME_PAIRS = 20
    
    game_params_arr = [None]*NUMBER_OF_GAME_PAIRS
    for i in range(0,NUMBER_OF_GAME_PAIRS):
        board_size = rand.randint(5,15)
        turns = rand.randint(10,70)
        turn_time_limit = rand.uniform(0.5,12.0)
        
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

    a2_params = {
      'caching':True,
      'init_max_depth': 2,
      'depth_delta':1,
      'use_iterative' : ITERATIVE,
      'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.05, 0.0)
                
    }
    
    a3_params = {
      'caching':True,
      'init_max_depth': 2,
      'depth_delta':1,
      'use_iterative' : ITERATIVE,
      'evaluator' : WeightedEvaluatorH(0.4, 0.05, 0.1, 0.0)
                
    }
    
    a  = AnytimeSmartAlphaBetaPrintAgentParams
    ar = RandomAgent
    
    for _ in range(0,50):
        tester.run_game_pair(a,a1_params,ar,{},game_params_arr[rand.randint(0,10)])
        
    for _ in range(0,50):
        tester.run_game_pair(a,a2_params,ar,{},game_params_arr[rand.randint(0,10)])
    

    for _ in range(0,50):
        tester.run_game_pair(a,a3_params,ar,{},game_params_arr[rand.randint(0,10)])
    # number of wins    
    

# -------------------End of -------------------------
if __name__ == '__main__':
    main()

