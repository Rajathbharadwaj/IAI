import numpy as np
from itertools import product


class Node:
    state = np.array([0, 1, 2, 3, 4, 5, 6, 7])

    def __init__(self, column_positions):
        super().__init__()
        self.state = np.array(column_positions)

    def get_cost(self):
        return Node.state_cost(self.state)

    @staticmethod
    def state_cost(state):
        # Return the number of queens being attacked.
        cost = 0
        for index, queen in enumerate(state):
            cost += (np.count_nonzero(state == queen) - 1)
            cost += (np.count_nonzero(abs(state - queen) == abs(np.arange(8) - index)) - 1)
        return (cost // 2)

    def get_child_states(self):
        children = []
        for index, queen in product(range(8), range(8)):
            if (queen != self.state[index]):
                new_state = self.state.copy()
                new_state[index] = queen
                children.append(new_state)
        return children

    def random_child(self):
        new_state = self.state.copy()
        index = np.random.randint(8)
        choices = [a for a in range(8) if a != self.state[index]]
        new_state[index] = np.random.choice(choices)
        return Node(new_state), Node.state_cost(new_state)

    def first_choice_child(self):
        cost = self.get_cost()
        children = self.get_child_states()
        np.random.shuffle(children)
        side_state, side_cost = None, None
        for child in children:
            child_cost = Node.state_cost(child)
            if child_cost < cost:
                return Node(child), child_cost
            if side_state is None and child_cost == cost:
                side_state, side_cost = child, child_cost
        if side_state is not None:
            return Node(side_state), side_cost
        return Node(child), child_cost

    def lowest_cost_child(self):
        children = self.get_child_states()
        costs = [Node.state_cost(child) for child in children]
        best_child_index = np.argmin(costs)
        return Node(children[best_child_index]), costs[best_child_index]

    @staticmethod
    def visualize(state):
        board = [['.' for j in range(8)] for i in range(8)]
        for col, queen in enumerate(state):
            board[queen][col] = 'Q'
        print("-" * 16)
        for line in board: print(" ".join(line))
        print("-" * 16)


