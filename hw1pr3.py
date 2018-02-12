import numpy as np
import random
# random.seed(4)
MAX_DEPTH = 0

def opposite(_in):
    if _in == 'u':
        return 'd'
    elif _in == 'd':
        return 'u'
    elif _in == 'l':
        return 'r'
    elif _in == 'r':
        return 'l'
    else:
        print("\nError, bad arg to opposite()\n")
        return '?'

class Board:
    def __init__ (self, _state):
        self.state = _state
        self.last_move = '?'
        self.score = -1

    #shuffle the tiles
    def randomize(self):
        self.state = [[-1,-1,-1], [-1, -1, -1], [-1, -1, -1]]
        #arrange the sample from 1-8 in a random order
        order = random.sample(range(9), 9)
        i = 0
        x = 0
        y = 0

        #filter these into the board one at a time
        while y < 3:
            while x < 3:
                self.state[x][y] = order[i]
                x += 1
                i += 1
            x = 0
            y += 1

    # scores the current board state and stores in in score
    def evaluate_score(self):
        #index for the correct location of each tile
        CORRECT_LOCATIONS = []
        x = 0
        y = 0
        #generate CORRECT_LOCATIONS
        while y < 3:
            while x < 3:
                CORRECT_LOCATIONS.append([x,y])
                x += 1
            x = 0
            y += 1

        _score = 0
        i = 1
        y = 0
        found = False

        #find each tile and determine its distance from its home
        while (i < 9):
            while (y < 3):
                try:
                    # print ("%s: %s, %s" % (i, y, self.state[y].index(i)))
                    self.state[y].index(i)
                    found = True
                except:
                    i += 0

                if found:
                    x = self.state[y].index(i)
                    _score += abs(y-CORRECT_LOCATIONS[i-1][1])
                    _score += abs(x-CORRECT_LOCATIONS[i-1][0])
                    # print("Correct location of %s is %s, but found it at %s" % (i, CORRECT_LOCATIONS[i-1], [x,y]))
                    # print("Score %s" % score)
                    i += 1
                found = False
                y += 1
            y = 0

        #update score
        self.score = _score
        return _score

    # returns a list of possible children for a given board state
    def find_possible_children(self):
        # self.state = [[1,2,3],[4,0,5],[6,7,8]]
        #start with all moves possible
        up = True
        down = True
        left = True
        right = True
        #remove the possibility of undoing the last move
        if (self.last_move != '?'):
            opp = opposite(self.last_move)
            if (opp == 'u'):
                up = False
            elif (opp == 'd'):
                down = False
            elif (opp == 'l'):
                left = False
            elif (opp == 'r'):
                right = False

        #find the blank tile
        blank_x = 0
        blank_y = 0

        for y in range(3):
            for x in range(3):
                if self.state[y][x] == 0:
                    blank_x = x
                    blank_y = y

        #get rid of impossible choices
        if blank_x == 0:
            right = False
        elif blank_x == 2:
            left = False

        if blank_y == 0:
            down = False
        elif blank_y == 2:
            up = False

        possible_children = []
        if up:
            possible_children += ['u']
        if down:
            possible_children += ['d']
        if left:
            possible_children += ['l']
        if right:
            possible_children += ['r']

        return possible_children

    #takes arg u d l r and moves the tile into the correct pos
    def move(self, direction):
        #find the blank tile
        blank_x = 0
        blank_y = 0

        for y in range(3):
            for x in range(3):
                if self.state[x][y] == 0:
                    blank_y = y
                    blank_x = x

        target_x = blank_y
        target_y = blank_x

        # print("Old x: %s old y: %s" % (target_x,target_y))
        #
        # print("moving: %s" % direction)
        #find our target tile adjacent to the blank space
        if direction=='u':
            target_y += 1
        elif direction == 'd':
            target_y -= 1
        elif direction == 'l':
            target_x += 1
        elif direction == 'r':
            target_x -= 1
        else:
            print("Error, move received invalid value %s" %direction)

        # print("New x: %s and new y: %s" % (target_x,target_y))
        # swap them
        # print(self.state[target_y][target_x])
        self.state[blank_x][blank_y] = self.state[target_y][target_x]
        self.state[target_y][target_x] = 0

        self.last_move = direction

    def print_special(self):
        print (self.evaluate_score())
        for i in self.state:
            print(i)

        print('\n')

class Node:
    def __init__ (self, _state, _depth):
        self.board = Board(_state)
        self.depth = _depth
        self.children = []
        self.move_queue = []

    def build_children(self):
        if (self.depth > MAX_DEPTH):
            return

        kids = self.board.find_possible_children()
        for i in kids:
            child_board = Board(self.board.state)
            child_board.move(i)
            child_node = Node(child_board.state, self.depth+1)
            new_queue = self.move_queue + [i]
            child_node.move_queue = new_queue
            # child_node.board.evaluate_score()
            if (self.depth < MAX_DEPTH):
                child_node.build_children()

            self.children += [child_node]
            if (self.depth == MAX_DEPTH):
                print("%s, leading to a score of %s and a state of:" % (new_queue, child_node.board.score))
                child_board.print_special()
            else:
                print("Depth: %s" % self.depth)

thing = np.zeros((3,3))
x = Node(thing, 0)
x.board.randomize()
x.board.print_special()
print("Options:")
x.build_children()
while True:
    move = input("Which dir?")
    x.board.move(move)
    x.board.print_special()
    print("Options:")
    x.build_children()
