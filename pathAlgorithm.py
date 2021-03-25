import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.spatial.distance import cdist
# math library made for this algorithmf


# The path algorithm takes in a list of attatchment points where the first point is the location of the feeder.
# It then creates a path between each attatchment point and turns with a radius of 2m.
# Using A* proved to be inefficent as we are not looking for the shortest path.


# taking in three lists: Attatchment points, desired locations, and obsticles

# Input-format = [[[x,y],h],[[x,y],h],[[x,y],h],[[x,y],h],....,[[x,y],h],]
# Output-format: List = [[[x,y,z],h],[[x,y,z]],[[x,y,z]],[[x,y,z],h],....]


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

    # Function for getting the distance between two points

    def getDistance(self, point1, point2):
        delta_x = point2[0] - point1[0]
        delta_y = point2[1] - point1[1]

        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        return distance

    # Function for checking where the next point lies in reference to the current position.

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
        points=[]
        # z- direction, is always zero since it is the roof stags that are scaled while the rail stays leveled.
        z = 0

        # not correct as locations are added at the end
        # all_locations = attatchment_locations + desired_locations

        # Main loop of the algorithm, runs until the whole list of attatchment points have been initilized.
        while tracker < len(attatchment_locations)-1:
            print("tracker",tracker)
            print("len",len(attatchment_locations)-1)

            # initilizing the first line
            # the first and second attatchment points
            # Keeping track of previous, current and next position
            current_position = attatchment_locations[tracker]
            next_position = attatchment_locations[tracker + 1]
            previous_position = attatchment_locations[tracker - 1]
            tracker += 1

            vector = [current_position, next_position]
            path.append(vector)
            points.append(next_position)
            print("Point: ", points[-1])

            # checking for turn and what direction the turn is
            direction = self.InLineOfSight(
                path[-1][0], path[-1][1], current_position)

            # On the same line
            
            if len(path[-1]) == 2 and direction != 0:
                vector = [current_position, next_position]
                path.append(vector)
                
                """vector = [current_position, next_position]
                path.append(vector)"""

                # if direction == 1 and path[-1][0][1] > path[-1][1][1]:

            else:
                center = self.findCenter(
                    path[-1][0], path[-1][1], direction)

                PointOnArc = self.getTangentPointM(
                    center, current_position, path[-1][1], direction)

                startEndAngles = self.getStartEndAng(
                    center, path[-1][1], PointOnArc)

                if (direction == 1 and path[-1][0][1] > path[-1][1][1]):

                    if (startEndAngles[0] < 0):  # Outgoing from IV quater
                        #newEndAng = 2 * math.pi + startEndAngles[0]
                        #newStartAng = startEndAngles[1]
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
        #Adding the first point
        points.insert(0,self.start)
        return path,points

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
                #print("CURRENT INDEX:  ", current_point)
                #print("BEFORE REMOVING: ", updated_data)

                if current_point in updated_data:
                    dummy_list.remove(current_point)
                    #print("AFTER REMOVING: ", dummy_list)

                # finds the closest point.
                if len(dummy_list) != 0:
                    point = self.closest_node(current_point, dummy_list)
                    if point not in best_path:
                        best_path.append(point)
                        #print("CLOSEST AND ADDED POINT: ", point)
                else:
                    pass
            else:
                pass

        # next_position = path[index]
            #print("PATH: ", best_path)
        

        return best_path

    def closest_node(self, node, nodes):
        return nodes[cdist([node], nodes).argmin()]


PathAlgorithm = pathAlgorithm(2000, [0, 0], [-2000, -2000])

data = [[0, 0], [0, 17000], [25000, 40000], [35000, -40000],
        [100000, 60000], [-10000, 59000], [-20000, -20000]]

desired_locations = [(500, 500), (2000, 3000), (2700, 4000)]

#path,points = PathAlgorithm.algorithm(data)
path = PathAlgorithm.bestPath(data,[])

#print("all points",points)
print("path",path)


'''
path = [[[0, 0, 0], [0, 1700, 0]], [[2500, 4000, 0], [
    3500, -4000, 0]], [[10000, 6000, 0], [1000, 5900]]]
'''
x = []
y = []


#pointlist = [[0, 0], [0, 10000], [-2000, 12000], [-10000, 12000],
 #            [-11414.21356, 11414.21356], [-13414.21356, 9414.21356]]


for i in path:
    x.append(i[0])
    y.append(i[1])


print("x",x)
print("y",y)
r = 2000


for i in range(len(x)-2):
    angle_in_r = math.atan2((y[i+1]-y[i]),(x[i+1]-x[i])) #The end position for the previous line(which is the curves start) minus its start position in atan2 gives us the angle in
    angle_out_r = math.atan2((y[i+2]-y[i+1]),(x[i+2]-x[i+1]))
    angle_in_d = angle_in_r*180/np.pi
    angle_out_d = angle_out_r*180/np.pi
    if angle_in_r <0:
        angle_in_d = 360+(angle_in_r*180/np.pi)
    if angle_out_r < 0:
        angle_out_d = 360+(angle_out_r*180/np.pi)
    
    going_up = y[i+1] - y[i]
    going_right = x[i+1]- x[i]
    if going_right==0:
        going_right=0.00001
    turn_right_refframe = x[i+2]-x[i+1]
    turn_up_refframe = y[i+2]-y[i+1]
    print("turn",i)
    print("right",going_right)
    print("up",going_up)
    print("turnright",turn_right_refframe)
    print("turnup", turn_up_refframe) #gotta fix adjustments of the angle on the circle!!
    print("Degree angle in: "+str(angle_in_d))
    print("Degree angle out: "+str(angle_out_d))

    index = 0
    centerlist1 = []
    centerlist2 = []
    x_temp = x[i+1]
    y_temp = y[i+1]
    x_step = np.linspace(x[i+1],x[i],100000)
    y_step = np.linspace(y[i+1],y[i],100000)
    x_step2 = np.linspace(x[i+2],x[i],100000)
    y_step2 = np.linspace(y[i+2],y[i],100000)
    print("xstep",x_step)
    print("ystep",y_step)

    if going_up >= 0 and turn_right_refframe >= 0: #Going around top left quad
        print("ystepindex",y_step[index])
        print("yi",y[i])
        print("x_step[index]",x_step[index])
        while y_step[index] != y[i] or x_step[index] != x[i]:
            
            xc1 = x_step[index] + np.sin(angle_in_r)*r
            yc1 = y_step[index] - np.cos(angle_in_r)*r
            a = [np.round(xc1,6),np.round(yc1,6)]
            centerlist1.append(a)
            index += 1
        while y_step2[index] != y[i] or x_step2[index] != x[i]:
            
            xc2 = x_step2[index] + np.sin(angle_in_r)*r
            yc2 = y_step2[index] - np.cos(angle_in_r)*r
            a = [np.round(xc2,6),np.round(yc2,6)]
            centerlist2.append(a)
            index += 1
        #print("center",centerlist1)
        list1 = [[0, 17000], [25000, 40000], [35000, -40000], [100000, 60000], [-10000, 59000], [-20000, -20000]]
        list2 = [[0, 17001], [25020, 40000], [35000, -40003], [100000, 60200], [-10000, 59000], [-20000, -30000]]

        out = any(check in centerlist1 for check in centerlist2)
  
        # Checking condition
        print("aaaaaaa")
        if out:
            print("True") 
        else :
            print("False")
            






    """
    if abs(going_up/going_right) >= 1 and y[i+2]-y[i+1]>0:  #Here the curve is mostly going vertically contra sideways on entry  
        print("aaaaa")
        if going_up >= 0 and turn_right_refframe >= 0: #up and turn towards right
            print("5555")
            if angle_in_d < 90:
                angle_in = angle_out_d + 90 - 360 #we got to swap in and output angles since the arc only move right
                angle_out = angle_in_d + 90
            if angle_in_d >= 90:
                angle_in = angle_in_d + 180  #we got to swap in and output angles since the arc only move right
                angle_out = angle_out_d + 360
        elif going_up >= 0 and turn_right_refframe < 0: #up and turn towards left, 
            print("666")
            if angle_in_d >= 90 and angle_out_d >= 90:
                angle_in = angle_in_d - 90
                angle_out = angle_out_d - 90
            if angle_in_d < 90 or angle_out_d < 90:
                angle_in = angle_in_d - 90 + 360
                angle_out = angle_out_d - 90 +360
        elif going_up < 0 and turn_right_refframe >= 0: #down and turn towards right
            print("77777")
            if angle_in_d >= 90 and angle_out_d >= 90:   
                angle_in = angle_in_d - 90
                angle_out = angle_out_d - 90
            if angle_out_d < 90:
                angle_in = angle_in_d - 90
                angle_out = angle_out_d - 90 + 360
        elif going_up < 0 and turn_right_refframe < 0: #down and turn towards left
            print("888")
            if angle_in_d >= 90 and angle_out_d >= 90:   
                angle_in = angle_out_d + 90 #we got to swap in and output angles since the arc only move right
                angle_out = angle_in_d + 90
            if angle_out_d < 90:
                angle_in = angle_out_d - 90
                angle_out = angle_in_d - 90 + 360
    elif abs(going_up/going_right) < 1: #Here the curve is mostly going sideways contra vertically on entry 
        print("bbbb")
        if going_right >= 0 and turn_up_refframe < 0: #right and turns downward
            print("11111111111")
            if angle_in_d < 90:
                angle_in = angle_out_d + 90 - 360 #we got to swap in and output angles since the arc only move right
                angle_out = angle_in_d + 90
            if angle_in_d >= 90:
                angle_in = angle_out_d + 90 #we got to swap in and output angles since the arc only move right
                angle_out = angle_in_d + 90
        elif going_right >= 0 and turn_up_refframe >= 0: #right and turns up
            print("22222222")
            if angle_in_d >= 90 and angle_out_d >= 90: 
                angle_in = angle_in_d - 90
                angle_out = angle_out_d - 90
            if angle_in_d < 90:
                angle_in = angle_in_d - 90 + 360
                angle_out = angle_out_d +360
        elif going_right < 0 and turn_up_refframe >= 0: #left and turn up
            print("333333")
            if angle_in_d < 90:
                angle_in = angle_in_d + 90 - 360 #we got to swap in and output angles since the arc only move right
                angle_out = angle_out_d + 90
            if angle_in_d >= 90:
                angle_in = angle_out_d + 90 #we got to swap in and output angles since the arc only move right
                angle_out = angle_in_d + 90
        elif going_right < 0 and turn_up_refframe < 0: #left and turn down
            print("44444")
            if angle_in_d >= 90 and angle_out_d >= 90: 
                angle_in = angle_in_d - 90
                angle_out = angle_out_d - 90
            if angle_in_d < 90:
                angle_in = angle_in_d - 90 + 360
                angle_out = angle_out_d - 90 + 360
    print("Degree angle in on circle: "+str(angle_in))
    print("Degree angle out on circle: "+str(angle_out))
    print("")"""

plt.scatter(x, y)
plt.plot(x, y)
plt.show()
