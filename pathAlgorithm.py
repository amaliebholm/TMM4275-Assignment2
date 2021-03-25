from scipy.spatial.distance import cdist
import numpy as np
import numpy
import math
import sys
import matplotlib.pyplot as plt
# math library made for this algorithmf
from calculations import Calculations as calc
from scipy.spatial import distance
import sympy


# The path algorithm takes in a list of attatchment points where the first point is the location of the feeder.
# It then creates a path between each attatchment point and turns with a radius of 2m.
# Using A* proved to be inefficent as we are not looking for the shortest path.


# taking in three lists: Attatchment points, desired locations, and obsticles

# Input-format = [[[x,y],h],[[x,y],h],[[x,y],h],[[x,y],h],....,[[x,y],h],]
# Output-format: List = [[[x,y],h],[[x,y]],[[x,y]],[[x,y],h],....]


class pathAlgorithm:

    def __init__(self, turn_radius, start, end):
        self.turn_radius = turn_radius  # 2m (2000) is the fixed radius
        self.start = start  # feeder
        self.end = end  # last attatchment point of the rail

    """
    gets the center (X, Y) of the the curve for the specified (in constructor) radius
    dir, is a direction - (-1):clockwise/(+1)counter clockwise to
    decide which direction is the turn.
    """

    def closest_node(self, node, nodes):
        return nodes[cdist([node], nodes).argmin()]

    def bestPath(self, data, obsticles):
        obsticles = obsticles
        best_path = []
        index = 0
        start_position = data[index]
        best_path.append(start_position)
        data.remove(data[index])
        updated_data = data
        # print("Updated: ", data)

        dummy_list = []
        for i in updated_data:
            dummy_list.append(i)
        # print("DUMMY: ", dummy_list)

        for data_point in enumerate(updated_data):

            if data_point is not None:
                current_point = best_path[-1]
                # print("CURRENT INDEX:  ", current_point)
                # print("BEFORE REMOVING: ", updated_data)

                if current_point in updated_data:
                    dummy_list.remove(current_point)
                    # print("AFTER REMOVING: ", dummy_list)

                # finds the closest point.
                if len(dummy_list) != 0:
                    point = self.closest_node(current_point, dummy_list)
                    if point not in best_path:
                        best_path.append(point)
                        # print("CLOSEST AND ADDED POINT: ", point)
                else:
                    pass
            else:
                pass

        # next_position = path[index]
            print("PATH: ", best_path)

        return self.railAlgorithm(best_path)

   # Function for finding the center of the fictive circle given the current position, the next and the direction.
    def findCenter(self, current_position, next_position, direction):
        # Link:

        delta_x = next_position[0] - current_position[0]  # x_1 - x_2
        delta_y = next_position[1] - current_position[1]  # y_1 - y_2
        psi = math.atan2(delta_y, delta_x)  # arctanget
        psi += direction * math.pi / 2

        x_shifted = self.turn_radius * math.cos(psi)
        y_shifted = self.turn_radius * math.sin(psi)

        center = (next_position[0] + x_shifted, next_position[1] + y_shifted)

        return center

    # Function for getting the distance between two points (vector)

    def getDistance(self, point1, point2):
        delta_x = point2[0] - point1[0]
        delta_y = point2[1] - point1[1]

        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        return distance

    # Function for checking where the next point lies in reference to the current position.

    def normalizedVector(self, point, distance):

        normalizedVector = [point[0]/distance, point[1]/distance]

        print("Normalized Vector: ", normalizedVector)

        return normalizedVector

    def directonalVector(self, point1, point2):

        dirVec = [point1[0]-point2[0], point1[1] - point2[1]]

        print("Direction Vector: ", dirVec)

        return dirVec

    # Fucntion for getting the angle between two vectors

    def angleBetweenVectors(self, vector1, vector2):

        unit_vector1 = np.divide(vector1, np.linalg.norm(vector1))
        unit_vector2 = np.divide(vector2, np.linalg.norm(vector2))

        dot_product = np.dot(unit_vector1, unit_vector2)
        psi = numpy.arccos(dot_product)
        print("PSI: ", psi)

        return psi

    # Function for finding the arc angle
    def arcInclusiveAngle(self, angleVectors):
        psi = angleVectors
        psi = sympy.cot((psi/2))
        print("PSI/2: ", psi)
        psi = math.radians(psi)
        alpha = numpy.arcsin(psi)
        alpha = 2*alpha
        print("ALPHA: ", alpha)
        return alpha

    def InLineOfSight(self, point1, point2, point3):
        # Link:
        LOF = (point1[1] - point2[1]) * point3[0] + \
            (point2[0] - point1[0]) * point3[1] + \
            (point1[0] * point2[1] - point2[0] * point1[1])

        direction = 0

        if LOF > 0:
            direction = 1
            return direction
        elif LOF < 0:
            direction = -1
            return direction
        else:
            return direction

    def railAlgorithm(self, best_path):
        index = 0
        curved_path = []

        # initialize
        '''
        vector = [best_path[0], best_path[1]]
        curved_path.append(vector)
        '''
        print("THE BEST PATH: ", best_path)
        print("THE curved path: ", curved_path)
        '''
        current_position = curved_path[index][0]
        next_position = curved_path[index][1]
        '''

        if len(curved_path) > 2:
            previous_position = curved_path[index - 1]
        else:
            pass

        while index < len(best_path)-1:
            index += 1
            '''
            current_position = curved_path[index][0]
            next_position = curved_path[index][1]
            '''
            print("ITERATION: ", index)
            print(best_path[index-1])
            print(best_path[index])
            print(best_path[index+1])

            if index == 1:
                vector = [best_path[index-1], best_path[index]]
                curved_path.append(vector)

            else:
                direction = self.InLineOfSight(
                    curved_path[-1][0], curved_path[-1][1], best_path[index-1])
                print("DIRECTION: ", direction)
                # Check for turn
                # no turn --> Straight line
                if (len(curved_path[-1]) == 2) and direction == 0:
                    vector = [best_path[index-1], best_path[index]]
                    curved_path.append(vector)

                else:  # Turn
                    '''
                    vector = [best_path[index], best_path[index+1]]
                    curved_path.append(vector)
                    '''
                    print(curved_path[-1][0])
                    print(curved_path[-1][1])
                    print(best_path[index-1])

                    if len(curved_path[-1]) == 2:

                        direction = self.InLineOfSight(
                            curved_path[-1][0], curved_path[-1][1], best_path[index - 1])

                        center = self.findCenter(
                            curved_path[-1][0], curved_path[-1][1], direction)

                        psi = self.angleBetweenVectors(
                            curved_path[-1][1], best_path[index-1])

                        # The angle between the center and  the  two endpoints of the arc
                        arcInteriorAngle = self.arcInclusiveAngle(psi)

                        directionVector = self.directonalVector(
                            best_path[index], best_path[index-1])

                     # Calculating distance along one of the vectors to the interception point on the arc. (End of arc)

                        distance_to_point_end_of_arc = self.turn_radius * \
                            sympy.cot(psi/2)

                        print("Distance to end: ", distance_to_point_end_of_arc)

                        my_new_list = [
                            i * distance_to_point_end_of_arc for i in directionVector]

                        end_point_of_arc = best_path[index-1] + my_new_list

                        print("END POINT ON CURVE: ", end_point_of_arc)
                    else:
                        pass

        return curved_path

    # Function for getting the intercepting tangent on the arc


PathAlgorithm = pathAlgorithm(2000, [0, 0], [-2000, -2000])

data = [[0, 0], [0, 1700], [2500, 4000], [3500, -4000],
        [10000, 6000], [-1000, 5900], [-2000, -2000]]

# desired_locations = [(500, 500), (2000, 3000), (2700, 4000)]
obsticles = []
path = PathAlgorithm.bestPath(data, obsticles)
print(path)


'''
path = [[[0, 0, 0], [0, 1700, 0]], [[2500, 4000, 0], [
    3500, -4000, 0]], [[10000, 6000, 0], [1000, 5900]]]
'''

x = []
y = []

pointlist = [[0, 0], [0, 10000], [-2000, 12000], [-10000, 12000],
             [-11414.21356, 11414.21356], [-13414.21356, 9414.21356]]
'''
for i in path:
    x.append(i[0])
    print(x)
    y.append(i[1])
    print(y)

print(x)
print(y)

plt.scatter(x, y)
plt.plot(x, y)
plt.show()
'''
# path = [[0, 0, 0], [100, 0, 0], [100, 400, 0], [100, 400, 0], [0, 400, 0]]
