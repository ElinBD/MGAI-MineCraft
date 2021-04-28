import utilityFunctions as utilityFunctions
from pymclevel import biome_types
import random
import math

# Information visible in mcedit, can be used for user-input
inputs = (
	("Canal House Generator", "label"),
	("Creator: Koen", "label"),
    ("length (x)", (8, 0, 128)),
    ("height (y)", (4, 0, 128)),
    ("length (z)", (6, 0, 128)),
    ("offset (x)", (0, -256, 256)),
    ("offset (y)", (4, 0, 256)),
    ("offset (z)", (0, -256, 256)),
    ("door location (W=0, N=1, E=2, S=3)", (0, 0, 3)),
    ("number of floors", (2, 1, 5)),
    ("facade type (small stairs=0, large stairs=1, bell=2, flat=3)", (0, 0, 3))
)
'''
("Pick a block:", alphaMaterials.Grass),
("Replace Only:", True),
("", alphaMaterials.Stone)
'''

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

        y = base_y+height_y
        for z in range(base_z + length_z - 1, z_south, -1):
            utilityFunctions.setBlock(level, (67,3), x, y, z)
            y += 1

    y_r = base_y+height_y

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

    y_r = base_y+height_y
    for z in range(base_z + length_z - 1, z_south, -1):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, (4,0), base_x, y, z)
            utilityFunctions.setBlock(level, (4,0), base_x + length_x - 1, y, z)
        y_r += 1


def small_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    y = base_y+height_y+1
    for x in range(base_x, x_center):
        utilityFunctions.setBlock(level, (67,0), x, y, base_z)
        y += 1

    y = base_y+height_y+1
    for x in range(base_x + length_x - 1, x_west, -1):
        utilityFunctions.setBlock(level, (67,1), x, y, base_z)
        y += 1

def large_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    y_r = base_y+height_y+1
    for x in range(base_x, x_center):
        utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
        y_r += 1
    y_r = base_y+height_y+1
    for x in range(base_x + length_x - 1, x_west, -1):
        utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
        y_r += 1

    # utilityFunctions.setBlock(level, (4,0), x_center, y_r, base_z)

    if length_x%2 != 0: # Building has an uneven with. Random chance to place another block in the middle on top
        extra_top = random.randint(0, 1)
        if extra_top:
            utilityFunctions.setBlock(level, (4,0), x_center, y_r, base_z)

def clock_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    y = base_y+height_y+1
    facade_height = int(y + length_x*0.7)
    print "fac2"
    print y
    print facade_height
    # facade_height = int(y + length_x*0.75)
    side_parts = length_x // 3
    middle_part = (length_x // 3) + (length_x % 3)
    for x in range(side_parts, middle_part + side_parts):
        for y_r in range(y, facade_height):
            utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
        # utilityFunctions.setBlock(level, (44,0), x, y_r, base_z)
    utilityFunctions.setBlock(level, (67,0), side_parts, facade_height-1, base_z)
    utilityFunctions.setBlock(level, (67,1), length_x-side_parts-1, facade_height-1, base_z)

    print "Building facade 2"
    for x in range(side_parts, x_center):
        y = facade_height
        y_r = facade_height + (x-side_parts) * 0.5
        print "Coor"
        print x
        print y
        print y_r
        while y < y_r:
            if y_r-y > 0.5:
                utilityFunctions.setBlock(level, (4,0), x, y, base_z)
            else:
                # pass
                utilityFunctions.setBlock(level, (44,0), x, y, base_z)
            y += 1
        y_r += 0.5

    y_r = facade_height
    for x in range(length_x-side_parts-1, x_center-1, -1):
        y = facade_height
        y_r = facade_height + ((length_x-side_parts-1)-x) * 0.5
        print "Coor"
        print x
        print y
        print y_r
        while y < y_r:
            if y_r-y > 0.5:
                utilityFunctions.setBlock(level, (4,0), x, y, base_z)
            else:
                # pass
                utilityFunctions.setBlock(level, (44,0), x, y, base_z)
            y += 1
        y_r += 0.5

def facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z, facade_type):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    # Heightening the facade...
    for x in range(0, length_x):
        utilityFunctions.setBlock(level, (4,0), x, base_y+height_y, base_z)

    y_r = base_y+height_y
    for x in range(base_x, x_center):
        utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
        y_r += 1

    if length_x % 2 != 0:
        utilityFunctions.setBlock(level, (4,0), x_center, y_r-1, base_z)
        utilityFunctions.setBlock(level, (4,0), x_center, y_r, base_z)

    y_r = base_y+height_y
    for x in range(base_x + length_x - 1, x_west, -1):
        utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
        y_r += 1

    # Roof types. Roof type 0 is just doing nothing: small staircase facade.
    if facade_type == 0: # Small staircase facade
        small_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z)

    elif facade_type == 1: # Large staircase facade
        large_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z)

    elif facade_type == 2: # Lit. translation: clock/neck type facade
        small_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z) # Side of facade
        clock_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z) # Center of facade





def north_south_roof(level, box, length_x, height_y, length_z, base_x, base_y, base_z, facade_type):
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


def build_floor(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z, front_side, stair_loc, top_offset):
    wall_block = (20,0)
    #Walls of the house:
    x = base_x#z-directional wall
    for z in range(base_z + 1, base_z + length_z - 1):
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, wall_block, x, y, z)

    z = base_z
    for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, wall_block, x, y, z)

    #Other walls:
    x = base_x + length_x - 1#z-directional wall
    for z in range(base_z + 1, base_z + length_z - 1):
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, wall_block, x, y, z)

    z = base_z + length_z - 1
    for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, wall_block, x, y, z)

    #Corner Pillars:
    for y in range(base_y, base_y+height_y + top_offset):
         utilityFunctions.setBlock(level, (3,0), base_x, y, base_z)
         utilityFunctions.setBlock(level, (3,0), base_x, y, base_z + length_z - 1)
         utilityFunctions.setBlock(level, (3,0), base_x + length_x - 1, y, base_z)
         utilityFunctions.setBlock(level, (3,0), base_x + length_x - 1, y, base_z + length_z - 1)

    if stair_loc == 0:
        #stair on west side, grow to south side
        start_x = base_x + 1
        start_z = base_z + length_z - height_y - 2

        for i in range(height_y):
            utilityFunctions.setBlock(level, (67,2), start_x, base_y+i, start_z+i)
            if i < height_y - 1:
                utilityFunctions.setBlock(level, (67,7), start_x, base_y+i, start_z+i+1)
            else:#one extra floor block for more convenient walking
                utilityFunctions.setBlock(level, (1,0), start_x, base_y+i, start_z+i+1)

        y_ceiling = base_y + height_y - 1

        for z in range(base_z + 1, start_z):
            utilityFunctions.setBlock(level, (1,0), base_x + 1, y_ceiling, z)
        for x in range (base_x + 2, base_x + length_x - 1):
            for z in range(base_z + 1, base_z + length_z - 1):
                utilityFunctions.setBlock(level, (1,0), x, y_ceiling, z)
    #elif stair_loc == 1:
        #stair on north side grow to west side
    elif stair_loc == 2:
        #stair on east side grow to north side
        start_x = base_x + length_x - 2
        start_z = base_z + height_y + 1
        utilityFunctions.setBlock(level, (67,1), start_x, base_y, start_z)

        for i in range(height_y):
            utilityFunctions.setBlock(level, (67,3), start_x, base_y+i, start_z-i)
            if i < height_y - 1:
                utilityFunctions.setBlockIfEmpty(level, (67,6), start_x, base_y+i, start_z-i-1)
            else:#one extra floor block for more convenient walking
                utilityFunctions.setBlockIfEmpty(level, (1,0), start_x, base_y+i, start_z-i-1)

        y_ceiling = base_y + height_y - 1

        for z in range(start_z + 1, base_z + length_z - 1):
            utilityFunctions.setBlock(level, (1,0), base_x + length_x - 2, y_ceiling, z)
        for x in range (base_x + 1, base_x + length_x - 2):
            for z in range(base_z + 1, base_z + length_z - 1):
                utilityFunctions.setBlock(level, (1,0), x, y_ceiling, z)
    #else: #if stair_loc == 3:
        #stair on south side grow to east side

# Start of the Generation script
#  @ level: Minecraft world
#  @ box: selected box by mcedit
#  @ options: user defined inputs from mcedit
def build_house(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z, door_loc, no_floors, facade_type):
    #Walls:
    temp_base_y = base_y
    stair_loc = 0
    for i in range(no_floors):
        if i == no_floors - 1:
            build_floor(level, box, options, length_x, height_y, length_z, base_x, temp_base_y, base_z, 1, stair_loc, 1)
        else:
            build_floor(level, box, options, length_x, height_y, length_z, base_x, temp_base_y, base_z, 1, stair_loc, 0)
        stair_loc += 2
        stair_loc %= 4
        temp_base_y += height_y
    temp_base_y -= height_y - 1

    #floor:
    for x in range (base_x + 1, base_x + length_x - 1):
        for z in range(base_z + 1, base_z + length_z - 1):
            utilityFunctions.setBlock(level, (1,0), x, base_y-1, z)

    #doors and windows:
    #x_door = random.randint(0, 1)
    #door_x = 0
    #door_z = 0

    door_loc = 1

    if door_loc % 2 == 0:
        #door in E/W section
        east_west_roof(level, box, options, length_x, height_y, length_z, base_x, temp_base_y, base_z)
        door_z = random.randint(base_z + 2, base_z + length_z - 2)
        door_x = base_x if door_loc == 0 else base_x + length_x - 1

    else:
        #door in N/S section
        north_south_roof(level, box, length_x, height_y, length_z, base_x, temp_base_y, base_z, facade_type)
        facade(level, box, length_x, height_y, length_z, base_x, temp_base_y, base_z, facade_type) # TODO: maybe should return the total height of the building, so we can place windows accordingly in the facade front
        # windows(level, box, length_x, height_y, length_z, base_x, temp_base_y, base_z, facade_type)
        door_x = random.randint(base_x + 2, base_x+length_x - 2)
        door_z = base_z if door_loc == 1 else base_z + length_z - 1

    #floor block underneeth door:
    utilityFunctions.setBlock(level, (1,0), door_x, base_y - 1, door_z)

    #clear blocks for the door:
    utilityFunctions.setBlock(level, (0,0), door_x, base_y, door_z)
    utilityFunctions.setBlock(level, (0,0), door_x, base_y + 1, door_z)

    #setBlock(x, y, z,"acacia_door")
    #place actual door:
    # "acacia_door"
    #utilityFunctions.setBlock(level, ("acacia_door", door_loc), door_x, base_y, door_z)
    #utilityFunctions.setBlock(level, "acacia_door[half=upper]", door_x, base_y, door_z)

    utilityFunctions.setBlock(level, (71, door_loc), door_x, base_y, door_z)
    #utilityFunctions.setBlock(level, (71, door_loc)[half=upper], door_x, base_y+1, door_z)

    #north_south_roof(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z)


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




def perform(level, box, options):
    #'''
    height_y = options["height (y)"]
    length_z = options["length (z)"]
    length_x = options["length (x)"]
    base_x = options["offset (x)"]
    base_y = options["offset (y)"]
    base_z = options["offset (z)"]
    door_loc = options["door location (W=0, N=1, E=2, S=3)"]
    no_floors = options["number of floors"]
    facade_type = options["facade type (small stairs=0, large stairs=1, bell=2, flat=3)"]
    #'''

    #build_floor(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z, 1, 2)
    build_house(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z, door_loc, no_floors, facade_type)

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
