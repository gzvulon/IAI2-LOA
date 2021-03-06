from s_heuristics import winner_heuristics
from game_agent import GameAgent
from s_eval_mass import CenterMassEvaluator
from s_alpha_beta import  SmartAlphaBetaSearch
from s_statistics import GTimeStatistics
from s_enums import QUAD_TABLE_TAG, ITERATIVE, NON_ITERATIVE, SIMPLE_WINNER,\
    QUAD_WINNER
from s_quad_table import QuadTable, QuadTableNoUpdate
from s_end_timer import EndTimer, TimeOutException
from loa_game import LinesOfActionState, WHITE, BLACK
from s_turn_cache import TurnCache, NoneTurnCache
from random import Random

class AnytimeSmartAlphaBetaPrintAgentParamsOld(GameAgent):
    # ----------------------- Info API -------------------------------
    def get_name(self):
        return self.alphaBeta.get_name()
    
    def myinit(self, caching, init_max_depth, depth_delta,  use_iterative):
        ''' 
        use string names names
        allow to confine agent'''
        self.caching = caching
        self.depth_delta = depth_delta
        self.use_iterative = use_iterative
        self.rand = Random(0)
        self.init_max_depth = init_max_depth
        
        self.use_quads = False
        
        #TODO:
        self.winner_check = QUAD_WINNER 
    
    # ---------------------- Timer ----------------------------------
    def start_timer(self):
        EndTimer.set_limit_and_start(self.corrected_turn_time_limit)
    
    def stop_timer(self):
        EndTimer.stop() 
    
    # ---------------------- Game Interface ----------------------------------
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        #TODO: use my_init to config final agent
        
        # we need init state to determine if we have to
        self.init_state = game_state
        self.prev_state = game_state
        
        #save params
        self.safe_delta = 0.085
        self.corrected_turn_time_limit = turn_time_limit - self.safe_delta
        self.player = player
        
        # choose evaluator
        self.evaluator = CenterMassEvaluator()

        #TODO: check set_uptime
        
        # == Setup info set ==
        self.info_set = {}
        
        self.info_set[QUAD_TABLE_TAG] = {
            ITERATIVE: QuadTable,
            NON_ITERATIVE: QuadTableNoUpdate
        }[self.use_iterative](game_state.board, game_state.size, initialize =True)
        
        # == Setup caching ==
        if self.caching: self.turn_cache = TurnCache()
        else:       self.turn_cache = NoneTurnCache()

        
     
    # ---------------------  The heuristics ------------------------------    
    def utility(self,state,info_set):
        GTimeStatistics.start_measure("heur")
        r = self.evaluator.evaluate(state, self.player,info_set)
        GTimeStatistics.stop_measure("heur")
        return r
    
    def info_print(self,game_state):
        pass
#        print "The heuristics of game state"
#        print game_state
#        r1,r2 = self.evaluator.evaluate2(game_state, self.player,end_time)
#        r = r1 + r2
#        print "r=", r, "    their:",r1, "    fix:",r2      

    def _update_info_set_no_action(self, oldstate, newstate, info_set):
        new_info_set = {}
        for info_tag, info_table in info_set.items():
            new_info_set[info_tag] = self.turn_cache.get_wkt(newstate, # use cache
                 info_tag, info_tag + '.update_no_action', 
                 lambda: info_table.updateWithoutAction(oldstate, newstate)                 )
        return new_info_set 
    
    
    def choose_default_answer(self,current_state):
        #succesors = self.turn_cache.get(current_state, LinesOfActionState.getSuccessors)
        succesors = current_state.getSuccessors()
                # choose default move randomly: 
        index = self.rand.randint(0, len(succesors)-1)
        res_action, res_state = succesors.items()[index]
        return res_action, res_state
         
        
    def move(self, game_state):
        self.start_timer()
        self.res_action, self.res_state = self.choose_default_answer(game_state)
        print "w=",CenterMassEvaluator().evaluate(game_state,WHITE)
        print "b=",CenterMassEvaluator().evaluate(game_state,BLACK)
        try:
            EndTimer.check("m10")
            # calculate info set for this game_state
            if self.init_state is self.prev_state:
                state_info_set = self.info_set #first turn is us: we already has infoset
            else: 
                state_info_set = self._update_info_set_no_action(self.prev_state, game_state, self.info_set)
            
            EndTimer.check("m20")
            # calculate info set for result game_state
            self.res_info_set = self._update_info_set_no_action(game_state, self.res_state, state_info_set)
            
            #choose our move
            # results saved in self.res_action, self.res_state
            self.search(game_state,  state_info_set, self.init_max_depth)
            
            #save our turn and its info set: to be able calculate next one

        except TimeOutException: #TODO for release handle all exceptios
            pass
        
        # save data about our move
        self.prev_state = self.res_state
        self.info_set   = self.res_info_set 
        return self.res_action
    
    # --------------------------- search algorithm ------------------------
    
    def search(self, current_state, info_set, init_max_depth):
        '''
        @param info_set: info set of current_state
        '''        
        # start iterative search
        curr_max_depth = init_max_depth
        # print "time left", end_time - time.clock(), "d=", curr_max_depth
        
        while True:
            EndTimer.check("start search")
            print  "time left", EndTimer.time_left(), "d=", curr_max_depth
            alg = SmartAlphaBetaSearch(self.player, self.utility, self.turn_cache, self.winner_check,self.use_quads)
            self.res_action, self.res_state, self.res_info_set = alg.search(current_state, curr_max_depth, info_set)
            curr_max_depth += self.depth_delta #TODO: TODO
        
        
                
        