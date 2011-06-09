from game_agent import GameAgent
from s_alpha_beta import  SmartAlphaBetaSearch
from s_statistics import GTimeStatistics, VisitsStatisticsClass,\
    TimeStatisticsClass
from s_enums import QUAD_TABLE_TAG, ITERATIVE, NON_ITERATIVE, QUAD_WINNER
from s_quad_table import QuadTable, QuadTableNoUpdate
from s_end_timer import EndTimer, TimeOutException
from loa_game import LinesOfActionState
from s_turn_cache import TurnCache, NoneTurnCache, TurnCacheCleanable
from random import Random
from s_eval_mass import CenterMassEvaluator
from s_quad_evaluator import QuadEvaluator
import gc

class AnytimeSmartAlphaBetaPrintAgentParams(GameAgent):
    # ----------------------- Info API -------------------------------
    def get_name(self):
        return "Smart Anytime Agent. Params: caching=%s, depth_delta=%s, use_iterative=%s, init_max_depth=%s, evaluator=%s" %(         
        self.caching,
        self.depth_delta,
        self.use_iterative,
        self.init_max_depth,
        self.evaluator
        )
    
    def myinit(self, caching, init_max_depth, depth_delta,  use_iterative, evaluator, max_states_in_cache=15000):
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
        self.evaluator = evaluator
        self.max_states_in_cache = max_states_in_cache
        
        #statistics
        self.node_statistics = VisitsStatisticsClass(self.get_name())
        self.time_statistics = TimeStatisticsClass()
    
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
        self.last_game_state = game_state
        self.collected = 0
        
        #save params
        self.safe_delta = 0.8
        self.corrected_turn_time_limit = turn_time_limit - self.safe_delta
        self.player = player

        #TODO: check set_uptime
        
        # == Setup info set ==
        self.info_set = {}
        
        self.info_set[QUAD_TABLE_TAG] = {
            ITERATIVE: QuadTable,
            NON_ITERATIVE: QuadTableNoUpdate
        }[self.use_iterative](game_state.board, game_state.size, initialize =True)
        
        # == Setup caching ==
        if self.caching: self.turn_cache = TurnCacheCleanable(self.max_states_in_cache)
        else:       self.turn_cache = NoneTurnCache()
 
     
    # ---------------------  The heuristics ------------------------------    
    
    def utility(self, state, info_set):
        GTimeStatistics.start_measure("agent.utility")
        hv = self.evaluator.evaluate(state, self.player,info_set)
        GTimeStatistics.stop_measure("agent.utility")
        return hv
               
    def info_print(self, game_state):
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
                 lambda: info_table.updateWithoutAction(oldstate, newstate) )
        return new_info_set 
    
    
    def choose_default_answer(self,current_state):
        succesors = self.turn_cache.get(current_state, LinesOfActionState.getSuccessors)
        #succesors = current_state.getSuccessors()
                # choose default move randomly: 
        index = self.rand.randint(0, len(succesors)-1)
        res_action, res_state = succesors.items()[index]
        return res_action, res_state
         
        
    def move(self, game_state):
        self.start_timer()
        self.res_action, self.res_state = self.choose_default_answer(game_state)
        self.turn_cache.clean_up_if_need(game_state, self.last_game_state)
        
        #gc stuff
        gc.enable()
        collected = self.time_statistics.measure_function(gc.collect)
        self.collected += collected
        gc.disable()
        
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
            self.node_statistics.clear_monitor()
            pass
        #save data about last gamestate
        self.last_game_state = game_state
        # save data about our move

        self.prev_state = self.res_state
        self.info_set   = self.res_info_set 
        self.stop_timer()
#        print "cm", CenterMassEvaluator().evaluate(self.res_state, self.player, self.res_info_set)
#        print "e", QuadEvaluator().evaluate(self.res_state, self.player, self.res_info_set)
        
        return self.res_action
    
    # --------------------------- search algorithm ------------------------
    
    def search(self, current_state, info_set, init_max_depth):
        '''
        @param info_set: info set of current_state
        '''        
        # start iterative search
        curr_max_depth = init_max_depth
        print init_max_depth
        # print "time left", end_time - time.clock(), "d=", curr_max_depth
        alg = SmartAlphaBetaSearch(self.player, self.utility, self.turn_cache, self.time_statistics, self.node_statistics, self.winner_check, )
        
        while True:
            EndTimer.check("start search")
            
            self.node_statistics.start_monitor(curr_max_depth)
            r = alg.search(current_state, curr_max_depth, info_set)
            self.node_statistics.stop_monitor(curr_max_depth)
            
            self.res_action, self.res_state, self.res_info_set = r
            print "Solution at depth:", curr_max_depth, "  time left:", EndTimer.time_left()
            curr_max_depth += self.depth_delta 
            
    # -------------------------- AUX --------------------------------
    def __str__(self):
        sb = [
        "@@@@@@Agent",
        self.get_name(),
        "== Node statistics ==",
        self.node_statistics,
        "== Turn_cache ==",
        self.turn_cache ,
        "== Time statistics== ",
        self.time_statistics,
        "== GC ==",
        "Collected:%s" % self.collected
        ]
        
        res = "\n".join([str(x) for x in sb])
        return res
    def __repr__(self):
        return self.__str__()
        
        
        
        

                   
        