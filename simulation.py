#!usr/bin/env python
# -*- coding: utf-8 -*-
"""Simulator Module"""
import urllib2
import csv
import argparse
import random
import datetime

class Queue(object):
    """Queue

    Attributes = None
    """

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


class Server(object):
    """Docstring
    Attributes: None
    """

    def __init__(self):
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
        self.time_remaining = new_task.proccs_time()


class Request(object):
    """Request

    Attributes: None
    """

    def __init__(self, time, time_req):
        self.timestamp = time
        self.time_req = time_req

    def proccs_time(self):
        return self.time_req

    def wait_time(self, current_time):
        return current_time - self.timestamp


def simulate_one_server(num_seconds, time_required):
    """
    Args:
        host_server (inst): Instance of the server class.
        request_queue (inst): Instance of the Queue class.
        waiting_time (list): List hold waiting time.
        request_link (inst): Instance of Request class.
    Returns:
        None
    Examples:
        >>> simulate_one_server(9, 2)
        >>>
    """
    host_server = Server()
    request_queue = Queue()
    waiting_times = []
    request_link = Request(num_seconds, time_required)
    request_queue.enqueue(request_link)

    for current_second in range(num_seconds):

        if (not host_server.busy()) and (not request_queue.is_empty()):
            next_task = request_queue.dequeue()
            waiting_times.append(next_task.wait_time(current_second))
            host_server.start_next(next_task)

        host_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print "Average Wait %6.2f secs %3d tasks remaining." % \
    (average_wait, request_queue.size())


def simulate_many_servers(request_file, servers):
    """
    Args:
        servers_list (list): List of servers to query.
        server_room (dict): Instances of Servers to query.

    Returns:
        None

    Examples:
        >>> simulate_many_servers(file, 4)
        >>>
    """
    servers_list = [n for n in range(0, int(servers))]
    server_room = {}
    for computer in servers_list:
        server_room[computer] = simulate_one_server
    for data in request_file:
        for serv_num in servers_list:
            random.seed(datetime.datetime.now())
            server_num = random.choice(servers_list)
            server_room[server_num](int(data[0]), int(data[2]))


def main():
    """
    Args:
        parsers (inst): Parser class intance for terminal input.

    Returns:
        None

    Examples:
        >>> main()
        >>> The URL you've submitted is INVALID, enter VALID URL.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--file', help='Enter URL Link to CSV File')
    parser.add_argument('-c', '--servers', help='Enter number of Servers')

    args = parser.parse_args()

    try:
        if args.file:
            grab_file = urllib2.urlopen(args.file)
            read_file = csv.reader(grab_file)
            for row in read_file:
                simulate_one_server(int(row[0]), int(row[2]))
        elif args.servers:
            grab_file = urllib2.urlopen('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv')
            read_file = csv.reader(grab_file)
            simulate_many_servers(read_file, args.servers)
        else:
            print 'Invalid attempt, not a server, not a url'

    except urllib2.URLError as url_err:
        print 'The URL you\'ve submitted is INVALID, enter VALID URL'
        raise url_err

if __name__ == '__main__':
    main()
