import random
import math
from collections import deque

opponent = {'X':'O', 'O':'X'}
state = input("Input the board: ")
EMPTY, BLACK, WHITE, OUTER = '.', 'X', 'O', '?'
E,W = 1, -1
DIRECTIONS = (E, W)
STABLE = []
for x in range(len(state)):
    if state[x]!='?' and state[x]!=EMPTY:
       STABLE.append(x)

def is_move_valid(board, player, move):
    """Is this a legal move for the player?"""
    moves = []
    for d in DIRECTIONS:
        temp = move
        curr = temp+d
        while[curr] == opponent[player]:
            if board[temp+d]==player:
                moves.append(d)
            curr += d
    return moves


def get_valid_moves(board):
    """Get a list of all legal moves for player."""
    moves = []
    for index in range(len(board)):
        if board[index] == EMPTY:
            moves.append(index)
    return moves

def make_move(board, player, move):
    """Update the board to reflect the move by the specified player."""
    # returns a new board/string
    moves = is_move_valid(board, player, move)
    list_temp = list(board)
    list_temp[move] = player
    for d in moves:
        current = move + d
        while list_temp[current] == opponent[player]:
            list_temp[current] = player
            STABLE.remove(current)
            current += d
    return "".join(list_temp)

def getChildren(state, player, moves):
    children = []
    for index in moves:
        next_state = make_move(state, player, index)
        children.append(next_state)
    return children

def bfs(state, player):
    q = deque()
    q.append(state)
    s = set()
    while len(q) != 0:
        n = q.popleft()
        s.add(n)
        moves = get_valid_moves(n)
        children = getChildren(n, player, moves)
        for new_state in children:
            s.add(new_state)
    return s

state_list = list(state)
black_set = bfs(state, BLACK)
white_set = bfs(state, WHITE)
print(STABLE)