# TMM4275-Assignment2

This project is a part of the course TMM4275 Knowledge-Based Enineering, Project. The main task is making an automatic KBE system to define a rail installation layout for the K2 EasyFeed equipment for inputs given by a ccustomer. The system will return a layout of the system, represented in Simens NX.  

This project is made by: 
* Kasper Kallseter
* Magnus Myklegard
* Amalie Berge Holm

### The Rail

The image below show an example of a NX modelling of the rail: 
![rail_model_image.png](https://github.com/amaliebholm/TMM4275-Assignment2/blob/main/Images/rail_model_image.png)

First, the customer will define the size of the room: 
* Room height 
* Room width 
* Room length 
* Height from the floor to the rail 

Then, the customer will give coordinates of the different variables in the room: 
* Attachement point in the ceiling
* Feeding location for the cart
* Locations the cart should visit in the room 
* Obstacles in the room that the cart has to avoid (given as whole areas within the room)

### The KBE Application Architecture

This is a diagram showing the main blocks and interconnections between them. 

![Client-Server](url)

The main lines of the KBE architecture are the same as in assignment 1, where the customer set values for different parameters on a website, which are then, if the are within some constraints, sent to a DFA template and made into a NX model. The main difference in the architecture is that the constraints for heights and variables within the room are now given by the room itself, therefor the DFA server do both tasks, of taking the input, and checking whether it is within the room size. This emilinates the need for an Fuseki server to take in constraints from the product engineer, and checking this up against the values given by the customer. Now the product engineer sets a DFA template which the input, after being verified, is written to.

### ULM Sequence Diagram

The ULM sequence diagram showing how an order making scenario will play out. From how the customer makes the order of the rail, to the algorithm finding the best path and this path being made in NX. 

![seq-diag.PNG](https://github.com/amaliebholm/TMM4275-Assignment2/blob/main/Images/seq-diag.PNG)

In assignment 1 Olingvo and Apache Jena Fuseki was used to communicate with the server containing the parameters, set by both the customer and the product engineer. In assignment 2 the product engineer set a DFA template which was written to by the DFA server, as well as cheching if they are within the room, and not needing a Manufacture Checker Server or a Fuseki Server. 

Another difference from assignment 1 is that web browser client now uses three different websites rather than only one, to get the values from the customer. This makes the sequence diagram more heavy on the left hand side for assignment 2. 

### Development Tools

This code was made using python in Visual Studio Code. Knowledge Fusion and Journal was used in NX to make models of the rail. NX Open was used to make journals, to be able to easily take pictures of the product for every order. 

In assignment 1 Olingvo and Apache Jena Fuseki was used to communicate with the server containing the parameters, as stated above, this was not used in assignment 2, since the constraints the variables has to be within is both set by the DFA server, in the same place where they are fetched from the customer. 


### Code Description 

- `DFA_RailServer.py` - Setting up the web-page that the customer uses to place an order, making sure that the variables are set within the size of the room. Giving the lists of different variables as output. This is done by three webpages linked together, sending the customer to the next one when all the necessary values are given. 
- `rail.py`- ... This takes in the list of the sorted points, adds the curves and creates the dfa file that is used to create the 3d model. 
- `pathAlgorithm.py` - Has the purpose of finding the optimal path through the points given by the user in the webserver client. It uses euclidean distance between a point and the rest to find the shortest paths.
- `aStarAlgorithm.py` - We first tried to implement the shortest path through the points given from the webserver using the A* algorithm, but this proved to be very difficult. The solution we tried was to update the start point and end point to the current and next points in the list, but the heuristic became increasingly worse through each iteration.
- `rail_journal.py` - A journal using NX Open to take a picture of the ordered rail and saving it in the folder with the rest of the files. 

### DFAs
- `Rail_Order.dfa` - Containing the NX file whith the parameters given by the customer
- `Rail_template.dfa` - Containing the rail template 
- `Arc_template.dfa` - Containing the arc template
- `Line_template.dfa` - Containing the line template
- `Roof_mount_template.dfa` - Containing the template for how roof mounts
- `path_and_combine.dfa`- Containing the template for combining the whole rile according to the path 

## Video of working KBE system

## Examples of Three Different Product Orders  

### A Customer Trying to Order Outside the Constraints
Befor submitting variables for both the size of the room and before being able to add a variable to the room, the values are verified. If a customer tries to set values outside of these verifications they will recieve a notification. If the room size is below or equal to zero of ir the rail height is higher than the ceiling height the customer will recieve this alert: 
![alert.PNG](https://github.com/amaliebholm/TMM4275-Assignment2/blob/main/Images/alert.PNG)

If the customer tries to add a variable that is located outside the room then they will recieve this response:
![constraint.PNG](https://github.com/amaliebholm/TMM4275-Assignment2/blob/main/Images/constraint.PNG)

### Example 1 


### Example 2

### Example 3

### Common Colclusion on Building KBE System based on A1 and A2
Before this class noen of us had any experience with building KBE Systems, through these two assignments we have already learned a lot. How there are a complex structure and architecture surrounding what can seam as a simple web page for a customer. How important it is that all these components are able to comunicate in a proper way. 
