# coding=utf-8
import heapq, random
from collections import deque

class BPQueue(object):
    def __init__(self, limit=None, *args):
        self.limit = limit
        self.queue = list()

    def __getitem__(self, val):
        return self.queue[val]

    def __len__(self):
        return len(self.queue)

    def append(self, x):
        #Push the value item onto the heap, maintaining the heap invariant.
        heapq.heappush(self.queue, x)  
        if self.limit and len(self.queue) > self.limit:
            self.queue.remove(heapq.nlargest(1, self.queue)[0])

    def extend(self, iterable):
        for x in iterable:
            self.append(x)
