# coding=utf-8
import heapq
from collections import deque
import random
class BoundedPriorityQueue(object):
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

  #  def pop(self):
   #     return heapq.heappop(self.queue)    #Pop and return the smallest item from the heap, 

    def extend(self, iterable):
        for x in iterable:
            self.append(x)

   # def clear(self):
    #    for x in self:
     #       self.queue.remove(x)

#    def remove(self, x):
 #       self.queue.remove(x)

    #Return a list with the n smallest elements from the dataset defined by iterable.
  #  def sorted(self):
   #     return heapq.nsmallest(len(self.queue), self.queue)