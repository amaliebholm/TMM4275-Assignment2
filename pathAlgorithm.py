import numpy as np
import math
import sys
import matplotlib.pyplot as plt


# The path algorithm takes in a list of attatchment points where the first point is the location of the feeder.
# It then creates a path between each attatchment point and turns with a radius of 2m.
# Using A* proved to be inefficent as we are not looking for the shortest path.


# taking in three lists: Attatchment points, desired locations, and obsticles


class pathAlgorithm:

    def __init__(self, turn_radius, start, end):
        self.turn_radius = turn_radius
        self.start = start  # feeder
        self.end = end  # last attatchment point of the rail

    """
    gets the center (X, Y) of the the curve for the specified (in constructor) radius
    dir, is a direction - (-1):clockwise/(+1)counter clockwise to
    decide which direction is the turn.
    """

    def findCenter(self, current_position, next_position, dir):
        y = next_position[1] - current_position[1]
        x = next_position[0] - current_position[0]
        theta = math.atan2(y, x)
        print("Theta:", theta)

        theta += dir * math.pi / 2

        xPlus = self.turn_radius * math.cos(theta)
        yPlus = self.turn_radius * math.sin(theta)

        ret = (next_position[0] + xPlus, next_position[1] + yPlus)
        print("Arc center:", ret)
        return ret









    def algorithm(self, attatchment_locations, desired_locations):
        path = []
        tracker = 0

        # not correct as locations are added at the end
        all_locations = attatchment_locations + desired_locations

        # Main loop of the algorithm, runs until the whole list of attatchment points have been initilized.
        while tracker < len(attatchment_locations)-1:

            # initilizing the first line
            # the first and second attatchment points
            # Keeping track of previous, current and next position
            current_position = attatchment_locations[tracker]
            next_position = attatchment_locations[tracker + 1]
            # previous_position = attatchment_points[tracker - 1]
            # tracker += 1

            line = (current_position, next_position)
            path.append(line)
            print("Path: ", path[-1])

            # checking for turn and what direction the turn is
            direction = self.getPointRefToLine(
                path[-1][0], path[-1][1], current_position)

            if len(path[-1]) == 2 and direction != 0:
                line = (current_position, next_position)
                path.append(line)

            # if direction == 1 and path[-1][0][1] > path[-1][1][1]:

            else:

                center = self.findCenter(path[-1][0], path[-1][1], direction)

                bPrim = self.getBPrim(
                    center, current_position, path[-1][1], direction)

                startEndAngles = self.getStartEndAng(
                    center, path[-1][1], bPrim)

                if (direction == 1 and path[-1][0][1] > path[-1][1][1]):
                    newStartAng = 0  # placeholder
                    newEndAng = 0  # placeholder




                    if (startEndAngles[0] < 0):  # Outgoing from IV quater
                        newEndAng = 2 * math.pi + startEndAngles[0]
                        newStartAng = startEndAngles[1]
                        curve = (path[-1][1], bPrim)
                        print("POSITIONS: ", path[-1][0], path[-1][1])
                        print("CURVE: ", curve)
                        path.append(curve)




                    elif center[1] > current_position[1]:
                        # Not any special case
                        curve = (
                            startEndAngles[0], startEndAngles[1], center, path[-1][1], bPrim)
                        path.append(curve)





                    else:
                        newStartAng = startEndAngles[1]
                        newEndAng = startEndAngles[0]
                        # Just 3 elements
                        curve_aux = (newStartAng, 2 * math.pi, center)
                        path.append(curve_aux)
                        curve = (0, newEndAng, center,
                                 path[-1][1], bPrim)
                        path.append(curve)





                    # Incoming line to IV quater
                elif (dir > 0) and (ret[-1][0][1] < pointB[1]):
                    # redifine the angles first
                    newStartAng = 0  # placeholder
                    newEndAng = 0  # placeholder





                    # Outgoing from IV quater
                    if ((startEndAngles[0] < 0) and (startEndAngles[1] < 0)):
                        # Normal order, but in +scale
                        newStartAng = 2 * math.pi + startEndAngles[0]
                        newEndAng = 2 * math.pi + startEndAngles[1]
                        curve = (newStartAng, newEndAng,
                                    center, path[-1][1], bPrim)
                        path.append(curve)






                    elif startEndAngles[0] < 0:  # Not only the IV quater, but other quater(s) as well --> aux. curve needed
                        newStartAng = startEndAngles[0] + 2 * math.pi
                        newEndAng = startEndAngles[1]
                        # Just 3 elements
                        curve_aux = (newStartAng, 2 * math.pi, center)
                        path.append(curve_aux)
                        curve = (0, newEndAng, center,
                                    path[-1][1], bPrim)
                        path.append(curve)

                elif (dir < 0) and (path[-1][0][1] > pointB[1]):  # Incoming line to I quater, but clockwise rotation
                    if startEndAngles[0] < 0:
                        curve = (
                            startEndAngles[1], 2 * math.pi + startEndAngles[0], center, ret[-1][1], bPrim)
                        path.append(curve)
                    else:
                            # Just 3 elements
                            curve_aux = (0, startEndAngles[0], center)
                            path.append(curve_aux)

                            curve = (
                                startEndAngles[1], 2 * math.pi, center, path[-1][1], bPrim)
                            path.append(curve)

                elif (startEndAngles[0] < 0):  # Create auxiliary curve
                        # ORDER? - Nope. :)
                        curve = (
                            0, startEndAngles[1], center, path[-1][1], bPrim)
                        path.append(curve)

                        # Just 3 elements
                        curve_aux = (
                            2 * math.pi + startEndAngles[0], 2 * math.pi, center)
                        path.append(curve_aux)
                else:
                        curve = (
                            startEndAngles[0], startEndAngles[1], center, path[-1][1], bPrim)
                        path.append(curve)
                    # Add the line (bPrim, the point)
                    line = (bPrim, points[i])
                    path.append(line)

            return path

    # Checking for obsitcle collison and evasion




    def getPointRefToLine(self, pointA, pointB, pointC):
        # http://www.math.by/geometry/eqline.html
        # (x, y)
        check = (pointA[1] - pointB[1]) * pointC[0] + \
            (pointB[0] - pointA[0]) * pointC[1] + \
            (pointA[0] * pointB[1] - pointB[0] * pointA[1])
        if check < 0:
            return -1
        elif check > 0:
            return 1
        else:
            return 0




    def getBPrim(self, center, pointC, pointB, dir):

        distance = self.getDistance(center, pointC)
        print("Distance - center to pointC:", distance)

        # Searching B'
        # math.pi/2 - angOCBprim #180-90-OCB'
        angCOBprim = math.acos(self.turn_radius / distance)

        # Cooridnates of B'
        # Find C'
        # Find angle OCC'
        # Rotate radius above O by 180 - angle(OCC') - angle(COB')
        cPrim = (center[0], pointC[1])
        angCOCPrim = math.asin((pointC[0] - cPrim[0]) / distance)
        if angCOCPrim < 0:
            angCOCPrim *= -1
        print("angCOBprim", angCOBprim)
        print("angCOCPrim", angCOCPrim)
        angleRot = 0
        # Identify the quater of C point w.r.t. O
        # I quater: Cx-Ox > 0 and Cy-Oy > 0
        if (pointC[0] - center[0] > 0) and (pointC[1] - center[1] > 0):
            if dir > 0:
                angleRot = -math.pi / 2 + angCOBprim + angCOCPrim
                angleRot *= -1
            else:
                angleRot = math.pi / 2 + angCOBprim - angCOCPrim

        # II quater: Cx-Ox < 0 and Cy-Oy > 0
        if (pointC[0] - center[0] < 0) and (pointC[1] - center[1] > 0):
            if dir < 0:
                angleRot = math.pi / 2 + angCOBprim + angCOCPrim
            else:
                angleRot = math.pi / 2 - (angCOBprim - angCOCPrim)

        # III quater: Cx-Ox < 0 and Cy-Oy < 0
        if (pointC[0] - center[0] < 0) and (pointC[1] - center[1] < 0):
            if dir > 0:
                angleRot = 1.5 * math.pi - (angCOBprim + angCOCPrim)
            else:
                angleRot = 1.5 * math.pi + (angCOBprim - angCOCPrim)

        # IV quater: Cx-Ox > 0 and Cy-Oy < 0
        if (pointC[0] - center[0] > 0) and (pointC[1] - center[1] < 0):
            if dir > 0:
                angleRot = math.pi / 2 + (angCOBprim - angCOCPrim)
                angleRot *= -1
            else:
                angleRot = -math.pi / 2 + angCOBprim + angCOCPrim
            # angleRot *= -1

        return self.getRotXY(center, angleRot)







    """
    gets distance between two points
    """

    def getDistance(self, pointA, pointB):
        yDelta = pointB[1] - pointA[1]
        xDelta = pointB[0] - pointA[0]

        ret = math.sqrt(xDelta ** 2 + yDelta ** 2)
        return ret






    def getRotXY(self, center, angle):

        xPlus = self.turn_radius * math.cos(angle)
        yPlus = self.turn_radius * math.sin(angle)

        ret = (center[0] + xPlus, center[1] + yPlus)
        print("The point on arc:", ret)
        return ret









    def getStartEndAng(self, center, point1, point2):
        # Find the first point - point1 or point2 - w.r.t. the quaters of the circle for given center.
        ang1 = self.angVia3Points(center, (center[0] + 5, center[1]), point1)
        ang2 = self.angVia3Points(center, (center[0] + 5, center[1]), point2)
        # Check if the point is below the center --> two arcs to be generated (to be processed at the caller side).
        if center[1] > point1[1] and center[0] < point1[0]:  # IV quater - incoming
            ang1 *= -1

        if center[1] > point2[1] and center[0] < point2[0]:  # IV quater - outgoing
            ang2 *= -1

        if center[1] > point1[1] and center[0] > point1[0]:  # III quater - incoming
            ang1 = 2 * math.pi - ang1

        if center[1] > point2[1] and center[0] > point2[0]:  # III quater - outgoing
            ang2 = 2 * math.pi - ang2

        if ang1 < ang2:
            return (ang1, ang2)
        else:
            return (ang2, ang1)










    def angVia3Points(self, center, point1, point2):
        vec1 = (point1[0] - center[0], point1[1] - center[1])
        vec2 = (point2[0] - center[0], point2[1] - center[1])

        scalarProd12 = vec1[0] * vec2[0] + vec1[1] * vec2[1]

        modVec1 = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
        modVec2 = math.sqrt(vec2[0] ** 2 + vec2[1] ** 2)

        ang = math.acos(scalarProd12 / (modVec1 * modVec2))

        return ang








'''
TESTER
'''

PathAlgorithm = pathAlgorithm(2000, (0, 0), (-2000, -2000))

data = [(0, 0), (0, 1700), (2500, 4000), (3500, -4000),
        (10000, 6000), (-1000, 5900), (-2000, -2000)]

desired_locations = [(500, 500), (2000, 3000), (2700, 4000)]

PathAlgorithm.algorithm(data, desired_locations)

'''
path = [[[0, 0, 0], [0, 1700, 0]], [[2500, 4000, 0], [
    3500, -4000, 0]], [[10000, 6000, 0], [1000, 5900]]]

x = []
y = []

for i in path:
    x.append(i[0][0])
    y.append(i[0][1])

print(x)
print(y)

plt.scatter(x, y)
plt.plot(x, y)
plt.show()
'''


path = [[0, 0, 0], [100, 0, 0], [100, 400, 0], [100, 400, 0], [0, 400, 0]]
