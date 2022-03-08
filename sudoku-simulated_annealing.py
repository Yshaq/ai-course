# SOLVING SUDOKU by SIMULATED ANNEALING
# Submitted by
# Name: A V Vysakh
# Roll No: 20074001
# Branch: CSE (IDD)

import random
import numpy as np
import math 
from random import choice

# Constant parameters
STARTING_TEMPERATURE = 15
REHEATING_TEMPERATURE = 5
ITERATIONS_PER_TEMPERATURE = 50
COOLING_RATE = 0.99
STUCK_COUNT_FOR_REHEAT = 80
MIN_ALLOWED_TEMPERATURE = 0.008


# Print sudoku in format
def printSudoku(sudoku):
    for i in range(len(sudoku)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(sudoku[i,j])+" "
        print(line)


# Cost function - number of duplicates in all rows and columns
def cost(sudoku):
    rc = rowCost(sudoku)
    cc = colCost(sudoku)
    return (rc+cc)

def rowCost(sudoku):
    cost = 0
    for row in sudoku:
        cost = cost + 9 - len(np.unique(row))
    return cost

def colCost(sudoku):
    trans = np.transpose(sudoku)
    cost = rowCost(trans)
    return cost


# operation to get neighbour
# choose a random 3*3 block and then swap two unfixed numbers
def operation(sudoku_real, fixedSudoku):
    sudoku = np.copy(sudoku_real)
    block_row = random.randint(0,2)
    block_col = random.randint(0,2)
    
    while True:
        cell1_row = random.randint(0,2) + block_row*3
        cell1_col = random.randint(0,2) + block_col*3
        if fixedSudoku[cell1_row, cell1_col] == 0:
            break

    
    while True:
        cell2_row = random.randint(0,2) + block_row*3
        cell2_col = random.randint(0,2) + block_col*3
        if fixedSudoku[cell2_row, cell2_col] == 0 and (cell1_row, cell1_col) != (cell2_row, cell2_col):
            break

    temp = sudoku[cell1_row, cell1_col]
    sudoku[cell1_row, cell1_col] = sudoku[cell2_row, cell2_col]
    sudoku[cell2_row, cell2_col] = temp
    return sudoku


# returns 9x9 grid, 1 denoting fixed numbers in sudoku
def getFixedSudoku(sudoku):
    fixedSudoku = np.full((9,9), 0)
    for i in range(9):
        for j in range(9):
            if sudoku[i,j] != 0:
                fixedSudoku[i,j] = 1

    return fixedSudoku


# Randomly fill the sudoku such that each block has unique numbers
def randomFill(sudoku):
    listOfBlocks = getBlockList()
    for block in listOfBlocks:
        for box in block:
            if sudoku[box[0],box[1]] == 0:
                currentBlock = sudoku[block[0][0]:(block[-1][0]+1),block[0][1]:(block[-1][1]+1)]
                sudoku[box[0],box[1]] = choice([i for i in range(1,10) if i not in currentBlock])
    return sudoku

# Returns a list of (list of cells in each 3x3 block), used in randomFill()
def getBlockList():
    finalList = []
    for block_col in range(3):
        for block_row in range(3):
            cells_in_block = []
            for cell_row in range(3):
                for cell_col in range(3):
                    i = block_row*3 + cell_row
                    j = block_col*3 + cell_col
                    cells_in_block.append([i,j])
            finalList.append(cells_in_block)
    return finalList


# function for solving sudoku
def solve(sudoku):

    fixedSudoku = getFixedSudoku(sudoku)
    
    randomFill(sudoku)

    current_sudoku = np.copy(sudoku)
    temp = STARTING_TEMPERATURE
    current_cost = cost(current_sudoku)
    stuck = 0
    while True:
        previous_cost = current_cost

        for _ in range(ITERATIONS_PER_TEMPERATURE):
            # generate neighbour state
            neighbour = operation(current_sudoku, fixedSudoku)
            neighbour_cost = cost(neighbour)
            current_cost = cost(current_sudoku)

            # check probability and update current state
            p = 1/(1+math.exp((neighbour_cost-current_cost)/temp))
            xx = random.random()
            if xx < p:
                current_sudoku = neighbour

            # is cost 0? then return
            current_cost = cost(current_sudoku)
            if current_cost == 0:
                return current_sudoku


        # if cost of sudoku = 0, return
        current_cost = cost(current_sudoku)
        if current_cost == 0:
            return current_sudoku

        # check for reheating
        if previous_cost == current_cost:
            stuck += 1
        else:
            stuck = 0

        if stuck > STUCK_COUNT_FOR_REHEAT or temp < MIN_ALLOWED_TEMPERATURE:
            print("REHEATING")
            temp += REHEATING_TEMPERATURE
        
        temp *= COOLING_RATE
        print("\n---------------------\ncost: ", current_cost, " temp: ", temp, "\n")
        printSudoku(current_sudoku)


if __name__ == "__main__":

    startingSudoku = '''
    620390001
    040000290
    108060000
    402008900
    000901402
    310070008
    900023805
    260580300
    830000129
    '''

    # Convert the given sudoku into 9*9 array
    sudoku = np.array([[int(i) for i in line] for line in startingSudoku.split()])

    print("Your given sudoku is: (0 is blank space)")
    printSudoku(sudoku)
    print("press any key to continue...")
    input()

    solution = solve(sudoku)
    print("\n---------------------\nSOLUTION FOUND!!!\ncost of solution: ", cost(solution), "\n")
    printSudoku(solution)