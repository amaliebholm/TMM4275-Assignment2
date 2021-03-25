from scipy.spatial.distance import cdist
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
# math library made for this algorithmf
from calculations import Calculations as calc
from scipy.spatial import distance


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
        print("DUMMY: ", dummy_list)

        for data_point in enumerate(updated_data):

            if data_point is not None:
                current_point = best_path[-1]
                print("CURRENT INDEX:  ", current_point)
                print("BEFORE REMOVING: ", updated_data)

                if current_point in updated_data:
                    dummy_list.remove(current_point)
                    print("AFTER REMOVING: ", dummy_list)

                # finds the closest point.
                if len(dummy_list) != 0:
                    point = self.closest_node(current_point, dummy_list)
                    if point not in best_path:
                        best_path.append(point)
                        print("CLOSEST AND ADDED POINT: ", point)
                else:
                    pass
            else:
                pass

        # next_position = path[index]
            print("PATH: ", best_path)

        return best_path

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

        return normalizedVector

    def directonalVector(self, point1, point2):

        dirVec = [point1[0]-point2[0], point1[1] - point2[1]]

        return dirVec

    # Fucntion for getting the angle between two vectors

    def angleBetweenVectors(self, vector1, vector2):

        unit_vector1 = np.divide(vector1, np.linalg.norm(vector1))
        unit_vector2 = np.divide(vector2, np.linalg.norm(vector2))

        dot_product = np.dot(unit_vector1, unit_vector2)
        psi = np.arccos(dot_product)

        return psi

    # Function for finding the arc angle
    def arcInclusiveAngle(self, angleVectors):
        psi = angleVectors
        alpha = 2*np.arcsin((psi/2))

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

    # Function for getting the intercepting tangent on the arc

    def getTangentPointM(self, center, point3, point2, direction):

        distance = self.getDistance(center, point3)
        print(distance)

        angle_point3_center_M = math.acos(self.turn_radius / distance)

        N = [center[0], point3[1]]
        angle_point3_center_N = math.asin(
            (point3[0] - N[0]) / distance)  # arc sine

        if angle_point3_center_N < 0:
            angle_point3_center_N *= -1
        angleRotation = 0

        # Mapping which qaudrant N is located in
        # I quadrant:
        if (point3[0] - center[0] > 0) and (point3[1] - center[1] > 0):
            if direction > 0:
                angleRotation = -math.pi / 2 + angle_point3_center_M + angle_point3_center_N
                angleRotation *= -1
            else:
                angleRotation = math.pi / 2 + angle_point3_center_M - angle_point3_center_N

        # II quadrant:
        if (point3[0] - center[0] < 0) and (point3[1] - center[1] > 0):
            if direction < 0:
                angleRotation = math.pi / 2 + angle_point3_center_M + angle_point3_center_N
            else:
                angleRotation = math.pi / 2 - \
                    (angle_point3_center_M - angle_point3_center_N)

        # III quadrant:
        if (point3[0] - center[0] < 0) and (point3[1] - center[1] < 0):
            if direction > 0:
                angleRotation = 1.5 * math.pi - \
                    (angle_point3_center_M + angle_point3_center_N)
            else:
                angleRotation = 1.5 * math.pi + \
                    (angle_point3_center_M - angle_point3_center_N)

        # IV quadrant:
        if (point3[0] - center[0] > 0) and (point3[1] - center[1] < 0):
            if direction > 0:
                angleRotation = math.pi / 2 + \
                    (angle_point3_center_M - angle_point3_center_N)
                angleRotation *= -1
            else:
                angleRotation = -math.pi / 2 + angle_point3_center_M + angle_point3_center_N

        # Getting the coordinates of M:
        M = self.pointOnArc(center, angleRotation)

        return M

    # function for fetching a point on a arc
    def pointOnArc(self, center, angle):

        x_shifted = self.turn_radius * math.cos(angle)
        y_shifted = self.turn_radius * math.sin(angle)

        arcPoint = [center[0] + x_shifted, center[1] + y_shifted]
        print("The point on arc: ", arcPoint)
        return arcPoint

    def getStartEndAng(self, center, point1, point2):
        # Find the first point - point1 or point2 - w.r.t. the quaters of the circle for given center.
        angle_1 = self.angleBetween(center, (center[0] + 5, center[1]), point1)
        angle_2 = self.angleBetween(center, (center[0] + 5, center[1]), point2)
        # Check if the point is below the center --> two arcs to be generated (to be processed at the caller side).

        # IV quadrant - incoming
        if center[1] > point1[1] and center[0] < point1[0]:
            angle_1 *= -1
        # IV quadrant - outgoing
        if center[1] > point2[1] and center[0] < point2[0]:
            angle_2 *= -1

        # III quadrant - incoming
        if center[1] > point1[1] and center[0] > point1[0]:
            angle_1 = 2 * math.pi - angle_1
        # III quadrant - outgoing
        if center[1] > point2[1] and center[0] > point2[0]:
            angle_2 = 2 * math.pi - angle_2

        if angle_1 < angle_2:
            return (angle_1, angle_2)
        else:
            return (angle_2, angle_1)

    def angleBetween(self, center, point1, point2):
        vector1 = (point1[0] - center[0], point1[1] - center[1])
        vector2 = (point2[0] - center[0], point2[1] - center[1])

        scalar = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        length_vector1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
        length_vector2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

        angle = math.acos(scalar / (length_vector1 * length_vector2))

        return angle

    def algorithm(self, attatchment_locations):
        path = []
        tracker = 0
        # z- direction, is always zero since it is the roof stags that are scaled while the rail stays leveled.
        z = 0

        # not correct as locations are added at the end
        # all_locations = attatchment_locations + desired_locations

        # Main loop of the algorithm, runs until the whole list of attatchment points have been initilized.

        while tracker < len(attatchment_locations)-1:

            # initilizing the first line
            # the first and second attatchment points
            # Keeping track of previous, current and next position
            current_position = attatchment_locations[tracker]
            next_position = attatchment_locations[tracker + 1]
            previous_position = attatchment_locations[tracker - 1]
            tracker += 1

            vector = [current_position, next_position]
            path.append(vector)
            print("Path: ", path[-1])

            # Finding the best path

            # checking for turn and what direction the turn is
            direction = self.InLineOfSight(
                path[-1][0], path[-1][1], current_position)

            # On the same line
            if len(path[-1]) == 2 and direction != 0:
                vector = [current_position, next_position]
                path.append(vector)

            # if direction == 1 and path[-1][0][1] > path[-1][1][1]:

            else:

                # initializing necessery helper functions:

                center = self.findCenter(
                    path[-1][0], path[-1][1], direction)

                psi = self.angleBetweenVectors(path[-1][0], path[-1][1])

                # The angle between the center and  the  two endpoints of the arc
                arcInteriorAngle = self.arcInclusiveAngle(psi)

                dirVec = self.directonalVector(path[-1][0], path[-1][1])

                PointOnArc = self.getTangentPointM(
                    center, current_position, path[-1][1], direction)

                startEndAngles = self.getStartEndAng(
                    center, path[-1][1], PointOnArc)

                if (direction == 1 and path[-1][0][1] > path[-1][1][1]):

                    if (startEndAngles[0] < 0):  # Outgoing from IV quater
                        # newEndAng = 2 * math.pi + startEndAngles[0]
                        # newStartAng = startEndAngles[1]
                        pointOnCurve = [path[-1][1], PointOnArc]
                        print("POSITIONS: ", path[-1][0], path[-1][1])
                        print("POINT ON CURVE: ", pointOnCurve)
                        path.append(pointOnCurve)

                    elif center[1] > current_position[1]:

                        curve = [path[-1][1], PointOnArc]
                        path.append(curve)

                    else:
                        newStartAng = startEndAngles[1]
                        newEndAng = startEndAngles[0]

                        pointOnCurve = [path[-1][1], PointOnArc]
                        print("POINT ON CURVE: ", pointOnCurve)
                        path.append(pointOnCurve)

                    # Incoming line to IV quater
                elif (direction > 0) and (path[-1][0][1] < path[-1][1][1]):
                    # redifine the angles first
                    newStartAng = 0
                    newEndAng = 0
                    # Outgoing from IV quater
                    if ((startEndAngles[0] < 0) and (startEndAngles[1] < 0)):
                        # Normal order, but in +scale
                        newStartAng = 2 * math.pi + startEndAngles[0]
                        newEndAng = 2 * math.pi + startEndAngles[1]

                        pointOnCurve = [path[-1][1], PointOnArc]
                        print("POINT ON CURVE: ", pointOnCurve)
                        path.append(pointOnCurve)
                    # Not only the IV quater, but other quater(s) as well --> aux. curve needed
                    elif startEndAngles[0] < 0:
                        newStartAng = startEndAngles[0] + 2 * math.pi
                        newEndAng = startEndAngles[1]

                        pointOnCurve = [path[-1][1], PointOnArc]
                        print("POINT ON CURVE: ", pointOnCurve)
                        path.append(pointOnCurve)

                # Incoming line to I quater, but clockwise rotation
                elif (direction < 0) and (path[-1][0][1] > path[-1][1][1]):
                    if startEndAngles[0] < 0:

                        pointOnCurve = [path[-1][1], PointOnArc]
                        path.append(pointOnCurve)
                        print("POINT ON CURVE: ", pointOnCurve)
                    else:

                        pointOnCurve = [path[-1][1], PointOnArc]
                        path.append(pointOnCurve)
                        print("POINT ON CURVE: ", pointOnCurve)

                elif (startEndAngles[0] < 0):

                    pointOnCurve = [path[-1][1], PointOnArc]
                    path.append(pointOnCurve)

                else:

                    pointOnCurve = [path[-1][1], PointOnArc]
                    path.append(pointOnCurve)
                    # Add the line (PointOnArc, the point)
                    vector = [PointOnArc, attatchment_locations[tracker]]
                    path.append(vector)

        return path


PathAlgorithm = pathAlgorithm(2000, [0, 0], [-2000, -2000])

data = [[0, 0], [0, 1700], [2500, 4000], [3500, -4000],
        [10000, 6000], [-1000, 5900], [-2000, -2000]]

# desired_locations = [(500, 500), (2000, 3000), (2700, 4000)]

path = PathAlgorithm.algorithm(data)
print(path)

'''
path = [[[0, 0, 0], [0, 1700, 0]], [[2500, 4000, 0], [
    3500, -4000, 0]], [[10000, 6000, 0], [1000, 5900]]]
'''

x = []
y = []

pointlist = [[0, 0], [0, 10000], [-2000, 12000], [-10000, 12000],
             [-11414.21356, 11414.21356], [-13414.21356, 9414.21356]]

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

# path = [[0, 0, 0], [100, 0, 0], [100, 400, 0], [100, 400, 0], [0, 400, 0]]
