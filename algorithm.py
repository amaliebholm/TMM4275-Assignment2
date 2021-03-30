import numpy as np
import math
import sys
import matplotlib.pyplot as plt
# math library made for this algorithm
from calculations import Calculations as calc
from scipy.spatial import distance
from scipy.spatial.distance import cdist


def closest_node(node, nodes):
    return nodes[cdist([node], nodes).argmin()]


def algorithm(data, obsticles):
    obsticles = obsticles
    path = []
    index = 0
    start_position = data[index]
    original_data = data
    path.append(start_position)
    data.remove(data[index])
    updated_data = data
    # print("Updated: ", data)

    dummy_list = []
    for i in updated_data:
        dummy_list.append(i)
    print("DUMMY: ", dummy_list)

    for data_point in enumerate(updated_data):

        if data_point is not None:
            current_point = path[-1]
            print("CURRENT INDEX:  ", current_point)
            '''
            if current_point[1] not in path:
                path.append(current_point[1])
            '''

            print("BEFORE REMOVING: ", updated_data)

            if current_point in updated_data:
                dummy_list.remove(current_point)
                print("AFTER REMOVING: ", dummy_list)

            # finds the closest point.
            if len(dummy_list) != 0:
                point = closest_node(current_point, dummy_list)
                if point not in path:
                    path.append(point)
                    print("CLOSEST AND ADDED POINT: ", point)
            else:
                pass
        else:
            pass

    # next_position = path[index]
    print("PATH: ", path)
    return path

    def interceptorCheck(point1, point2, point3):
        segment1 = [point1, point2]
        segment2 = [point2, point3]

        I1 = [min(point1[0], point2[0]), max(point1[0], point2[0])]
        I2 = [min(point2[0], point3[0]), max(point3[0], point3[1])]
        Ia = [max(min(point1[0], point1[1]), min(point2[0], point2[1])), min(
            max(point2[0], point2[1]), max(Xpoint3[0], point3[1]))]

        if (max(X1, X2) < min(X3, X4)):
            return False  # There is no mutual abcisses

    return

    def checkForObsticles(path, obsticles):

        # Neeed to check if the shortest lines between out points intercept any obsticles.
        return

    def lineCrossCheck(self, line, obstacle):
        # obstacle to come in format (x, y, length, width, orientation)
        # lets set x,y to be upper left corner of a rectangle
        # for 0 orientation.

        pointA = line[0]
        pointB = line[1]

        # Find all the vertices of the rectangle.
        # Check if they have a common point in-between vertices of rectangle.
        # For instance, there is a rectangle KLNM.
        # Check slide 22 for lables:
        # --> http://lobov.biz/academia/kbe-project/200316

        # A solution:
        # For KL: Angle KAL = KAB + BAL ? or For LM: Angle LAM = LAB + BAM ?
        # For LN: Angle LAN = LAB + BAN ?
        # In other words AB passes in-between either KL or LM.

        # Calculate K, L, M, N points
        orientationRad = obstacle[4] / 180 * math.pi
        pointK = (obstacle[0], obstacle[1])
        pointL = (
            obstacle[0] + obstacle[2] * math.cos(orientationRad), obstacle[1] + obstacle[2] * math.sin(orientationRad))
        pointM = (
            obstacle[0] + obstacle[3] * math.sin(orientationRad), obstacle[1] - obstacle[3] * math.cos(orientationRad))
        # Rotation of -90 degrees of radius width from point L --> pointN
        pointN = (pointL[0] + obstacle[3] * math.cos(-math.pi / 2 + orientationRad),
                  pointL[1] + obstacle[3] * math.sin(-math.pi / 2 + orientationRad))

        print("K: ", pointK)
        print("L: ", pointL)
        print("N: ", pointN)
        print("M: ", pointM)

        # Rounding error will be hit --> making this method unreliable?
        # Let's see.
        angKAL = self.angVia3Points(pointA, pointK, pointL)
        angKAB = self.angVia3Points(pointA, pointK, pointB)
        angBAL = self.angVia3Points(pointA, pointB, pointL)
        difKAL = angKAL - (angKAB + angBAL)  # Is it 0?

        print("Check angles dif for KAL:", str(difKAL))

        angLAM = self.angVia3Points(pointA, pointL, pointM)
        angLAB = self.angVia3Points(pointA, pointL, pointB)
        angBAM = self.angVia3Points(pointA, pointB, pointM)
        difLAM = angLAM - (angLAB + angBAM)  # Is it 0?

        print("Check angles dif for LAM:", str(difLAM))

        angLAN = self.angVia3Points(pointA, pointL, pointM)
        # angLAB is calculated already
        angBAN = self.angVia3Points(pointA, pointB, pointN)
        difLAN = angLAN - (angLAB + angBAN)  # Is it 0?

        print("Check angles dif for LAN:", str(difLAN))

        # Make angles positive first
        if difKAL < 0:
            difKAL *= -1
        if difLAM < 0:
            difLAM *= -1
        if difLAN < 0:
            difLAN *= -1

        # Taking in mind rounding error. That is why "< 0.000001"
        if difKAL < 0.000001 or difLAM < 0.000001 or difLAN < 0.000001:
            return True
        else:
            return False


data2 = [[0, 1700], [2500, 4000], [3500, -4000],
         [10000, 6000], [-1000, 5900], [-2000, -2000]]

data = [[0, 0], [0, 1700], [-1000, 5900], [3500, -4000],
        [10000, 6000], [-2000, -2000], [2500, 4000]]


# node = data[0]

path = algorithm(data, data2)

x = []
y = []

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
