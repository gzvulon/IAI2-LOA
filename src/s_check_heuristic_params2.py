from s_enums import ITERATIVE
from s_weighted_evaluator import WeightedEvaluatorH
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams
from s_game_runner import GameTester
from s_agents import RandomAgent
from s_check_games_generator import load_games

def main():
    tester = GameTester("Heuristic Params2")
    
    game_params_arr = load_games()
    
    a1_params = {
      'caching':True,
      'init_max_depth': 2,
      'depth_delta':1,
      'use_iterative' : ITERATIVE,
      'evaluator' : WeightedEvaluatorH(0.3, 0.0, 0.05, 0.0)
                
    }
    a  = AnytimeSmartAlphaBetaPrintAgentParams
    ar = RandomAgent
    
    for game_params in game_params_arr:
        tester.run_game_pair(a,a1_params,ar,{},game_params)
    # number of wins 
    print tester.result()
    tester.save_result()   
# -------------------End of -------------------------
if __name__ == '__main__':
    main()

