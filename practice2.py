import math as m
import numpy as np

def arc_center(radius, xstart,ystart, xend,yend, dir):
    y = yend - ystart
    x = xend - xstart
    th = m.atan2(y, x)
    print("Theta:", th)

    th += dir * m.pi / 2

    xPlus = radius * m.cos(th)
    yPlus = radius * m.sin(th)

    ret = (xstart + xPlus, ystart + yPlus)
    print("Arc center:", ret)
    return ret

def arc_center2(x1,y1,x2,y2,ang1,ang2,dir):
    #x is the distance from point 1 to point 2
    x = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    #finds the total angle of the arc
    if dir == True: #right 
        theta = ang2 - ang1
        if ang1 > ang2:
            theta = ang2 + (360-ang1)
    elif dir == False: #left
        theta = ang1 - ang2
        if ang2 > ang1:
            theta = ang1 + (360-ang2)
    print("Theta:" + theta)
    r = np.sqrt((x**2) / 2*(1-m.cos(theta)))


arc_center2(0,0,2,2,0,90,1)