"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xcount = 0
    ocount = 0
    # ecount = 0
    for i in board:
        for j in i:
            if j == "X":
                xcount +=1
            elif j == "O":
                ocount +=1
            # else:
                # ecount +=1
    if xcount >ocount:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    act=set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                act.add((i,j))
    return act

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard = copy.deepcopy(board)
    turn = player(board)
    i = action[0]
    j = action[1]
    if i >3 or j>3:
        raise ValueError("Invaid move")
    if newboard[i][j] == EMPTY:
        newboard[i][j] = turn
    else:
        raise ValueError("Not empty!")
    return newboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != EMPTY:
                if 0<j<2:
                    if board[i][j-1] == board[i][j] and board[i][j]==board[i][j+1]:
                        return board[i][j]
                if 0<i<2:
                    if board[i][j] == board[i-1][j] and board[i][j] == board[i+1][j]:
                        return board[i][j]
                if 0<i<2 and 0<j<2:
                    if (board[i][j] == board[i-1][j-1] and board[i][j] == board[i+1][j+1]) or (board[i][j] == board[i-1][j+1] and board[i][j] == board[i+1][j-1]):
                        return board[i][j]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win = winner(board)
    count =0
    if win != None:
        return True
    for i in board:
        for j in i:
             if j == EMPTY:
                 count +=1
    if count ==0:
        return True
    else:
        return False
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == "X":
        return 1
    elif win =="O":
        return -1
    else:
        return 0

def max_min(board):
    if terminal(board):
        return False
    score = -9999
    acts = actions(board)
    for act in acts:
        newboard = result(board, act)
        if not terminal(newboard):
            play = player(newboard)
            if play == "O":
                tmp = min_max(newboard)
            else:
                tmp = max_min(newboard)
        else:
            tmp = utility(newboard) 
        if tmp > score:
            score = tmp
    return score

def min_max(board):
    if terminal(board):
        return False
    score = 9999
    acts = actions(board)
    for act in acts:
        newboard = result(board, act)
        if not terminal(newboard):
            play = player(newboard)
            if play == "O":
                tmp = min_max(newboard)
            else:
                tmp = max_min(newboard)
        else:
            tmp = utility(newboard) 
        if tmp < score:
            score = tmp
    return score



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    optimal = (0,0)
    acts = actions(board)
    play = player(board)
    if play == "O":
        tmp = 9999
        for act in acts:
            newboard = result(board, act)
            score = max_min(newboard)
            if score <tmp:
                tmp = score
                optimal = act
    else:
        tmp = -9999
        for act in acts:
            newboard = result(board, act)
            score = min_max(newboard)
            if score >tmp:
                tmp = score
                optimal = act
    return optimal