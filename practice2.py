import math as m
import numpy as np

#The feeder can only make turns with radius of 2m
r = 2

#Vi får inn en liste med start og slutt punkter for hvert element
pointlist = np.array([[-2,-10],[-2,100],[0,102]]) #eksempel på en rett linje og så en kruve som har gått 180grader

prev_line_start = np.array(pointlist[0]) #since the line starts in prigo, this variable will be change whenever a new line is implemented
for i in range(len(pointlist)-1):
    print("Start of new loop" + str(i))
    prevx = prev_line_start[0] #x start-position for previous line
    prevy = prev_line_start[1] #y start-postion for previous line
    xs = pointlist[i][0] #x start-position for the arc
    ys = pointlist[i][1] #y start-position for the arc
    xe = pointlist[i+1][0] #x end-position for the arc
    ye = pointlist[i+1][1] #y end-position for the arc
    print("---")
    print(xs)
    print(ys)
    print(xe)
    print(ye)
    print("---")

    """To determine which side of the line from A = (prevx,prevy) to B = (xs,ys) (in our case the previous straight line), a point P = (xe,ye)
    is on we need to compute the value d. If d < 0, then the point lies on one side of the line, and if d > 0,
    then it lies on the other side. If d=0, then the point lies exactly on the line"""
    d=(xe-prevx)*(ys-prevy) - (ye-prevy)*(xs-prevx)
    #We choose direction -1 for left, 0 for on line and 1 for right
    if d < 0:
        dir = -1
    elif d >0:
        dir = 1
    else:
        dir = 0
        print("Mistake this should not on the line, since it is an arc")
    print("dir: " + str(dir))

    #Now we calculate what the center of the arc is

    d = np.sqrt((xs-xe)**2 + (ys-ye)**2) #the distance between (xstart,ystart) and (xend,yend)
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
    ycenter2 = (ys+ye)/2 + ((xs-xe)/2)*link

    print("xc1 " + str(xcenter1))
    print("yc1 " + str(ycenter1))
    print("xc2 " + str(xcenter2))
    print("yc2 " + str(ycenter2))
    print("----center done----")

    