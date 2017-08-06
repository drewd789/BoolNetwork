class BoolNetwork:
    def __init__(self, num_nodes, rules):
        self.num_nodes = num_nodes
        self.rules = rules
        self.state = [0]*self.num_nodes
    def next(self):
        self.state = [rule(self.state) for rule in self.rules]
        print self.state

class TanhNetwork:
    def __init__(self, num_nodes, weights=None):
        pass
    def next(self):
        pass

if __name__ == '__main__':
    b = BoolNetwork(1, [lambda nodes:not nodes[0]])
    b.next()
    b.next()
    b.next()
