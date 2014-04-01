#synchronize.py



 
from red.services.base import Service
from threading import Thread




class Synchronize(Service, Thread):

    def processMessage(self, msg):
        if "head" in msg and "data" in msg:
            if msg["head"] == "match":
                self.syncMatch(msg["data"])

    def syncMatch(self, data):
        print data