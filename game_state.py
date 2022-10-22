from operator import sub, add
from rich.pretty import pprint
from problem import Problem
from node import Node

MISSIONARY_IDX = 0
CANNIBAL_IDX = 1
BOAT_IDX = 2


class State:
    def __init__(self, left_side):
        self.left_side = left_side
        self.boat_capacity = 2

    def __repr__(self):
        return 'L: ' + str(self.left_side) + '   R: ' + str(self.right_side)

    def __str__(self):
        return 'L: ' + str(self.left_side) + '   R: ' + str(self.right_side)

    def __eq__(self, other):
        return self.left_side == other.left_side

    def __lt__(self, other):
        return self.left_side < other.left_side

    def __add__(self, other):
        if not isinstance(other, tuple):
            raise TypeError('Cannot add state and {}'.format(type(other)))
        new_state_tuple = tuple(map(add, self.left_side, other))
        return State(new_state_tuple)

    def __sub__(self, other):
        if not isinstance(other, tuple):
            raise TypeError('Cannot subtract {} from state'.format(type(other)))
        new_state_tuple = tuple(map(sub, self.left_side, other))
        return State(new_state_tuple)

    def __hash__(self):
        return hash(self.left_side)

    @property
    def right_side(self):
        total = (3, 3, 1)
        return tuple(map(sub, total, self.left_side))

    @property
    def num_missionaries(self):
        return self.left_side[MISSIONARY_IDX]

    @property
    def num_cannibals(self):
        return self.left_side[CANNIBAL_IDX]

    @property
    def num_boat(self):
        return self.left_side[BOAT_IDX]

    @property
    def missionaries_are_safe(self):
        rs = State(self.right_side)

        return (self.num_missionaries == 0 or self.num_missionaries >= self.num_cannibals) and \
               (rs.num_missionaries == 0 or rs.num_missionaries >= rs.num_cannibals)

    @property
    def is_valid(self):
        rs = State(self.right_side)

        num_missionaries_valid = (0 <= self.num_missionaries <= 3) and (0 <= rs.num_missionaries <= 3)
        num_cannibals_valid = (0 <= self.num_cannibals <= 3) and (0 <= rs.num_cannibals <= 3)
        num_boat_valid = (0 <= self.num_boat <= 1) and (0 <= rs.num_boat <= 1)

        return num_missionaries_valid and num_cannibals_valid and num_boat_valid and self.missionaries_are_safe


class MissionariesAndCannibals(Problem):

    def __init__(self):
        initial_state = State((3, 3, 1))
        goal_test = State((0, 0, 0))

        self.all_possible_actions = [
            (1, 0, 1),
            (2, 0, 1),
            (0, 1, 1),
            (0, 2, 1),
            (1, 1, 1)
        ]

        super().__init__(initial_state, goal_test)

    def actions(self, node):
        all_nodes = [self.__perform_action(node, action) for action in self.all_possible_actions]
        valid_nodes = filter(lambda n: n.state.is_valid, all_nodes)
        return [n.action for n in valid_nodes]

    def result(self, node, action):
        if action not in self.actions(node):
            raise Exception('action not in actions!')

        return self.__perform_action(node, action)

    @staticmethod
    def __perform_action(node, action):
        if node.depth % 2 == 0:
            state = node.state - action
        else:
            state = node.state + action
        return Node(state, node, action)

    @staticmethod
    def h(node):
        """
        :param node:
        :return: returns the heuristic as follows
        h(n) = No. of people in the current side / boat capacity
        """
        return (node.state.num_missionaries + node.state.num_cannibals) / node.state.boat_capacity
