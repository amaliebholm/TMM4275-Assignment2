from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import numpy as np

# Initial valies of room
room_height = 0
room_length = 0
room_width = 0
rail_height = 0 

# Placing points into different lists
attachement_points = [] 
visit_locations = []
obstacles = []
#each element on form: [(x_start, y_start), (x_end, y_end), spes_height]

# Initial values of variables
x = 0
y = 0 
obs_string = ""
spes_height = 0 
var_type = ""
weight = 0 

HOST_NAME = '127.0.0.1'  # locathost - http://127.0.0.1
#complete address would be: http://127.0.0.1:1234
PORT_NUMBER = 1234

dfaPath = ... 

#f = open(dfaPath + "templates\\My_Chair_template.dfa", "r") 
#fileContent = f.read()
#f.close() #Opens and reads the DFA template to so that a new DFA file of the order can be made later

# Handler of HTTP requests / responses


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        global room_height, room_width, room_length, matrix_room, matrix_height, rail_height, x, y, obs_string, spes_height, var_type
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
        elif path.find("/setSize") != -1: #The webpage path to order a chair
            s.wfile.write(bytes('<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            s.wfile.write(bytes('<form action="/setSize" method="post">', 'utf-8')) #Create a form to take in values
            
            s.wfile.write(bytes('<h4>Set room size (m):</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Room height:<br><input type="text" name="room_height" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>Room width:<br><input type="text" name="room_width" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>Room length:<br><input type="text" name="room_length" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>Height from floor to railing:<br><input type="text" name="rail_height" value="0">', "utf-8"))

            s.wfile.write(bytes('<br><br><button type="submit">Set size</button><p>Click "Set size" to set the room size</p>', "utf-8"))
            s.wfile.write(bytes('<button type="submit" formaction="/setVariables">Continue</button><p>Click "Continue" to continue to add varialbes</p></form>', "utf-8"))

            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/sketch_room.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))


        else:
            s.wfile.write(bytes('<html><head><title>Cool interface.</title></head>', 'utf-8'))
            s.wfile.write(bytes("<body><p>The path: " + path + "</p>", "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))

    def do_POST(s):
        global room_height, room_width, room_length, matrix_room, matrix_height, rail_height, x, y, obs_string, spes_height, var_type
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        within_constraints = False #Boolean to see check if the customers order is within the manufactor constraints

        # Check what is the path
        path = s.path
        print("Path: ", path)

        if path.find("/setSize") != -1:
            content_len = int(s.headers.get('Content-Length')) #Gets the string with the rail values
            post_body = s.rfile.read(content_len)
            param_line = post_body.decode()
            print("Body: ", param_line)

            splitString = param_line.split("&") #Splits string so that the values can be set for each variable
            newSplit = []
            for i in splitString:
                newSplit.append(i.split("="))

            room_height = int(newSplit[0][1])
            room_width = int(newSplit[1][1])
            room_length = int(newSplit[2][1])
            rail_height = int(newSplit[3][1])
            #Every variable has been given their value from the string

            room_constraint = False

            if rail_height < room_height:
                if room_height > 0:
                    if room_length > 0:
                        if room_width > 0:
                            print("Params OK")
                            room_constraint = True
            else:
                room_constraint = False
            

            s.wfile.write(bytes('<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            s.wfile.write(bytes('<form action="/setSize" method="post">', 'utf-8')) #Create a form to add variables

            s.wfile.write(bytes('<h4>Your room size is set to (m):</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Room height:<br><input type="text" name="room_height" value="' + str(room_height) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room width:<br><input type="text" name="room_width" value="' + str(room_width) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room length:<br><input type="text" name="room_length" value="' + str(room_length) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Height from floor to railing:<br><input type="text" name="rail_height" value="' + str(rail_height) + '">', "utf-8"))

            if room_constraint == True: 
                s.wfile.write(bytes('<br><br> <button type="submit">Set size</button><p>Click "Set size" to set the room size</p>', "utf-8"))
                s.wfile.write(bytes('<button type="submit" formaction="/setVariables">Continue</button><p>Click "Continue" to continue to add varialbes</p>', "utf-8"))
            elif room_constraint == False:
                s.wfile.write(bytes('<script>function alert(){alert("The room height, length and width must be more than zero, and rail height must be lower than room height!");} </script>', "utf-8"))
                s.wfile.write(bytes('<br><br><button type="submit" onclick="alert();">Set size</button> <p>Click "Set size" to set the room size</p>', "utf-8"))
                s.wfile.write(bytes('<button type="submit" formaction="/setVariables">Continue</button> <p>Click "Continue" to continue to add varialbes</p>', "utf-8"))


            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/sketch_room.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
            s.wfile.write(bytes('</form></body></html>', "utf-8"))

        elif path.find("/setVariables") != -1:
            content_len = int(s.headers.get('Content-Length')) #Gets the string with the rail values
            post_body = s.rfile.read(content_len)
            param_line = post_body.decode()
            print("Body: ", param_line)

            splitString = param_line.split("&") #Splits string so that the values can be set for each variable
            newSplit = []
            for i in splitString:
                newSplit.append(i.split("="))

            try:
                x = int(newSplit[0][1])
                x = int(newSplit[1][1])
                obs_string = newSplit[3][1]
                spes_height = int(newSplit[4][1])
                var_type = newSplit[5][1]
                #Every variable has been given their value from the string 
            except:
                pass

            within_constraints = False

            # Checking if the koordinates are within the room size
            if x <= room_width and x >= 0:
                if y < room_length and y >= 0:
                    if spes_height > 0: 
                        print("Params OK")
                        within_constraints = True
                                
            else: 
                within_constraints = False

            s.wfile.write(bytes('<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            s.wfile.write(bytes('<form action="/setVariables" method="post">', 'utf-8')) #Create a form to add variables
            s.wfile.write(bytes('<p>You have set the room size (m): room height: ' + str(room_height)+ ', room width: '+ str(room_width) + ', room length: '+ str(room_length)+ ', rail hight: '+ str(rail_height) + '.</p>', 'utf-8'))
            
            s.wfile.write(bytes('<button type="submit" formaction="/setSize">Change</button><p>Click "Change" to set the new room size</p>', "utf-8"))
            
            s.wfile.write(bytes('<h4>Add variales in the room:</h4>', "utf-8"))
            s.wfile.write(bytes('<p>Different varialbes you can add:</p>', "utf-8"))
            s.wfile.write(bytes('<p>1. An attachment point for the rail in the ceiling</p>', "utf-8"))
            s.wfile.write(bytes('<p>2. Feeding location for the cart</p>', "utf-8"))
            s.wfile.write(bytes('<p>3. Locations the cart should visit</p>', "utf-8"))
            s.wfile.write(bytes('<p>4. An obstacle in the room, the feeder can not pass through these points</p>', "utf-8"))

            # Image illustrating 3D and 2D perspective 
            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/sketch_room.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
            
            # Adding the coordinates of the variable       
            s.wfile.write(bytes('<h4>Seen from above, where are the variables located in the room? Give the coordinates below:</h4>', "utf-8"))
            s.wfile.write(bytes('<p>Go through the room chronologically and add variables as the appear in the room.</p>', "utf-8"))
            s.wfile.write(bytes('<br>Point in the width direction:<br><input type="text" name="x" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>Point in the length direction:<br><input type="text" name="y" value="0">', "utf-8"))
            s.wfile.write(bytes('<br><br> If the varaible is an obstacle add three more points, marking off the area the obstacle obtain in the room, filling the points [point in width, point in length]:<br><input type="text" name="obs_string" value="[0, 0], [0, 0], [0, 0]">', "utf-8"))
            s.wfile.write(bytes('<br>Ceiling height in this area (change if it differs form gnereal height):<br><input type="text" name="spes_height" value="' + str(room_height) + '">', "utf-8"))

            # Adding type of variable 
            s.wfile.write(bytes('<br>Type of variable:<br><select name="var_type" id="var_type"><option value="ATTACH_POINT">1. Attachment point</option><option value="FEED_LOC">2. Feeding location</option><option value="VISIT_LOC">3. Locations the cart should visit</option><option value="OBSTACLE">4. Obstacle </option></select>', "utf-8"))

            if within_constraints == True:
                s.wfile.write(bytes('<button type="submit">Add variable</button>', "utf-8")) 

                if var_type == "RESET":
                    var_type_str = "Reset area"
                elif var_type == "ATTACH_POINT":
                    attachement_points.append([[x, y], spes_height])
                    var_type_str = "Attachment point"
                elif var_type == "FEED_LOC":
                    attachement_points.append([[x, y], spes_height])
                    # Feeding location inserted at start of the visit_location list
                    var_type_str = "Feeding location"
                elif var_type == "VISIT_LOC":
                    attachement_points.append([[x, y], spes_height])
                    var_type_str = "Location to visit"
                elif var_type == "OBSTACLE":
                    attachement_points.append([x, y], obs_string)
                    var_type_str = "Obstacle"
            elif within_constraints == False:
                s.wfile.write(bytes('<script>function alert(){alert("The location must be within the room size!");} </script>', "utf-8"))
                s.wfile.write(bytes('<button type="submit" onclick="alert();">Add variable</button>', "utf-8")) 

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
            s.wfile.write(bytes('<br><p>List of attachement points: [(point in width, poing in length), ceiling height]:</p>', "utf-8"))
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

            #sending submit to a new page? Now it acts ass "Add variable"
            s.wfile.write(bytes('<button type="submit" formaction="/sendOrder">Submit</button><p>Click "Submit" to send the order of your rail</p></form>', "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))
        
            return attachement_points, visit_locations, obstacles
        
        elif path.find("/sendOrder") != -1:
            s.wfile.write(bytes('<html><body><h2>Rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            s.wfile.write(bytes('<form action="/sendOrder" method="post">', 'utf-8'))
            s.wfile.write(bytes('<label for="Thanks">Thank you for your order!</label><br>', 'utf-8'))

            s.wfile.write(bytes('<br><p>You have order a rail for the room size (m): room height: ' + str(room_height)+ ', room width: '+ str(room_width) + ', room length: '+ str(room_length)+ ', rail hight: '+ str(rail_height) + '.</p>', 'utf-8'))

            s.wfile.write(bytes('<br><p>With the following varialbes: </p>', "utf-8"))
            
            # Write the points as lists on the webpage
            list_att = ""
            for li in attachement_points:
                list_att += "<li>" + str(li) + "</li>"
            s.wfile.write(bytes('<br><p>List of attachement points: [(start width, end wifth), (start length, end length), ceiling height]:</p>', "utf-8"))
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

            s.wfile.write(bytes('<br><button type="submit" formaction="/setSize">Reset room</button><p>Click "Reset room" to reset the while room size and the while rail order</p>', "utf-8"))
            s.wfile.write(bytes('<br><button type="submit" formaction="/setVariables">Reset variables</button><p>Click "Reset variables" to reset the variables in the room</p>', "utf-8"))
            s.wfile.write(bytes('<br><button type="submit">Submit</button><p>Click "Submit" to send the order of your rail</p>', "utf-8")) 
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