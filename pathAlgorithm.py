from scipy.spatial.distance import cdist
import numpy as np
import numpy
import math
import sys
import matplotlib.pyplot as plt
from scipy.spatial import distance
import sympy


# The path algorithm takes in a list of attatchment points where the first point is the location of the feeder.
# It then creates a path between each attatchment point and turns with a radius of 2m.
# Using A* proved to be inefficent as we are not looking for the shortest path between points, but
# shortest path through ALL points.
# taking in three lists: Attatchment points, desired locations, and obsticles

# Input-format = [[[x,y],h],[[x,y],h],[[x,y],h],[[x,y],h],....,[[x,y],h],]
# Output-format: List = [[x,y,h],[x,y,h],[x,y,h],[x,y,h],....]


class pathAlgorithm:

    def __init__(self, turn_radius):
        self.turn_radius = turn_radius  # 2m (2000) is the fixed radius

    # Calculating the closest point using eucledian distance from cdist.
    def closest_node(self, node, nodes):
        return nodes[cdist([node], nodes).argmin()]

    # List transformer, used to transform one input to a ouput
    def listTransformer(self, data):
        mock_data = data
        try:
            new_list = []
            for i in mock_data:
                z_value = i[1]
                i.remove(z_value)
                for j in i:
                    j.append(z_value)
                    new_list.append(j)
        except:
            IndexError
        return new_list

    # Function that makes the input have 90 deegre turns, for testing purposes
    def preProcessData(self, data):
        # Initializing
        new_list = self.listTransformer(data)
        print(new_list)
        index = 0
        dummy_list = new_list
        list_of_points = []
        # Adding the two first points
        list_of_points.append(new_list[0])
        list_of_points.append(new_list[1])

        # Looping through the list and changing the X and Y coordinates to form a 90 degrees turn
        for index, element in enumerate(new_list):
            try:
                if new_list[0] == dummy_list[0]:
                    dummy_list[index] = new_list[index]
                    # list_of_points.append(dummy_list[0])

                # every other element changes Y value
                if index % 2 == 0 and index != 0:
                    dummy_list[index][1] = new_list[index+1][1]
                    list_of_points.append(dummy_list[index])

                # the rest changes x-value
                else:
                    dummy_list[index+1][0] = new_list[index][0]
                    list_of_points.append(dummy_list[index+1])
            except:
                IndexError

        # print("NEW LIST : ", dummy_list)
        # print("LIST: ", list_of_points)

        return new_list

    '''
    -----------------------------------------------
    ALGORITHM FOR FINDING THE BEST PATH
    -----------------------------------------------
    '''

    def bestPath(self, data):
        '''
        The function takes a list of points as input. It then finds the shortest
        euclidean path between the current point and all the other points in the list. It then
        selects the point which is closest to the current point, adds it to the list and
        moves to that point. Then it repeats until the list is empty
        '''

        best_path = []
        index = 0
        # initilizing the start position
        start_position = data[index]
        best_path.append(start_position)
        # removing the start position form the list
        # this is because if it was included the shortest path would be to itself.
        data.remove(data[index])
        updated_data = data
        # print("Updated: ", data)
        # Dummy list for keeping track of removed points
        dummy_list = []

        for i in updated_data:
            dummy_list.append(i)

        # main loop.
        for data_point in enumerate(updated_data):

            # Updates the current point to the last added element in the list
            if data_point is not None:
                current_point = best_path[-1]
                # print("CURRENT INDEX:  ", current_point)
                # print("BEFORE REMOVING: ", updated_data)

                # Checks if the current point is in the upgraded data list, removes it from the
                # dummy list if it is.
                if current_point in updated_data:
                    dummy_list.remove(current_point)
                    # print("AFTER REMOVING: ", dummy_list)

                if len(dummy_list) != 0:
                    # Calculating the distance from the current point to all other points in the dummy list.
                    point = self.closest_node(current_point, dummy_list)
                    if point not in best_path:
                        best_path.append(point)
                        # best_path.append(point)
                        print("CLOSEST AND ADDED POINT: ", point)
                else:
                    pass
            else:
                pass

            print("PATH: ", best_path)
        # self.railAlgorithm(best_path)
        # returns the shortest path
        return best_path

    def findCenterOfCircle(self, current_position, next_position, direction):
        '''
        Function for finding the center of the fictive circle given the current position,
        the next and the direction. We know that the point we have (current position) must be on the circles circumference.
        Deriving the center will be. NB Not checking if there obsticles in the way of the turn. See gemoeterics.jpeg for reference.
        '''

        # Finding out which quadrant we are on.

        # Finding the slope
        delta_x = next_position[0] - current_position[0]  # x_1 - x_2
        delta_y = next_position[1] - current_position[1]  # y_1 - y_2
        #slope = delta_y/delta_x
        # Checking if a point is on the line.

        # From our current point the center lays a distance, of the given radius, away from the center.

        # link: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/atan2
        psi = math.atan2(delta_y, delta_x)  #

        # We need to know which side of the line the center is located. We use the side of where the next point is.
        psi += (math.pi / 2) * direction

        x_shifted = self.turn_radius * math.cos(psi)
        y_shifted = self.turn_radius * math.sin(psi)

        center = [next_position[0] + x_shifted, next_position[1] + y_shifted]

        return center

    # Function for getting the distance between two points (vector)
    def findDistance(self, point1, point2):
        delta_x = point2[0] - point1[0]
        delta_y = point2[1] - point1[1]

        # Vectorial distance function
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        return distance

    # Function for checking where the next point lies in reference to the current position.
    def normalizedVector(self, point, distance):

        normalizedVector = [point[0]/distance, point[1]/distance]

        print("Normalized Vector: ", normalizedVector)

        return normalizedVector

    # Function for finding the  direction of a vector
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

    # Function for finding the interior arc angle of the circle segment
    def arcInclusiveAngle(self, angleVectors):
        psi = angleVectors
        psi = sympy.cot((psi/2))
        print("Psi: ", psi)
        psi = math.radians(psi)
        alpha = numpy.arcsin(psi)
        alpha = 2*alpha
        print("ALPHA: ", alpha)
        return alpha

    # Function to check if a point lays on what side of a line.
    def InLineOfSight(self, point1, point2, point3):
        # Link: https://stackoverflow.com/questions/1560492/how-to-tell-whether-a-point-is-to-the-right-or-left-side-of-a-line?fbclid=IwAR1C4J0-pFEgesJUtpIS4xY3jSdjKB8HUovqKBuCTo0QtfQ3DPGx4ya2nPk
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

    # Function for changing the path so it does not collide with obsticles in the room
    def optimalPath(self, best_path, obsticles):
        # We want to check if the path runs in to obsticles

        optimal_path = []

        # We have to check if there any obsticles at all:
        if obsticles:
            print("="*80)
            print("Obsticles detected")
            print("Checking if path is compromised ")
            print("="*80)
            for path in best_path:
                for obsticle in obsticles:
                    check = self.intersectionChecker(path, obsticle)
                    if check == True:
                        updated_path = self.obsticleAvoider(path, obsticle)

        else:
            print("No obsticles exists in the room, returning best path")
            return best_path

        return optimal_path

    # Function for determining which quadrant the intersiction point( our known point) is located in.
    def identifyingQuadrant(self, center, next_position):
        # source: https://www.geeksforgeeks.org/finding-quadrant-coordinate-respect-circle/

        qaudrant = 0

        delta_x = next_position[0] - center[0]  # Change in x-direction
        delta_y = next_position[1] - center[1]  # Change in y-direction

        # first quadrant
        if delta_x > 0 and delta_y > 0:  # (x, y) is first quadrant
            qaudrant = 1
            return qaudrant

        # Second quadrant
        elif delta_x < 0 and delta_y > 0:  # (-x, y) is second quadrant
            qaudrant = 2
            return qaudrant

        # Third quadrant
        elif delta_x < 0 and delta_y < 0:  # (-x, -y) is third quadrant
            qaudrant = 3
            return qaudrant

        # Fourth quadrant
        elif delta_x > 0 and delta_y < 0:  # (x, -y) is fourth quadrant
            qaudrant = 4
            return qaudrant
        else:
            print("No quadrant could be found")
            pass

    def intersectionChecker(self, vector, obsticle):
        # Obsticles are on the form (corner1 , corner2 , corner3 , corner4)
        # This is assuming that the customer has inputed an rectangular obsticle which as parallel with the x-axis.
        # best path algorithm to find linesegments?
        cross_check = False
        segments = []
        sorted_corners = self.bestPath(obsticle)
        # initializing the obsticle and the vector:
        first_corner = sorted_corners[0]
        second_corner = sorted_corners[1]
        third_corner = sorted_corners[2]
        fourth_corner = sorted_corners[3]

        segment1 = [first_corner, second_corner]
        segment2 = [second_corner, third_corner]
        segment3 = [third_corner, fourth_corner]
        segment4 = [fourth_corner, first_corner]

        segments.append(segment1).append(
            segment2).append(segment3).append(segment4)

        start_point, end_point = vector[0], vector[1]

        vseg = [start_point, end_point]

        # Defining intervals for intersection:

        interval1 = [min(first_corner), max(second_corner)]

        vector_interval = [min(start_point), max(end_point)]
        # The lines intersect if they share a points.
        # f1(x) = A1*x + b1 = y
        # f2(x) = A2*x + b2 = y

        for segment in segments:

            A1 = (segment[0][1]-segment[1][1])/(segment[0][0]-segment[1][0])
            A2 = (vseg[0][1]-vseg[1][1]) / (vseg[0][0]-vseg[1][0])
            b1 = segment[0][1] - A1*segment[0][0]
            b2 = vseg[0][1]-A2*vseg[0][0]
            Xa = (b2 - b1) / (A1 - A2)
            Y1 = A1 * Xa + b1
            Y2 = A2 * Xa + b2
            check = Y1 == Y2

            if ((Xa < max(min(segment[0][0], segment[1][0]), min(vseg[0][0], vseg[1][0]))) or
                    (Xa > min(max(segment[0][0], segment[1][0]), max(vseg[0][0], vseg[1][0])))):
                return cross_check  # there is no intersection
            else:
                cross_check = True
                return cross_check
        '''
        # avoiding the obsticle
        if cross_check == True:

        else:
            print("No avoidance necessary")
            return cross_check

            # If not, no avoidens needed
        return cross_check
        '''

    def obsticleAvoider(self, vector, obsticle):
        new_path = []

        return new_path

    def angleFinder(self, center, point1, point2):
        # https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
        # We need to determine the angle between the circle center and the two point
        vector_1 = (point1[0] - center[0], point1[1] - center[1])
        vector_2 = (point2[0] - center[0], point2[1] - center[1])
        v1v2scalar = vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]
        # Vectorial distance formula
        lenght_vec1 = math.sqrt(vector_1[0] ** 2 + vector_1[1] ** 2)
        length_vec2 = math.sqrt(vector_2[0] ** 2 + vector_2[1] ** 2)
        angle = math.acos(v1v2scalar / (lenght_vec1 * length_vec2))

        return angle

    def findTangentPoint(self, direction, current_position, next_position, center):

        # Need to find if the incoming line is in a spesific quadrant
        # Defining the quadrants
        # We are looking for B', see Geometrics.jpeg
        quadrant = int()

        dist_NextPos_currPos = self.findDistance(
            current_position, next_position)

        dist_cent_NextPos = self.findDistance(center, next_position)

        # Finding the angle between the next position, the center and the intercepiton point
        sigma = math.acos(
            self.turn_radius/dist_cent_NextPos)
        print("Sigma: ", sigma)

        # finding Zstar
        alpha = 2*math.pi - sigma

        z_delta_x = next_position[0] - center[0]
        z_delta_y = next_position[1] - center[1]

        # Zstar, point on the circle, see Trig.jpeg, source: https://gamedev.stackexchange.com/questions/80277/how-to-find-point-on-a-circle-thats-opposite-another-point
        Z_star = [z_delta_x/dist_cent_NextPos*self.turn_radius + center[0],
                  z_delta_y/dist_cent_NextPos*self.turn_radius + center[1]]
        print("Z* POSITION: ", Z_star)
        # Need to know which quadrant Z_star is in order to find out which way to find B'
        quadrant = self.identifyingQuadrant(center, next_position)
        # direction is either -1 (right) or 1 (left)
        if quadrant == 1:
            if direction > 0:
                rotation = -math.radians(sigma)
            else:
                rotation = math.radians(sigma)

        if quadrant == 2:
            if direction > 0:
                rotation = - math.radians(sigma)
            else:
                rotation = math.radians(sigma)

        if quadrant == 3:
            if direction > 0:
                rotation = math.radians(sigma)
            else:
                rotation = -math.radians(sigma)

        if quadrant == 4:
            if direction > 0:
                rotation = math.radians(sigma)
            else:
                rotation = -math.radians(sigma)

        B_prime_x = math.cos(rotation)*self.turn_radius + center[0]
        B_prime_y = math.sin(rotation)*self.turn_radius + center[1]

        Bprime = [B_prime_x, B_prime_y]

        return Bprime

    '''
    ---------------------------------------------------------
    MAIN ALGORITHM FOR FINDING THE RAIL - FINDING THE CURVES
    --------------------------------------------------------
    '''

    def railAlgorithm(self, data, obsticles):

        # initialize
        all_obsticles = obsticles
        best_path = self.bestPath(data)
        print("THE BEST PATH: ", best_path)
        index = 0
        curved_path = []
        # Making a mock path to keep progression through removing paths evaluated
        tracker_path = best_path
        current_position = tracker_path[0]
        next_position = tracker_path[1]
        vector = [current_position, next_position]
        curved_path.append(vector)
        tracker = 0

        # Will run as long  as there are elements in the tracker_path list
        # Checking for turns in the path.
        while tracker_path:
            # index += 1
            # print("ITERATION: ", index)
            # print(best_path[index])
            # print(best_path[index + 1])
            # print(best_path[index+1])
            # Adding the first path between the start position and next position.
            if len(tracker_path) != 1:
                current_position = tracker_path[index]
                next_position = tracker_path[index + 1]
            else:
                # curved_path.append(current_position)
                break
            '''
            if index == 0:
                vector = [current_position, next_position]
                curved_path.append(vector)
                # tracker_path.remove(current_position)
            '''

            # Finding where the next point is located in reference to the current path
            print("CURVED PATH: ", curved_path)
            direction = self.InLineOfSight(
                curved_path[-1][0], curved_path[-1][1], tracker_path[index+1])
            print("DIRECTION: ", direction)

            # Check for turn
            # no turn --> Straight line
            if direction == 0 and tracker != 0:
                vector = [tracker_path[index], tracker_path[index + 1]]
                curved_path.append(vector)
                tracker_path.remove(current_position)

            else:  # Turn

                # if len(curved_path[-1]) == 2:
                print("CURVED PATH: ", curved_path)
                direction = self.InLineOfSight(
                    curved_path[-1][0], curved_path[-1][1], tracker_path[index+1])

                # Finding the center of the circle which will become the turn arc.
                center = self.findCenterOfCircle(
                    curved_path[-1][0], curved_path[-1][1], direction)

                # Finding Bprime on the turn arc. (The exiting point of the arc)
                Bprime = self.findTangentPoint(
                    direction, current_position, next_position, center)

                next_vector = [Bprime, next_position]

                curved_path.append(next_vector)
                # best_path.insert(index + 1, Bprime)

                tracker_path.remove(current_position)

                # ====================================================
                '''
                psi = self.angleBetweenVectors(
                    curved_path[-1][1], tracker_path[index])

                # The angle between the center and  the  two endpoints of the arc
                arcInteriorAngle = self.arcInclusiveAngle(psi)

                directionVector = self.directonalVector(
                    best_path[index], best_path[index-1])
                '''
                # ====================================================

                # Calculating distance along one of the vectors to the interception point on the arc. (End of arc)

                # distance_to_point_end_of_arc = self.turn_radius * \
                #    sympy.cot(psi/2)

                # print("Distance to end: ", distance_to_point_end_of_arc)

                # my_new_list = [
                #    i * distance_to_point_end_of_arc for i in directionVector]

                # end_point_of_arc = [sum(x) for x in zip(
                #    best_path[index-1], my_new_list)]

                # end_point_of_arc = [x/1000 for x in end_point_of_arc]

                # curved_path.append(end_point_of_arc)

                # print("END POINT ON CURVE: ", end_point_of_arc)

                # print("CURVED PATH: ", curved_path)

            # index += 1

            # Getting optimised path (Taking obsticles into account)
            # optimsied_path = self.optimalPath(curved_path, all_obsticles)
            # print("OPTIMIZED PATH: ", optimsied_path)
            # optimsied_path = self.listTransformer(optimsied_path)
            # curved_path, optimsied_path, best_path
            print("BEST PATH AFTER RUN: ", best_path)

            tracker += 1
        print("CURVED PATH AFTER RUN: ", curved_path)
        return curved_path


"""
--------------------------------------------------
TESTING AND VARIABLE INITIATION
--------------------------------------------------
"""

PathAlgorithm = pathAlgorithm(2000)

data = [[0, 0], [0, 1700], [2500, 4000], [3500, -4000],
        [10000, 6000], [-1000, 5900], [-2000, -2000]]

dataPRe = [[0, 0], [0, 1700], [2500, 1700], [2500, -4000],
           [10000, -4000], [10000, 5900], [-2000, 5900]]

Newpointlist = [[[1000, 2700], 10], [[3700, 10000], 0], [[-2000, 12000], 6], [[3000, 12000], 15],
                [[-10000, 5000], 0], [[5900, 29876], 7], [[7000, 3000], 0], [[4000, - 5700], 20], [[2456, 17000], 1]]

Newpointlist2 = [[[1500, 2700], 10], [[7700, 10000], 0], [[-5000, 16000], 6], [[1000, 4000], 15],
                 [[-10000, 5000], 0], [[5900, 29876], 7], [[7000, 3000], 0], [[4000, - 5700], 20], [[2456, 17000], 1]]

pointlist = [[[0, 0], 10], [[0, 10000], 0], [[-2000, 12000], 6], [[-10000, 12000], 15],
             [[-11414.21356, 11414.21356], 0], [[-13414.21356, 9414.21356], 7]]

ninty_degrees_path = [[0, 0], [0, 10000], [2000, 10000], [2000, 4000]]

path = [[[0, 0, 0], [0, 1700, 0]], [[2500, 4000, 0], [
    3500, -4000, 0]], [[10000, 6000, 0], [1000, 5900]]]

obsticles = []

# desired_locations = [(500, 500), (2000, 3000), (2700, 4000)]


# path = PathAlgorithm.bestPath(dataPRe)
all_locations = [[[7000, 8000], 10000], [[7000, 29000], 10000],
                 [[16000, 29000], 10000], [[16000, 7000], 10000]]
'''
if len(Newpointlist2) > 0:
    ninty_path = PathAlgorithm.preProcessData(Newpointlist2)
    print(ninty_path)
'''

best_path_run = PathAlgorithm.railAlgorithm(data, obsticles)

x = []
y = []

# Function for plotting the rail on a 2d grid.

for i in best_path_run:
    x.append(i[0])
    y.append(i[1])

plt.scatter(x, y)
plt.plot(x, y)
plt.show()

# path = [[0, 0, 0], [100, 0, 0], [100, 400, 0], [100, 400, 0], [0, 400, 0]]
