import numpy as np

def generateRoom():
    array = np.ones((3,4), dtype=np.int16)
    return array

#check if we've gotten all the dirt out of the room
def isRoomClean(_room):
    for x in range(_room.shape[0]):
        for y in range(_room.shape[1]):
            if (_room[x][y] == 1):
                return False
    #if we've made it this far without returning, the room is clean
    return True

room = generateRoom()
currentX = 0
currentY = 0
last_direction = '0' #we haven't gone anywhere yet
next_move = 'e'
last_move = 'e'
state = "working"
maxX = room.shape[1]-1
maxY = room.shape[0]-1

#if the room is wide, go horizontally
#else go vertically
# if (room.shape[0] < room.shape[1]):
#     next_move = 'e'
#     last_move = 'e'
# else:
#     next_move = 's'
#     last_move = 's'

#main loop
while isRoomClean(room)==False:
    #if dirty, clean it
    if room[currentY, currentX] == 1 :
        #succ
        room [currentY, currentX] = 0
        print("succ")
    #otherwise we have to move
    else:
        #if we're going straight
        if state=="working":
            #moving east
            if (last_move == 'e'):
                #if we hit the east wall, turn
                if (currentX==maxX):
                    state = "turning"
                    currentY += 1
                    next_move = 'w'
                    last_move = 's'
                    print("wall, moved south")
                else: #keep going
                    currentX += 1
                    last_move = 'e'
                    print('headed east')
            elif last_move=='w':
                if currentX==0: #if we hit the west wall
                    state="turning"
                    currentY+=1
                    next_move = 'e'
                    print("wall, moved south")
                else: #keep going
                    currentX -= 1
                    last_move = 'w'
                    print('headed west')
        elif next_move == 'w':
            currentX -= 1
            next_move = '?'
            last_move = 'w'
            state = "working"
            print("turn completed")
        elif next_move == 'e':
            currentX += 1
            next_move = '?'
            last_move = 'e'
            state = "working"
            print("turn completed")
        #if we're turning
        #else if state=="turning":
        #    if (last_move == 's': #stopping here

    print(room)
    # input("press enter to continue")
