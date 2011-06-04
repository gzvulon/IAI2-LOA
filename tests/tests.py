'''
Created on Jun 3, 2011

@author: inesmeya
'''
from loa_game import LinesOfActionState, WHITE
from s_alpha_beta import AnyTimeSmartAlphaBeta
from s_heuristics import winner_heuristics
from s_eval_mass import CenterMassEvaluator




def main():
    test2()



g = [0]
def p():
    print g[0]

def test2():
    class A():
        def f(self):
            g[0] = 222
    
    a = A()
    a.f()
    p()
    
def test1():
    
    ev = CenterMassEvaluator()
    player = WHITE
    def h(state,info_dict):
        r = winner_heuristics(state, player)
        if r == 0:
            r = ev.evaluate(state, player)
        return r
    
    state = LinesOfActionState(6, 50)
    alphaBeta = AnyTimeSmartAlphaBeta(player, 3, h, caching=True)
    
    alphaBeta.search(state, 0, 3.0)
    alphaBeta.search(state, 0, 3.0)

    hit_rate = alphaBeta.turn_cache.statistics.hit_rate()
    print hit_rate
    
    
if __name__ == '__main__':
    main()