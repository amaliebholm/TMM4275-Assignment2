# TMM4275-Assignment2

This project is a part of the course TMM4275 Knowledge-Based Enineering, Project. The main task is making an automatic KBE system to define a rail installation layout for the K2 EasyFeed equipment for inputs given by a ccustomer. The system will return a layout of the system, represented in Simens NX.  

This project is made by: 
* Kasper Kallseter
* Magnus Myklegard
* Amalie Berge Holm

### The Rail

The image below show a NX modelling of the rail: 
![name](url)

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

![ULM:PNG](url)

In assignment 1 Olingvo and Apache Jena Fuseki was used to communicate with the server containing the parameters, set by both the customer and the product engineer. In assignment 2 the product engineer set a DFA template which was written to by the DFA server, as well as cheching if they are within the room, and not needing a Manufacture Checker Server or a Fuseki Server. 

### Development Tools

This code was made using python in Visual Studio Code. Knowledge Fusion and Journal was used in NX to make models of the rail.

In assignment 1 Olingvo and Apache Jena Fuseki was used to communicate with the server containing the parameters, as stated above, this was not used in assignment 2, since the constraints the variables has to be within is both set by the DFA server, in the same place where they are fetched from the customer. 


### Code Description 

- `DFAserver.py` - Setting up the web-page that the customer uses to place an order, making sure that the variables are set within the size of the room. Giving the lists of different variables as output. 
- `astar_alg.py`- ... 
- Rest of .py files ... 

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
Image of the alerts 

### Example 1 
![Ex1%20-%20setParams.PNG](url)

### Example 2

### Example 3

### Common Colclusion on Building KBE System based on A1 and A2
... 
