from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import pathAlgorithm
import rail


# Initial valies of room size
room_height = 0
room_length = 0
room_width = 0
rail_height = 0

# Placing points into different lists
attachement_points = []  # On form [(x,y), height]
visit_locations = []  # On form [(x,y), height]
obstacles = []  # On form [(x,y),(x,y),(x,y),(x,y) height], to form an area
global algo_path

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
pathToImg = "C:\\Users\\Amalie\\Documents\\GitHub\\TMM4275-Assignment2\\rail_model_image.png"  # Ama Windows
pathToDFA = "C:\\Users\\Amalie\\Documents\\GitHub\\TMM4275-Assignment2\\DFAs\\Rail_Order.dfa"  # Ama Windows

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

            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/Images/main/sketch_room.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
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
            all_locations = attachement_points.copy() + visit_locations.copy()
            algo_path = pathAlgorithm.pathAlgorithm(
                2000).preProcessData(all_locations)
            print("PATH: ", algo_path)
            rail


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
            '''
            s.wfile.write(bytes('<br> Model of your rail: ', "utf-8"))
            s.wfile.write(
                bytes('<br> <img src="rail_model_image.jpg">', "utf-8"))
            s.wfile.write(bytes(
                '<br><button type="submit">Submit</button><p>Click "Submit" to send the order of your rail</p>', "utf-8"))
            s.wfile.write(bytes('</form></body></html>', "utf-8"))'''

            return room_height, room_width, room_length, rail_height, attachement_points, visit_locations, obstacles


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
