from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import pathAlgorithm
import numpy as np
import math as m


# Initial valies of room size
room_height = 0
room_length = 0
room_width = 0
rail_height = 0

# Placing points into different lists
attachement_points = []  # On form [(x,y), height]
visit_locations = []  # On form [(x,y), height]
obstacles = []  # On form [(x,y),(x,y),(x,y),(x,y) height], to form an area

# Initial values of variables
x = 0
x_2 = 0
x_3 = 0
x_4 = 0
y = 0
y_2 = 0
y_3 = 0
y_4 = 0
obs_string = ""
spes_height = 0
var_type = ""
algo_path = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

HOST_NAME = '127.0.0.1'  # locathost - http://127.0.0.1
# Complete address would be: http://127.0.0.1:1234
PORT_NUMBER = 1234

# Setting the local paths
#pathToImg = "/Users/kasper/Documents/GitHub/TMM4275-Assignment2/rail_model_image.png" # Ama Windows
#pathToDFA = "/Users/kasper/Documents/GitHub/TMM4275-Assignment2/DFAs/" # Ama Windows

pathToImg = "C:\\Users\\Amalie\\Documents\\GitHub\\TMM4275-Assignment2\\rail_model_image.png" # Ama Windows
pathToDFA = "C:\\Users\\Amalie\\Documents\\GitHub\\TMM4275-Assignment2\\DFAs\\Rail_Order.py" # Ama Windows#

# Initial time for changed file, uploaded image 
lastTimeFileChange = 0.0

# Handler of HTTP requests / responses


class MyHandler(BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        global room_height, room_width, room_length, matrix_room, matrix_height, rail_height, x, y, obs_string, spes_height, var_type,algo_path,attachement_points
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        path = s.path
        if path.find("/") != -1 and len(path) == 1:
            s.wfile.write(
                bytes('<html><head><title>Cool interface.</title></head>', 'utf-8'))
            s.wfile.write(
                bytes("<body><p>Current path: " + path + "</p>", "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))
        elif path.find("/info") != -1:
            s.wfile.write(
                bytes('<html><head><title>Cool interface.</title></head>', 'utf-8'))
            s.wfile.write(
                bytes("<body><p>Current path: " + path + "</p>", "utf-8"))
            s.wfile.write(bytes("<body><p>Let's order a chair</p>", "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))
        # The webpage to start the rail order and set the room size
        elif path.find("/setSize") != -1:
            s.wfile.write(bytes(
                '<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            # Create a form to take in values
            s.wfile.write(
                bytes('<form action="/setSize" method="post">', 'utf-8'))

            s.wfile.write(bytes('<h4>Set room size (m):</h4>', "utf-8"))
            s.wfile.write(bytes(
                '<br>Room height:<br><input type="text" name="room_height" value="0">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Room width:<br><input type="text" name="room_width" value="0">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Room length:<br><input type="text" name="room_length" value="0">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Height from floor to railing:<br><input type="text" name="rail_height" value="0">', "utf-8"))

            s.wfile.write(bytes(
                '<br><br><button type="submit">Set size</button><p>Click "Set size" to set the room size</p>', "utf-8"))
            s.wfile.write(bytes(
                '<button type="submit" formaction="/setVariables">Continue</button><p>Click "Continue" to continue to add varialbes</p></form>', "utf-8"))

            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/Images/sketch_room.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))

        else:
            s.wfile.write(
                bytes('<html><head><title>Cool interface.</title></head>', 'utf-8'))
            s.wfile.write(
                bytes("<body><p>The path: " + path + "</p>", "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))

    def do_POST(s):
        global room_height, room_width, room_length, matrix_room, matrix_height, rail_height, x, y, obs_string, spes_height, var_type,algo_path,attachement_points
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        room_constraint = False  # Boolean to see check if room is within constraits
        # B oolean to see check if variable given is within the room
        variable_constraints = False

        # Check what is the path
        path = s.path
        print("Path: ", path)

        if path.find("/setSize") != -1:
            # Gets the string with the rail values
            content_len = int(s.headers.get('Content-Length'))
            post_body = s.rfile.read(content_len)
            param_line = post_body.decode()
            print("Body: ", param_line)

            # Splits string so that the values can be set for each variable
            splitString = param_line.split("&")
            newSplit = []
            for i in splitString:
                newSplit.append(i.split("="))

            room_height = int(newSplit[0][1])
            room_width = int(newSplit[1][1])
            room_length = int(newSplit[2][1])
            rail_height = int(newSplit[3][1])
            # Every variable has been given their value from the string

            if rail_height < room_height:
                if room_height > 0:
                    if room_length > 0:
                        if room_width > 0:
                            print("Room size OK")
                            room_constraint = True

            s.wfile.write(bytes(
                '<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            # Create a form to add variables
            s.wfile.write(
                bytes('<form action="/setSize" method="post">', 'utf-8'))

            s.wfile.write(
                bytes('<h4>Your room size is set to (m):</h4>', "utf-8"))
            s.wfile.write(bytes(
                '<br>Room height:<br><input type="text" name="room_height" value="' + str(room_height) + '">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Room width:<br><input type="text" name="room_width" value="' + str(room_width) + '">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Room length:<br><input type="text" name="room_length" value="' + str(room_length) + '">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Height from floor to railing:<br><input type="text" name="rail_height" value="' + str(rail_height) + '">', "utf-8"))
            # Checking if the variable is within constraints
            s.wfile.write(bytes(
                '<br><br><button type="submit">Set size</button> <p>Click "Set size" to set the room size</p>', "utf-8"))

            if room_constraint:  # If the room is within the constraints: submit the valies and continue
                s.wfile.write(bytes(
                    '<button type="submit" formaction="/setVariables">Continue</button><p>Click "Continue" to continue to add varialbes</p>', "utf-8"))
            else:  # If the room is not within the constraints: alert that the values are outside constraints
                print("Room size NOT OK")
                s.wfile.write(bytes('<script>function alertFunction(){alert("The rail height, ' + str(rail_height) + ', must be lower than the room height, ' + str(
                    room_height) + '.  Room height, ' + str(room_height) + ', width, ' + str(room_width) + ', and length ' + str(room_length) + ', must be more than zero!");} </script>', "utf-8"))
                s.wfile.write(bytes(
                    '<button onclick="alertFunction()">Continue</button><p>Click "Continue" to continue to add varialbes</p>', "utf-8"))

            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/Images/sketch_room.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
            s.wfile.write(bytes('</form></body></html>', "utf-8"))

        elif path.find("/setVariables") != -1:  # Web page to add variables in the room
            # Gets the string with the rail values
            content_len = int(s.headers.get('Content-Length'))
            post_body = s.rfile.read(content_len)
            param_line = post_body.decode()
            print("Body: ", param_line)

            # Splits string so that the values can be set for each variable
            splitString = param_line.split("&")
            newSplit = []
            for i in splitString:
                newSplit.append(i.split("="))

            try:
                x = int(newSplit[0][1])
                y = int(newSplit[1][1])
                spes_height = int(newSplit[2][1])
                x_2 = int(newSplit[3][1])
                y_2 = int(newSplit[4][1])
                x_3 = int(newSplit[5][1])
                y_3 = int(newSplit[6][1])
                x_4 = int(newSplit[7][1])
                y_4 = int(newSplit[8][1])
                var_type = newSplit[9][1]
                # Every variable has been given their value from the string
            except:
                pass

            # Checking if the koordinates are within the room size
            try:
                if x <= room_width and x >= 0:
                    if x_2 <= room_width and x_2 >= 0:
                        if x_3 <= room_width and x_3 >= 0:
                            if x_4 <= room_width and x_4 >= 0:
                                if y <= room_length and y >= 0:
                                    if y_2 <= room_length and y_2 >= 0:
                                        if y_3 <= room_length and y_3 >= 0:
                                            if y_4 <= room_length and y_4 >= 0:
                                                if spes_height > 0:
                                                    print("Params OK")
                                                    variable_constraints = True
            except:
                pass

            s.wfile.write(bytes(
                '<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            # Create a form to add variables
            s.wfile.write(
                bytes('<form action="/setVariables" method="post">', 'utf-8'))
            s.wfile.write(bytes('<p>You have set the room size (m): room height: ' + str(room_height) + ', room width: ' + str(
                room_width) + ', room length: ' + str(room_length) + ', rail hight: ' + str(rail_height) + '.</p>', 'utf-8'))

            s.wfile.write(bytes(
                '<button type="submit" formaction="/setSize">Change</button><p>Click "Change" to set the new room size</p>', "utf-8"))

            s.wfile.write(bytes('<h4>Add variales in the room:</h4>', "utf-8"))
            s.wfile.write(
                bytes('<p>Different varialbes you can add:</p>', "utf-8"))
            s.wfile.write(
                bytes('<p>1. An attachment point for the rail in the ceiling</p>', "utf-8"))
            s.wfile.write(
                bytes('<p>2. Feeding location for the cart</p>', "utf-8"))
            s.wfile.write(
                bytes('<p>3. Locations the cart should visit</p>', "utf-8"))
            s.wfile.write(bytes(
                '<p>4. An obstacle in the room, the feeder can not pass through these points</p>', "utf-8"))

            # Image illustrating 3D and 2D perspective
            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/Images/sketch_room.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))

            # Adding the coordinates of the variable
            s.wfile.write(bytes(
                '<h4>Seen from above, where are the variables located in the room? Give the coordinates below:</h4>', "utf-8"))
            s.wfile.write(bytes(
                '<p>Go through the room chronologically and add variables as the appear in the room.</p>', "utf-8"))
            s.wfile.write(
                bytes('Width coordinate: <input type="text" name="x" value="0">', "utf-8"))
            s.wfile.write(
                bytes('<br>Length coordinate: <input type="text" name="y" value="0">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Ceiling height in this area (change if it differs form gnereal height): <input type="text" name="spes_height" value="' + str(room_height) + '">', "utf-8"))
            s.wfile.write(bytes(
                '<br><br> If the varaible is an obstacle add three more points, marking off the area the obstacle obtain in the room, filling the points: [width coordinate, length coordinate]', "utf-8"))
            s.wfile.write(bytes(
                '<br><br>Obstacle coordinate 2:<br> Width coordinate: <input type="text" name="x_2" value="0"> Length coordinate: <input type="text" name="y_2" value="0">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Obstacle coordinate 3:<br> Width coordinate: <input type="text" name="x_3" value="0"> Length coordinate: <input type="text" name="y_3" value="0">', "utf-8"))
            s.wfile.write(bytes(
                '<br>Obstacle coordinate 4:<br> Width coordinate: <input type="text" name="x_4" value="0"> Length coordinaten: <input type="text" name="y_4" value="0">', "utf-8"))

            # Adding type of variable
            s.wfile.write(bytes('<br>Type of variable:<br><select name="var_type" id="var_type"><option value="ATTACH_POINT">1. Attachment point</option><option value="FEED_LOC">2. Feeding location</option><option value="VISIT_LOC">3. Locations the cart should visit</option><option value="OBSTACLE">4. Obstacle </option></select>', "utf-8"))
            # Checking if the variable is within constraints
            s.wfile.write(
                bytes('<button type="submit">Add variable</button>', "utf-8"))

            if variable_constraints:  # Add if the variable to the lists of variables if it is within the constraints

                if var_type == "RESET":
                    var_type_str = "Reset area"
                elif var_type == "ATTACH_POINT":
                    attachement_points.append([[x, y], spes_height])
                    var_type_str = "Attachment point"
                elif var_type == "FEED_LOC":
                    attachement_points.insert(0, [[x, y], spes_height])
                    # Feeding location inserted at start of the visit_location list
                    var_type_str = "Feeding location"
                elif var_type == "VISIT_LOC":
                    visit_locations.append([[x, y], spes_height])
                    var_type_str = "Location to visit"
                elif var_type == "OBSTACLE":
                    obstacles.append(
                        [[x, y], [x_2, y_2], [x_3, y_3], [x_4, y_4]])
                    var_type_str = "Obstacle"

            else:  # Write message that the variable was not valid
                print("Variable NOT OK")
                s.wfile.write(bytes(
                    '<br><strong style="color: red;">The variable was outside the constraints.</strong>', "utf-8"))
                s.wfile.write(bytes('<p style="color:red;"> Width coordinates, ' + str(x) + ' (Obsacle: ' + str(x_2) + ' ,' + str(
                    x_3) + ' ,' + str(x_4) + ') must be within the room width ' + str(room_width) + '. </p>', "utf-8"))
                s.wfile.write(bytes('<p style="color:red;"> Length coordinates, ' + str(y) + ' (Obsacle: ' + str(y_2) + ' ,' + str(
                    y_3) + ' ,' + str(y_4) + ') must be within the room length ' + str(room_length) + '. </p>', "utf-8"))
                s.wfile.write(bytes('<p style="color:red;">Ceiling height, ' +
                                    str(spes_height) + ' must be positive.</p>', "utf-8"))

            # Print out the current lists of points
            print("Attachment points:")
            print(attachement_points)
            print("Visiting locations:")
            print(visit_locations)
            print("Obstacles")
            print(obstacles)

            # Write the points as lists on the webpage
            list_att = ""
            for li in attachement_points:
                list_att += "<li>" + str(li) + "</li>"
            s.wfile.write(bytes(
                '<br><p>List of attachement points: [[width coordinate, length coordinate], ceiling height]:</p>', "utf-8"))
            s.wfile.write(bytes('<ul>' + list_att + '</ul>', "utf-8"))

            list_visit = ""
            for li in visit_locations:
                list_visit += "<li>" + str(li) + "</li>"
            s.wfile.write(bytes('<p>List of locations to visit:</p>', "utf-8"))
            s.wfile.write(bytes('<ul>' + list_visit + '</ul>', "utf-8"))

            list_obs = ""
            for li in obstacles:
                list_obs += "<li>" + str(li) + "</li>"
            s.wfile.write(bytes('<p>List of obstacles:</p>', "utf-8"))
            s.wfile.write(bytes('<ul>' + list_obs + '</ul>', "utf-8"))

            # Continue to sendOrder
            s.wfile.write(bytes(
                '<button type="submit" formaction="/sendOrder">Submit</button><p>Click "Submit" to send the order of your rail</p></form>', "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))

            return room_height, room_width, room_length, rail_height, attachement_points, visit_locations, obstacles

        # Review of order, and allowing the customer to go back and reset at different points
        elif path.find("/sendOrder") != -1:
            global algo_path
            all_locations = attachement_points.copy() + visit_locations.copy()
            algo_path = pathAlgorithm.pathAlgorithm(
                2000).preProcessData(all_locations)
            print("PATH: ", algo_path)
            
        pointlist = algo_path #USE these when working togheter with the dfa server
        mount_list = attachement_points
        print(pointlist)

        fixedlist = []
        for place in pointlist: #Here we transform from meters to millimeters
            fixed_part_list = [i * 1000 for i in place]
            fixedlist.append(fixed_part_list)
        pointlist = fixedlist 

        fixedlist = []
        for place in mount_list: #Here we transform from meters to millimeters
            fixed_part_list = [i * 1000 for i in place]
            fixedlist.append(fixed_part_list)
        mount_list = fixedlist 

        dfaPath = "C:\\Users\\Amalie\\Documents\\GitHub\\TMM4275-Assignment2\\DFAs\\"
        #The location of your DFA files

        f = open(dfaPath + "templates\\Rail_template.dfa", "r") 
        rail = f.read()
        f.close() #Opens and reads the DFA template so that a new DFA file of the order can be made

        f = open(dfaPath + "templates\\Arc_template.dfa", "r") 
        arc_temp = f.read()
        f.close() #Opens and reads the arc DFA template so that curves can be added to the rail

        f = open(dfaPath + "templates\\Line_template.dfa", "r") 
        line_temp = f.read()
        f.close() #Opens and reads the line DFA template so that straight lines can be added to the rail

        f = open(dfaPath + "templates\\Roof_mount_template.dfa", "r") 
        mount_temp = f.read()
        f.close() #Opens and reads the line DFA template so that straight lines can be added to the rail

        f = open(dfaPath + "templates\\path_and_combine.dfa", "r") 
        the_end = f.read()
        f.close() #Opens and reads the DFA file that contains the the joining and coloring

        startx = pointlist[0][0] 
        starty = pointlist[0][1]
        startz = rail_height

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

        def add_roof_mount(index,x,y,z,roof,string): #In this case z is the coordinate of the lowest point of the rail_profile
            new_mount = mount_temp
            new_mount = new_mount.replace("<roofmount_temp>", "mount_" + str(index))
            new_mount = new_mount.replace("<X>", str(x))
            new_mount = new_mount.replace("<Y>", str(y))
            new_mount = new_mount.replace("<Z>", str(z+313.334))
            new_mount = new_mount.replace("<height>", str(roof-z-313.334))

            string = string + new_mount
            return string


        #The feeder can only make turns with radius of 2m
        r = 2000
        element_string=" "
        prev_line_start = np.array(pointlist[0]) #variable for the start of the line that came before the arc, this variable will be change whenever a new line is implemented
        next_line_end = np.array(pointlist[3]) #variable for the end of the line that comes after the arc, this variable will be change whenever a new line is implemented
        adjusted_points = [pointlist[0]] 
        for i in range(len(pointlist)-2): #This for loop adjust the lines the lines length so that there are room for the curves
            line_up = pointlist[i+1][1] - pointlist[i][1] #value for how much the line is going up/down towards corner
            line_right = pointlist[i+1][0] - pointlist[i][0] #value for how much the line is going right/left towards corner
            line_turn_right_refframe = pointlist[i+2][0] - pointlist[i+1][0] ##value for how much the line is going right/left after corner
            line_turn_up_refframe = pointlist[i+2][1] - pointlist[i+1][1] #value for how much the line is going up/down towards corner
            """
            print("line_up",line_up)
            print("line_right",line_right)
            print("line_turn_right_refframe",line_turn_right_refframe)
            print("line_turn_up_refframe",line_turn_up_refframe)
            print("")"""

            print("line_up",line_up)
            print("line_right",line_right)
            print("line_turn_right_refframe",line_turn_right_refframe)
            print("line_turn_up_refframe",line_turn_up_refframe)
            print("")
            if line_up >0: #scenario when the rail is going upwards before corner
                if line_turn_right_refframe > 0: #When rail is turning right in the ref frame
                    ytemp1 = pointlist[i+1][1]-r #shorten the line by the radius to make space for a curve
                    xtemp2 = pointlist[i+1][0]+r #move the start of the next line the equvilant sideways
                    adjusted_points.append([pointlist[i+1][0],ytemp1,rail_height])
                    adjusted_points.append([xtemp2,pointlist[i+1][1],rail_height])
                if line_turn_right_refframe < 0:
                    ytemp1 = pointlist[i+1][1]-r #shorten the line by the radius to make space for a curve
                    xtemp2 = pointlist[i+1][0]-r #move the start of the next line the equvilant sideways in the direction
                    adjusted_points.append([pointlist[i+1][0],ytemp1,rail_height])
                    adjusted_points.append([xtemp2,pointlist[i+1][1],rail_height])
            elif line_up < 0: #scenario when the rail is going downwards before corner
                if line_turn_right_refframe > 0: #When rail is turning right in the ref frame
                    ytemp1 = pointlist[i+1][1]+r #shorten the line by the radius to make space for a curve
                    xtemp2 = pointlist[i+1][0]+r #move the start of the next line the equvilant sideways
                    adjusted_points.append([pointlist[i+1][0],ytemp1,rail_height])
                    adjusted_points.append([xtemp2,pointlist[i+1][1],rail_height])
                if line_turn_right_refframe < 0:
                    ytemp1 = pointlist[i+1][1]+r #shorten the line by the radius to make space for a curve
                    xtemp2 = pointlist[i+1][0]-r #move the start of the next line the equvilant sideways in the direction
                    adjusted_points.append([pointlist[i+1][0],ytemp1,railheight])
                    adjusted_points.append([xtemp2,pointlist[i+1][1],railheight])
            elif line_right > 0: #scenario when the rail is going right before corner
                if line_turn_up_refframe > 0: #When rail is turning right in the ref frame
                    xtemp1 = pointlist[i+1][0]-r #shorten the line by the radius to make space for a curve
                    ytemp2 = pointlist[i+1][1]+r #move the start of the next line the equvilant sideways
                    adjusted_points.append([xtemp1,pointlist[i+1][1],rail_height])
                    adjusted_points.append([pointlist[i+1][0],ytemp2,rail_height])
                if line_turn_up_refframe < 0:
                    xtemp1 = pointlist[i+1][0]-r #shorten the line by the radius to make space for a curve
                    ytemp2 = pointlist[i+1][1]-r #move the start of the next line the equvilant sideways
                    adjusted_points.append([xtemp1,pointlist[i+1][1],railheight])
                    adjusted_points.append([pointlist[i+1][0],ytemp2,railheight])
            elif line_right < 0: #scenario when the rail is going right before corner
                if line_turn_up_refframe > 0: #When rail is turning right in the ref frame
                    xtemp1 = pointlist[i+1][0]+r #shorten the line by the radius to make space for a curve
                    ytemp2 = pointlist[i+1][1]+r #move the start of the next line the equvilant sideways
                    adjusted_points.append([xtemp1,pointlist[i+1][1],railheight])
                    adjusted_points.append([pointlist[i+1][0],ytemp2,railheight])
                if line_turn_up_refframe < 0:
                    xtemp1 = pointlist[i+1][0]+r #shorten the line by the radius to make space for a curve
                    ytemp2 = pointlist[i+1][1]-r #move the start of the next line the equvilant sideways
                    adjusted_points.append([xtemp1,pointlist[i+1][1],rail_height])
                    adjusted_points.append([pointlist[i+1][0],ytemp2,rail_height])
            else:
                print("Something went wrong making space for the curves")
        adjusted_points.append(pointlist[-1]) #This adds the last point of the list
        adjusted_points.append(pointlist[-1]) #This adds a "ghost" point so that the last element has a "next" postion to be used when getting created
        print("adjusted_points", adjusted_points)

        pointlist = adjusted_points #Using the newly compiled points
        for i in range(len(pointlist)-2): #This for loop inserts lines and arcs into the dfa file

            side=(pointlist[i+2][0]-pointlist[i][0])*(pointlist[i+1][1]-pointlist[i][1]) - (pointlist[i+2][1]-pointlist[i][1])*(pointlist[i+1][0]-pointlist[i][0])
            #We choose direction -1 for left, 0 for on line and 1 for right
            if side < 0:
                dir = -1
            elif side >0:
                dir = 1
            else:
                dir = 0
            #print("dir:",dir)
            if i==0 or i/2==np.round(i/2):
                print("\nStart on new loop for line: " + str(i))
                print("---")
                rail = add_line(i,pointlist[i][0],pointlist[i][1],rail_height,pointlist[i+1][0],pointlist[i+1][1],rail_height,rail)
            #arcs
            elif i!=0 and i/2!=np.round(i/2): 

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

                if (dir != 0):
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
                
                going_up = ys - yprev_line_start
                going_right = xs- xprev_line_start
                if going_right ==0:
                    going_right = 0.00001
                turn_right_refframe = xe-xs
                turn_up_refframe = ye-ys
                """
                print("right",going_right)
                print("up",going_up)
                print("turnright",turn_right_refframe)
                print("turnup", turn_up_refframe)"""
                
                if dir!=0: #Here we change the angles from the reference frame to the arc angles in the dfa file
                    if abs(going_up/going_right) >= 1:  #Here the curve is mostly going vertically contra sideways on entry  
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
                            if angle_in_d < 90:
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
                rail = add_arc(i,r,angle_in,angle_out,xcenter,ycenter,0,rail) # Temp set to 0 if this is correct, thinking maybe z = railheight is for the roof mounting
            else:
                print("Neither arc or line?")   

            if i != (len(pointlist)-3): #Making the string that says what parts to curve_join
                element_string = element_string + "element_" + str(i) + ":, "
            else:
                element_string = element_string + "element_" + str(i) + ":"

        #For loop to add the roof mounts
        for i in range(len(mount_list)):
            rail = add_roof_mount(i,mount_list[i][0],mount_list[i][1],rail_height,room_height,rail)

        rail = rail + the_end

        rail = rail.replace("<ALL_ELEMENTS>", element_string)

        f = open(dfaPath + "Rail_Order.dfa", "w")
        f.write(rail)
        f.close()


        s.wfile.write(
            bytes('<html><body><h2>Rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
        s.wfile.write(
            bytes('<form action="/sendOrder" method="post">', 'utf-8'))
        s.wfile.write(
            bytes('<label for="Thanks">Thank you for your order!</label><br>', 'utf-8'))

        # The room size
        s.wfile.write(bytes('<br><p>You have order a rail for the room size (m): room height: ' + str(room_height) + ', room width: ' +
                            str(room_width) + ', room length: ' + str(room_length) + ', rail hight: ' + str(rail_height) + '.</p>', 'utf-8'))

        s.wfile.write(
            bytes('<br><p>With the following varialbes: </p>', "utf-8"))

        # Write the points as lists on the webpage
        list_att = ""
        for li in attachement_points:
            list_att += "<li>" + str(li) + "</li>"
        s.wfile.write(bytes(
            '<p>List of attachement points: [[point in width, poing in length], ceiling height]:</p>', "utf-8"))
        s.wfile.write(bytes('<ul>' + list_att + '</ul>', "utf-8"))

        list_visit = ""
        for li in visit_locations:
            list_visit += "<li>" + str(li) + "</li>"
        s.wfile.write(bytes('<p>List of locations to visit:</p>', "utf-8"))
        s.wfile.write(bytes('<ul>' + list_visit + '</ul>', "utf-8"))

        list_obs = ""
        for li in obstacles:
            list_obs += "<li>" + str(li) + "</li>"
        s.wfile.write(bytes('<p>List of obstacles:</p>', "utf-8"))
        s.wfile.write(bytes('<ul>' + list_obs + '</ul>', "utf-8"))

        # Giving options to go back and reset at room size or variables, or submitting the order
        s.wfile.write(bytes(
            '<br><button type="submit" formaction="/setSize">Reset room</button><p>Click "Reset room" to reset the while room size and the while rail order</p>', "utf-8"))
        s.wfile.write(bytes(
            '<br><button type="submit" formaction="/setVariables">Reset variables</button><p>Click "Reset variables" to reset the variables in the room</p>', "utf-8"))
        s.wfile.write(bytes(
            '<br><button type="submit">Submit</button><p>Click "Submit" to send the order of your rail</p>', "utf-8"))

        # Giving options to go back and reset at room size or variables, of submitting the order
        s.wfile.write(bytes(
            '<br><button type="submit" formaction="/setSize">Reset room</button><p>Click "Reset room" to reset the while room size and the while rail order</p>', "utf-8"))
        s.wfile.write(bytes(
            '<br><button type="submit" formaction="/setVariables">Reset variables</button><p>Click "Reset variables" to reset the variables in the room</p>', "utf-8"))

        print("starting...")
        # First param - is the frequency
        # Second param - is the function
        # Third param - path of image
        # it auto-starts, no need of rt.start()
        #rt = RepeatedTimer(5, imgSaver, pathToImg)
        '''
        try:
            sleep(25)  # your long-running job goes here...
        finally:
            rt.stop()  # better in a try/finally block to make sure the program ends
            '''
        s.wfile.write(bytes('<br> Model of your rail: ', "utf-8"))
        s.wfile.write(
            bytes('<br> <img src="rail_model_image.jpg">', "utf-8"))
        s.wfile.write(bytes(
            '<br><button type="submit">Submit</button><p>Click "Submit" to send the order of your rail</p>', "utf-8"))
        s.wfile.write(bytes('</form></body></html>', "utf-8"))

        return room_height, room_width, room_length, rail_height, attachement_points, visit_locations, obstacles


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
