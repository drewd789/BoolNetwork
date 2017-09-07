import numpy as np
from random import choice

# There are two conventions used in this code to represent the state of
#   a node.
#   * Asymmetric:  off is represented by 0, on is represented by 1.
#   * Symmetric:   off is represented by -1, on is represented by 1.
# The convention used internally may vary from class to class.  The
#   get_state method will automatically convert to the asymmetric
#   representation.  The set_state method assumes the input is in
#   asymmetric representation.

class BoolNetwork:
    def __init__(self, num_nodes, rules):
        self.num_nodes = num_nodes
        self.rules = rules
        self.state = np.ones(self.num_nodes)
    def next(self):
        self.state = np.array([rule(self.state) for rule in self.rules])
    def get_state(self):
        return np.array(self.state)
    def set_state(self, state):
        self.state = np.array(state)

class PropensityNetwork(BoolNetwork):
    def __init__(self, num_nodes, rules, propensities):
        self.num_nodes = num_nodes
        self.rules = rules
        self.state = np.ones(self.num_nodes)
        self.propensities = propensities
    def next(self):
        new_state = [rule(self.state) for rule in self.rules]
        propensities = [prop[node] for prop, node in zip(self.propensities, new_state)]
        uniform = np.random.rand(self.num_nodes)
        self.state = [[a,b][u] for a,b,u in zip(self.state, new_state, uniform < propensities)]

class TanhNetwork:
    def __init__(self, num_nodes, weights=None, learning_rate=0.01):
        self.num_nodes = num_nodes
        self.state = np.ones(self.num_nodes + 1)
        self.last_state = None
        if weights:
            self.weights = weights
        else:
            self.weights = np.zeros((self.num_nodes,self.num_nodes+1))
        self.learning_rate = learning_rate
    def next(self):
        self.last_state = self.state.copy()
        self.tan_state = np.tanh(self.weights.dot(self.state))
        self.state[:-1] = sym_to_asym(self.tan_state)
        self.state[:-1] = np.random.rand(self.num_nodes) < self.state[:-1]
        self.state[:-1] = asym_to_sym(self.state[:-1])
    def train(self, state):
        error = self.state[:-1] - state
        delta_nodes = error * (1-self.tan_state**2)
        self.updates = delta_nodes[np.newaxis].T.dot(self.last_state[np.newaxis])
        self.weights -= self.learning_rate * self.updates
    def set_state(self, state):
        self.state[:-1] = asym_to_sym(state)
    def get_state(self):
        return sym_to_asym(self.state[:-1])

# Returns a random state vector of length n in asymmetric representation.
def random_state(n):
    return np.array([choice([0,1]) for _ in xrange(n)])

def sym_to_asym(a):
    return (np.array(a) + 1)/2

def asym_to_sym(a):
    return 2*np.array(a) - 1

# Test of a very simple deterministic boolean network.
def test1():
    try:
        b = BoolNetwork(4,
                        [lambda n:(n[1]),
                         lambda n:(n[2]),
                         lambda n:(n[3]),
                         lambda n:(n[0])])
        t = TanhNetwork(4)
        while 1:
            b.set_state(random_state(b.num_nodes))
            t.set_state(b.get_state())
            b.next()
            t.next()
            print b.get_state()
            print t.get_state()
            print
            t.train(b.get_state())
    except KeyboardInterrupt, e:
        print
        print t.weights

# Test of a simple propensity network.
def test2():
    try:
        b = PropensityNetwork(4,
                        [lambda n:(n[1]),
                         lambda n:(n[2]),
                         lambda n:(n[3]),
                         lambda n:(n[0])],
                        [(.9,.9)]*4)
        t = TanhNetwork(b.num_nodes)
        while 1:
            b.set_state(random_state(b.num_nodes))
            t.set_state(b.get_state())
            b.next()
            t.next()
            print b.get_state()
            print t.get_state()
            print
            t.train(b.get_state())
    except KeyboardInterrupt, e:
        print
        print t.weights

if __name__ == '__main__':
    test2()
