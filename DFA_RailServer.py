from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import numpy as np

room_height = 0
room_length = 0
room_width = 0
rail_height = 0 
matrix_room = []

var_type = ""
x_start = 0
x_end = 0 
y_start = 0
y_end = 0 
spes_height = 0 

attachement_points = [] 
feeding_location = []
visit_locations = []
obstacles = []

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
        global room_height, room_width, room_length, matrix_room, rail_height, x_start, x_end, y_start, y_start, var_type, spes_height
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

            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/3D-2D.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))

        elif path.find("/setVariables") != -1:
            s.wfile.write(bytes('<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            s.wfile.write(bytes('<form action="/setVariables" method="post">', 'utf-8')) #Create a form to add variables
            s.wfile.write(bytes('<p>You have set the room size: room height: '+ str(room_height) + ', room width: '+ str(room_width) + ', room length: '+ str(room_length)+ ', rail hight: '+ str(rail_height) + '.</p>', 'utf-8'))
            
            s.wfile.write(bytes('<button type="submit" formaction="/setSize">Change</button><p>Click "Change" to set the new room size</p>', "utf-8"))

            s.wfile.write(bytes('<h4>Add variales in the room:</h4>', "utf-8"))
            s.wfile.write(bytes('<p>Different varialbes you can add:</p>', "utf-8"))
            s.wfile.write(bytes('<p>1. An attachment point for the rail in the ceiling</p>', "utf-8"))
            s.wfile.write(bytes('<p>2. Feeding location for the cart</p>', "utf-8"))
            s.wfile.write(bytes('<p>3. Locations the cart should visit</p>', "utf-8"))
            s.wfile.write(bytes('<p>4. An obstacle in the room, the feeder can not pass through these points</p>', "utf-8"))
            s.wfile.write(bytes('<p>5. Specific area with different hight of ceiling</p>', "utf-8"))

            # Image illustrating 3D and 2D perspective 
            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/3D-2D.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))

            
            # Adding the coordinates of the variable 
            s.wfile.write(bytes('<h4>Seen from above, where are the variables located in the room? Give the coordinates below:</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Start point in the width direction:<br><input type="text" name="x_start" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>End point in the width direction:<br><input type="text" name="x_end" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>Start point in the length direction:<br><input type="text" name="y_start" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>End point in the length direction:<br><input type="text" name="y_end" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>In case of 5. Specific ceiling height:<br><input type="text" name="spes_height" value="0">', "utf-8"))
            # Adding type of variable 
            s.wfile.write(bytes('<br>Type of variable:<br><select name="var_type" id="var_type"><option value="ATTACH_POINT">1. Attachment point</option><option value="FEED_LOC">2. Feeding location</option><option value="VISIT_LOC">3. Locations the cart should visit</option><option value="OBSTACLE">4. Obstacle </option><option value="HIGHT">5. Specific hight of ceiling </option></select>', "utf-8"))
           
            s.wfile.write(bytes('<button type="submit">Add variable</button>', "utf-8"))

            s.wfile.write(bytes('<br><br><input type="submit" value="Submit"></form><p> Click "Submit" to send order of your rail.</p>', "utf-8"))
            
            s.wfile.write(bytes('</body></html>', "utf-8"))
        else:
            s.wfile.write(bytes('<html><head><title>Cool interface.</title></head>', 'utf-8'))
            s.wfile.write(bytes("<body><p>The path: " + path + "</p>", "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))

    def do_POST(s):
        global room_height, room_width, room_length, matrix_room, rail_height, x_start, x_end, y_start, y_start, var_type, spes_height

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

            # Matrix representing the room: 
            # Length = number of rows
            # Width = number of columns
            matrix_room = [[0 for w in range(room_width)]for l in range(room_length)]
            print(np.matrix(matrix_room))

            s.wfile.write(bytes('<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            s.wfile.write(bytes('<form action="/setSize" method="post">', 'utf-8')) #Create a form to add variables

            s.wfile.write(bytes('<h4>Your room size is set to (m):</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Room height:<br><input type="text" name="room_height" value="' + str(room_height) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room width:<br><input type="text" name="room_width" value="' + str(room_width) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room length:<br><input type="text" name="room_length" value="' + str(room_length) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Height from floor to railing:<br><input type="text" name="rail_height" value="' + str(rail_height) + '">', "utf-8"))

            s.wfile.write(bytes('<br><br> <button type="submit">Set size</button><p>Click "Set size" to set the room size</p>', "utf-8"))
            s.wfile.write(bytes('<button type="submit" formaction="/setVariables">Continue</button><p>Click "Continue" to continue to add varialbes</p></form>', "utf-8"))

            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/3D-2D.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))

        elif path.find("/setVariables") != -1:
            content_len = int(s.headers.get('Content-Length')) #Gets the string with the rail values
            post_body = s.rfile.read(content_len)
            param_line = post_body.decode()
            print("Body: ", param_line)

            splitString = param_line.split("&") #Splits string so that the values can be set for each variable
            newSplit = []
            for i in splitString:
                newSplit.append(i.split("="))

            x_start = int(newSplit[0][1])
            x_end = int(newSplit[1][1])
            y_start = int(newSplit[2][1])
            y_end = int(newSplit[3][1])
            spes_height = int(newSplit[4][1])
            var_type = newSplit[5][1]
            #Every variable has been given their value from the string

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
            s.wfile.write(bytes('<p>5. Specific area with different hight of ceiling</p>', "utf-8"))

            # Image illustrating 3D and 2D perspective 
            s.wfile.write(bytes('<img src="https://raw.githubusercontent.com/amaliebholm/TMM4275-Assignment2/main/3D-2D.jpeg" alt="Image illustrating 3D and 2D perspective" width="650" height="400">', "utf-8"))
            
            # Adding the coordinates of the variable 
                   
            s.wfile.write(bytes('<h4>Seen from above, where are the variables located in the room? Give the coordinates below:</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Start point in the width direction:<br><input type="text" name="x_start" value="' + str(x_start) + '">', "utf-8"))
            s.wfile.write(bytes('<br>End point in the width direction:<br><input type="text" name="x_end" value="' + str(x_end) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Start point in the length direction:<br><input type="text" name="y_start" value="' + str(y_start) + '">', "utf-8"))
            s.wfile.write(bytes('<br>End point in the length direction:<br><input type="text" name="y_end" value="' + str(y_end) + '">', "utf-8"))
            s.wfile.write(bytes('<br>In case of 5. Specific ceiling height:<br><input type="text" name="spes_height" value="' + str(spes_height) + '">', "utf-8"))

            # Adding type of variable 
            s.wfile.write(bytes('<br>Type of variable:<br><select name="var_type" id="var_type"><option value="ATTACH_POINT">1. Attachment point</option><option value="FEED_LOC">2. Feeding location</option><option value="VISIT_LOC">3. Locations the cart should visit</option><option value="OBSTACLE">4. Obstacle </option><option value="HIGHT">5. Specific hight of ceiling </option></select>', "utf-8"))

            s.wfile.write(bytes('<button type="submit">Add variable</button>', "utf-8")) 

            list_el = var_type + ' from width ' + str(x_start) + ' to ' + str(x_end) + ' and from length ' + str(y_start) + ' to ' + str(y_end)
            s.wfile.write(bytes('<br><label>'+ list_el + '. </label>', "utf-8"))
            
            # make a list of already made points, so the client kan view them (and delete?)
            
            if var_type == "ATTACH_POINT":
                weight = 1
            elif var_type == "FEED_LOC":
                weight = 2
            elif var_type == "VISIT_LOC":
                weight = 3
            elif var_type == "OBSTACLE":
                weight = 4
            elif var_type == "HIGHT":
                weight = 5
            print("weight:")
            print(weight)
            
            # Length = number of rows
            # Width = number of columns
            # Adding the variable to the matrix 
            print(np.matrix(matrix_room))

            r = room_length - y_start - 1 
            c = x_start - 1 
            while (r >= (y_end - 1) & (r > 0)):
                while (c <= (x_end - 1) & (c > 0)):
                    matrix_room[r][c] = weight
                    c += 1
                r-= 1
            
            # make a list of already made points, so the client kan view them (and delete?)

            s.wfile.write(bytes('<br><br><input type="submit" value="Submit"></form><p> Click "Submit" to send order of your rail.</p></body></html>', "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))
        
            return print(np.matrix(matrix_room))



if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()