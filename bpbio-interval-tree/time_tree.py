import sys
import random
from interval_tree import Interval, IntervalTree
import interval_tree
import time


N=300000
TRIES = 1000
START, STOP = 390000, 400000

def rands(n=N, len_range=(200, 6000), start_max=2000000):

    def rand():
        start = random.randint(1, start_max)
        return (start, start + random.randint(*len_range))

    return [rand() for i in xrange(n)]

intervals = rands(N)


def search(tree, start, stop, tries):
    t0 = time.time()
    for i in range(tries):
        res = tree.find(start, stop)
    t1 = time.time()
    return res, t1 - t0

print "\npython...", interval_tree
t0 = time.time()
tree = IntervalTree([Interval(*it) for it in intervals])
t1 = time.time()
print "time to build with %i intervals: %.3f" % (N, t1 - t0)

found, t = search(tree, START, STOP, TRIES)
print "time to search %i times: %.3f. found %i intervals" % (TRIES, t, len(found))



from shed_tree import Interval, IntervalTree
import shed_tree


t0 = time.time()
tree = IntervalTree([Interval(*it) for it in intervals])
t1= time.time()
print "\nshedskin...", shed_tree
print "time to build with %i intervals: %.3f" % (N, t1 - t0)
found, t = search(tree, START, STOP, TRIES)
print "time to search %i times: %.3f. found %i intervals" % (TRIES, t, len(found))
