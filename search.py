"""
Referenced from https://github.com/aimacode/aima-python/blob/master/search.py
"""

from node import Node
from collections import deque
from utils import memoize, argmax_random_tie
from utils import PriorityQueue
from problem import Problem


def breadth_first_graph_search(problem):
    node = Node(problem.initial_state)
    print(node)
    if problem.is_goal(node.state):
        return node
    frontier = deque([node])
    print(frontier)
    explored = set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expand(problem):

            if child.state not in explored and child not in frontier:
                if problem.is_goal(child.state):
                    return child
                frontier.append(child)

    return None


def depth_first_graph_search(problem):
    frontier = [(Node(problem.initial_state))]

    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)
    return None


def best_first_graph_search(problem: Problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial_state)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


def hill_climbing(problem):
    current = Node(problem.initial_state)
    print(type(current))
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors, key=lambda node: problem.value(node))
        if problem.value(neighbor) <= problem.value(current.state):
            break
        current = neighbor
    return current.state
