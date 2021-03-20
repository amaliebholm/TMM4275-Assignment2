import math as m
import numpy as np
#Creates a costume rail from the user-inputs adjusting and pasting the templates
#for lines and curves into the rail template

dfaPath = "K:\\Biblioteker\\Dokumenter\\Skole\\Automatisering\\TMM4275-Assignment2\\DFAs\\" #The location of your DFA files

f = open(dfaPath + "templates\\Rail_template.dfa", "r") 
rail = f.read()
f.close() #Opens and reads the DFA template so that a new DFA file of the order can be made

f = open(dfaPath + "templates\\Arc_template.dfa", "r") 
arc_temp = f.read()
f.close() #Opens and reads the arc DFA template so that curves can be added to the rail

f = open(dfaPath + "templates\\Line_template.dfa", "r") 
line_temp = f.read()
f.close() #Opens and reads the line DFA template so that straight lines can be added to the rail

f = open(dfaPath + "templates\\path_and_combine.dfa", "r") 
the_end = f.read()
f.close() #Opens and reads the DFA file that contains the the joining and coloring

startx = 0#added by user input?
starty = 0
startz = 0

rail = rail.replace("Rail_template (ug_base_part)", "Rail_Order (ug_base_part)") #Replaces the template with the customers chair values
rail = rail.replace("<STARTX>", str(startx)) #First we need to insert the start position for our rail
rail = rail.replace("<STARTY>", str(starty))
rail = rail.replace("<STARTZ>", str(startz))



def add_arc(index,radius,angle1,angle2,x,y,z,string):
    new_arc = arc_temp
    new_arc = new_arc.replace("<arc_temp>", "element_" + str(index))
    new_arc = new_arc.replace("<RADIUS>", str(radius))
    new_arc = new_arc.replace("<ANGLE1>", str(angle1))
    new_arc = new_arc.replace("<ANGLE2>", str(angle2))
    new_arc = new_arc.replace("<XCENTER>", str(x))
    new_arc = new_arc.replace("<YCENTER>", str(y))
    new_arc = new_arc.replace("<ZCENTER>", str(z))

    string = string + new_arc
    return string

def add_line(index,x1,y1,z1,x2,y2,z2,string):
    new_line = line_temp
    new_line = new_line.replace("<line_temp>", "element_" + str(index))
    new_line = new_line.replace("<X1>", str(x1))
    new_line = new_line.replace("<X2>", str(x2))
    new_line = new_line.replace("<Y1>", str(y1))
    new_line = new_line.replace("<Y2>", str(y2))
    new_line = new_line.replace("<Z1>", str(z1))
    new_line = new_line.replace("<Z2>", str(z2))

    string = string + new_line
    return string


#Vi får inn en liste med start og slutt punkter for hvert element
#pointlist = np.array([[0,0],[0,10],[-2,12]]) #opp,sving venstre
#pointlist = np.array([[0,0],[0,10],[2,12]]) #opp sving høyre
#pointlist = np.array([[0,20],[0,10],[2,8]]) #ned sving mot høyre(refrenceframe), dvs venstre for linjens perspektiv
#pointlist = np.array([[-1,20],[0,10],[-2,8]]) #ned sving mot venstre(refrenceframe)
#pointlist = np.array([[0,0],[0,10],[2,12],[10,12],[11,13],[12,16]])
pointlist = np.array([[0,0,0],[0,10,0],[-2,12,0],[-10,12,0],[-11.41421356,11.41421356,0],[-13.41421356,9.41421356,0]])



#next_line_end = np.array([12,10]) #høyre
#next_line_end = np.array([-10,12]) #venstre


#The feeder can only make turns with radius of 2m
r = 2
element_string=" "
prev_line_start = np.array(pointlist[0]) #variable for the start of the line that came before the arc, this variable will be change whenever a new line is implemented
next_line_end = np.array(pointlist[3]) #variable for the end of the line that comes after the arc, this variable will be change whenever a new line is implemented
#Assume every other line and arc?
for i in range(len(pointlist)-1):
    if i==0 or i/2==np.round(i/2):
        print("\nStart on new loop for line: " + str(i))
        print("---")
        rail = add_line(i,pointlist[i][0],pointlist[i][1],pointlist[i][2],pointlist[i+1][0],pointlist[i+1][1],pointlist[i+1][2],rail)
    #arcs
    elif i!=0 and i/2!=np.round(i/2): #Temp solution to only get arc, here the arc and lines are every other time
        if i!= 0:
            prev_line_start = np.array(pointlist[i-1])
        if i < len(pointlist)-2:
                next_line_end = np.array(pointlist[i+2])
        print("\nStart on new loop for arc: " + str(i))
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


        print("---Center---")

        if (dir != 0): #Should actually have an if statement that surely dont calculate lines
            xa = 0.5*(xe-xs) #https://math.stackexchange.com/questions/1781438/finding-the-center-of-a-circle-given-two-points-and-a-radius-algebraically
            ya = 0.5*(ye-ys)
            a = np.sqrt(xa**2 + ya**2)
            b = np.sqrt(r**2-a**2)
            xmid = xs + xa
            ymid = ys + ya

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
        
        if dir!=0: #Here we change the angles from the reference frame to the arc angles in the dfa file
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
        rail = add_arc(i,r,angle_in,angle_out,xcenter,ycenter,0,rail) # Temp set to 0 if this is correct, thinking maybe z = pointlist[i][2] is for the roof mounting
    else:
        print("Neither arc or line?")

    print((len(pointlist)-2))    

    if i != (len(pointlist)-2): #Making the string that says what parts to curve_join
        element_string = element_string + "element_" + str(i) + ":, "
    else:
        element_string = element_string + "element_" + str(i) + ":"




rail = rail + the_end

#rail = rail.replace("<ALL_ELEMENTS>", "element_1:")
rail = rail.replace("<ALL_ELEMENTS>", element_string)

f = open(dfaPath + "Rail_Order.dfa", "w") #Saves the customers chair as a new DFA file with the name My_Chair_Order.dfa
f.write(rail)
f.close()
