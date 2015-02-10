#! /usr/bin/python3

from __future__ import division

from gi.repository import Gst, GLib, GObject

class Beeper(object):
    def __init__(self):
        GObject.threads_init()
        Gst.init([])
        
        self.sink = Gst.ElementFactory.make('alsasink', None)
        if not self.sink:
            # Will try to use the pc speaker instead...
            return
        
        self.pipe = Gst.Pipeline()
        self.src = Gst.ElementFactory.make('audiotestsrc', None)
        self.src.set_property('volume', 1)
        self.pipe.add(self.src)
        self.pipe.add(self.sink)
        self.src.link(self.sink)
    
    def beep(self, freq=440, volume=.1):
        if not self.sink:
            self.beep_with_beep()
            return
        
        self.src.set_property('freq', freq)
        self.src.set_property('volume', volume)
        self.pipe.set_state( Gst.State.PLAYING )
        self.ml = GLib.MainLoop()
        GLib.timeout_add( 500, self.stop )
        self.ml.run()
    
    def beep_with_beep(self):
        import subprocess
        subprocess.call(['beep'])
    
    def stop(self):
        self.pipe.set_state( Gst.State.PAUSED )
        self.ml.quit()

if __name__ == '__main__':
    b = Beeper()
    b.beep()
