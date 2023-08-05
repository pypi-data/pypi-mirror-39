#! /usr/bin/env python
# coding: utf-8


"""
timer.py - A class for counting time.
"""


def get_timer(delay = 0, callback = False):
    """
    Method that returns a Timer instance.
    
    param: delay, the amount of time the Timer is set for.
    
    param: callback, an optional function to have the timer 
        run when it reaches its set time.
    
    return: Timer, a timer object.
    """
    return Timer(delay, callback)


class Timer(object):
    """
    A timer that runs for a set amount of time and then stops. Can 
    be given a callback to run when it finishes.
    """
    
    def __init__(self, duration, callback):
        """
        Constructor for Timer class.
        
        param: duration, an integral length of time.
        
        param: callback , an optional callback to run when the 
            timer completes.
        """
        self.duration = duration
        self.callback = callback
        self.event_time = 0
        self.timing = False
        self.finished = False


    def set_duration(self, seconds):
        """
        Sets the length of the timer.
        
        param: time, an integral length of time in seconds.
        """
        self.duration = seconds


    def set_callback(self, cb):
        """
        Sets the callback for the timer.
        
        param: cb, a function to call when the timer is finished.
        """
        self.callback = cb


    def start(self):
        """
        Starts the timer to counting.
        """
        self.timing = True


    def stop(self):
        """
        Halts the timer at its current time.
        """
        self.timing = False


    def is_timing(self):
        """
        Returns whether the timer is counting or not.
        
        return: boolean, True/False if the timer is counting.
        """
        return self.timing


    def is_finished(self):
        """
        Returns whether the timer has finished counting or not.
        
        return: boolean, True/False if the timer finshed counting.
        """
        return self.finished


    def reset(self):
        """
        Start the timer counting over from zero.
        """
        self.event_time = 0
        self.finished = False


    def update(self, time_passed):
        """
        Call once per gameloop. Updates the timer variables.
        """
        if self.is_timing():
            self.event_time += time_passed
            if self.event_time >= self.duration:
                if self.callback is not False:
                    self.callback()
                self.finished = True
                self.timing = False

