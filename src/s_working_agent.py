from s_heuristics import winner_heuristics
from game_agent import GameAgent
from s_eval_mass import CenterMassEvaluator
from s_alpha_beta import AnyTimeSmartAlphaBeta

class AnytimeSmartAlphaBetaPrintAgentParams(GameAgent):

    def myinit(self, caching, depth_delta):
        self.caching = caching
        self.depth_delta = depth_delta
        
    def h(self,state,end_time):
        r = winner_heuristics(state, self.player)
        if r == 0:
            r = self.evaluator.evaluate(state, self.player,end_time)
        return r
    
    def info_print(self,game_state):
        pass
#        print "The heuristics of game state"
#        print game_state
#        r1,r2 = self.evaluator.evaluate2(game_state, self.player,end_time)
#        r = r1 + r2
#        print "r=", r, "    their:",r1, "    fix:",r2      

    
    def move(self, game_state):
      
        action, next_state = self.alphaBeta.search(game_state,None,self.turn_time_limit)
        return action
    
        #game_state.getS()[action]
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.evaluator =  CenterMassEvaluator()
        self.player = player
        self.turn_time_limit = turn_time_limit
        
        self.alphaBeta = AnyTimeSmartAlphaBeta(self.player, 3, self.h, depth_delta=self.depth_delta, caching=self.caching)        
        