import math
import numpy as np

# ------ Global variables -------

global_path = []


def astar(input_matrix):
    path = []

    width = len(input_matrix[0])
    height = len(input_matrix)

    # ---- finding the start coordinate and goal coordiante -----
    # The feeder is defined as the  start node: 2, and the last feeding station is defined as the goal: 3.
    (i_start, j_start) = [[(i, j) for j, cell in enumerate(
        row) if cell == 2] for i, row in enumerate(input_matrix) if 2 in row][0][0]
    # and take the goal position (used in the heuristic)
    (i_goal, j_goal) = [[(i, j) for j, cell in enumerate(
        row) if cell == 3] for i, row in enumerate(input_matrix) if 3 in row][0][0]

    print("Start position: ", i_start, j_start)
    print("Goal position: ", i_goal, j_goal)

    def heuristic(i, j): return abs(i_goal - i) + abs(j_goal - j)
    def comp(state): return state[2] + state[3]  # get the total cost

    # small variation for easier code, state is (coord_tuple, previous, path_cost, heuristic_cost)
    fringe = [((i_start, j_start), list(), 0, heuristic(i_start, j_start))]

    visited = {}  # empty dictionary of nodes who have been visited

    return path


dummy_matrix = [[0, 0, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 5, 5, 3, 0],
                [0, 0, 5, 5, 5, 0, 0, 0],
                [0, 1, 2, 0, 1, 1, 1, 0],
                [0, 1, 0, 0, 0, 0, 0, 0]]


if __name__ == "__main__":
    astar(dummy_matrix)
