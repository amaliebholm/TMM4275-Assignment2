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

    # Initializing the search lists
    fringe = [((i_start, j_start), list(), 0, heuristic(i_start, j_start))]

    visited = {}  # empty dictionary of nodes who have been visited

    while True:
        # first state
        current_state = fringe.pop(0)

        # checking if we are in the goal position:
        (i, j) = current_state[0]
        if input_matrix[i][j] == 3:
            path = [current_state[0]] + current_state[1]
            path.reverse()
            return path
        # Setting the cost
        visited[(i, j)] = current_state[2]
        # check for if the path has a viable turn, (has to be able to turn with a radius of 2m).
        # The neighbor nodes needs to form a freespace kvadrat for a turn.

        # exploring neighbors:
        neighbors = list()
        if i > 0 and input_matrix[i-1][j] > 0:
            neighbors.append((i-1, j))
        if i < height and input_matrix[i+1][j] > 0:
            neighbors.append((i+1, j))
        if j > 0 and input_matrix[i][j-1] > 0:
            neighbors.append((i, j-1))
        if j < width and input_matrix[i][j+1] > 0:
            neighbors.append((i, j+1))
        print("Current state: ", current_state)
        for n in neighbors:
            next_cost = current_state[2] + 1
            if n in visited and visited[n] >= next_cost:
                continue
            fringe.append((n, [current_state[0]] + current_state[1],
                           next_cost, heuristic(n[0], n[1])))

        # resort the list (SHOULD use a priority queue here to avoid re-sorting all the time)
        fringe.sort(key=comp)
        print("Sorted path: ", fringe)

    return path


dummy_matrix = [[0, 0, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 5, 5, 3, 0],
                [0, 0, 5, 5, 5, 0, 0, 0],
                [0, 1, 2, 0, 1, 1, 1, 0],
                [0, 1, 0, 0, 0, 0, 0, 0]]

dummy_matrix2 = [[0, 2, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 1, 1, 1, 1, 0],
                 [0, 1, 1, 1, 0, 1, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 0, 5, 5, 0, 0],
                 [0, 0, 5, 5, 5, 0, 0, 0],
                 [0, 1, 1, 0, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 3, 0, 0]]

if __name__ == "__main__":
    astar(dummy_matrix)
    astar(dummy_matrix2)
