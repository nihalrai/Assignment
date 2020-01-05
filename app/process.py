import time
import csv
import json
import threading
import traceback


# Reference: https://stackoverflow.com/questions/33640283/thread-that-i-can-pause-and-resume

class Process(threading.Thread):
    def __init__(self):
        self.can_run = threading.Event()
        self.thing_done = threading.Event()
        self.thing_done.set()
        self.can_run.set()

    def run(self, content, file):
        while True:
            self.can_run.wait()
            try:
                self.thing_done.clear()
                with open('D:///flask_check//{}'.format(file), 'w') as t:
                    writer = csv.writer(t)
                    #writer.writerows(content)
            finally:
                self.thing_done.set()

    def pause(self):
        self.can_run.clear()
        self.thing_done.wait()

    def resume(self):
        self.can_run.set()
