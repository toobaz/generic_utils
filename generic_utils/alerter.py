import time
from gi.repository import Notify


class Alerter(object):
    def __init__(self, name='Alerter'):
        self.name = name
        Notify.init(name)
    def alert(self, msg):
        n = Notify.Notification.new(self.name, msg, None)
        n.show()
