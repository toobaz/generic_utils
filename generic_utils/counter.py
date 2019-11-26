from __future__ import print_function
from __future__ import division
import sys
import time

class Counter(object):
    def __init__(self, until=None, every=None, lines=True):
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
        self._lines = lines
        self.total = None
    
    def count(self, howmany=1, through=None, symbol='.'):
        to_draw = 0
        if howmany == 1:
            if self._every != -1 and not (self.c % self._every):
                to_draw = 1
        else:
            leftovers = self.c % self._every
            to_draw = (leftovers + howmany) // self._every

        self.c += howmany

        self._draw_dots(to_draw, symbol=symbol)
                
        if self._until and self._until <= self.c:
            self.end()
        
        if through is not None:
            return through
        else:
            return self.c
    
    def _draw_dots(self, dots=1, symbol='.'):
        # Could be more efficient (in checking newlines):
        for i in range(dots):
            self._draw_dot(symbol=symbol)
   
    def _draw_dot(self, symbol='.'):
        print(symbol, end="")
        sys.stdout.flush()

        self._dots_in_line += 1

        if self._dots_in_line == 50 and self._lines:
            if self._until:
                print(" %d of %d (%0.2f%%) after %0.2f" % (self.c, self._until, 100 * self.c/self._until, time.time() - self._start))
            else:
                print(" %d after %0.2f" % (self.c, time.time() - self._start))
            sys.stdout.flush()
            self._dots_in_line = 0
    
    def end(self):
        if self.total:
            return
        self.total = time.time() - self._start
        print(" %d done in %0.2f" % (self.c, self.total))


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
        taken = now - self._times[-1]
        total = now - self._times[0]
        print("Seconds taken:", taken, "of", total)
        sys.stdout.flush()
        self._times.append(now)
        return taken, total
    
    def summary(self):
        for step in self._steps_list:
            print("Step %s: executed %d times taking %f seconds."
                                    % (step,
                                       self._steps[step][0],
                                       self._steps[step][1]))
