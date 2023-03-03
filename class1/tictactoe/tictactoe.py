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
    actions=set()
    for i in board:
        for j in i:
            if j == "EMPTY":
                set.add((i,j))
    return actions

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
    if newboard[i][j] == "Empty":
        newboard[i][j] = turn
    else:
        raise ValueError("Not empty!")
    return newboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        for j in range(len(i)):
            try:
                if any(
                    board[i][j-1] == board[i][j] and board[i][j]==board[i][j+1],
                    board[i][j] == board[i-1][j] and board[i][j] == board[i+1][j],
                    board[i][j] == board[i-1][j-1] and board[i][j] == board[i+1][j+1],
                    board[i][j] == board[i-1][j+1] and board[i][j] == board[i+1][j-1]
                ):
                    return board[i][j]
            except ValueError:
                pass
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winner = winner(board)
    count =0
    if winner != None:
        return True
    for i in board:
        for j in i:
             if j == "EMPTY":
                 count +=1
    if count ==0:
        return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner = winner(board)
    if winner == "X":
        return 1
    elif winner =="O":
        return -1
    else:
        return 0

def max_min(board):
    if terminal(board):
        return False
    score = -9999
    actions = actions(board)
    for i in range(len(actions)):
        result = result(board, actions[i])
        if not terminal(result):
            player = player(result)
            if player == "O":
                tmp = min_max(result)
            else:
                tmp = max_min(result)
        else:
            tmp = utility(result) 
        if tmp > score:
            score = tmp
    return score

def min_max(board):
    if terminal(board):
        return False
    score = 9999
    actions = actions(board)
    for i in range(len(actions)):
        result = result(board, actions[i])
        if not terminal(result):
            player = player(result)
            if player == "O":
                tmp = min_max(result)
            else:
                tmp = max_min(result)
        else:
            tmp = utility(result) 
        if tmp < score:
            score = tmp
    return score



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    scores = {}
    optimal = (0,0)
    actions = actions(board)
    player = player(board)
    if player == "O":
        tmp = 9999
        for action in actions:
            scores[action] = min_max(result)
            if scores[action] <tmp:
                tmp = scores[action]
                optimal = action
    else:
        tmp = -9999
        for action in actions:
            scores[action] = max_min(result)
            if scores[action] >tmp:
                tmp = scores[action]
                optimal = action
    return optimal