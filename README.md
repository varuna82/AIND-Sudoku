# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation is applied to a problem state to reduce solution space.
   By solving Naked Twins problem in a Sudoku state,
   we could reduce the solution space Sudoku solution search.
   To solve the Naked Twins problem, program traverse through all the units and
   find two boxes with same possible values within the unit. Then, removes those values
   from peers within the unit.

   We could apply this repeatedly (along with other constraint propagation methods)
   to reduce solution state of the Sudoku state.
   However, applying only constraint propagation alone doesn't gaurantee a solution.
   There fore using a search algorithm is recommended to solve the Sudoku board itself.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal Sudoku has two additional constraints to the Sudoku game.
   In Diagonal Sudoku two diagonals should contain all the digits from
   1 to 9, in addition to normal Sudoku.
   In this program diagonal Sudoku is solved by applying following constraint propagations
   to all the units (each row, each column, 3x3 principle squares, diagonals)
     - Eliminate
     - Only choice
     - Naked Twins

   Applying above algorithm repeatedly could solve a simple Diagonal Sudoku game.
   However, search algorithm should be used along with constraint propagation to solve
   complex Diagonal Sudoku games.

   In this program, we use Depth First search along with the constraint propagation to
   solve Diagonal Sudoku games.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.