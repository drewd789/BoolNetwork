import numpy as np
from random import choice

class BoolNetwork:
    def __init__(self, num_nodes, rules):
        self.num_nodes = num_nodes
        self.rules = rules
        self.state = [True]*self.num_nodes
    def next(self):
        self.state = [rule(self.state) for rule in self.rules]
    def get_state(self):
        return map(lambda x:x*2-1, self.state)
    def set_state(self, state):
        self.state = map(int, (state + 1.)/2.)

class PropensityNetwork:
    def __init__(self, num_nodes, rules, propensities):
        self.num_nodes = num_nodes
        self.rules = rules
        self.state = [True]*self.num_nodes
        self.propensities = propensities
    def next(self):
        print 'old state', self.state
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
        self.state[:-1] = (self.tan_state + 1.)/2.
        self.state[:-1] = np.random.rand(self.num_nodes) < self.state[:-1]
        self.state[:-1] = self.state[:-1]*2. - 1.
    def train(self, state):
        error = self.state[:-1] - state
        delta_nodes = error * (1-self.tan_state**2)
        self.updates = delta_nodes[np.newaxis].T.dot(self.last_state[np.newaxis])
        self.weights -= self.learning_rate * self.updates
    def set_state(self, state):
        self.state[:-1] = state
    def get_state(self):
        return map(int, self.state[:-1])

def random_state(n):
    return np.array([choice([-1.,1.]) for _ in xrange(n)])

# Test of a very simple network.
def test1():
    try:
        b = BoolNetwork(4,
                        [lambda n:(n[1]),
                         lambda n:(n[2]),
                         lambda n:(n[3]),
                         lambda n:(n[0])])
        b.state = [1,0,1,0]
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

def test2():
    try:
        b = PropensityNetwork(4,
                        [lambda n:(n[1]),
                         lambda n:(n[2]),
                         lambda n:(n[3]),
                         lambda n:(n[0])],
                        [(.1,.2), (.3,.4), (.5,.6), (.7,.8)])
        b.state = [1,0,1,0]
        b.next()
    except KeyboardInterrupt, e:
        print
        print t.weights

if __name__ == '__main__':
    test2()
