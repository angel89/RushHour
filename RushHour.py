#Script to solve the rush hour game.
#Creates states representing the positions of the cars on the board and adds it to a FIFO queue. Will then select a car(searches the board left to right, top to bottom) to find the cars new posible positions and create a new state for each of them. These new states are then added to the queue and the nodesdictionary.
#The script will continue extracting states from the queue and creating new ones until a state is found that has an "r" at the end position.
#By saving the states, moves and previous state into a dictionary when the victory conditions are met they can be recovered and printed out by backtracking.
#Each state is represented by a string, the x's are blank spaces and each number represents a type of car:
# 1 = length 2 vertical car
# 2 = length 3 vertical car
# 3 = length 2 horizontal car
# 4 = length 3 horizontal car
# rr = red car
#When changing the size of the board, make sure to also change the endposition and the startState. Also the rr car must always be on the same horizontal line as the endposition. There is an example of different sized boards commented out in the script

from collections import deque

startState = "444122" \
             "133122" \
             "1xrr22" \
             "331xxx" \
             "x11x33" \
             "x13333" \

# startState = "444122x" \
#              "133122x" \
#              "1xrr22x" \
#              "331xxxx" \
#              "x11x33x" \
#              "x13333x" \
#              "xxxxxxx"

#Index of the end position
endposition = 17
# endposition=20

#Size of the grid
sizegrid = 6
# sizegrid=7

#Dictionary for the different types of lengths
lengthDict = {"1":2, "2":3, "3":2, "4":3,"r":2}

#Dictionary to see if its a vertical or horizontal car
typedict = {"1":sizegrid, "2":sizegrid, "3":1, "4":1,"r":1}

#FIFO queue for the states to be checked
queue = deque([startState])

#Dictionary to keep track of the nodes path, the moves made and to avoid adding duplicate states. For the key it uses a new state and as its value pair a list containing the move made and the previouse state.
nodesdicitonary = {startState : None}


#Function to check if there are any horizontal positions availabe to which the car at currInx can slide to
def horizIndx2Check(currIndx, length, currentnode):
    #Set used to save the new positions found
    foundindexes = set()
    #While loop to check if the new position has a blank space, if its inside the boundries of the board and if it has space for the car.  This loop is to search to the right of the car horizontally.
    i=0
    while (i + (currIndx%sizegrid) + length < sizegrid):
        if (currentnode[currIndx + i + length] == "x"):
            foundindexes.add(currIndx + i + 1)
            i += 1
        else:
            break
    # While loop to check if the new position has a blank space, if its inside the boundries of the board and if it has space for the car. This loop is to search to the left of the car horizontally.
    i=1
    while ((currIndx%sizegrid) - i > -1):
        if (currentnode[currIndx - i] == "x"):
            foundindexes.add(currIndx - i)
            i += 1
        else:
            break
    #Returns the new positions for the car at currIndx
    return foundindexes

#Function to check if there are any vertical positions availabe to which the car at currInx can slide to
def vertIndx2Check(currIndx, length, currentnode):
    #Set used to save the positions found
    foundindexes = set()
    #While loop to check if the new position has a blank space, if its inside the boundries of the board and if it has space for the car.  This loop is to search downwards.
    i = 0
    while (currIndx + sizegrid*(length+i) < sizegrid*sizegrid):
        if (currentnode[currIndx + sizegrid*(length + i)] == "x"):
            foundindexes.add(currIndx + sizegrid*(i + 1))
            i += 1
        else:
            break
    # While loop to check if the new position has a blank space, if its inside the boundries of the board and if it has space for the car.  This loop is to search upwards.
    i = 1
    while (currIndx - sizegrid*i > -1):
        if (currentnode[currIndx - sizegrid*i] == "x"):
            foundindexes.add(currIndx - sizegrid*i)
            i += 1
        else:
            break
    # Returns the new positions for the car at currIndx
    return foundindexes

#Function to create new nodes and check if the conditions for victory are met(red car at the goal position).
def createNewNodes(currentnode, newpostion, index, length, HorOrVert):

    #While loop untill no more new positions are left
    while(newpostion):
        #A set with the new positions for the car at index
        newpos = newpostion.pop()
        #Temporary list to help in creating the new state by swaping the current position with the new one.
        temp = list(currentnode)

        #This creates the new state by swapping the car with blank spaces from its current postion(index) to its new one(newpos). Used 2 for's because on 1 space movements the x was overwriting the cars symbol on the new state.
        for n in range(length):
            temp[index + n*HorOrVert] = "x"
        for n in range(length):
            temp[newpos + n*HorOrVert] = currentnode[index]
        #Join the list to create a state
        newnode = "".join(temp)

        #Checks if the new state already exist in the nodes dictionary.
        if(newnode not in nodesdicitonary):
            #If it dosent, it creates a new node with the move made, its new state and its previouse node.
            nodesdicitonary[newnode] = [[index, newpos], currentnode]
            #Adds the new node to the queue
            queue.append(newnode)
            #Checks if the red car has reached its goal.
            if (newnode[endposition : endposition+1] == "r"):
                #Calls victory function to print out the states and moves used.
                victory(newnode)
                return True

    return False

#This function prints out the states used and moves made to reach the final state.
def victory(endnode):

    # This is the last state.
    print("Victory")
    for n in range(sizegrid):
        print(endnode[sizegrid*n : n*sizegrid + sizegrid])
    print("")

    # While loop to print out the states and moves used to get to the final state
    while(True):
        try:
            moves,endnode=nodesdicitonary.get(endnode)
            print("Move car at " + str(moves[0]) + " to " + str(moves[1]))

            for n in range(sizegrid):
                print(endnode[sizegrid*n : n*sizegrid+sizegrid])
            print("")
        except:
            break

#While loop to extract the states saved in the FIFO queue
while(queue):
    currentnode = queue.popleft()
    # Create a set containing the indexes left to check for the current state.
    bagOindxs = set(range(sizegrid*sizegrid))

    while(bagOindxs):
        #Saves the index being checked(currIndex)
        currIndex = int(bagOindxs.pop())
        # Gets the value of the state at currIndex
        valueCurrent = currentnode[currIndex]
        #Gets the type and length of the car.
        lengthCar = lengthDict.get(valueCurrent)
        HorOrVer = typedict.get(valueCurrent)

        #If to check if its a vertical car.
        if (HorOrVer == sizegrid ):
            # Function to find the new available positions to which to slide the car to.
            foundindicies = vertIndx2Check(currIndex, lengthCar, currentnode)

            #For used to remove the indexes the current car is using from the set of indexes left(bagOindxs).
            for n in range(lengthCar-1):
                bagOindxs.remove((currIndex) + (sizegrid*(n+1)))

        # If to check if its a horizontal car.
        elif (HorOrVer == 1 ):
            # Function to find the new available positions to which to slide the car to.
            foundindicies = horizIndx2Check(currIndex, lengthCar, currentnode)

            # For used to remove the indexes the current car is using from the set of indexes left(bagOindxs).
            for n in range(lengthCar - 1):
                bagOindxs.remove(currIndex + n + 1)

        #Function to create new nodes, returns true if the victory conditions are met.
        end = createNewNodes(currentnode, foundindicies, currIndex, lengthCar, HorOrVer)

        #Breaks when victory conditions are met
        if(end):
            break
    # Breaks when victory conditions are met
    if (end):
        break




# def Vertcreatenewnodes(currentnode,posibleindices,index,length):
#
#     while(posibleindices):
#         a = posibleindices.pop()
#         temp = list(currentnode)
#
#         for n in range(length):
#             temp[index + n*6] = "x"
#         for n in range(length):
#             temp[a + n*6] = currentnode[index]
#         newnode = "".join(temp)
#
#         if (newnode not in nodesdicitonary):
#             nodesdicitonary[newnode] = [[index,a],currentnode]
#             queue.append(newnode)
