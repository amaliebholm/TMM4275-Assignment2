import math
import sys

class PathPlanner:
    """
    Constructor for the PathPlanner class.
    """

    def __init__(self, radius):
        print("PathPlanner initialized.")
        self.radius = radius


    """
    Gets as input coordinates collection [(x1,y1), (x2,y2),...,(xn,yn)]
    Returns sequence of lines/curves
    """

    def getPath(self, points):
        # to be populated with results - lines ((x1,y1),(x2,y2))
        # and curves (startAng,endAng,(xc,yc), (xs,ys), (xe,ye)) / (xs,ys), (xe,ye) - redundant infomation, but needed to simplify planning of the next curve.
        ret = []
        i = 0
        while i < len(points) - 1:
            i += 1
            if i == 1:
                # Just a line to start (see i+1 in the beginning)
                line = (points[i - 1], points[i])
                ret.append(line)
            else:
                # Check if not on the same line.
                if (len(ret[-1]) == 2) and (self.getPointRefToLine(ret[-1][0], ret[-1][1], points[i]) == 0):
                    # Same line just adding new segement on it.
                    line = (points[i - 1], points[i])
                    ret.append(line)
                else:
                    # Curve is needed.
                    if len(ret[-1]) == 2:
                        # There was line before
                        dir = self.getPointRefToLine(ret[-1][0], ret[-1][1], points[i])
                        center = self.getCenterXY(ret[-1][0], ret[-1][1], dir)
                        """print("aaaaaa")
                        print(ret[-1][0])
                        print(ret[-1][1])
                        print(points[i])
                        print(center)
                        print("bbbb")"""
                        bPrim = self.getBPrim(center, points[i], ret[-1][1], dir)
                        pointB = ret[-1][1]
                        startEndAngles = self.getStartEndAng(center, pointB, bPrim)
                        if (dir > 0) and (ret[-1][0][1] > pointB[1]):
                            # redifine the angles first
                            newStartAng = 0  # placeholder
                            newEndAng = 0  # placeholder
                            if (startEndAngles[0] < 0):  # Outgoing from IV quater
                                newEndAng = 2 * math.pi + startEndAngles[0]
                                newStartAng = startEndAngles[1]
                                curve = (newStartAng, newEndAng, center, ret[-1][1], bPrim)
                                ret.append(curve)
                            elif center[1] > points[i][1]:  # The desitnation is below the circle
                                # Not any special case
                                curve = (startEndAngles[0], startEndAngles[1], center, ret[-1][1], bPrim)
                                ret.append(curve)
                            else:
                                newStartAng = startEndAngles[1]
                                newEndAng = startEndAngles[0]
                                curve_aux = (newStartAng, 2 * math.pi, center)  # Just 3 elements
                                ret.append(curve_aux)
                                curve = (0, newEndAng, center, ret[-1][1], bPrim)
                                ret.append(curve)
                        elif (dir > 0) and (ret[-1][0][1] < pointB[1]):  # Incoming line to IV quater
                            # redifine the angles first
                            print("\n\nnnder")
                            newStartAng = 0  # placeholder
                            newEndAng = 0  # placeholder
                            if ((startEndAngles[0] < 0) and (startEndAngles[1] < 0)):  # Outgoing from IV quater
                                newStartAng = 2 * math.pi + startEndAngles[0]  # Normal order, but in +scale
                                newEndAng = 2 * math.pi + startEndAngles[1]
                                curve = (newStartAng, newEndAng, center, ret[-1][1], bPrim)
                                ret.append(curve)
                            elif startEndAngles[
                                0] < 0:  # Not only the IV quater, but other quater(s) as well --> aux. curve needed
                                newStartAng = startEndAngles[0] + 2 * math.pi
                                newEndAng = startEndAngles[1]
                                curve_aux = (newStartAng, 2 * math.pi, center)  # Just 3 elements
                                ret.append(curve_aux)
                                curve = (0, newEndAng, center, ret[-1][1], bPrim)
                                ret.append(curve)
                        elif (dir < 0) and (ret[-1][0][1] > pointB[1]):  # Incoming line to I quater, but clockwise rotation
                            print("\n\nnnher")
                            if startEndAngles[0] < 0:
                                curve = (startEndAngles[1], 2 * math.pi + startEndAngles[0], center, ret[-1][1], bPrim)
                                ret.append(curve)
                                
                            else:
                                curve_aux = (0, startEndAngles[0], center)  # Just 3 elements
                                ret.append(curve_aux)
                                curve = (startEndAngles[1], 2 * math.pi, center, ret[-1][1], bPrim)
                                ret.append(curve) 
                        elif (startEndAngles[0] < 0):  # Create auxiliary curve
                            # ORDER? - Nope. :)
                            curve = (0, startEndAngles[1], center, ret[-1][1], bPrim)
                            ret.append(curve)

                            curve_aux = (2 * math.pi + startEndAngles[0], 2 * math.pi, center)  # Just 3 elements
                            ret.append(curve_aux)

                        else:
                            curve = (startEndAngles[0], startEndAngles[1], center, ret[-1][1], bPrim)
                            ret.append(curve)
                        # Add the line (bPrim, the point)
                        line = (bPrim, points[i])
                        ret.append(line)
                    else:
                        # IS THAT NEEDED AT ALL?
                        # Curve-to-curve connection
                        # Find direction of the slope
                        # Find auxiliary point on the slope
                        # Calculate the new curve
                        # Add the line to the point
                        pass
        print("aaaa")
        print(ret[0])
        print("")
        print(ret[1])
        print("")
        print(ret[2])
        print("")
        print(ret[3])
        print("")
        print(ret[4])
        print("")
        print(ret[5])
        print("")
        print(ret[6])
        print("")
        print(ret[7])
        print("")
        print(ret[8])
        print("")
        print(ret[9])
        return ret

    """
    Gets adjusted trajectory taking obstacles information
    Returns sequence of lines/curves
    """

    def getPathOA(self, points, obstacles):
        # 1. Get normal path.
        # 2. Check which lines are blocked by obstacles
        # 3. Introduce via points
        # 4. Generate a path for new updated set of points
        originalPath = self.getPath(points)

        for obj in originalPath:
            for obstacle in obstacles:
                # Check if the obstacle blocks any of the lines/curves in original path
                if len(obj) == 2:  # It is a line
                    # Line inside of rectangular check
                    if lineCrossCheck(obj, obstacle):
                        # Find via Point.
                        viaPoint = getViaPoint(obj, obstacle)

    """
    A dedicated method to check the line and rectangular intersection
    """

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

    """
    Returns via point to be integrated to the path.
    """

    def getViaPoint(self, obj, obstacle):
        # Find nearest points to line/curve...
        # Get via points then
        pass

    """
    Gets position of the point (PointC) with respect to the line formed by 
    points pointA and pointB.
    Possible results:
    1 - "_left_ turn" towards pointC with respect to dircetion pointA --> pointB of the line.
    -1 - "_right_ turn" towards pointC with respect to dircetion pointA --> pointB of the line.
    0 - pointC is on the line formed by points A and B. No turn is needed.
    """

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

    """
    gets the center (X, Y) of the the curve for the specified (in constructor) radius
    dir, is a direction - (-1):clockwise/(+1)counter clockwise to 
    decide which direction is the turn.
    """

    def getCenterXY(self, pointA, pointB, dir):
        y = pointB[1] - pointA[1]
        x = pointB[0] - pointA[0]
        theta = math.atan2(y, x)
        print("Theta:", theta)

        theta += dir * math.pi / 2

        xPlus = self.radius * math.cos(theta)
        yPlus = self.radius * math.sin(theta)

        ret = (pointB[0] + xPlus, pointB[1] + yPlus)
        print("Arc center:", ret)
        return ret

    """
    gets distance between two points
    """

    def getDistance(self, pointA, pointB):
        yDelta = pointB[1] - pointA[1]
        xDelta = pointB[0] - pointA[0]

        ret = math.sqrt(xDelta ** 2 + yDelta ** 2)
        return ret

    """
    Gets B' coordinates
    """

    def getBPrim(self, center, pointC, pointB, dir):

        distance = self.getDistance(center, pointC)
        print("Distance - center to pointC:", distance)

        # Searching B'
        angCOBprim = math.acos(self.radius / distance)  # math.pi/2 - angOCBprim #180-90-OCB'

        """
        Not used so far
        distCBprim = distance * math.cos(angOCBprim)
        print("Distance CB'", distCBprim)
        """

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
    Get coordinates of the point on the arc as result of rotation to dir
    by angle
    """

    def getRotXY(self, center, angle):

        xPlus = self.radius * math.cos(angle)
        yPlus = self.radius * math.sin(angle)

        ret = (center[0] + xPlus, center[1] + yPlus)
        print("The point on arc:", ret)
        return ret

    def angVia3Points(self, center, point1, point2):
        vec1 = (point1[0] - center[0], point1[1] - center[1])
        vec2 = (point2[0] - center[0], point2[1] - center[1])

        scalarProd12 = vec1[0] * vec2[0] + vec1[1] * vec2[1]

        modVec1 = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
        modVec2 = math.sqrt(vec2[0] ** 2 + vec2[1] ** 2)

        ang = math.acos(scalarProd12 / (modVec1 * modVec2))

        return ang

    """
    Get start and end angles
    """

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


'''
Test
'''
pathPlanner = PathPlanner(2000)
pointA = (0, 0)
pointB = (0, 1000)
pointC = (1500, 4000)
pointD = (3500, -4000)
pointE = (10000, 6000)
pointF = (-1000, 5900)
pointG = (-2000, -2000)

# ***
print("*****************************************")
print("For the same points checking the planner")
print("*****************************************")
data = [pointA, pointB, pointC, pointD, pointE, pointF, pointG]
result = pathPlanner.getPath(data)
print("The path for rail to follow:", result)
Xs = "["
Ys = "["
for p in result:
    if len(p) == 2:
        Xs += str(p[0][0]) + " " + str(p[1][0]) + " "
        Ys += str(p[0][1]) + " " + str(p[1][1]) + " "
print("Xs", Xs)
print("Ys", Ys)

# ***
"""
print("*****************************************")
print("Test for lineCrossCheck()")
print("*****************************************")
obstacle = (-500, 500, 1000, 25, 70)
testLine = (pointA, pointB)
print("Obstacle detected?:", pathPlanner.lineCrossCheck(testLine, obstacle))
"""