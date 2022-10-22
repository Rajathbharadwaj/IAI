import itertools
import math
import time

from utils import argmax_random_tie, is_in
from game_state import State


class Problem(object):
    def __init__(self, initial_state, goal=None):
        self.initial_state = initial_state
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError


class NQueens(Problem):

    def __init__(self, n, initial):
        self.n = n
        self.initial = initial

    def actions(self, state):
        """Actions move the queen in each column to any of the other,
        unfilled row spots.
        """
        actions = []
        for column in range(self.n):
            for row in [x for x in range(self.n) if x != state[column]]:
                actions.append([column, row])
        return actions

    def result(self, state, move):
        """Makes the given move on a copy of the given state."""
        new_state = state[:]
        new_state[move[0]] = move[1]
        return new_state

    def goal_test(self, state):
        """Check to see if there are no conflicts."""
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

    def conflicted(self, state, row, col):
        """Check to see if placing a queen at (row, col) would conflict with
        anything.
        """
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        return (row1 == row2  # # same row
                or col1 == col2  # # same column
                or row1 - col1 == row2 - col2  # # same \ diagonal
                or row1 + col1 == row2 + col2)  # # same / diagonal

    def value(self, state):

        # Start with the highest possible score (n combined 2).
        value = math.factorial(self.n) / (2 * math.factorial(self.n - 2))

        # Loop through all pairs, subtracting one for every conflicted pair.
        for pair in itertools.combinations(range(self.n), 2):
            if self.conflict(state[pair[0]], pair[0], state[pair[1]], pair[1]):
                value -= 1

        return value


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
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):

        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action,
                         problem.path_cost(self.path_cost, self.state,
                                           action, next_state))
        return next_node

    def solution(self):

        return [node.action for node in self.path()[1:]]

    def path(self):

        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


def hill_climbing(problem):
    current = Node(problem.initial)

    side_step, moves = 0, 0
    while True:
        neighbors = current.expand(problem)

        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors,
                                     key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) <= problem.value(current.state):
            break
        current = neighbor
        moves += 1
    return current.state, moves


def hill_climbing_with_sidestep(problem, sideStep=100):
    current = Node(problem.initial)
    side_step, moves = 0, 0
    while True:
        neighbors = current.expand(problem)

        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors,
                                     key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) > problem.value(current.state):
            return current.state, moves

        if problem.value(neighbor.state) <= problem.value(current.state):
            side_step += 1
            if side_step > sideStep:
                return current.state, moves
        else:
            side_step = 0
        current = neighbor
        moves += 1





if __name__ == '__main__':

    n = 8
    goal = []
    moves_taken = []
    time_taken = []
    for i in range(1001):
        start = time.time()
        p = NQueens(n, [0]*n)
        hill_solution, moves = hill_climbing(p)
        print('Hill-climbing without sideways move:')
        print('\tSolution: ' + str(hill_solution))
        print('\tMoves: ' + str(moves))
        print('\tValue:    ' + str(p.value(hill_solution)))
        print('\tGoal?     ' + str(p.goal_test(hill_solution)))
        print(f'******************* RUN {i}************')
        end = time.time() - start
        time_taken.append(end)
        moves_taken.append(moves)
        goal.append(p.goal_test(hill_solution))

    import numpy as np

    print('********** Without Side ways move')
    moves_taken_avg = np.average(moves_taken)
    time_taken_avg = np.average(time_taken)
    number_of_success = goal.count(True)
    number_of_failure = 1000-number_of_success
    print(moves_taken_avg)
    print(time_taken_avg)
    print(f'Success {number_of_success}')
    print(f'Failure {number_of_failure}')
