### NAME: Rachel Malone
### ID: 21249309

#!/usr/bin/python

import os, sys
import json
import numpy as np
import re


def solve_ed36ccf7(x):
    
    """ This function takes the input array x and then
    rotates the array by 90 degrees anti-clockwise. This
    rotated array is then outputted as the result and
    is called x_out.

    Parameters:
    x -- input array
    
    Returns:
    x_out -- output array
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

def solve_2204b7a8(x):

    """ This function takes the input array x and searches for the non-zero
    boundary lines. These boundaries will exist on the top and bottom rows or
    on the left most and irght most column. Any remaining non-zero values will be
    mapped to these boundary values based on proximity (value is mapped to
    boundary value nearest to it)

    Parameters:
    x -- input array
    
    Returns:
    x -- array after values have been mapped
    """
    
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
                    x[i,j] = vert_1
                
                ### If value == 3 but column index is greater than or equal
                ### to middle index, map this value to colour_2_vert.
                elif x[i,j] == 3 and j >= x.shape[1] // 2:
                    x[i,j] = vert_2
        
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
                    x[i,j] = horiz_1
                    
                ### If value == 3 but row index is greater than or equal
                ### to middle index, map this value to colour_2_horiz.
                elif x[i,j] == 3 and i >= x.shape[0] // 2:
                    x[i,j] = horiz_2

    return x

def solve_05269061(x):
    return x


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

