### NAME: Rachel Malone
### ID: 21249309
### Git URL: https://github.com/rachelkmalone/ARC

#!/usr/bin/python

import os, sys
import json
import numpy as np
import re


### Code Commentary
# The following ARC tasks were solved as part of Assignment 3:
# Task: c1d99e64, ed36ccf7, 3de23699, 2204b7a8, 1caeab9d, a78176bb, a3df8b1e, 67a423a3
# The doc string created for each function details the task function and how many of the training and test grids were
# solved correctly.

# While most of the tasks selected for this assignment vary in difficulty and the task form itself, there are some similarities
# to be seen such as the use of libraries. A key library used throughout the solve_* functions is numpy. Numpy is a python library
# that offers support with matrix and array manipulation. In the functions it is denoted as "np". The np.where() function is commonly
# used to find and replace values in the arrays. It works by giving a condition, array and value to change to as parameters. It is
# seen in tasks 3de23699, 1caeab9d, a78176bb and 67a423a3. Np.unique() is frequently used to help locate the "colour" values found in the
# arrays. The function np.array() is also used in the functions. It tasks an input (these can ranges from lists to dataframes) and
# turns them into an array. This is helpful after using a list comprehension to create a list of the array values to turn this output
# into a list. Other numpy functions used include np.nonzero(), np.sort() and np.add().

# Another commonly used practise across the solve_* functions is the use of list comprehensions. These were regularly used to help
# fund the indexes where a certain "colour's" corresponding value existed. For example, the code "grey_list = [x[i,j] for j in range(x.shape[1])
# for i in range(x.shape[0]) if x[i,j] == 5] finds all indexes with corresponding value of 5 (grey) in the array and saves them to a list (see task
# a78176bb). However, list comprehensions were also used to the change and over-write values at a particular instance. For example, in tasks
# ed36ccf7, a list comprehension is used to change indexes so that the ouputted array is turned 90 degress anti-clockwise.

# The task themselves also saw a few similarities between them. Many of them included changing colours to a different colour. For example,
# tasks c1d99e64 sought to change any row/column full of zeros to a 2 or tasks 67a423a3 looked to change the 8 points around the intersection
# of non-zero lines to the value 4. Another similarity seen across tasks was creating diagonals throughout the array. Tasks a78176bb and a3df8b1e
# both required the creation of diagonal lines starting from specific points in the array. Initially, it was believed numpy functions such
# as np.fill_diagonal() or np.diagonal() could be used but due to the specific points where the diagonal needed to be created, it proved easier
# to take an interative approach to change the values to create the desired final array. A third example of commonalities between task description
# included "moving" values around the array. Task ed36ccf7 (turn array 90 degrees anti-clockwise) and 1caeab9d (moving blocks of red and yellow to be
# in line with blue) both seek to change the indexes of particular values in the array giving the look that those values have been moved.


def solve_c1d99e64(x):
    
    """ This function searches for rows and columns that
    are entirely made of zeros. It then changes these
    rows/ columns to be filled with value 2

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array
    
    Training Grids Solved: 3/3
    Test Grids Solved: 1/1
    """
    
    ### Create a copy of the input array.
    ### We will use this to added and change values.
    x_out = x.copy()
    
    ### Find rows and columns where only zeros appear
    row_zero = [row for row in range(x.shape[0]) if len(np.unique(x[row])) ==1]
    col_zero = [col for col in range(x.shape[1]) if len(np.unique(x.transpose()[col])) ==1 ]
    
    ### Change the chosen rows and columns to be value 2
    x_out[row_zero, :] = 2
    x_out[:, col_zero] = 2

    return x_out


def solve_ed36ccf7(x):
    
    """ This function takes the input array x and then
    rotates the array by 90 degrees anti-clockwise. This
    rotated array is then outputted as the result and
    is called x_out.

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array
    
    Training Grids Solved: 4/4
    Test Grids Solved: 1/1
    """
    
    ### Create a list of lists. Each list will represent a row of
    ### the newly rotated x. The loop begins by iterating through
    ### the row indexes of x, starting from it's highest index
    ### and working backwards to zero. It then iterates through
    ### the column indexes, beginning from zero and working
    ### up to the highest value
    list_x = [[x[j,i] for j in range(x.shape[1])] for i in range(x.shape[0]-1,-1,-1)]
    
    ### Take the list of lists and transform to an array x_out
    x_out = np.array(list_x, dtype = int)
    
    return x_out
    
def solve_3de23699(x):
    
    """ This function creates a rectangle around the outermost
    non-zero values and then removes zero values around it. Next
    it changes the inner values to the same value as the
    rectangle corners and then removes a border of width 1
    from the array.

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array
    
    Training Grids Solved: 4/4
    Test Grids Solved: 1/1
    """
    
    ### Create a copy of the input array.
    ### We will use this to added and change values.
    x_out = x.copy()
    
    ### Trim zeros outside rectangle where non-zero value exist
    non_zero = np.nonzero(x_out)
    sorted_rows = np.sort(non_zero[0])
    sorted_cols = np.sort(non_zero[1])
    x_out = x_out[sorted_rows[0]: sorted_rows[-1]+1,
                  sorted_cols[0]: sorted_cols[-1]+1]
    
    ### Find colour in corners and colour of inner parts
    colour_1 = x_out[0,0]
    colour_2 = [value for value in np.unique(x_out) if value != colour_1 and value != 0]
    

    ### Change inner colours to colours in corner
    x_out = np.where(x_out != colour_2, x_out, colour_1)
    
    ### Remove border by moving in 1 index at every side
    x_out = x_out[1:-1, 1:-1]

    return x_out
    

def solve_2204b7a8(x):
        
    """ This function takes the input array x and searches for the non-zero
    boundary lines. These boundaries will exist on the top and bottom rows or
    on the left most and irght most column. Any remaining non-zero values will be
    mapped to these boundary values based on proximity (value is mapped to
    boundary value nearest to it)

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array after values have been mapped
    
    Training Grids Solved: 3/3
    Test Grids Solved: 1/1
    """
    
    ### Create a copy of the input array.
    ### We will use this to added and change values.
    x_out = x.copy()
    
    ### Find the 2 colours to map to
    ### Check if they are on the left most/ Right most vertical axis
    ### Check the colour of the midpoint of the left column isn't 0 or 3
    if x[x.shape[0]//2, 0] != 0 and x[x.shape[0]//2, 0] != 3:
        vert_1 = x[x.shape[0]//2, 0]
        vert_2 = x[x.shape[0]//2, x.shape[1] - 1]
        
        ### Iterate through the values of x and check where there's a 3.
        for i in range(x.shape[0] - 1):
            for j in range(x.shape[1] - 1):
                
                ### Check if this value's column index is less than the middle index.
                ### If both true, map this value to colour_1_vert.
                if x[i,j] == 3 and j < x.shape[1] // 2:
                    x_out[i,j] = vert_1
                
                ### If value == 3 but column index is greater than or equal
                ### to middle index, map this value to colour_2_vert.
                elif x[i,j] == 3 and j >= x.shape[1] // 2:
                    x_out[i,j] = vert_2
        
    ### Check if mapping colours are on top/ bottom horizontal axis
    ### Check the colour of the midpoint of top row isn't 0 or 3
    elif x[0, x.shape[1]//2] != 0 and x[0, x.shape[1]//2] != 3:
        horiz_1 = x[0, x.shape[1] // 2]
        horiz_2 = x[x.shape[0] - 1, x.shape[1]//2]
        
        
        ### Iterate through the values of x and check where there's a 3.
        for i in range(x.shape[0] - 1):
            for j in range(x.shape[1] - 1):
                
                ### Check if this value's row index is less than the middle index.
                ### If both true, map this value to colour_1_horiz.
                if x[i,j] == 3 and i < x.shape[0] // 2:
                    x_out[i,j] = horiz_1
                    
                ### If value == 3 but row index is greater than or equal
                ### to middle index, map this value to colour_2_horiz.
                elif x[i,j] == 3 and i >= x.shape[0] // 2:
                    x_out[i,j] = horiz_2
    return x_out
    
    
def solve_1caeab9d(x):
    
    """ This function looks at the 3 coloured components
    (red, yellow, blue) from the input array. The red and
    yellow components are shifted along their column indexes
    to be in line with the blue component.

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array
    
    Training Grids Solved: 3/3
    Test Grids Solved: 1/1
    """
    
    ### Create a copy of the input array.
    ### We will use this to added and change values.
    x_out = x.copy()
    
    ### 1=blue, 2=red, 4=yellow
    ### Find the biggest columns index where blue values exists
    blue_list = [[i,j] for j in range(x_out.shape[1]) for i in range(x_out.shape[0])
                      if x_out[i,j] == 1]
    ### Find the biggest columns index where blue exists
    bottom_row_blue = blue_list[-1][0]
  
    def colour_array(colour_int, array, bottom_row_blue):
        '''Grab all points of colour_int and move them along column
        to be inline with the blue component
        '''
        ### get indexes where this colour exists
        colour_list = [[i,j] for j in range(array.shape[1]) for i in range(array.shape[0])
                      if array[i,j] == colour_int]
        
        ### Find the biggest columns index where this colour exists
        bottom_row_color = colour_list[-1][0]
        ### Calculate how far up/down this colour shape needs to move
        diff = bottom_row_blue - bottom_row_color
        ### Move colour shape
        colour_list = [[i+diff,j] for [i,j] in colour_list]
        ### Create an array where only the chosen colour component exists
        array = np.where(array == colour_int, array, 0)
        array.fill(0)
        for indexes in colour_list:
            array[indexes[0], indexes[1]] = colour_int
        
        return array
    
    ### Create a unique array for each colour
    red_array  = colour_array(2, x_out, bottom_row_blue)
    yellow_array = colour_array(4, x_out, bottom_row_blue)
    blue_array = colour_array(1, x_out, bottom_row_blue)
    
    ### Add arrays together to get final output
    x_out = np.add(red_array, blue_array)
    x_out = np.add(yellow_array, x_out)
        
        
    return x_out
    
    
def solve_a78176bb(x):

    """ This function searches for a triangle of the value 5 along a diagonal
    in the array. Triangles can be formed above and below the diagonaol.
    The function then creates a diagonal of the same value as the
    original diagonal along the point diagonally opposite the peak of
    the triangle of 5's. It then resets any values of 5 to a 0.

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array after new diagonals have been created
    
    Training Grids Solved: 3/3
    Test Grids Solved: 1/1
    """
    
    
    ### Create a copy of the input array.
    ### We will use this to added and change values.
    x_out = x.copy()
    
    ### Find the colour we will later need to change our desired
    ### diagonal to. Iterate through each value in x and record
    ### any values that are not 0 (black) or 5 (grey).
    ### Should be a list of all the same value.
    colour_list = [[i,j] for j in range(x.shape[1]) for i in range(x.shape[0])
                   if x[i,j] != 0 and x[i,j] !=5]
    
    ### Extract this value and call it num_color
    num_colour = x[colour_list[0][0], colour_list[0][1] ]
    
    ### Create a list of all indexes in x where the value is 5 (grey)
    grey_list = [x[i,j] for j in range(x.shape[1]) for i in range(x.shape[0])
                   if x[i,j] == 5]
 
    ### Track the number of steps across a grey triangle has
    ### to detemine max length for upper trianlges
    across_colour_ind = []
   
    ### Track the number of steps across a grey triangle has
    ### to detemine max length for upper trianlges
    down_colour_ind = []
    
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            
            
            ### Check for upper triangles (formed above the coloured diagonal)
            if x[i,j] in grey_list and x[i,j-1] == num_colour and x[i+1,j] == num_colour:
                
                ### Initialise the index of the grey point
                across_index = [0,0]
                
                for k in range(x.shape[1] - j - 1):
                    
                    ### Check if the value beside current value is also grey
                    if x[i,j+k] in grey_list:
                        
                        ### Update the index refering to end of grey line
                        across_index = [i,j+k]
                
                ### When the grey line has been fully finished, add the last
                ### indexes to across_colour_list (list fof grey indexes)
                across_colour_ind.append(across_index)
                
                ### Using the grey point found at the longest edge in the triangle
                ### (located at across_colour_ind[0]) move diagonally up and to the right
                ### to find a point on the diagonal we want to make
                diag_point_upper = [across_colour_ind[0][0]-1, across_colour_ind[0][1]+1]
                
                ### Using the point we found on the diagonal, find the left most and top most
                ### Value on the diagonal
                diag_start_upper = [diag_point_upper[0]-diag_point_upper[0],
                                     diag_point_upper[1]-diag_point_upper[0]]
                
                ### Fill the diagonal with the correct colour
                indexes = np.arange(x.shape[1]- diag_start_upper[1])
                x_out[indexes, indexes + diag_start_upper[1]] = num_colour
                
            
            
            ### Check for lower triangles (formed below the coloured diagonal)
            elif x[i,j] in grey_list and x[i-1,j] == num_colour and x[i,j+1] == num_colour:
                
                ### Initialise steps down counter
                down_index = [0,0]
                
                for k in range(x.shape[0] - i - 1):
        
                    if x[i+k, j] in grey_list:
                        down_index = [i+k,j]
                        
                ### When the grey line has been fully finished, add the last
                ### indexes to across_colour_list (list fof grey indexes)
                down_colour_ind.append(down_index)
                
                ### Using the grey point found at the longest edge in the triangle
                ### (located down_colour_ind[0]) move diagonally down and to the left
                ### to find a point on the diagonal we want to make
                diag_point_lower = [down_colour_ind[0][0]+1, down_colour_ind[0][1]-1]

                ### Using the point we found on the diagonal, find the left most and top most
                ### Value on the diagonal
                diag_start_lower = [diag_point_lower[0]-diag_point_lower[1],
                                     diag_point_lower[1]-diag_point_lower[1]]
                
                ### Fill the diagonal with the correct colour
                indexes = np.arange(x.shape[0]- diag_start_lower[0])
                x_out[indexes  + diag_start_lower[0], indexes] = num_colour
                
                
    ### Remove all values that are equal to 5
    x_out = np.where(x_out != 5, x_out, 0)
    return x_out
    
    
def solve_a3df8b1e(x):
    
    """ This function intakes an array x, and creates a
    blue diagonal from the bottom left point up and to the
    right. It then takes the end point of that diagonal
    and creates another diagonal up and left from there.
    This process is repeated until the the values reach the
    top row of the array.

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array
    
    Training Grids Solved: 3/3
    Test Grids Solved: 1/1
    """
    
    ### Fill diagonal from Left to Right Fill
    def left_to_right(start_point, arr):
        '''Fill diagonal from start_point up and to the right'''
        
        for j in range(arr.shape[1]):
            ### Set values on right/up diagonal to 1
            arr[start_point[0] - j, start_point[1]+j]  = 1
            ### Save point
            end_point = [start_point[0] - j, start_point[1]+j]
            ### Check if we reached top row of array
            if end_point[0] == 0:
                break
            else:
                continue
        return end_point, arr

    ### Fill diagonal from Right to left fill
    def right_to_left(start_point, arr):
        '''Fill diagonal from start_point up and to the left'''
        
        for j in range(arr.shape[1]):
            ### Set values on left/up diagonal to 1
            arr[start_point[0]-j,start_point[1]-j] = 1
            ### Save point
            end_point = [start_point[0]-j,start_point[1]-j]
            ### Check if we reached top row of array
            if end_point[0] == 0:
                break
            else:
                continue
        return end_point, arr
   

    ### Create a copy of the input array.
    ### We will use this to added and change values.
    x_out = x.copy()
    
    ### Grab original start point of diagonals
    end_point = [x.shape[0]-1, 0]
    
    ### Loop will run as long the end point isn't on the top row
    while end_point[0] != 0:
        ### Run diagonal up and right
        end_point, x_out = left_to_right(end_point, x_out)
        ### Run diagonal up and left
        end_point, x_out = right_to_left(end_point, x_out)
    
    
    return x_out
    
    
def solve_67a423a3(x):

    """ This function searches for the intersection of
    2 non-zero lines. The 8 values that are formed around
    this point of intersection are then relabelled to 4.

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array after new diagonals have been created
    
    Training Grids Solved: 3/3
    Test Grids Solved: 1/1
    """

    def find_repeat_ind(arr):
        
        """ This function intakes an array of indices and checks
        which of the 2 rows in the array contains only one unique value.
        It returns the single unique value of the chosen row.

        Parameters:
        arr -- input array of indicies.
    
        Returns:
        index -- integer, the single unique value
        """
        
        if len(np.unique(arr[0])) == 1:
            index = np.unique(arr[0])[0]
        elif len(np.unique(arr[1])) == 1:
            index = np.unique(arr[1])[0]
        return index
    
    ### Create a copy of the input array.
    ### We will use this to added and change values.
    x_out = x.copy()
    
    ### np.unique() returns an ordered list of unique elements
    ### Extract the 2 non-zero elements (zero at index 0)
    num_1 = np.unique(x)[1]
    num_2 = np.unique(x)[2]
    
    ### For each value, create an array to show the
    ### indexes where the value appears
    num_1_ind = np.asarray(np.where(x == num_1))
    num_2_ind = np.asarray(np.where(x == num_2))
    
    ### Call function find_repeat_ind()
    ### to find point of intersection of
    ### the 2 lines. The point of
    ### intersection would be x_out[index_num_1, index_num_2]
    index_num_1 = find_repeat_ind(num_1_ind)
    index_num_2 = find_repeat_ind(num_2_ind)
    
    
    outer_ind = [[-1, -1], [-1, 0], [-1, 1], ### Top row
                 [0, -1], [0, 1],            ### Middle row
                 [1, -1], [1, 0], [1, 1]]    ### Bottom row
    
    ### Take all indexes around the point of intersection
    #### and set them to 4
    for pair in outer_ind:
        x_out[index_num_1 + pair[0], index_num_2 + pair[1]] = 4
    
    return x_out
    
    

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    if y.shape != yhat.shape:
        print(f"False. Incorrect shape: {y.shape} v {yhat.shape}")
    else:
        print(np.all(y == yhat))


if __name__ == "__main__": main()

