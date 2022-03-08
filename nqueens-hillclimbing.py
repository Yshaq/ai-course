# Solving N-Queens problem by hill climbing algorithm
# Submitted by:
#   Name: A V Vysakh
#   Roll no: 20074001
#   Branch: CSE (IDD)

import numpy as np
import random

# Returns a random state of chessboard. Each row of the chessboard contains one queen, as this constraint must be satisfied in the solution.
def random_starting(n):
    # a state (chessboard) is represented by a N*N 2D array where each element represents a square on chessboard. 0 represents an empty square whereas 1 represents a queen.
    board = np.full((n,n), 0)

    for i in range(n):
        queen = random.randint(0, n-1)
        board[i][queen] = 1
    return board


def check_vertical(board, queen, n):
    x = 0
    qi, qj = queen[0], queen[1]
    for i in range(n):
        if board[i][qj] == 1:
            x = x+1
    x = x-1
    return x


def check_diagonals(board, queen, n):
    x = 0
    qi, qj = queen[0], queen[1]
    i, j = qi-1, qj-1
    while(i>=0 and j>=0):
        if board[i][j] == 1:
            x = x+1
        i = i-1
        j = j-1
    
    i, j = qi+1, qj+1
    while(i<n and j<n):
        if board[i][j] == 1:
            x = x+1
        i = i+1
        j = j+1
    
    i, j = qi+1, qj-1
    while(i<n and j>=0):
        if board[i][j] == 1:
            x = x+1
        i = i+1
        j = j-1

    i, j = qi-1, qj+1
    while(i>=0 and j<n):
        if board[i][j] == 1:
            x = x+1
        i = i-1
        j = j+1

    return x


# Function returns the position of the N queens on the board
def find_queens(board, n):
    queens = []
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                queens.append([i,j])   
    return queens


# Heuristic function. The heuristic of a state is taken as the number of pairs of queens that can attack each other.
def heuristic(board, n):
    queens = find_queens(board, n)
    h = 0
    for queen in queens:
        h = h+check_vertical(board, queen, n)
        h = h+check_diagonals(board, queen, n)

    return int(h/2)


# Returns list of all (n)(n-1) neighbouring states, each queen constrained to move along it's current row.
def generate_neighbours(board, n):
    queens = find_queens(board, n)
    neighbours = []
    for queen in queens:
        qi, qj = queen[0], queen[1]
        for j in range(n):
            if j != qj:
                neighbour = np.copy(board)
                neighbour[qi][qj] = 0
                neighbour[qi][j] = 1
                neighbours.append(neighbour)

    return neighbours


# Function implementing the hill climbing (descent) algorithm
def hill_climbing(n):
    curr_state = random_starting(n)
    print("\nRANDOMIZED STARTING STATE:\n", curr_state)
    print("pairs of queens that can attack each other: ", heuristic(curr_state, n))

    while True:
        curr_h = heuristic(curr_state, n)
        neighbours = generate_neighbours(curr_state, n)

        best_neighbour = neighbours[0]
        best_h = heuristic(best_neighbour, n)

        for neighbour in neighbours:
            neighbour_h = heuristic(neighbour, n)
            if neighbour_h < best_h:
                best_neighbour = neighbour
                best_h = neighbour_h

        if best_h < curr_h:
            curr_state = best_neighbour
        else:
            break

    print("\n----------------\nHILL CLIMBING ENDED, FINAL STATE:\n", curr_state)
    curr_h = heuristic(curr_state, n)
    print("pairs of queens that can attack each other: ", curr_h)

    return curr_state, curr_h


def main():
    n = int(input("Enter N: "))
    choice = 1
    
    while(choice == 1):

        solution, curr_h = hill_climbing(n)

        if curr_h != 0 and n>3:
            print("----------------\nThe algorithm has been trapped in a local optimum/plateau. Would you like to random restart?\n1. Random restart\n2. Exit")
            choice = int(input("Enter choice: "))

        else:
            print("We have reached the global optimum solution!")
            break


    
if __name__ == "__main__":
    main()