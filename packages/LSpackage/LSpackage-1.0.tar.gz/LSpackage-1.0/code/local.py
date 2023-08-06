from utils import BPQueue
from models import SearchNodeValueOrdered
import math
import random

def allExpander(fringe, iteration, viewer):
    '''
    Expand all nodes on the fringe.
    '''
    expanded_neighbors = [node.expand(local_search=True)
                          for node in fringe]
    list(map(fringe.extend, expanded_neighbors))

def firstExpander(fringe, iteration):
    '''
    Expands only the first node on the fringe.
    '''
    curr = fringe[0]
    neighbors = curr.expand(local_search=True)
    fringe.extend(neighbors)


def hillClimbing(problem, iterationsLimit=0):
    '''
    Hill Climbing search algorithm.

    If iterationsLimit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    This algorithm requires: SearchProblem.actions, SearchProblem.result, and
    SearchProblem.value.
    '''
    return localSearchAlg(problem, firstExpander,
                         iterationsLimit=iterationsLimit,
                         fringe_size=1, stop_when_no_better=True)

def localSearchAlg(problem, fringe_expander, iterationsLimit=0, fringe_size=1,
                  random_initial_states=False, stop_when_no_better=True):
    '''
    Basic Algorithm for all Local Search algorithms.
    This algorithm requires: 
    SearchProblem.actions, SearchProblem.result, SearchProblem.value.
    '''
    # work with queue - append , pop, extend, clear, remove or sorted
    fringe = BPQueue(fringe_size)
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

        if iterationsLimit and iteration >= iterationsLimit:
            run = False

        elif old_best.value >= best.value and stop_when_no_better:
            run = False
            
    return best
