from utils import BoundedPriorityQueue
from models import SearchNodeValueOrdered
import math, random

def _all_expander(fringe, iteration, viewer):
    '''
    Expands All nodes on the fringe are expanded.
    '''
    expanded_neighbors = [node.expand(local_search=True)
                          for node in fringe]
    list(map(fringe.extend, expanded_neighbors))

def _first_expander(fringe, iteration):
    '''
    Only the first node on the fringe is expanded.
    '''
    current = fringe[0]
    neighbors = current.expand(local_search=True)
    fringe.extend(neighbors)


def hill_climbing(problem, iterations_limit=0):
    '''
    Hill climbing search.

    If the iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires to use hill_climbing: action,result and value 
    '''
    return _local_search(problem, _first_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=1, stop_when_no_better=True)

def _local_search(problem, fringe_expander, iterations_limit=0, fringe_size=1,
                  random_initial_states=False, stop_when_no_better=True):
    '''
    Basic algorithm for all local search algorithms.
    '''
    # BoundedPriorityQueue - append , extend in a queue
    fringe = BoundedPriorityQueue(fringe_size)
    #in case of random values
    fringe.append(SearchNodeValueOrdered(state=problem.initial_state, problem=problem))

    iteration = 0
    run = True
    best = None

    while run:

        old_best = fringe[0]
        fringe_expander(fringe, iteration)
        best = fringe[0]
        iteration += 1

        if iterations_limit and iteration >= iterations_limit:
            run = False

        elif old_best.value >= best.value and stop_when_no_better:
            run = False
            
    return best
