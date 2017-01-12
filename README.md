# Ricochet Robots
An optimal solver for the puzzle - Ricochet Robots.

This solver uses [A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) to calculate the optimal path to the destination from the given source.

###Cost function:###
Here, the cost function consists of <b>f(n) = g(n) + h(n)</b>  
Where,  
&nbsp; &nbsp; <b>g(n)</b> - Total number of blocks visited so far.  
&nbsp; &nbsp; <b>h(n)</b> - Manhattan distance between the given position and the goal position.  
Since, the chosen h(n) is an admissible heuristic (never overestimates the goal) and repeated states are handled, A* algorithm is guaranteed to be _complete_ as well as _optimal_.

###Example Format for the test file###
8 # Number of rows  
8 # Number of columns  
[(0, 4), (1, 1), (2, 5), (4, 4), (4, 7), (1, 0), (6, 2), (7, 6)] # List of block locations  
(6, 4) # Where the ball starts  
(2, 4) # Goal location  

I have also uploaded a test file for a 50x50 board under the test folder. To use this new test file, replace the value for the variable _path_to_file_containing_puzzle_ in Ricochet.pyde to the new test file name.

###Pre-reequisites:###
1. Python 2.7
2. Processing 3.2.3, which can be installed from https://processing.org
3. Install python mode in Processing. 

###Execution###
The solver can be executed using the Ricochet.pyde file via the Processing IDE.
