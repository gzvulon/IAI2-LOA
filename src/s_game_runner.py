# -*- coding:utf-8 -*-
"""
Created on Jun 8, 2011

@author: inesmeya
"""
from loa_game import LinesOfActionState, BLACK, WHITE
from game_runner import GameRunner
from s_working_agent import AnytimeSmartAlphaBetaPrintAgentParams


class  GameTester():
    def __init__(self, name):
        self.name = name


    def run_game(self,agent_class1, params1, agent_class2, params2, game_params):
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
            raise
        finally:
            print "Test name"
            for p,a in agents.items():
                print "Player ", p
                print a   
    
    def run_game_pair(self, agent_class1, params1, agent_class2, params2, game_params):
        '''agent_class1 
        '''
        print "Runnig a1 vs a2"
        self.run_game(agent_class1, params1, agent_class2, params2, game_params)
        print "Runnig a2 vs a1"
        self.run_game(agent_class2, params2, agent_class1, params1, game_params)