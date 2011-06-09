# -*- coding:utf-8 -*-
"""
Created on Jun 8, 2011

@author: inesmeya
"""
from loa_game import LinesOfActionState, BLACK, WHITE, TIE
from game_runner import GameRunner
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams


class  GameTester():
    def __init__(self, name, same_agents=True):
        self.name = name
        self.games_stat =[]
        self.pairs =[]
        self.games_num = 0
        self.same_agents = same_agents
        
        self.agent1 = None
        self.agent1_wins = 0
        self.agent1_pair_wins = 0
        
        self.agent2 = None
        self.agent2_wins = 0
        self.agent2_pair_wins = 0

    def run_game(self,agent_class1, params1, agent_class2, params2, game_params):
        self.games_num +=1
        '''
        @param agent_class1: white agent class
        '''
        agent1 = agent_class1()
        agent2 = agent_class2()
        # initialize agents with supports myinit
        for agent, params in [(agent1,params1), (agent2,params2)]:
            if isinstance(agent, AnytimeSmartAlphaBetaPrintAgentParams):
                agent.myinit(**params)
        
        agents = {WHITE: agent1, BLACK: agent2}
        state = LinesOfActionState(game_params['size'], game_params['turns_left'])
        game_runner =  GameRunner(state, agents, game_params['turn_time_limit'] , 
                                game_params['setup_time_limit'])
        
        try:
            winner = game_runner.run()
            print 'Winner:', winner
        
        except Exception, e:
            print e
            print "Assuming winner is Tie"
            winner = TIE
            raise
        finally:
            print "Test name"
            for p,a in agents.items():
                print "Player ", p
                print a
        #destroy caching
        try:
            agent1.destroy_cache()
            agent2.destroy_cache()

        except:
            pass
                
        # Statistics
        if self.same_agents == False:
            res = ("\nGame",game_params,"Agents:\n",agent1,agent2,winner)
            self.games_stat.append(res)
        
        return winner
    
    def get_pair_winner(self,w1,w2):
        sum =  w1 + w2
        if sum == 0:
            return TIE
        elif sum > 0:
            return 1
        return 2
        
        
    def winer_to_number(self, w):
        if w == TIE:
            return 0
        elif w == WHITE:
            return 1
        return -1     
        
    
    def add_game_winner(self,w):
        if w > 0:
            self.agent1_wins +=1
        if w < 0:
            self.agent2_wins +=1
    
    def add_pair_winner(self,w):
        if w==1:
            self.agent1_pair_wins += 1
        if w==2:
            self.agent2_pair_wins +=1
                
    def run_game_pair(self, agent_class1, params1, agent_class2, params2, game_params):
        '''agent_class1 
        '''
        print "Runnig a1 vs a2"
        winner1 = self.run_game(agent_class1, params1, agent_class2, params2, game_params)
        wn1 = self.winer_to_number(winner1)
        self.add_game_winner(wn1)
        
        print "Runnig a2 vs a1"
        winner2 = self.run_game(agent_class2, params2, agent_class1, params1, game_params)
        wn2 = -self.winer_to_number(winner2)
        self.add_game_winner(wn2)
        
        winner = self.get_pair_winner(wn1,wn2)
        self.add_pair_winner(winner)
         
    def result(self):
        sb = [
              "===========%s===============" % self.name,
              "games:%s" % self.games_num,
              "agent1 wins:%s" % self.agent1_wins,
              "agent1 paired wins:%s" % self.agent1_pair_wins,
              "agent2 wins:%s" % self.agent2_wins,
              "agent2 paired wins:%s" % self.agent2_pair_wins,              
               ]
        r = "\n".join(sb)
        if self.same_agents == False:
            
            for g in self.games_stat:
                r += "\nGame\n"
                for it in g:
                    r += str(it)
        return r 
        
    def save_result(self):
        myfile = file( self.name +".txt", 'w')
        print >> myfile, self.result()
        myfile.close()