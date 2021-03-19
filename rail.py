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

startx = 0#added by user input
starty = 0
startz = 0

rail = rail.replace("Rail_template (ug_base_part)", "Rail_Order (ug_base_part)") #Replaces the template with the customers chair values
rail = rail.replace("<STARTX>", str(startx)) #First we need to insert the start position for our rail
rail = rail.replace("<STARTY>", str(starty))
rail = rail.replace("<STARTZ>", str(startz))



def add_arc(index,radius,angle1,angle2,x,y,z,string,left):
    new_arc = arc_temp
    new_arc = new_arc.replace("<arc_temp>", "element_" + str(index))
    new_arc = new_arc.replace("<RADIUS>", str(radius))
    new_arc = new_arc.replace("<ANGLE1>", str(angle1))
    new_arc = new_arc.replace("<ANGLE2>", str(angle2))
    if left == True:
        new_arc = new_arc.replace("<XCENTER>", str(x - radius))
    if left == False:
        new_arc = new_arc.replace("<XCENTER>", str(x + radius))
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

def get_center(radius, xstart,ystart, xend,yend, dir):
    y = yend - ystart
    x = xend - xstart
    theta = m.atan2(y, x)
    print("Theta:", theta)

    theta += dir * m.pi / 2

    xPlus = radius * m.cos(theta)
    yPlus = radius * m.sin(theta)
    d = np.sqrt((xstart-xend)**2 + (ystart-yend)**2)
    katet = np.sqrt(radius**2 - d*0.5)
    print("xs",xstart)
    print("xe",xend)
    print("xplus",0.5*d*np.cos(theta) + katet*np.sin(theta -1.57))
    print("ys",ystart)
    print("ye",yend)
    print("sin", np.sin(theta))
    print(d*np.cos(theta))
    xres = xstart - d*np.cos(theta)

    ret = [xstart - d*np.cos(theta), np.round(yend - 2*np.sin(theta),6)]

    print("Arc center:", ret)
    return ret

def gcenter(radius, xstart,ystart, xend,yend, dir):
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


#index,radius,angle1,angle2,x,y,z,string,left
rail = add_line(1,0,0,0,2,2,0,rail)
rail = add_arc(2,4,0,110,0,2,0,rail,False)
#rail = add_arc(2,4,100,170,4,10,0,rail,False)


rail = rail + the_end

rail = rail.replace("<ALL_ELEMENTS>", "element_1:")
print(rail)
f = open(dfaPath + "Rail_Order.dfa", "w") #Saves the customers chair as a new DFA file with the name My_Chair_Order.dfa
f.write(rail)
f.close()

#get_center(2, 2,2, 4,4, 1)
gcenter(2, 2,2, 0,0, 1)