'''
Created on Jun 3, 2011

@author: inesmeya
'''
from loa_game import LinesOfActionState, WHITE
from s_alpha_beta import AnyTimeSmartAlphaBeta
from s_heuristics import winner_heuristics
from s_eval_mass import CenterMassEvaluator
from s_statistics import GTimeStatistics, TimeStatisticsClass
import time





def main():
    test4()

def test4():
    stats = TimeStatisticsClass()
    
    def f():
        return time.clock()
    
    def g():
        return GTimeStatistics.measure_function(f)
    
    
    def all():
        sum = 0.0
        prev = time.clock()
        for _ in xrange(1000):
            next = g()
            delta = next - prev
            sum += delta
            prev = next
        return sum
    
    start = time.clock()
    sum = stats.measure_function(all)
    end = time.clock()
    
    runtime = end - start
    calculated = sum
    avg_approx = GTimeStatistics.stats['f'].average*1000
    
    
    print "runtime:", runtime
    print "calculated:", calculated
    print "gstats:", avg_approx
    print "stats:", stats.stats['all'].average
    
    print "Dcalculated:", runtime - calculated
    print "Dgstats:", runtime - avg_approx
    print "Dstats:", runtime - stats.stats['all'].average    
    
    
    


def test3():
    try:
        raise Exception("df")
    except Exception as e:
        print e
    print "F"


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