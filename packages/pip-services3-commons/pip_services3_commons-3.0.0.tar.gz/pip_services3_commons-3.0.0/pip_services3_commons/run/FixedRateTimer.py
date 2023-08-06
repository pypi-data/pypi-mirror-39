# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.FixedRateTimer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Fixed rate timer implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
from threading import Thread, Event, Lock

from .INotifiable import INotifiable
from .IClosable import IClosable

class Timer(Thread):
    def __init__(self, interval, callback):
        Thread.__init__(self)
        self._interval = interval
        self._callback = callback
        self._event = Event()

    def run(self):
        while not self._event.is_set():
            self._callback()
            time.sleep(self._interval)

    def stop(self):
        if self.isAlive() == True:
            # set event to signal thread to terminate
            self._event.set()
            # block calling thread until thread really has terminated
            self.join()

class FixedRateTimer(IClosable):
    """
    Timer that is triggered in equal time intervals.

    It has summetric cross-language implementation
    and is often used by Pip.Services toolkit to perform periodic processing and cleanup in microservices.
    """
    task = None
    delay = None
    interval = None
    started = False
    
    _timer = None
    _lock = None

    def __init__(self, task = None, interval = None, delay = None):
        """
        Creates new instance of the timer and sets its values.

        :param task: (optional) a Notifiable object or callback function to call when timer is triggered.

        :param interval: (optional) an interval to trigger timer in milliseconds.

        :param delay: (optional) a delay before the first triggering in milliseconds.
        """
        self._lock = Lock()
        self.task = task
        self.delay = delay
        self.interval = interval
        self.started = False

    def start(self):
        """
        Starts the timer.
        Initially the timer is triggered after delay.
        After that it is triggered after interval until it is stopped.
        """
        self._lock.acquire()
        try:
            # Stop previously set timer
            if self._timer != None:
                self._timer.stop()
                self._timer = None

            # Set a new timer
            self._timer = Timer(self.delay / 1000, self._timer_callback)
            self._timer.start()
            
            # Set started flag
            self.started = True
        finally:
            self._lock.release()


    def _timer_callback(self):
        try:
            self.task.notify("pip-commons-timer")
        except:
            # Ignore or better log
            pass

    def stop(self):
        """
        Stops the timer.
        """
        self._lock.acquire()
        try:
            # Stop the timer
            if self._timer != None:
                self._timer.stop()
                self._timer = None
            
            # Unset started flag
            self.started = False
        finally:
            self._lock.release()

    def close(self, correlation_id):
        """
        Closes the timer.
        This is required by [[ICloseable]] interface,
        but besides that it is identical to stop().

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self.stop()

