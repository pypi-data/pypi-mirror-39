class SearchProblem(object):
    '''Abstract class to manipulate the search space of the problem, and it will be
       represented as a graph. Each state corresponds with a problem state and
       each problem action corresponds with an edge.
    '''

    def __init__(self, initial_state=None):
        self.initial_state = initial_state

    def actions(self, state):
        '''Returns the actions available to perform from `state`.
           The returned value is an iterable over actions.
           Actions are problem-specific and no assumption should be made about
           them.
        '''
        raise NotImplementedError

    def result(self, state, action):
        '''Returns the resulting state of applying `action` to `state`.'''
        raise NotImplementedError

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        return 1

    def value(self, state):
        '''Returns the value of `state` and it's a number (int or float).'''
        raise NotImplementedError

class SearchNode(object):
    '''Node for the process of searching.'''

    def __init__(self, state, parent=None, action=None, cost=0, problem=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.problem = problem or parent.problem
        self.depth = depth

    def expand(self, local_search=False):
        '''Create successors.'''
        new_nodes = [] #list
        for action in self.problem.actions(self.state):
            new_state = self.problem.result(self.state, action)
            #print(new_state) # all steps untill the end
            cost = self.problem.cost(self.state, action, new_state)
            ''' Reference to the type of the current instance. '''
            nodefactory = self.__class__
            new_nodes.append(nodefactory(state=new_state, parent=None if local_search else self,
                                         problem=self.problem, action=action,
                                         cost=self.cost + cost, depth=self.depth + 1))
        return new_nodes

    def path(self):
        '''Path (list of nodes and actions) from root to this node.'''
        node = self
        path = []
        while node:
            path.append((node.action, node.state))
            node = node.parent
        return list(reversed(path))

class SearchNodeValueOrdered(SearchNode):
    def __init__(self, *args, **kwargs):
        super(SearchNodeValueOrdered, self).__init__(*args, **kwargs)
        ''' Check the values'''
        self.value = self.problem.value(self.state)

    def __lt__(self, other):
        #is equivalent to self,other
        # value must work inverted, because heapq sorts 1-9
        # and we need 9-1 sorting
        return -self.value < -other.value