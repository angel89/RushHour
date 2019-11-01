# RushHour
  
Script to solve the rush hour game.
Creates states representing the positions of the cars on the board and adds it to a FIFO queue. Will then select a car(searches the board left to right, top to bottom) to find the cars new posible positions and create a new state for each of them. These new states are then added to the queue and the nodesdictionary.
The script will continue extracting states from the queue and creating new ones untill a state is found that has an "r" at the end position.
By saving the states, moves and previous state into a dictionary when the victory conditions are met they can be recovered and printed out by backtracking.
Each state is represented by a string, the x's are blank spaces and each number represents a type of car:
 1 = length 2 vertical car
 2 = length 3 vertical car
 3 = length 2 horizontal car
 4 = length 3 horizontal car
 rr = red car
When changing the size of the board, make sure to also change the endposition and the startState. Also the rr car must always be on the same horizontal line as the endposition. There is an example of different sized boards commented out in the script

startState = "444122" \
             "133122" \
             "1xrr22" \
             "331xxx" \
             "x11x33" \
             "x13333" \
