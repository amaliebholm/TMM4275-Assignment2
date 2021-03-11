#Creates a costume rail from the user-inputs adjusting and pasting the templates
#for lines and curves into the rail template

dfaPath = "C:\\Users\\Amalie\\Documents\\GitHub\\TMM4275-KBE-project\\DFAs\\" #The location of your DFA files

rail = open(dfaPath + "templates\\Rail_template.dfa", "r") 
fileContent = rail.read()
rail.close() #Opens and reads the DFA template so that a new DFA file of the order can be made

arc_temp = open(dfaPath + "templates\\Arc_template.dfa", "r") 
fileContent = arc_temp.read()
arc_temp.close() #Opens and reads the arc DFA template so that curves can be added to the rail

line_temp = open(dfaPath + "templates\\Line_template.dfa", "r") 
fileContent = line_temp.read()
line_temp.close() #Opens and reads the line DFA template so that straight lines can be added to the rail

