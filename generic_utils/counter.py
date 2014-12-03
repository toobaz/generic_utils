from __future__ import print_function
from __future__ import division
import sys
import time

class Counter(object):
    def __init__(self, every=None, until=None):
        self.c = 0
        if every:
            self._every = every
        elif until:
            self._every = until // 250
        else:
            self._every = 100
        self._dots_in_line = 0
        self._start = time.time()
        self._until = until
    
    def count(self):
        self.c += 1
        
        if not (self.c % self._every):
            print(".", end="")
            sys.stdout.flush()
            self._dots_in_line += 1
        
        if self._dots_in_line == 50:
            if self._until:
                print(" %d of %d (%0.2f%%) after %0.2f" % (self.c, self._until, 100 * self.c/self._until, time.time() - self._start))
            else:
                print(" %d after %0.2f" % (self.c, time.time() - self._start))
            sys.stdout.flush()
            self._dots_in_line = 0
        
        if self._until == self.c:
            self.end()
        return self.c
    
    def end(self):
        print(" %d after %0.2f" % (self.c, time.time() - self._start))


class TimeCounter(object):
    def __init__(self):
        self._times = []
        now = time.time()
        self._times.append(now)
    
    def step(self):
        now = time.time()
        self._times.append(now)

    def time(self):
        now = time.time()
        print("Seconds taken:", now - self._times[-1], "of", now - self._times[0])
        self._times.append(now)
