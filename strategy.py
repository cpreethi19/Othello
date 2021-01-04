#Jan 12, 0952 version 

import random
import math

#### Othello Shell
#### P. White 2016-2018


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'

# To refer to neighbor squares we can add a direction to a square.
N,S,E,W = -10, 10, 1, -1
NE, SE, NW, SW = N+E, S+E, N+W, S+W
DIRECTIONS = (N,NE,E,SE,S,SW,W,NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}
OPPONENT={BLACK: WHITE, WHITE: BLACK}
WEIGHTS = [0,   0,   0,  0,  0,  0,  0,   0,   0, 0,
           0, 150, -50, 20,  5,  5, 20, -30, 150, 0,
           0, -30, -40, -5, -5, -5, -5, -40, -30, 0,
           0,  20,  -5, 15,  3,  3, 15,  -5,  20, 0,
           0,   5,  -5,  3,  3,  3,  3,  -5,   5, 0,
           0,   5,  -5,  3,  3,  3,  3,  -5,   5, 0,
           0,  20,  -5, 15,  3,  3, 15,  -5,  20, 0,
           0, -30, -40, -5, -5, -5, -5, -40, -30, 0,
           0, 150, -30, 20,  5,  5, 20, -30, 150, 0,
           0,   0,   0,  0,  0,  0,  0,   0,   0, 0,]
"""WEIGHTS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 10,-5, 3, 3, 3, 3,-5, 10, 0,
           0,-5,-8,-1,-1,-1,-1,-8,-5, 0,
           0, 3,-1, 1, 0, 0, 1,-1, 3, 0,
           0, 3,-1, 0, 1, 1, 0,-1, 3, 0,
           0, 3,-1, 0, 1, 1, 0,-1, 3, 0,
           0, 3,-1, 1, 0, 0, 1,-1, 3, 0,
           0,-5,-8,-1,-1,-1,-1,-8,-5, 0,
           0, 10,-5, 3, 3, 3, 3,-5, 10, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]"""
WEIGHTSUM = 0
for num in WEIGHTS:
    WEIGHTSUM+=num

########## ########## ########## ########## ########## ##########
# The strategy class for your AI
# You must implement this class
# and the method best_strategy
# Do not tamper with the init method's parameters, or best_strategy's parameters
# But you can change anything inside this you want otherwise
#############################################################
class Node():
    def __init__(self, board_string, move, board_score):
        self.board = board_string
        self.score = board_score
        self.last_move = move

class Strategy():

    def __init__(self):
        pass

    def get_starting_board(self):
        """Create a new board with the initial black and white positions filled."""
        string = OUTER*10+"?........?"*3+"?...o@...?"+"?...@o...?"+"?........?"*3+OUTER*10
        return string

    def get_pretty_board(self, board):
        """Get a string representation of the board."""
        str = ""
        index = 0
        while index<100:
            str += board[index:index+10]+"\n"
            index+=10
        return str

    def opponent(self, player):
        """Get player's opponent."""
        return OPPONENT[player]
        pass

    def find_bracket(self, board, player, square, direction):
        """
        Find a square that forms a match with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.

        Assumes that 'square' is a blank. Direction is one of the eight valid
        directions. Return the index of a square in 'player''s color
        so that there is a string of opponent pieces in between.
        """
        temp = square + direction
        while board[temp] == OPPONENT[player]:
            if temp < 0: return False
            if board[temp + direction] == player:
                return True
            temp+=direction
        return False

    def is_move_valid(self, board, player, move):
        """Is this a legal move for the player?"""
        moves = []
        for d in DIRECTIONS:
            if self.find_bracket(board, player, move, d):
                moves.append(d)
                continue
            """temp = move+d
            while board[temp]==OPPONENT[player]:
                if board[temp+d]==player:
                    moves.append(d)
                    break
                temp+=d"""
        return moves

    def get_valid_moves(self, board, player):
        """Get a list of all legal moves for player."""
        moves = []
        for index in range(100):
            if board[index]==EMPTY:
                moves_list = self.is_move_valid(board, player, index)
                if len(moves_list)!=0:
                    moves.append(index)
        return moves

    def has_any_valid_moves(self, board, player):
        """Can player make any moves?"""
        moves = self.get_valid_moves(board, player)
        if len(moves)==0: return False
        return True

    def make_move(self, board, player, move):
        """Update the board to reflect the move by the specified player."""
        # returns a new board/string
        moves = self.is_move_valid(board, player, move)
        list_temp = list(board)
        list_temp[move] = player
        for d in moves:
            current = move
            while list_temp[current+d]==self.opponent(player):
                list_temp[current+d] = player
                current+=d
        return "".join(list_temp)
    
    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if EMPTY in board:
            opp = self.opponent(prev_player)
            moves_player = self.get_valid_moves(board, prev_player)
            moves_opp = self.get_valid_moves(board, opp)
            if len(moves_opp)!=0:return opp
            elif len(moves_player)!=0: return prev_player
        return None

    def weighted_heuristic(self, board):
        white_weights = 0
        black_weights = 0
        for index in range(len(board)):
            if board[index] == BLACK:
                black_weights+=WEIGHTS[index]
            if board[index] == WHITE:
                white_weights += WEIGHTS[index]
        sum = abs(black_weights)+abs(white_weights)
        return black_weights-white_weights, sum

    def mobility_heuristic(self, board):
        black_moves = len(self.get_valid_moves(board, BLACK))
        white_moves = len(self.get_valid_moves(board, WHITE))
        return black_moves-white_moves

    def frontier_heuristic(self, board):
        black_frontier = 0
        white_frontier = 0
        for index in range(len(board)):
            if board[index]==BLACK:
                val = 0
                for d in DIRECTIONS:
                    if board[index+d]==EMPTY: val = -1
                black_frontier+=val
            if board[index]==WHITE:
                val = 0
                for d in DIRECTIONS:
                    if board[index+d]==EMPTY: val = -1
                white_frontier+=val
        return black_frontier-white_frontier

    def corners(self, board, player):
        if board[11]==player or board[18]==player or board[81]==player or board[88]==player: return 120
        else: return 0

    def score(self, board, player=BLACK):
        """Compute player's score (number of player's pieces minus opponent's)."""
        own = 0
        opp = 0
        for char in board:
            if char == BLACK: own+=1
            if char == WHITE: opp+=1
        return own-opp

    def minmax_score(self, board, player=BLACK):
        s1, s2 = self.weighted_heuristic(board)
        s = s1 / (s2+2)
        m = self.mobility_heuristic(board)
        f = self.frontier_heuristic(board)
        c = board.count(player) - board.count(OPPONENT[player])
        r = random.random()
        """if board.count(EMPTY)>54: return m+50+random.random()
        elif board.count(EMPTY)>12: return 4*s+f+m-2*c+50+self.corners(board, player)+random.random()
        else: return c+400+random.random()"""
        return board.count(EMPTY)*(m)/5+11*s-5*c+random.random()
        #else: return 10*c+s+random.random()

    def game_over(self, board, player):
        """Return true if player and opponent have no valid moves"""
        pass

    ### Monitoring players

    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    ################ strategies #################

    def minmax_search(self, node, player, depth):
        # determine best move for player recursively
        # it may return a move, or a search node, depending on your design
        # feel free to adjust the parameters
        best = {BLACK: max, WHITE: min}
        board = node.board
        if depth == 0:
            node.score = self.minmax_score(board, player)
            return node
        my_moves = self.get_valid_moves(board, player)
        #print(my_moves)
        children = []
        for move in my_moves:
            next_board = self.make_move(board, player, move)
            next_player = self.next_player(next_board, player)
            if next_player is None:
                s = 1000 * self.minmax_score(next_board)
                c = Node(next_board, move, s)
                children.append(c)
            else:
                c = Node(next_board, move, 0)
                c.score = self.minmax_search(c, next_player, depth - 1).score
            children.append(c)
        winner = best[player](children, key=lambda x: x.score)
        node.score = winner.score
        return winner

    def alphabeta(self, node, player, depth, alpha, beta):
        # determine best move for player recursively
        # it may return a move, or a search node, depending on your design
        # feel free to adjust the parameters
        best = {BLACK: max, WHITE: min}
        board = node.board
        if depth == 0:
            node.score = self.minmax_score(board, player)
            return node
        my_moves = self.get_valid_moves(board, player)
        #print(my_moves)
        children = []
        for move in my_moves:
            next_board = self.make_move(board, player, move)
            next_player = self.next_player(next_board, player)
            cur_score = 0
            if next_player is None:
                cur_score = 100000 * self.minmax_score(next_board)
                c = Node(next_board, move, cur_score)
                children.append(c)
            else:
                c = Node(next_board, move, 0)
                c.score = self.alphabeta(c, next_player, depth - 1, alpha, beta).score
                cur_score = c.score
                children.append(c)
            if player==BLACK: alpha = max(cur_score, alpha)
            if player==WHITE: beta = min(cur_score, beta)
            if alpha >= beta: break
        winner = best[player](children, key=lambda x: x.score)
        node.score = winner.score
        return winner

    def minmax_strategy(self, board, player):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        node = Node(board, None, 0)
        next_node = self.minmax_search(node, player, 3)
        return next_node.last_move

    def alphabeta_strategy(self, board, player):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        node = Node(board, None, 0)
        next_node = self.alphabeta(node, player, 3, -1*(math.inf), math.inf)
        return next_node.last_move

    def random_strategy(self, board, player):
        moves = self.get_valid_moves(board, player)
        return random.choice(moves)

    def best_strategy(self, board, player, best_move, still_running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        depth = 1
        while(True):
            ## doing random in a loop is pointless but it's just an example
            best_move.value = self.alphabeta_strategy(board, player)
            depth += 1

    def hardcode_strategy(self, board, player):
        moves = self.get_valid_moves(board, player)
        next_move = random.choice(moves)
        dirs = self.is_move_valid(board, player, next_move)
        bad_move = [12, 21, 22, 17, 28, 27, 71, 72, 82, 87, 77, 76]
        if 11 in moves:
            return 11
        elif 18 in moves:
            return 18
        elif 81 in moves:
            return 81
        elif 88 in moves:
            return 88
        if next_move in bad_move and (11 in moves or 18 in moves or 81 in moves or 88 in moves):
            next_move = random.choice(moves)
        return next_move

    #standard_strategy = minmax_strategy


###############################################
# The main game-playing code
# You can probably run this without modification
################################################
import time
from multiprocessing import Value, Process
import os, signal
silent = False


#################################################
# StandardPlayer runs a single game
# it calls Strategy.standard_strategy(board, player)
#################################################
class StandardPlayer():
    def __init__(self):
        pass

    def play(self):
        ### create 2 opponent objects and one referee to play the game
        ### these could all be from separate files
        ref = Strategy()
        black = Strategy()
        white = Strategy()

        print("Playing Standard Game")
        board = ref.get_starting_board()
        player = BLACK
        strategy = {BLACK: black.alphabeta_strategy, WHITE: white.random_strategy}
        print(ref.get_pretty_board(board))
        self.node = Node(board, None, None)
        while player is not None:
            move = strategy[player](board, player)
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
            print(ref.get_pretty_board(board))
            #input()
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board)>0 else "White"))



#################################################
# ParallelPlayer simulated tournament play
# With parallel processes and time limits
# this may not work on Windows, because, Windows is lame
# This calls Strategy.best_strategy(board, player, best_shared, running)
##################################################
class ParallelPlayer():

    def __init__(self, time_limit = 5):
        self.black = Strategy()
        self.white = Strategy()
        self.time_limit = time_limit

    def play(self):
        ref = Strategy()
        print("play")
        board = ref.get_starting_board()
        player = BLACK

        print("Playing Parallel Game")
        strategy = lambda who: self.black.best_strategy if who == BLACK else self.white.best_strategy
        while player is not None:
            best_shared = Value("i", -99)
            best_shared.value = -99
            running = Value("i", 1)

            p = Process(target=strategy(player), args=(board, player, best_shared, running))
            # start the subprocess
            t1 = time.time()
            p.start()
            # run the subprocess for time_limit
            p.join(self.time_limit)
            # warn that we're about to stop and wait
            running.value = 0
            time.sleep(0.01)
            # kill the process
            p.terminate()
            time.sleep(0.01)
            # really REALLY kill the process
            if p.is_alive(): os.kill(p.pid, signal.SIGKILL)
            # see the best move it found
            move = best_shared.value
            if not silent: print("move = %i , time = %4.2f" % (move, time.time() - t1))
            if not silent:print(board, ref.get_valid_moves(board, player))
            # make the move
            board = ref.make_move(board, player, move)
            if not silent: print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))

if __name__ == "__main__":
    # game =  ParallelPlayer(0.1)
    game = StandardPlayer()
    game.play()
