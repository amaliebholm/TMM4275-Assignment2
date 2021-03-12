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



def add_arc(index,radius,angle1,angle2,x,y,z,string):
    new_arc = arc_temp
    new_arc = new_arc.replace("<INDEX>", str(index))
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
    new_line = new_line.replace("<INDEX>", str(index))
    new_line = new_line.replace("<X1>", str(x1))
    new_line = new_line.replace("<X2>", str(x2))
    new_line = new_line.replace("<Y1>", str(y1))
    new_line = new_line.replace("<Y2>", str(y2))
    new_line = new_line.replace("<Z1>", str(z1))
    new_line = new_line.replace("<Z2>", str(z2))

    string = string + new_line
    return string

rail = add_line(1,0,0,0,0,10000,0,rail)
rail = rail + the_end

rail = rail.replace("<ALL_ELEMENTS>", "line_1:")

f = open(dfaPath + "Rail_Order.dfa", "w") #Saves the customers chair as a new DFA file with the name My_Chair_Order.dfa
f.write(rail)
f.close()
