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
                        #print("CLOSEST AND ADDED POINT: ", point)
                else:
                    pass
            else:
                pass

            #print("PATH: ", best_path)
        # self.railAlgorithm(best_path)
        # returns the shortest path
        return best_path

    def findCenterOfCircle(self, current_position, next_position, direction):
        '''
        Function for finding the center of the fictive circle given the current position,
        the next and the direction. We know that the point we have (current position) must be on the circles circumference.
        Deriving the center will be. NB Not checking if there obsticles in the way of the turn. See gemoeterics.jpeg for reference.
        '''

        # Finding the difference in x and y values between the current and next point, and slope
        delta_x = next_position[0] - current_position[0]  # x_1 - x_2
        delta_y = next_position[1] - current_position[1]  # y_1 - y_2
        #slope = delta_y/delta_x

        # From our current point the center lays a distance, of the given radius, away from the center.
        # We need to know which side of the line the center is located. We use the side of where the next point is.
        # link: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/atan2
        psi = math.atan2(delta_y, delta_x) + (math.pi / 2) * direction

        x_shifted = self.turn_radius * math.cos(psi)
        y_shifted = self.turn_radius * math.sin(psi)

        Ox, Oy = next_position[0] + x_shifted, next_position[1] + y_shifted

        center = [Ox, Oy]

        return center

    # Function for getting the distance between two points (vector distance)
    def findDistance(self, point1, point2):
        # Link: https://www.goeduhub.com/2071/write-python-program-calculate-distance-between-points-taking
        delta_x = point2[0] - point1[0]
        delta_y = point2[1] - point1[1]

        # Vectorial distance function
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        return distance

    # Function for checking where the next point lies in reference to the current position.
    def normalizedVector(self, point, distance):

        # link: https://mathworld.wolfram.com/NormalizedVector.html

        normalizedVector = [point[0]/distance, point[1]/distance]

        print("Normalized Vector: ", normalizedVector)

        return normalizedVector

    # Function for finding the  direction of a vector
    def directonalVector(self, point1, point2):

        # link: https://stackoverflow.com/questions/17332759/finding-vectors-with-2-points

        dirVec = [point1[0]-point2[0], point1[1] - point2[1]]

        print("Direction Vector: ", dirVec)

        return dirVec

    # Fucntion for getting the angle between two vectors

    def angleBetweenVectors(self, vector1, vector2):
        # Calculating the unit vectors
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

    # Function to check what direction the next point lays on in accordance to the line.
    def InLineOfSight(self, point1, point2, point3):
        # Link: https://stackoverflow.com/questions/1560492/how-to-tell-whether-a-point-is-to-the-right-or-left-side-of-a-line?fbclid=IwAR1C4J0-pFEgesJUtpIS4xY3jSdjKB8HUovqKBuCTo0QtfQ3DPGx4ya2nPk
        direction = 0

        # Evaluating the determinant of a vector cross product:
        LOF = (point3[0] - point1[1])*(point2[1] - point1[1]) - \
            (point3[1]-point1[1])*(point2[0]-point1[0])

        if LOF > 0:
            direction = 1
            return direction
        elif LOF < 0:
            direction = -1
            return direction
        else:
            return direction

    # Function for changing the path so it does not collide with obsticles in the room
    def optimalPath(self, best_path, obstacles):
        # We want to check if the path runs in to obsticles

        optimal_path = []

        # We have to check if there any obsticles at all:
        if obsticles:
            print("="*80)
            print("Obsticles detected")
            print("Checking if path is compromised ")
            print("="*80)
            for path in best_path:
                for obstacle in obstacles:
                    check = self.intersectionChecker(path, obstacle)
                    if check == True:
                        updated_path = self.obsticleAvoider(path, obstacle)

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

    def intersectionChecker(self, vector, obstacle):
        # Obsticles are on the form (corner1 , corner2 , corner3 , corner4)
        # This is assuming that the customer has inputed an rectangular obsticle which is parallel with the x-axis.
        # best path algorithm to find linesegments?
        cross_check = False
        segments = []
        sorted_corners = self.bestPath(obstacle)
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

    def findTangentPoint(self, direction, current_position, next_position, center):

        # Need to find if the incoming line is in a spesific quadrant
        # Defining the quadrants
        # We are looking for B', see Geometrics.jpeg and Trig.jpeg in the repository
        quadrant = int()

        dist_NextPos_currPos = self.findDistance(
            current_position, next_position)
        print("CENTER", center)
        dist_cent_NextPos = self.findDistance(center, next_position)
        print("DISTANCE FROM CENTER TO NEXT POSITION: ", dist_cent_NextPos)

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

    def railAlgorithm(self, data, obstacles):
        print("="*80)
        print("STARTING RAIL ALGORITHM")
        print("="*80)

        # initialize all variables:
        all_obstacles = obstacles
        list_path = []
        tracker_path = []  # Used for keeping track of progress
        curved_path = []
        index = 0
        tracker = 0

        # Creating the best path through the list of points
        best_path = self.bestPath(data)
        print("THE BEST PATH: ", best_path)

        # Getting optimized path (Taking obsticles into account)
        # optimsied_path = self.optimalPath(curved_path, all_obsticles)
        # print("OPTIMIZED PATH: ", optimsied_path)

        # Transforming the path into the right format: [[x,y,z],...]
        # optimsied_path = self.listTransformer(optimsied_path)

        # Making a mock path to keep progression through removing paths that have been evaluated
        tracker_path = best_path

        # initializing start path
        current_position = tracker_path[0]
        next_position = tracker_path[1]
        vector = [current_position, next_position]
        curved_path.append(vector)

        list_path.append(current_position)
        list_path.append(next_position)

        # MAIN LOOP: Will run as long  as there are elements in the tracker_path list
        # Checking for turns in the path.
        while tracker_path:
            index += 1
            # Keeping track of the last position evaluated
            position = tracker_path[index - 1]

            # Setting the current and next position untill there is one element left in the list
            if len(tracker_path) != 1:
                # Last element in the list, current position
                current_position = curved_path[-1][0]
                # Last element in the list, next position
                next_position = curved_path[-1][1]
                print("ITERATION: ", index)  # Keeping track of iteration
                print("="*80)
                print("CURRENT POSITION: ", current_position)
                print("NEXT POSITION: ", next_position)
            else:
                print("Process complete")
                break

            # Finding where the next point is located in reference to the current path
            print("CURVED PATH: ", curved_path)

            direction = self.InLineOfSight(
                curved_path[-1][0], curved_path[-1][1], best_path[index])
            print("DIRECTION: ", direction)

            # Check for turn
            # no turn --> Straight line
            if direction == 0:

                vector = [best_path[index], best_path[index + 1]]
                curved_path.append(vector)
                tracker_path.remove(position)

            else:  # Turn
                print("TURN DETECTED")
                # if len(curved_path[-1]) == 2:
                direction = self.InLineOfSight(
                    curved_path[-1][0], curved_path[-1][1], best_path[index])

                # Finding the center of the circle which will become the turn arc.
                print("POSITIONS: ", curved_path[-1][0], curved_path[-1][1])
                center = self.findCenterOfCircle(
                    curved_path[-1][0], curved_path[-1][1], direction)

                # Finding Bprime on the turn arc. (The exiting point of the arc)
                Bprime = self.findTangentPoint(
                    direction, curved_path[-1][0], curved_path[-1][1], center)

                next_vector = [next_position, Bprime]
                curved_path.append(next_vector)

                inital_vector = [Bprime, next_position]

                list_path.append(Bprime)
                list_path.append(best_path[index+1])
                print("LIST PATH: ", list_path)

                curved_path.append(inital_vector)
                # best_path.insert(index + 1, Bprime)

                tracker_path.remove(position)

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

            # curved_path, optimsied_path, best_path
            print("BEST PATH AFTER RUN: ", best_path)

            tracker += 1
            print("="*80)
        print("CURVED PATH AFTER RUN: ", curved_path)
        return curved_path


"""
--------------------------------------------------
TESTING AND VARIABLE INITIATION
--------------------------------------------------
"""

obsticles = []

#the_path = PathAlgorithm.bestPath(data)
#print("THE PATH", the_path)
best_path_run = PathAlgorithm.railAlgorithm(data, obsticles)

x = []
y = []

# Function for plotting the rail on a 2d grid.

for i in best_path_run:
    x.append(i[0])
    y.append(i[1])

plt.scatter(x, y)
# plt.plot(best_path_run[:])
plt.plot(x, y)
plt.show()
