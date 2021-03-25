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
* Obstacles in the room that the cart has to avoid (given as whole areas in the room)

### The KBE Application Architecture

This is a diagram showing the main blocks and interconnections between them. 

![Client-Server](https://github.com/amaliebholm/TMM4275-KBE-project/blob/main/Images/Client-Server.png)

The main changes form assignment 1 is .... 


### ULM Sequence Diagram

The ULM sequence diagram showing how an order making scenario will play out. From how the customer makes the order of the rail, to the algorithm finding the best path and this path being made in NX. 

![ULM:PNG](https://github.com/amaliebholm/TMM4275-KBE-project/blob/main/Images/ULM.PNG)


### Development Tools

This code was made using python in Visual Studio Code. Knowledge Fusion and Journal was used in NX to make models of the chair.


### Code Description 

- `DFAserver.py` - Setting up the web-page that the customer uses to place an order, making sure that the variables are set within the size of the room. Giving the lists of different variables as output. 
- `astar_alg.py`- ... 
- Rest of .py files ... 

### DFAs
- `Rail_Order.dfa` - Containing the NX file whith the parameters given by the customer

## Video of working KBE system

## Examples of Three Different Product Orders  

### A Customer Trying to Order Outside the Constraints
Image of the alerts 

### Example 1 
![Ex1%20-%20setParams.PNG](https://github.com/amaliebholm/TMM4275-KBE-project/blob/main/Images/Ex1%20-%20setParams.PNG)

### Example 2

### Example 3

### Common Colclusion on Building KBE System based on A1 and A2
... 
