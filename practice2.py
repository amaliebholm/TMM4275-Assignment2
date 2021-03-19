import math as m
import numpy as np

#The feeder can only make turns with radius of 2m
r = 2

#Vi får inn en liste med start og slutt punkter for hvert element
#pointlist = np.array([[0,0],[0,10],[-2,12]]) #opp,sving venstre
#pointlist = np.array([[0,0],[0,10],[2,12]]) #opp sving høyre
#pointlist = np.array([[0,20],[0,10],[2,8]]) #ned sving mot høyre(refrenceframe), dvs venstre for linjens perspektiv
#pointlist = np.array([[-1,20],[0,10],[-2,8]]) #ned sving mot venstre(refrenceframe)
#pointlist = np.array([[0,0],[0,10],[2,12],[10,12],[11,13],[12,16]])
pointlist = np.array([[0,0],[0,10],[-2,12],[-10,12],[-11,11],[-12,8]])


prev_line_start = np.array(pointlist[0]) #since the line starts in origo, this variable will be change whenever a new line is implemented
#next_line_end = np.array([12,10]) #høyre
#next_line_end = np.array([-10,12]) #venstre
next_line_end = np.array(pointlist[3])

for i in range(len(pointlist)-1):
    if i!= 0:
        prev_line_start = np.array(pointlist[i-1])
    print("\nStart of new loop" + str(i))
    xprev_line_start = prev_line_start[0] #x start-position for previous line
    yprev_line_start = prev_line_start[1] #y start-postion for previous line
    xs = pointlist[i][0] #x start-position for the arc
    ys = pointlist[i][1] #y start-position for the arc
    xe = pointlist[i+1][0] #x end-position for the arc
    ye = pointlist[i+1][1] #y end-position for the arc
    xnext_line_end =next_line_end[0]
    ynext_line_end =next_line_end[1]
    print("---")
    print("xs: " + str(xs))
    print("ys: " + str(ys))
    print("xe: " + str(xe))
    print("ye: " + str(ye))
    print("xprev: " + str(xprev_line_start))
    print("yprev: " + str(yprev_line_start))
    print("xendnext: " + str(xnext_line_end))
    print("yendnext: " + str(ynext_line_end))
    print("---")

    """To determine which side of the line from A = (xprev_line_start,yprev_line_start) to B = (xs,ys) (in our case the previous straight line), a point P = (xe,ye)
    is on we need to compute the value d. If d < 0, then the point lies on one side of the line, and if d > 0,
    then it lies on the other side. If d=0, then the point lies exactly on the line"""
    side=(xe-xprev_line_start)*(ys-yprev_line_start) - (ye-yprev_line_start)*(xs-xprev_line_start)
    #We choose direction -1 for left, 0 for on line and 1 for right
    if side < 0:
        dir = -1
    elif side >0:
        dir = 1
    else:
        dir = 0
        prev_line_start = [xs,ys]
        print("Mistake this should not be on the line, since it is an arc")
    print("dir: " + str(dir))

    #Now we calculate what the center of the arc is, not sure if it works with negative values, might have to add an if statement where we make sure the variable is positive with an absolute
    """ travel_x = xe-xs
    travel_y = ye-ys
    d = np.sqrt((xs-xe)**2 + (ys-ye)**2) #the distance between (xstart,ystart) and (xend,yend)
    theta = m.atan2(ye - ys, xe-xs) #The angle from position1 to position2
    adjustment_x = """
    print("---Center---")

    def gcenter(radius, xstart,ystart, xend,yend,dir):
        if dir != 0: #Should actually have an if statement that surely dont calculate lines
            xa = 0.5*(xend-xstart) #https://math.stackexchange.com/questions/1781438/finding-the-center-of-a-circle-given-two-points-and-a-radius-algebraically
            ya = 0.5*(yend-ystart)
            a = np.sqrt(xa**2 + ya**2)
            b = np.sqrt(radius**2-a**2)
            xmid = xstart + xa
            ymid = ystart + ya

            xcenter1 = xmid + b*ya/a
            ycenter1 = ymid - b*xa/a
            xcenter2 = xmid - b*ya/a
            ycenter2 = ymid + b*xa/a
            print("xcenter1: " + str(xcenter1))
            print("ycenter1: " + str(ycenter1))
            print("xcenter2: " + str(xcenter2))
            print("ycenter2: " + str(ycenter2))

            #To find the correct center we choose the center closest to the next lines end position
            next_end_distance1 = np.sqrt((xnext_line_end-xcenter1)**2 + (ynext_line_end-ycenter1)**2)
            next_end_distance2 = np.sqrt((xnext_line_end-xcenter2)**2 + (ynext_line_end-ycenter2)**2)

            if next_end_distance1 < next_end_distance2:
                xcenter = np.round(xcenter1,7)
                ycenter = np.round(ycenter1,7)
            elif next_end_distance2 < next_end_distance1:
                xcenter = np.round(xcenter2,7)
                ycenter = np.round(ycenter2,7)
            else:
                print("Couldnt find the correct center, might be on line")
                xcenter=None
                ycenter=None
        else:
            print("Couldnt find the correct center, might be on line")
            xcenter=None
            ycenter=None
            
        print("xcenter: " + str(xcenter))
        print("ycenter: " + str(ycenter))

        return xcenter,ycenter

    xcenter,ycenter = gcenter(r,xs,ys,xe,ye,dir)

    print("----Angles----")

    #Must find angle in and angle out for DFA input for the arcs, do this by using the previous and next line positions
    angle_in_r = m.atan2((ys-yprev_line_start),(xs-xprev_line_start)) #The end position for the previous line(which is the curves start) minus its start position in atan2 gives us the angle in
    angle_out_r = m.atan2((ynext_line_end-ye),(xnext_line_end-xe)) #The end position for the next line minus its start position(which is the curves end) in atan2 gives us the angle out

    print("Radian angle in: " +str(angle_in_r)) #Radians we need degrees for DFA file
    print("Radian angle out: " +str(angle_out_r)) #If the angles surpass 180 degress (meaning it goes downwards) the angle will be negative!!

    angle_in_d = angle_in_r*180/np.pi
    angle_out_d = angle_out_r*180/np.pi
    if angle_in_r <0:
        angle_in_d = 360+(angle_in_r*180/np.pi)
    if angle_out_r < 0:
        angle_out_d = 360+(angle_out_r*180/np.pi)
    print("Degree angle in: "+str(angle_in_d))
    print("Degree angle out: "+str(angle_out_d))
    print("----DFA file arc angles----") #Since DFA arcs can not go from a larger angle (e.g. 352) to a smaller angle(e.g.20), we gotta pull some tricks and reverse them or add 360 degrees
    
    going_up = ye - yprev_line_start
    going_right = xe- xprev_line_start
    turn_right_refframe = xe-xs
    turn_up_refframe = ye-ys
    print("right",going_right)
    print("up",going_up)
    print("turnright",turn_right_refframe)
    print("turnup", turn_up_refframe)
    
    if dir!=0:
        if abs(going_up/going_right) >= 1 and ye-ys>0:  #Here the curve is mostly going vertically contra sideways on entry  
            if going_up >= 0 and turn_right_refframe >= 0: #up and turn towards right
                if angle_in_d < 90:
                    angle_in = angle_out_d + 90 - 360 #we got to swap in and output angles since the arc only move right
                    angle_out = angle_in_d + 90
                if angle_in_d >= 90:
                    angle_in = angle_out_d + 90 #we got to swap in and output angles since the arc only move right
                    angle_out = angle_in_d + 90
            elif going_up >= 0 and turn_right_refframe < 0: #up and turn towards left, 
                if angle_in_d >= 90 and angle_out_d >= 90:
                    angle_in = angle_in_d - 90
                    angle_out = angle_out_d - 90
                if angle_in_d < 90 or angle_out_d < 90:
                    angle_in = angle_in_d - 90 + 360
                    angle_out = angle_out_d - 90 +360
            elif going_up < 0 and turn_right_refframe >= 0: #down and turn towards right
                if angle_in_d >= 90 and angle_out_d >= 90:   
                    angle_in = angle_in_d - 90
                    angle_out = angle_out_d - 90
                if angle_out_d < 90:
                    angle_in = angle_in_d - 90
                    angle_out = angle_out_d - 90 + 360
            elif going_up < 0 and turn_right_refframe < 0: #down and turn towards left
                if angle_in_d >= 90 and angle_out_d >= 90:   
                    angle_in = angle_out_d + 90 #we got to swap in and output angles since the arc only move right
                    angle_out = angle_in_d + 90
                if angle_out_d < 90:
                    angle_in = angle_out_d - 90
                    angle_out = angle_in_d - 90 + 360
        elif abs(going_up/going_right) < 1: #Here the curve is mostly going sideways contra vertically on entry 
            print("bbbb") 
            if going_right >= 0 and turn_up_refframe < 0: #right and turns downward
                if angle_in_d < 90:
                    angle_in = angle_out_d + 90 - 360 #we got to swap in and output angles since the arc only move right
                    angle_out = angle_in_d + 90
                if angle_in_d >= 90:
                    angle_in = angle_out_d + 90 #we got to swap in and output angles since the arc only move right
                    angle_out = angle_in_d + 90
            elif going_right >= 0 and turn_up_refframe >= 0: #right and turns up
                if angle_in_d >= 90 and angle_out_d >= 90: 
                    angle_in = angle_in_d - 90
                    angle_out = angle_out_d - 90
                if angle_out_d < 90:
                    angle_in = angle_in_d - 90 + 360
                    angle_out = angle_out_d - 90 + 360
            elif going_right < 0 and turn_up_refframe >= 0: #left and turn up
                if angle_in_d < 90:
                    angle_in = angle_out_d + 90 - 360 #we got to swap in and output angles since the arc only move right
                    angle_out = angle_in_d + 90
                if angle_in_d >= 90:
                    angle_in = angle_out_d + 90 #we got to swap in and output angles since the arc only move right
                    angle_out = angle_in_d + 90
            elif going_right < 0 and turn_up_refframe < 0: #left and turn down
                if angle_in_d >= 90 and angle_out_d >= 90: 
                    angle_in = angle_in_d - 90
                    angle_out = angle_out_d - 90
                if angle_out_d < 90:
                    angle_in = angle_in_d - 90 + 360
                    angle_out = angle_out_d - 90 + 360
        else:
            angle_in = None
            angle_out = None
            print("Something went wrong with the translation of angles")
        print("Angle in: " + str(angle_in))
        print("Angle out: " + str(angle_out))
        if i < len(pointlist)-3:
            next_line_end = np.array(pointlist[i+3])










    #DETTE SKAL POTENSIELT SLETTES
    
    """
    if noe: #up and turn towards right
        xcenter =
        ycenter =
    elif noe: #up and turn towards left
        xcenter =
        ycenter =
    elif noe: #down and turn towards right
        xcenter =
        ycenter =
    elif noe: #down and turn towards left
        xcenter =
        ycenter =
    else:
        xcenter = None
        ycenter = None
        print("Something went wrong with the positioning of the arc center")"""

    """
    print("----Center ----")
    print("xc1 " + str(xcenter1))
    print("yc1 " + str(ycenter1))
    print("xc2 " + str(xcenter2))
    print("yc2 " + str(ycenter2))
    print("----Angles----")"""

    """
    print(d)
    print("aaa")
    link =abs(((2*r/d)**2)-1) #SOMETHING AINT RIGHT, finne formel som finer riktig senter!!!
    if link <0:
        link = 0
    else:
        link =np.sqrt(abs(((2*r/d)**2)+1))

    print((xs+xe)/2)
    print((ys-ye)/2)
    print((2*r/d)**2)
    xcenter1 = (xs+xe)/2 + ((ys-ye)/2)* link
    xcenter2 = (xs+xe)/2 - ((ys-ye)/2)*link

    ycenter1 = (ys+ye)/2 - ((xs-xe)/2)*link
    ycenter2 = (ys+ye)/2 + ((xs-xe)/2)*link"""

    