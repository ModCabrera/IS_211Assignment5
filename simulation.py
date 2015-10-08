#!usr/bin/env python
# -*- coding: utf-8 -*-
"""Simulator Module"""
import urllib2
import time
import argparse

class Queue():

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Server(): #server process requests 

    def __init__(self, ppm):
        self.page_rate = ppm
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_pages() * 60 / self.page_rate


class Request(): #user requesting file from webserver

    def __init__(self, time):
        self.timestamp = time
        self.pages = random.randrange(1, 21)

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.pages

    def wait_time(self, current_time):
        return current_time - self.timestamp
    
def simulate_one_server(filename):
    pass #simulate one server, return average. 
    
    

def simulate_many_server(filename):
    pass #simulate many servers, return average.

def main(file):
    url = file
    response = urllib2.urlopen(url)
    


if __name__ == '__main__':
    main('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv')
