from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import numpy as np

room_height = 0
room_length = 0
room_width = 0 
matrix_room = []

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
        elif path.find("/orderRail") != -1: #The webpage path to order a chair
            s.wfile.write(bytes('<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            s.wfile.write(bytes('<form action="/orderRail" method="post">', 'utf-8')) #Create a form to take in values
            
            s.wfile.write(bytes('<h4>Set room size (m):</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Room height:<br><input type="text" name="room_height" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>Room length:<br><input type="text" name="room_length" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>Room width:<br><input type="text" name="room_width" value="0">', "utf-8"))
            s.wfile.write(bytes('<br><br> <button id = "renderButton"> Render </button> </form><p>Click "Render" to set the room size and add varaibles</p>', "utf-8"))

            s.wfile.write(bytes('<h4>Add variales in the room:</h4>', "utf-8"))

        else:
            s.wfile.write(bytes('<html><head><title>Cool interface.</title></head>', 'utf-8'))
            s.wfile.write(bytes("<body><p>The path: " + path + "</p>", "utf-8"))
            s.wfile.write(bytes('</body></html>', "utf-8"))

    def do_POST(s):

        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        within_constraints = False #Boolean to see check if the customers order is within the manufactor constraints

        # Check what is the path
        path = s.path
        print("Path: ", path)

        if path.find("/orderRail") != -1:
            content_len = int(s.headers.get('Content-Length')) #Gets the string with the rail values
            post_body = s.rfile.read(content_len)
            param_line = post_body.decode()
            print("Body: ", param_line)

            splitString = param_line.split("&") #Splits string so that the values can be set for each variable
            newSplit = []
            for i in splitString:
                newSplit.append(i.split("="))

            room_height = int(newSplit[0][1])
            room_length = int(newSplit[1][1])
            room_width = int(newSplit[2][1])
            #Every variable has been given their value from the string

            s.wfile.write(bytes('<html><body><h2>Determine rail specifications for your K2 EasyFeed:</h2>', "utf-8"))
            s.wfile.write(bytes('<form action="/orderRail" method="post">', 'utf-8')) #Create a form to take in values
            
            s.wfile.write(bytes('<h4>Your room size (m):</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Room height:<br><input type="text" name="room_height" value="' + str(room_height) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room length:<br><input type="text" name="room_length" value="' + str(room_length) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room width:<br><input type="text" name="room_width" value="' + str(room_width) + '">', "utf-8"))
            s.wfile.write(bytes('<br><br> <button id="renderButton"> Render </button> </form><p>Click "Render" to set the room size and add varaibles</p>', "utf-8"))

            # Matrix representing the room: 
            # Length = number of rows
            # Width = number of columns
            matrix_room = [[0 for w in range(room_width)]for l in range(room_length)]

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
            var_type = ""
            x_start = 0
            x_end = 0 
            y_start = 0
            y_end = 0 
            spes_height = 0 

            s.wfile.write(bytes('<h4>Seen from above, where are the variables located in the room? give the coordinates below</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Start point in the width direction:<br><input type="text" name="x_start" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>End point in the width direction:<br><input type="text" name="x_end" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>Start point in the length direction:<br><input type="text" name="y_start" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>End point in the length direction:<br><input type="text" name="y_end" value="0">', "utf-8"))
            s.wfile.write(bytes('<br>In case of 5. Specific ceiling height:<br><input type="text" name="spes_height" value="0">', "utf-8"))


            # Adding type of variable 
            s.wfile.write(bytes('<br>Type of variable:<br><select name="var_type" id="var_type"><option value="ATTACH_POINT">1. Attachment point</option><option value="FEED_LOC">2. Feeding location</option><option value="VISIT_LOC">3. Locations the cart should visit</option><option value="OBSTACLE">4. Obstacle </option><option value="HIGHT">5. Specific hight of ceiling </option></select>', "utf-8"))
           
            s.wfile.write(bytes('<script>function hello() {alert("Variable");}</script>', "utf-8"))    
            s.wfile.write(bytes('<button onclick="hello();">Add variable</button>', "utf-8")) 

             # make a list of already made points, so the client kan view them (and delete?)
             
            s.wfile.write(bytes('<p>'+ var_type + 'from width ' + str(x_start) + ' to ' + str(x_end) + ' and from length ' + str(y_start) + ' to ' + str(y_end) + '. </p>', "utf-8"))
            
            # make a list of already made points, so the client kan view them (and delete?)

            s.wfile.write(bytes('<br><br><input type="submit" value="Submit"></form><p> Click "Submit" to send order of your rail.</p></body></html>', "utf-8"))

            return room_height, room_length, room_width, matrix_room, print(np.matrix(matrix_room))



if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()