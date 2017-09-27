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
    def node_probs(self, state):
        probs = np.array([rule(state) for rule in self.rules])
        return probs
    def next(self):
        self.state = self.node_probs(self.state)
    def get_state(self):
        return np.array(self.state)
    def set_state(self, state):
        self.state = np.array(state)
    def transition(self, state):
        num_states = 2**self.num_nodes
        node_probs = self.node_probs(state)
        probs = np.zeros(num_states)
        for next_state in xrange(num_states):
            prod = 1
            for val,prob in zip(map(int,('{0:0%db}'%self.num_nodes).format(next_state)),node_probs):
                if val:
                    prod *= prob
                else:
                    prod *= (1-prob)
            probs[next_state] = prod
        return probs

class PropensityNetwork(BoolNetwork):
    def __init__(self, num_nodes, rules, propensities):
        self.num_nodes = num_nodes
        self.rules = rules
        self.state = np.ones(self.num_nodes)
        self.propensities = propensities
    def node_probs(self, state):
        new_state = [rule(state) for rule in self.rules]
        propensities = [prop[int(node)] for prop, node in zip(self.propensities, new_state)]
        probs = [prop*node+(1-prop)*old for prop, node, old in zip(propensities, new_state, state)]
        return np.array(probs)
    def next(self):
        probs = self.node_probs(self.state)
        uniform = np.random.rand(self.num_nodes)
        self.state = np.array(uniform < probs, dtype=np.float)

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
    def node_probs(self, state):
        tan_state = np.tanh(self.weights.dot(state))
        probs = sym_to_asym(tan_state)
        return probs
    def next(self):
        self.last_state = self.state.copy()
        self.tan_state = np.tanh(self.weights.dot(self.state))
        self.state[:-1] = sym_to_asym(self.tan_state)
        self.state[:-1] = np.random.rand(self.num_nodes) < self.state[:-1]
        self.state[:-1] = asym_to_sym(self.state[:-1])
    def train(self, state):
        error = self.state[:-1] - asym_to_sym(state)
        delta_nodes = error * (1-self.tan_state**2)
        self.updates = delta_nodes[np.newaxis].T.dot(self.last_state[np.newaxis])
        self.weights -= self.learning_rate * self.updates
    def set_state(self, state):
        self.state[:-1] = asym_to_sym(state)
    def get_state(self):
        return sym_to_asym(self.state[:-1]).astype(np.int)

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

def test3():
    b = PropensityNetwork(4,
                    [lambda n:(n[1]),
                     lambda n:(n[2]),
                     lambda n:(n[3]),
                     lambda n:(n[0])],
                    [(.9,.9)]*4)
    print b.transition([1,0,1,0])

if __name__ == '__main__':
    test3()
