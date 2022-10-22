from search import breadth_first_graph_search, depth_first_graph_search, astar_search, best_first_graph_search, hill_climbing
from game_state import MissionariesAndCannibals
from rich.pretty import pprint
from nqueens import NQueensProblem


def main():
    # instantiation of the problem
    problem_bfs = MissionariesAndCannibals()
    problem_dfs = MissionariesAndCannibals()
    problem_gbfs = MissionariesAndCannibals()
    problem_astar = MissionariesAndCannibals()

    pprint('Starting with BFS.....')
    result_bfs = breadth_first_graph_search(problem_bfs)
    if result_bfs:
        print_result(result_bfs)

    pprint('Starting with DFS.....')
    result_dfs = depth_first_graph_search(problem_dfs)

    if result_dfs:
        print_result(result_dfs)

    pprint('Starting with Greedy BFS',)
    result_gbfs = best_first_graph_search(problem_gbfs, lambda node: node.path_cost, display=True)

    if result_gbfs:
        print_result(result_gbfs)

    pprint('Starting with A*')
    result_astar = astar_search(problem_gbfs, display=True)

    if result_gbfs:
        print_result(result_astar)


# display the results gracefully
def print_result(result):
    lst = [(1, 0, 1),
            (2, 0, 1),
            (0, 1, 1),
            (0, 2, 1),
            (1, 1, 1)]
    for i, node in enumerate(result.path):
        if node.depth % 2 == 0:
            sign = 'L'
        else:
            sign = 'R'

        # structural integrity
        if node.action == lst[0]:
            val = '1M0C1B'
        elif node.action == lst[1]:
            val = '2M0C1B'
        elif node.action == lst[2]:
            val = '0M1C1B'
        elif node.action == lst[3]:
            val = '0M2C1B'
        elif node.action == lst[4]:
            val = '1M1C1B'
        else:
            val = ''

        pprint('{} -> {}'.format(val, sign))
        pprint('depth: {}'.format(node.depth))
        pprint('At left we have {}'.format(node.state.left_side))
        pprint('------------')


if __name__ == '__main__':
    main()
