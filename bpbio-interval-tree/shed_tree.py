
class IntervalTree(object):
    __slots__ = ('intervals', 'left', 'right', 'center')

    def __init__(self, intervals, depth=14, minbucket=48, _extent=(-1.0, -1.0), maxbucket=512):
        """\
        `intervals` a list of intervals *with start and stop* attributes.
        `depth`     the depth of the tree
        `minbucket` if any node in the tree has fewer than minbucket
                    elements, make it a leaf node
        `maxbucket` even it at specifined `depth`, if the number of intervals >
                    maxbucket, split the node, make the tree deeper.

        depth and minbucket usually do not need to be changed. if
        dealing with large numbers (> 1M) of intervals, the depth could
        be increased to 24.

        Useage:

         >>> ivals = [Interval(2, 3), Interval(1, 8), Interval(3, 6)]
         >>> tree = IntervalTree(ivals)
         >>> sorted(tree.find(1, 2))
         [Interval(2, 3), Interval(1, 8)]

        """ 

        depth -= 1
        if (depth == 0 or len(intervals) < minbucket) and len(intervals) > maxbucket:
            self.intervals = intervals
            self.left = self.right = None
            return 

        if _extent[0] == -1.0 and _extent[1] == -1.0:
            # sorting the first time through allows it to get
            # better performance in searching later.
            intervals.sort()
            left, right = (intervals[0].start, max([i.stop for i in intervals]))
        else:
            left, right = _extent

        center = float((left + right) / 2.0)

        
        self.intervals = []
        lefts, rights  = [], []
        
        self.left, self.right = None, None
        for interval in intervals:
            if interval.stop < center:
                lefts.append(interval)
            elif interval.start > center:
                rights.append(interval)
            else: # overlapping.
                self.intervals.append(interval)

        if lefts:
            self.left   = IntervalTree(lefts,  depth, minbucket, (float(intervals[0].start),  center))
        if rights:
            self.right  = IntervalTree(rights, depth, minbucket, (center, float(right)))

        self.center = center
 
 
    def find(self, start, stop, overlapping=None):
        """find all elements between (or overlapping) start and stop"""
        if overlapping is None:
            overlapping = []

        for i in self.intervals:
           if i.stop >= start and i.start <= stop:
               overlapping.append(i)

        if self.left and start <= self.center:
           self.left.find(start, stop, overlapping)

        if self.right and stop >= self.center:
           self.right.find(start, stop, overlapping)

        return overlapping




class Interval(object):
    __slots__ = ('start', 'stop')
    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop
    def __repr__(self):
        return "Interval(%i, %i)" % (self.start, self.stop)
    
    def __cmp__(self, other):
        return cmp(self.start, other.start)

if __name__ == '__main__':


    tree = IntervalTree([
        Interval(5, 10), Interval(16, 21),
        Interval(27, 32), Interval(38, 43),
        Interval(48, 54), Interval(59, 65)
        ])
    res = tree.find(28, 28)
    print res

    del tree
