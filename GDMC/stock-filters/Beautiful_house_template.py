import utilityFunctions as utilityFunctions
from pymclevel import biome_types
import random

# Information visible in mcedit, can be used for user-input
inputs = (
	("Settlement Generator", "label"),
	("Creators: me", "label")
	)
#TODO test below:
def placeStairsLeft(door_x, door_y, door_z, ground_y):
	stair_y = door_y
	stair_x = door_x
	stair_z = door_z
	while stair_y > ground_y:
		stair_y -= 1
		stair_x -= 1
		for i in range(base_y, stair_y):
			utilityFunctions.setBlock(level, (4,0), stair_x, i, stair_z-1)

		utilityFunctions.setBlock(level, (67,0), stair_x, stair_y, stair_z-1)



def placeStairsRight(door_x, door_y, door_z, ground_y):
	stair_y = door_y
	stair_x = door_x
	stair_z = door_z
	while stair_y > ground_y:
		stair_y -= 1
		stair_x += 1
		for i in range(base_y, stair_y):
			utilityFunctions.setBlock(level, (4,0), stair_x, i, stair_z-1)

		utilityFunctions.setBlock(level, (67,0), stair_x, stair_y, stair_z-1)
#TODO test above:

def east_west_roof(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z):
    z_center = base_z + length_z/2
    z_south = z_center - 1 if length_z % 2 == 0 else z_center
    for x in range(base_x, base_x + length_x):
        y = base_y+height_y
        for z in range(base_z, z_center):
            utilityFunctions.setBlock(level, (67,2), x, y, z)
            y += 1
        adjust = 0
        if length_z % 2 != 0:
            adjust = 1
            utilityFunctions.setBlock(level, (4,0), x, y - 1, z_center)
            #z_center = base_z + length_z/2 + 1

        y = base_y+height_y
        for z in range(base_z + length_z - 1, z_south, -1):
            utilityFunctions.setBlock(level, (67,3), x, y, z)
            y += 1
    
    y_r = base_y+height_y
    #'''
    for z in range(base_z, z_center):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, (4,0), base_x, y, z)
            utilityFunctions.setBlock(level, (4,0), base_x + length_x - 1, y, z)
        y_r += 1
    adjust = 0
    if length_z % 2 != 0:
        adjust = 1
        for y in range(base_y+height_y, y_r - 1):
            utilityFunctions.setBlock(level, (4,0), base_x, y, z_center)
            utilityFunctions.setBlock(level, (4,0), base_x + length_x - 1, y, z_center)
        # z_center = base_z + length_z/2 + 1

    y_r = base_y+height_y
    for z in range(base_z + length_z - 1, z_south, -1):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, (4,0), base_x, y, z)
            utilityFunctions.setBlock(level, (4,0), base_x + length_x - 1, y, z)
        y_r += 1
    #'''

def north_south_roof(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    for z in range(base_z, base_z + length_z):
        y = base_y+height_y
        for x in range(base_x, x_center):
            utilityFunctions.setBlock(level, (67,0), x, y, z)
            y += 1
        adjust = 0
        if length_x % 2 != 0:
            adjust = 1
            utilityFunctions.setBlock(level, (4,0), x_center, y - 1, z)

        y = base_y+height_y
        for x in range(base_x + length_x - 1, x_west, -1):
            utilityFunctions.setBlock(level, (67,1), x, y, z)
            y += 1
    
    y_r = base_y+height_y
    for x in range(base_x, x_center):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, (4,0), x, y, base_z)
            utilityFunctions.setBlock(level, (4,0), x, y, base_z + length_z - 1)
        y_r += 1
    adjust = 0
    if length_x % 2 != 0:
        adjust = 1
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, (4,0), x_center, y, base_z)
            utilityFunctions.setBlock(level, (4,0), x_center, y, base_z + length_z - 1)

    y_r = base_y+height_y
    for x in range(base_x + length_x - 1, x_west, -1):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, (4,0), x, y, base_z)
            utilityFunctions.setBlock(level, (4,0), x, y, base_z + length_z - 1)
        y_r += 1

    

# Start of the Generation script
#  @ level: Minecraft world
#  @ box: selected box by mcedit
#  @ options: user defined inputs from mcedit
def perform(level, box, options):
    height_y = 4
    length_z = 7
    length_x = 9
    base_x = 0
    base_y = 4
    base_z = 0

    #Walls of the house:
    x = base_x#z-directional wall
    for z in range(base_z + 1, base_z + length_z - 1):
        for y in range(base_y, base_y + height_y):
            utilityFunctions.setBlock(level, (4,0), x, y, z)

    z = base_z
    for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
        for y in range(base_y, base_y + height_y):
            utilityFunctions.setBlock(level, (4,0), x, y, z)

    #other walls:
    x = base_x + length_x - 1#z-directional wall
    for z in range(base_z + 1, base_z + length_z - 1):
        for y in range(base_y, base_y + height_y):
            utilityFunctions.setBlock(level, (4,0), x, y, z)

    z = base_z + length_z - 1
    for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
        for y in range(base_y, base_y + height_y):
            utilityFunctions.setBlock(level, (4,0), x, y, z)

    #Corner Pillars:
    
    for y in range(base_y, base_y+height_y):
         utilityFunctions.setBlock(level, (3,0), base_x, y, base_z)
         utilityFunctions.setBlock(level, (3,0), base_x, y, base_z + length_z - 1)
         utilityFunctions.setBlock(level, (3,0), base_x + length_x - 1, y, base_z)
         utilityFunctions.setBlock(level, (3,0), base_x + length_x - 1, y, base_z + length_z - 1)
    
    #floor:
    for x in range (base_x + 1, base_x + length_x - 1):
        for z in range(base_z + 1, base_z + length_z - 1):
            utilityFunctions.setBlock(level, (1,0), x, base_y-1, z)

    #doors and windows:
    x_door = random.randint(0, 1)
    #door_x = 0
    #door_z = 0
    if x_door == 1:
        #door in x section
        door_z = random.randint(base_z + 2, base_z + length_z - 2)
        door_x = random.randint(0, 1)
        if door_x == 0:
            door_x = base_x
        else:
            door_x = base_x + length_x - 1
    else:
        #door in z section
        door_x = random.randint(base_x + 2, base_x+length_x - 2)
        door_z = random.randint(0, 1)
        if door_z == 0:
            door_z = base_z
        else:
            door_z = base_z + length_z - 1
    
    #floor block underneeth door:
    utilityFunctions.setBlock(level, (1,0), door_x, base_y - 1, door_z)

    #clear blocks for the door:
    utilityFunctions.setBlock(level, (0,0), door_x, base_y, door_z)
    utilityFunctions.setBlock(level, (0,0), door_x, base_y + 1, door_z)
    
    #place actual door:
    utilityFunctions.setBlock(level, (71,0), door_x, base_y, door_z)
    utilityFunctions.setBlock(level, (71,7), door_x, base_y + 1, door_z)
    #utilityFunctions.setBlock(level, (71,0), door_x, base_y + 1, door_z)

    north_south_roof(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z)
    '''
    for i in range(base_y, door_y):
        utilityFunctions.setBlock(level, (4,0), door_x, i, door_z-1)

    if door_x <= width_x/2: # Door is on left side of the house, so stairs should go to the right
        placeStairsRight(door_x, door_y, door_z, base_y)
    elif door_x >= width_x/2: # Door is on right side of the house, so stairs should go to the left
        placeStairsLeft(door_x, door_y, door_z, base_y)
    else: # Door is in the middle of the house, so stairs should to left and right
        placeStairsLeft(door_x, door_y, door_z, base_y)
        placeStairsRight(door_x, door_y, door_z, base_y)
    '''
	#TODO: windows, roof and facade top (different styles)

	# while loop over windows: every 2 blocks, set as window if not door_x
	# potentially, we could change the height of the windows on ground floor for smaller houses
	# Also, we could generate houses with more width and windows of 2 meters wide
	# If you google for "grachtenpanden minecraft", you'll see some nice examples or inspiration
	# (or demotivation, wow those look nice... How do we even build such a thing?)

	# Roofs: a few different styles, I've written them down on a paper. Those are
	# a few basics. Again, look at "grachtenpanden minecraft for some inspiration".
	# A lot of stuff is done with slabs and stairs that have been rotated upside
	# down. How do we rotate in this program, anyway?

	# Roof: Just use the staircase builder, but wihout the 'meat' of the staircase,
	# that is, wihout the 'support'. Just use the stair blocks from minecraft. The
	# rear of the buildings can be staircases.


    # #door_x = 0
    # #door_z = 0
    # if x_door == 1:
    #     #door in x section
    #     door_z = random.randint(base_z+2, base_z+depth_z-2)
    #     door_x = random.randint(0, 1)
    #     if door_x == 0:
    #         door_x = base_x
    #     else:
    #         door_x = base_x+width_x
    # else:
    #     #door in z section
    #     door_x = random.randint(base_x+2, base_x+width_x-2)
    #     door_z = random.randint(0, 1)
    #     if door_z == 0:
    #         door_z = base_z
    #     else:
    #         door_z = base_z+depth_z
