#Creates a costume rail from the user-inputs adjusting and pasting the templates
#for lines and curves into the rail template

dfaPath = "C:\\Users\\Amalie\\Documents\\GitHub\\TMM4275-KBE-project\\DFAs\\" #The location of your DFA files

f = open(dfaPath + "templates\\Rail_template.dfa", "r") 
rail = f.read()
f.close() #Opens and reads the DFA template so that a new DFA file of the order can be made

startx = 0#added by user input
starty = 0
startz = 0

rail = rail_temp.replace("<STARTX>", str(startx)) #First we need to insert the start position for our rail
rail = rail.replace("<STARTY>", str(starty))
rail = rail.replace("<STARTZ>", str(startz))

f = open(dfaPath + "templates\\Arc_template.dfa", "r") 
arc_temp = f.read()
f.close() #Opens and reads the arc DFA template so that curves can be added to the rail

f = open(dfaPath + "templates\\Line_template.dfa", "r") 
line_temp = f.read()
f.close() #Opens and reads the line DFA template so that straight lines can be added to the rail


def add_arc(masse, sjuke,inputs):
    new_arc = arc_temp.copy()
    new_arc = new_arc.replace("<INDEX>", str(index))
    new_arc = new_arc.replace("<RADIUS>", str(radius))
    new_arc = new_arc.replace("<ANGLE1>", str(angle1))
    new_arc = new_arc.replace("<ANGLE2>", str(angle2))
    new_arc = new_arc.replace("<XCENTER>", str(x))
    new_arc = new_arc.replace("<YCENTER>", str(y))
    new_arc = new_arc.replace("<ZCENTER>", str(z))

    rail = rail + new_arc

def add_line(masse, sjuke,inputs):
    new_line = line_temp.copy()
    new_line = new_line.replace("<INDEX>", str(index))
    new_line = new_line.replace("<X1>", str(x1))
    new_line = new_line.replace("<X2>", str(x2))
    new_line = new_line.replace("<Y1>", str(y1))
    new_line = new_line.replace("<Y2>", str(y2))
    new_line = new_line.replace("<Z1>", str(z1))
    new_line = new_line.replace("<Z2>", str(z2))

    rail = rail + new_line

