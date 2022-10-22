import search, node, run

problem = run.NQueensProblem(8)
problem.initial_state

nn = node.Node(problem.initial_state)
search.hill_climbing(problem)
