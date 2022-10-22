"""
Referenced from https://github.com/aimacode/aima-python/blob/master/search.py
"""


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self)]

    def child_node(self, problem, action):
        next_state = problem.result(self, action)
        # next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_state

    @property
    def solution(self):
        return [node.action for node in self.path[1:]]

    @property
    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state == other.state and self.action == other.action \
                   and self.depth == other.depth and self.parent == other.parent
        else:
            return False

    def __hash__(self):
        return hash(self.state)
