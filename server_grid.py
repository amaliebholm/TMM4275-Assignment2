from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

room_height = 0
room_length = 0
room_width = 0 
attachement_points = [] 
visit_locations = []
obstacles = []
feeding_location = []

HOST_NAME = '127.0.0.1'  # locathost - http://127.0.0.1
#complete address would be: http://127.0.0.1:1234
PORT_NUMBER = 1234

# dfaPath = ... 

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
            
            s.wfile.write(bytes('<h4>Your room size (m):</h4>', "utf-8"))
            s.wfile.write(bytes('<br>Room hight:<br><input type="text" name="room_height" value="' + str(room_height) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room length:<br><input type="text" name="room_length" value="' + str(room_length) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room width:<br><input type="text" name="room_width" value="' + str(room_width) + '">', "utf-8"))
            s.wfile.write(bytes('<br><br> <button id="renderButton"> Render </button> </form><p> Click "Render" to make the preview grid</p>', "utf-8"))

            s.wfile.write(bytes('<h4>Add variales in the room:</h4>', "utf-8"))
            
            s.wfile.write(bytes('<style>.button {border: none; color: white; padding: 16px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 1px 2px; transition-duration: 0.4s; cursor: pointer;}', "utf-8"))
            s.wfile.write(bytes('.button1 {background-color: white; color: black; border: 2px solid #008000;} ', "utf-8"))
            s.wfile.write(bytes('.button1:hover {background-color: #008000; color: white;} ', "utf-8"))
            s.wfile.write(bytes('.button1.active {background-color: #008000; color: white;} ', "utf-8"))

            s.wfile.write(bytes('.button2 {background-color: white; color: black; border: 2px solid #FF0000;} ', "utf-8"))
            s.wfile.write(bytes('.button2:hover {background-color: #FF0000; color: white;} ', "utf-8"))

            s.wfile.write(bytes('.button3 {background-color: white; color: black; border: 2px solid #000000; } ', "utf-8"))
            s.wfile.write(bytes('.button3:hover {background-color: #000000; color: white;} ', "utf-8"))

            s.wfile.write(bytes('.button4 {background-color: white; color: black; border: 2px solid #0000FF;} ', "utf-8"))
            s.wfile.write(bytes('.button4:hover {background-color: #0000FF; color: white;} </style>', "utf-8"))

            s.wfile.write(bytes('<style>.grids {margin: 4px; padding: 5px; background: #FFFFFF; min-height: 500px;}', "utf-8"))
            s.wfile.write(bytes('.row {display: flex; flow-direction: row;}', "utf-8"))
            s.wfile.write(bytes('.grid {background: #FFFFFF; color:#000000; border: 1px slid #000000; border-radius:3px}', "utf-8"))
            s.wfile.write(bytes('.grid:hover {border-color: #696969; color: #FFFAF0; cursor: pointer:}</style>', "utf-8"))

            s.wfile.write(bytes('<script> (function(){color_green(e); color_red(e); color_black(e); color_blue(e);})</script>', "utf-8"))
            s.wfile.write(bytes('<script> function generate_grid(){$("renderButton").on("click", function() {var content = ""; var num = 1; for (var i = 1; i <= room_height; i++) {for (var j = 1; j <= room_length; j++) {if (j === 1) {content += "<div class="row"><div class="grid">" + num + "</div>";} else if (j === value) {content += "<div class="grid">" + num + "</div></di} else {content += "<div class="grid">" + num + "</div>";}num++;}}$("#grids");});})}</script>', "utf-8"))
            s.wfile.write(bytes('<script> function color_green(){$("#grids").on("click", ".grid", function(){var = value $(this).text(); alert("You click "+ value):});}', "utf-8"))
            s.wfile.write(bytes('<script> function setGreen(e) {var target = e.target, status = e.target.classList.contains("active"); e.target.classList.add(status ? "inactive" : "active"); e.target.classList.remove(status ? "active" : "inactive");} .active {background-color: #008000;} .inactive {background-color: #FFFFFF;}</script>', 'utf-8'))
            s.wfile.write(bytes('<script> var count = 1; function setColor(btn, color) {var property=document.getElementById(btn); if(count==0) {property.style.backgroundColor="#FFFFFF" count=1;} else {property.style.backgroundColor=color count=0;}} </script>', "utf-8")) 
            s.wfile.write(bytes('<script>function hello() {alert("Hello");}</script>', "utf-8"))
            s.wfile.write(bytes('<script>function color(id, color) {var col=col=document.getElementById(id); col.style.color=color;}</script>', "utf-8"))
            s.wfile.write(bytes('<script> btn1.btn.addEventListener("touchstart",function(){btn.classList.add("active");});;</script>', "utf-8"))

            s.wfile.write(bytes('<button class="button button1" type="button" id="btn1" onclick="color("btn1", "#008000")">Click here to add an attachment point for the rails in the ceiling </button>', "utf-8"))
            s.wfile.write(bytes('<button id="btn2" class="button button2">Click here to add locations the cart should visit </button>', "utf-8"))
            s.wfile.write(bytes('<button id="btn3" class="button button3">Click here to add an obstacle in the room, the feeder can not pass through these points </button>', "utf-8"))
            s.wfile.write(bytes('<button id="btn4" class="button button4">Click here the feeding location for the cart </button>', "utf-8"))


            s.wfile.write(bytes('<p onclick="myFunction(this)">Click me to change my text color.</p>', "utf-8"))      
            s.wfile.write(bytes('<button onclick="hello();">Hello</button>', "utf-8"))    

            s.wfile.write(bytes('<div id="grids"></div>', "utf-8"))

            s.wfile.write(bytes('<br><br><input type="submit" value="Submit"></form><p> Click "Submit" to send order.</p></body></html>', "utf-8"))

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
            s.wfile.write(bytes('<br>Room hight:<br><input type="text" name="room_height" value="' + str(room_height) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room length:<br><input type="text" name="room_length" value="' + str(room_length) + '">', "utf-8"))
            s.wfile.write(bytes('<br>Room width:<br><input type="text" name="room_width" value="' + str(room_width) + '">', "utf-8"))
            s.wfile.write(bytes('<br><br> <button id="renderButton"> Render </button> </form><p> Click "Render" to make the preview grid</p>', "utf-8"))

            s.wfile.write(bytes('<h4>Add variales in the room:</h4>', "utf-8"))

            s.wfile.write(bytes('<style>.button {border: none; color: white; padding: 16px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 1px 2px; transition-duration: 0.4s; cursor: pointer;}', "utf-8"))
            s.wfile.write(bytes('.button1 {background-color: white; color: black; border: 2px solid #008000;} ', "utf-8"))
            s.wfile.write(bytes('.button1:hover {background-color: #008000; color: white;} ', "utf-8"))
            s.wfile.write(bytes('.button1:focus {background-color: #008000; color: white;} ', "utf-8"))

            s.wfile.write(bytes('.button2 {background-color: white; color: black; border: 2px solid #FF0000;} ', "utf-8"))
            s.wfile.write(bytes('.button2:hover {background-color: #FF0000; color: white;} ', "utf-8"))

            s.wfile.write(bytes('.button3 {background-color: white; color: black; border: 2px solid #000000; } ', "utf-8"))
            s.wfile.write(bytes('.button3:hover {background-color: #000000; color: white;} ', "utf-8"))

            s.wfile.write(bytes('.button4 {background-color: white; color: black; border: 2px solid #0000FF;} ', "utf-8"))
            s.wfile.write(bytes('.button4:hover {background-color: #0000FF; color: white;} </style>', "utf-8"))

            s.wfile.write(bytes('<style>.grids {margin: 4px; padding: 5px; background: #FFFFFF; min-height: 500px;}', "utf-8"))
            s.wfile.write(bytes('.row {display: flex; flow-direction: row;}', "utf-8"))
            s.wfile.write(bytes('.grid {background: #FFFFFF; color:#000000; border: 1px slid #000000; border-radius:3px}', "utf-8"))
            s.wfile.write(bytes('.grid:hover {border-color: #696969; color: #FFFAF0; cursor: pointer:}</style>', "utf-8"))

            s.wfile.write(bytes('<script> (function(){color_green(e); color_red(e); color_black(e); color_blue(e);})</script>', "utf-8"))
            s.wfile.write(bytes('<script> function generate_grid(){$("renderButton").on("click", function() {var content = ""; var num = 1; for (var i = 1; i <= room_height; i++) {for (var j = 1; j <= room_length; j++) {if (j === 1) {content += "<div class="row"><div class="grid">" + num + "</div>";} else if (j === value) {content += "<div class="grid">" + num + "</div></di} else {content += "<div class="grid">" + num + "</div>";}num++;}}$("#grids");});})}</script>', "utf-8"))
            s.wfile.write(bytes('<script> function color_green(){$("#grids").on("click", ".grid", function(){var = value $(this).text(); alert("You click "+ value):});}', "utf-8"))
            s.wfile.write(bytes('<script> function setGreen(e) {var target = e.target, status = e.target.classList.contains("active"); e.target.classList.add(status ? "inactive" : "active"); e.target.classList.remove(status ? "active" : "inactive");} .active {background-color: #008000;} .inactive {background-color: #FFFFFF;}</script>', 'utf-8'))
            s.wfile.write(bytes('<script>var count = 1; function setColor(btn, color) {var property = document.getElementById(btn); if (count == 0) {property.style.backgroundColor = "#FFFFFF" count = 1;} else {property.style.backgroundColor = color count = 0;}}</script>', "utf-8")) 
            s.wfile.write(bytes('<script>function hello() {alert("Hello");}</script>', "utf-8"))
            s.wfile.write(bytes('<script> btn1.btn.addEventListener("touchstart",function(){btn.classList.add("active");});;</script>', "utf-8"))


            s.wfile.write(bytes('<button class="button button1" type="button" id="btn1" onclick="color("btn1", "#008000")">Click here to add an attachment point for the rails in the ceiling </button>', "utf-8"))
            s.wfile.write(bytes('<button id="btn2" class="button button2">Click here to add locations the cart should visit </button>', "utf-8"))
            s.wfile.write(bytes('<button id="btn3" class="button button3">Click here to add an obstacle in the room, the feeder can not pass through these points </button>', "utf-8"))
            s.wfile.write(bytes('<button id="btn4" class="button button4">Click here the feeding location for the cart </button>', "utf-8"))

            s.wfile.write(bytes('<p onclick="myFunction(this)">Click me to change my text color.</p>', "utf-8"))      
            s.wfile.write(bytes('<button onclick="hello();">Hello</button>', "utf-8"))    


            s.wfile.write(bytes('<div id="grids"></div>', "utf-8"))

            s.wfile.write(bytes('<br><br><input type="submit" value="Submit"></form><p> Click "Submit" to send order.</p></body></html>', "utf-8"))

            return room_height, room_length, room_width


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()