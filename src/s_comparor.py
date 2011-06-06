'''
Created on Jun 5, 2011

@author: inesmeya
'''


def compare(agents):
    try:
        winner = GameRunner(state, agents, 5.5 , 1).run()
    print 'Winner:', winner
        except Exception as e:
    print e
    

def compare_list(agents_pair_list):
    '''
    @param agents_pair_list: =[agents,...]
            agents: {BLACK: agent, WHITE agent}
    '''
    for agents in agents_pair_list:
        compare(agents)
    
    
    
    





if __name__ == '__main__':
    pass