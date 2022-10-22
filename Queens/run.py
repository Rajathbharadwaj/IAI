from tqdm import tqdm

from search import *
import time
from test_nq import hill_climbing, NQueens

if __name__ == '__main__':

    n = 8
    goal = []
    moves_taken = []
    time_taken = []
    print("Running Hill Climbing without side ways move:")
    for i in tqdm(range(1001)):
        start = time.time()
        p = NQueens(n, [0] * n)
        hill_solution, moves = hill_climbing(p)
        end = time.time() - start
        time_taken.append(end)
        moves_taken.append(moves)
        goal.append(p.goal_test(hill_solution))

    goal_withss = []
    moves_taken_withss = []
    time_taken_withss = []
    print("Running First-Choice (with 100 sidesteps):")
    for i in tqdm(range(1001)):
        start = time.time()
        hill = HillClimbing(tuple([0] * n))
        end_state, end_cost, is_plateau, moves = hill.first_choice(100)
        status = True if not is_plateau else False
        end = time.time() - start
        time_taken_withss.append(end)
        moves_taken_withss.append(moves)
        goal_withss.append(status)


    import numpy as np

    print('********** Without Side ways move')
    moves_taken_avg = np.average(moves_taken)
    time_taken_avg = np.average(time_taken)
    number_of_success = goal.count(True)
    number_of_failure = 1000-number_of_success
    print(f'Average Moves {moves_taken_avg}')
    print(f'Average Time {time_taken_avg}')
    print(f'Success {number_of_success}')
    print(f'Failure {number_of_failure}')
    print(f'Time taken to complete when success {number_of_success*time_taken_avg}')

    print('********** With Side ways move')
    moves_taken_avg_withss = np.average(moves_taken_withss)
    time_taken_avg_withss = np.average(time_taken_withss)
    number_of_success_withss = goal_withss.count(True)
    number_of_failure_withss = 1000-number_of_success_withss
    print(f'Average Moves {moves_taken_avg_withss}')
    print(f'Average Time {time_taken_avg_withss}')
    print(f'Success {number_of_success_withss}')
    print(f'Failure {number_of_failure_withss}')
    print(f'Time taken to complete when success {number_of_success_withss*time_taken_avg_withss}')