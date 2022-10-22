import itertools
import math
import time

from utils import argmax_random_tie, is_in



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


