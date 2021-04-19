import utilityFunctions as utilityFunctions
from pymclevel import biome_types
import random

# Information visible in mcedit, can be used for user-input
inputs = (
	("Settlement Generator", "label"),
	("Creators: Koen & Sem", "label")
	)

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


# Start of the Generation script
#  @ level: Minecraft world
#  @ box: selected box by mcedit
#  @ options: user defined inputs from mcedit
def perform(level, box, options):
	width_x = random.choice([5,7,9])

	if width_x == 5:
		center_x = 3
		depth_z = random.randint(6,10)
		height_y = random.randint(6,10)
		door_y = random.randint(0, 1)
	elif width_x == 7:
		center_x = 4
		depth_z = random.randint(6,14)
		height_y = random.randint(9,14)
		door_y = random.randint(0, 2)
	elif width_x == 9:
		center_x = 5
		depth_z = random.randint(6,18)
		height_y = random.randint(9,16)
		door_y = random.randint(0, 3)
	else: # Should never happen
		center_x = width_x // 2
		depth_z = 14
		height_y = 14
		door_y = 0

    base_x = 0
    base_y = 0
    base_z = 0

    #Walls of the house:
    for x in range (base_x, base_x+1):#z-directional wall
        for y in range(base_y, base_y+height_y):
            for z in range(base_z+1, base_z+depth_z):
                utilityFunctions.setBlock(level, (4,0), x, y, z)

    for x in range (base_x+1, base_x+width_x):#x-directional wall
        for y in range(base_y, base_y+height_y):
            for z in range(base_z, base_z+1):
                utilityFunctions.setBlock(level, (4,0), x, y, z)

    #other walls:
    for x in range (base_x+width_x, base_x+1+width_x):#z-directional wall
        for y in range(base_y, base_y+height_y):
            for z in range(base_z+1, base_z+depth_z):
                utilityFunctions.setBlock(level, (4,0), x, y, z)

    for x in range (base_x+1, base_x+width_x):#x-directional wall
        for y in range(base_y, base_y+height_y):
            for z in range(base_z+depth_z, base_z+1+depth_z):
                utilityFunctions.setBlock(level, (4,0), x, y, z)

    #Corner Pillars:
    for y in range(base_y, base_y+height_y):
         utilityFunctions.setBlock(level, (3,0), base_x, y, base_z)
         utilityFunctions.setBlock(level, (3,0), base_x, y, base_z+depth_z)
         utilityFunctions.setBlock(level, (3,0), base_x+width_x, y, base_z)
         utilityFunctions.setBlock(level, (3,0), base_x+width_x, y, base_z+depth_z)

    #floor:
    for x in range (base_x+1, base_x+width_x):
        for z in range(base_z+1, base_z+depth_z):
            utilityFunctions.setBlock(level, (1,0), x, base_y-1, z)

    #doors and windows:
    door_x = random.randint(1, width_x-1, 2) # Door can be placed left, right, middle, etc.
	if door_x != 1 or door_x != width_x-1: # Door is not leftmost or rightmost, so keep door at ground level after all
		door_y = 0

	door_z = base_z

	utilityFunctions.setBlock(level, (64,0), door_x, door_y, door_z)

	for i in range(base_y, door_y):
		utilityFunctions.setBlock(level, (4,0), door_x, i, door_z-1)

	if door_x <= width_x/2: # Door is on left side of the house, so stairs should go to the right
		placeStairsRight(door_x, door_y, door_z, base_y)
	elif door_x >= width_x/2: # Door is on right side of the house, so stairs should go to the left
		placeStairsLeft(door_x, door_y, door_z, base_y)
	else: # Door is in the middle of the house, so stairs should to left and right
		placeStairsLeft(door_x, door_y, door_z, base_y)
		placeStairsRight(door_x, door_y, door_z, base_y)

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
