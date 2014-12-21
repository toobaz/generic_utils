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
            self._every = (until // 250) or 1
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
    """In its simplest mode,
       
       tc = TimeCounter()
       [...]
       tc.step()
       [...]
       tc.time()
       
       this just reports the elapsed time: the difference between step() and
       time() is simply that only the latter outputs the time, the former has
       not output.
       
       If instead step() is passed a parameter, this will identify a given
       step. The TimeCounter will remember how many time each step() is called
       with each given identifier, and the total time spent in that step (each
       iteration of the step is considered as done when another call to step()
       is made). output() can then be used to get a summary of execution times.
    """
    def __init__(self):
        self._times = []
        now = time.time()
        self._times.append(now)
        # Values are (# iterations, total time) pairs:
        self._steps = {}
        # Just to remember the order:
        self._steps_list = []
        self._current = None
    
    def step(self, number=None):
        now = time.time()
        self._times.append(now)
        if self._current:
            # Previous step ended, record its time
            if not self._current in self._steps:
                self._steps[self._current] = [0,0]
                self._steps_list.append(self._current)
            self._steps[self._current][0] += 1
            self._steps[self._current][1] += now - self._times[-2]
        
        self._current = number

    def time(self):
        now = time.time()
        print("Seconds taken:", now - self._times[-1], "of", now - self._times[0])
        self._times.append(now)
    
    def summary(self):
        for step in self._steps_list:
            print("Step %s: executed %d times taking %f seconds."
                                    % (step,
                                       self._steps[step][0],
                                       self._steps[step][1]))
