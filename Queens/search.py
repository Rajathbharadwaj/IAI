from node import Node


class HillClimbing:
    def __init__(self, state):
        super().__init__()
        self.start_node = Node(state)

    def steepest_ascent(self, max_sidesteps=0):
        current_node = self.start_node
        current_cost = current_node.get_cost()
        moves = 0;
        side_steps = 0
        while True:
            next_child, next_cost = current_node.lowest_cost_child()
            if (next_cost > current_cost):
                return current_node.state, current_cost, (next_cost == current_cost), moves
            if (next_cost == current_cost):
                side_steps += 1
                if side_steps > max_sidesteps:
                    return current_node.state, current_cost, (next_cost == current_cost), moves
            else:
                side_steps = 0
            current_node, current_cost = next_child, next_cost
            moves += 1

    def first_choice(self, max_sidesteps=0):
        current_node = self.start_node
        current_cost = current_node.get_cost()
        moves = 0;
        side_steps = 0
        while True:
            next_child, next_cost = current_node.first_choice_child()
            if (next_cost > current_cost):
                return current_node.state, current_cost, (next_cost == current_cost), moves
            if (next_cost == current_cost):
                side_steps += 1
                if side_steps > max_sidesteps:
                    return current_node.state, current_cost, (next_cost == current_cost), moves
            else:
                side_steps = 0
            current_node, current_cost = next_child, next_cost
            moves += 1


