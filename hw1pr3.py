import numpy as np
import random
# random.seed(4)
MAX_DEPTH = 5
TOTAL_NODES = 0

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
        return '?'

class Board:
    def __init__ (self, _state):
        self.state = np.zeros((3,3))

        for i in range(3):
            for j in range(3):
                self.state[i][j] = _state[i][j]

        self.last_move = '?'
        self.score = -1

    #shuffle the tiles
    def randomize(self):
        self.state = [[1,2,3], [4, 5, 6], [7, 8, 0]]
        #arrange the sample from 1-8 in a random order
        order = []
        # amount = random.randint(50, 500)
        amount = 10
        last_choice = '?'
        for i in range(amount):
            choice = random.choice(['u','d','l','r'])
            while (choice == last_choice):
                choice = random.choice(['u','d','l','r'])

            order += [choice]
            last_choice = choice

        for i in order:
            self.move(i)

        print("Made %s random moves, attempting to solve..." % amount)


    # scores the current board state and stores in in score
    def evaluate_score(self):
        #index for the correct location of each tile
        CORRECT_LOCATIONS = []
        x = 0
        y = 0
        #generate CORRECT_LOCATIONS
        while y < 3:
            while x < 3:
                if not(x==2 and y==2):
                    CORRECT_LOCATIONS.append([x,y])
                x += 1
            x = 0
            y += 1
        _score = 0
        i = 1
        #find each tile and determine its distance from its home
        while (i < 9):
            y = 0
            while (y < 3):
                x = 0
                while (x < 3):
                    # if we found it
                    if (self.state[x][y] == i):
                        # add the total distance of each dimension to the score
                        _score += abs(y-CORRECT_LOCATIONS[i-1][0])
                        _score += abs(x-CORRECT_LOCATIONS[i-1][1])
                        # print("Correct location of %s is %s, but found it at %s" % (i, CORRECT_LOCATIONS[i-1], [y,x]))
                        # move to the next tile and reset the loop
                        i += 1
                        x = 3
                        y = 3
                    # if we didn't find it, check the next tile
                    else:
                        x += 1
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


        # print("Moving: %s" % direction)
        # print("New x: %s and new y: %s" % (target_x,target_y))
        # swap them
        # print(self.state[target_y][target_x])
        if (target_x > 2) or (target_x < 0):
            return
        elif (target_y > y) or (target_y < 0):
            return

        self.state[blank_x][blank_y] = self.state[target_y][target_x]
        self.state[target_y][target_x] = 0

        self.evaluate_score()
        self.last_move = direction

    def print_special(self):
        # print (self.score)
        for i in self.state:
            print(i)

class Node:
    def __init__ (self, _state, _depth):
        self.board = Board(_state)
        self.depth = _depth
        self.children = []
        self.move_queue = []

    def build_children(self):
        #stop at some point
        if (self.depth > MAX_DEPTH):
            return

        #each kid is just a possible combination of moves from the root
        kids = self.board.find_possible_children()

        #for every possible child
        for i in kids:
            #create a new board with the sequence of moves encoded
            child_board = Board(self.board.state)
            child_board.move(i)
            #create a new node using that board and update its vars
            child_node = Node(child_board.state, self.depth+1)
            new_queue = self.move_queue + [i]
            child_node.board.last_move = i
            child_node.move_queue = new_queue
            child_node.board.evaluate_score()
            self.children += [child_node]

            #if we're not too deep, build out its children
            #by recursively calling this function
            if (self.depth < MAX_DEPTH):
                child_node.build_children()

            # if (self.depth == MAX_DEPTH):
            #     print("%s, leading to a score of %s and a state of:" % (new_queue, child_node.board.score))
                # child_board.print_special()
            # else:
            #     print("Depth: %s" % self.depth)

    # returns a tuple of the score and the move_queue to get there
    def search_for_best_path(self):
        global TOTAL_NODES
        if (self.board.score == 0):
            return (self.board.score, self.move_queue)
        # pass it back up the tree
        if (self.depth > MAX_DEPTH):
            return (self.board.score, self.move_queue)

        # always declare your defaults
        best_path = (100, [])

        # take the minimum of all children
        for i in self.children:
            TOTAL_NODES += 1
            result = i.search_for_best_path()
            if result[0] < best_path[0]:
                best_path = result

        return best_path

total = 0
times = input("How many boards would you like to solve? (1 - 50 recommended)\n>")
for q in range(int(times)):
    thing = np.zeros((3,3))
    x = Node(thing, 0)
    x.board.randomize()
    x.board.evaluate_score()
    x.board.print_special()
    moves_taken = 0
    queue = []
    previous_score = 100
    while (x.board.score > 0):
        x.build_children()
        res = x.search_for_best_path()
        moves = res[1]
        if (res[0] == 0):
            for i in moves:
                x.board.move(i)
                moves_taken += 1
            # x.board.evaluate_score()
        else:
            x.move_queue = []
            for i in range(len(moves)):
                try:
                    x.move_queue += [moves[i]]
                except:
                    break

            for i in x.move_queue:
                x.board.move(i)
                moves_taken += 1

            x.move_queue = []
            x.children = []
            # x.board.evaluate_score()
            # print(x.board.score)
            if (res[0] >= x.board.score):
                # print ("Expanding search depth...")
                MAX_DEPTH += 1
    total += moves_taken
    print("Solved in %s moves \n" % moves_taken)

print("\nSolved %s boards" % times)
print("\nTotal moves: %s\nAverage: %s moves"%(total, total/int(times)))
print("\nTotal nodes expanded: %s\nAverage: %s nodes" % (TOTAL_NODES, TOTAL_NODES/int(times)))
# x.board.print_special()
# while True:
#     move = input("Which dir?")
#     x.board.move(move)
#     x.board.print_special()
#     print("Options:")
#     x.build_children()
