import utilityFunctions as utilityFunctions
from pymclevel import biome_types, schematic, MCSchematic, box as bx
from Beautiful_Pallete import Pallete
import random
import math

#from scematic import MCSchematic, extractSchematicFrom


# Information visible in mcedit, can be used for user-input
inputs = (
	("Canal House Generator", "label"),
	("Creator: Koen", "label"),
    ("length (x)", (7, 4, 128)),
    ("height (y)", (5, 3, 128)),
    ("length (z)", (12, 4, 128)),
    ("offset (x)", (0, -256, 256)),
    ("offset (y)", (4, 0, 256)),
    ("offset (z)", (0, -256, 256)),
    ("door location (N=0, W=1, S=2, E=3)", (0, 0, 3)),
    ("number of floors", (2, 1, 10)),
    ("facade type (small stairs=0, large stairs=1, bell=2, flat=3)", (0, 0, 3))
)


def small_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    y = base_y+height_y+1
    for x in range(base_x, x_center):
        utilityFunctions.setBlock(level, (pallete.quartz_stair,0), x, y, base_z)
        y += 1

    y = base_y+height_y+1
    for x in range(base_x + length_x - 1, x_west, -1):
        utilityFunctions.setBlock(level, (pallete.quartz_stair,1), x, y, base_z)
        y += 1

    if length_x % 2 != 0: # Building has an uneven with. Random chance to place another block in the middle on top
        extra_top = random.randint(0, 1)
        if extra_top:
            utilityFunctions.setBlock(level, pallete.quartz_slab, x_center, y, base_z)

def large_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    y_r = base_y+height_y+1
    for x in range(base_x, x_center):
        utilityFunctions.setBlock(level, pallete.wall, x, y_r, base_z)
        utilityFunctions.setBlock(level, pallete.quartz_slab, x, y_r+1, base_z)
        y_r += 1
    y_r = base_y+height_y+1
    for x in range(base_x + length_x - 1, x_west, -1):
        utilityFunctions.setBlock(level, pallete.wall, x, y_r, base_z)
        utilityFunctions.setBlock(level, pallete.quartz_slab, x, y_r+1, base_z)
        y_r += 1

    if length_x%2 != 0: # Building has an uneven with. Random chance to place another block in the middle on top
        extra_top = random.randint(0, 1)
        if extra_top:
            utilityFunctions.setBlock(level, pallete.wall, x_center, y_r, base_z)
            utilityFunctions.setBlock(level, pallete.quartz_slab, x_center, y_r+1, base_z)
        else:
            utilityFunctions.setBlock(level, pallete.quartz_slab, x_center, y_r, base_z)

def clock_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    y = base_y+height_y+1
    facade_height = int(y + length_x*0.7)
    side_parts = length_x // 3
    middle_part = (length_x // 3) + (length_x % 3)
    for x in range(side_parts, middle_part + side_parts):
        for y_r in range(y, facade_height):
            utilityFunctions.setBlock(level, pallete.wall, x, y_r, base_z)
    utilityFunctions.setBlock(level, (pallete.quartz_stair,0), side_parts, facade_height-1, base_z)
    utilityFunctions.setBlock(level, (pallete.quartz_stair,1), length_x-side_parts-1, facade_height-1, base_z)

    for x in range(side_parts, x_center):
        y = facade_height
        y_r = facade_height + (x-side_parts) * 0.5
        while y < y_r:
            if y_r-y > 0.5:
                utilityFunctions.setBlock(level, pallete.wall, x, y, base_z)
            else:
                utilityFunctions.setBlock(level, pallete.quartz_slab, x, y, base_z)
            y += 1
        y_r += 0.5

    y_r = facade_height
    for x in range(length_x-side_parts-1, x_center-1, -1):
        y = facade_height
        y_r = facade_height + ((length_x-side_parts-1)-x) * 0.5
        while y < y_r:
            if y_r-y > 0.5:
                utilityFunctions.setBlock(level, pallete.wall, x, y, base_z)
            else:
                utilityFunctions.setBlock(level, pallete.quartz_slab, x, y, base_z)
            y += 1
        y_r += 0.5

def facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z, facade_type):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    # Heightening the facade and replacing blocks with facade type...
    y_r = base_y+height_y+1
    for x in range(base_x, x_center):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.wall, x, y, base_z)
        y_r += 1

    if length_x % 2 != 0:
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.wall, x_center, y, base_z)

    y_r = base_y+height_y+1
    for x in range(base_x + length_x - 1, x_west, -1):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.wall, x, y, base_z)
        y_r += 1


    # Roof types. Roof type 0 is just doing nothing: small staircase facade.
    if facade_type == 0: # Small staircase facade
        small_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z)

    elif facade_type == 1: # Large staircase facade
        pass
        large_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z)

    elif facade_type == 2: # Lit. translation: clock/neck type facade
        small_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z) # Side of facade
        clock_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z) # Center of facade


def windows(level, box, length_x, height_y, length_z, base_x, temp_base_y, base_z, facade_type, door_x, base_y, no_floors, total_height): # This function currently assumes the building has an uneven width
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    window_max_height = height_y-3

    if height_y > 4:
        utilityFunctions.setBlock(level, (4,0), door_x, base_y+2, base_z) # Window above the door

    for i in range(base_x+1, length_x, 2): # Windows on ground level
        if i != door_x:
            for j in range(base_y, base_y+window_max_height):
                utilityFunctions.setBlock(level, (4,0), i, j+1, base_z)

    y_r = base_y + height_y + 1
    for floors in range(1, no_floors): # Windows on higher floors
        for i in range(base_x+1, length_x, 2):
            for j in range(window_max_height):
                # print y_r+j
                utilityFunctions.setBlock(level, (4,0), i, y_r+j, base_z)
        y_r += height_y

    # Do something with temp_base_y and the total_height of the building
    y_r = total_height-2
    for x in range(x_center, base_x, -2):
        for y in range(min(window_max_height, y_r-(temp_base_y+2))):
            utilityFunctions.setBlock(level, (20,0), x, base_y+temp_base_y+y+1, base_z)
        y_r -=2


    y_r = total_height-2
    for x in range(x_west, base_x + length_x - 1, +2):
        for y in range(min(window_max_height, y_r-(temp_base_y+2))):
            utilityFunctions.setBlock(level, (20,0), x, base_y+temp_base_y+y+1, base_z)
        y_r -=2


def windows_beta(level, box, length_x, height_y, length_z, base_x, temp_base_y, base_z, facade_type, door_x, base_y, no_floors, total_height): # This function currently assumes the building has an uneven width
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    window_max_height = height_y-3 # Depending on floor height. We want windows to be one block above the floor and one block below the ceiling, at most.
    n_windows = length_x//2 # Number of windows we would want on this building for a nice look
    if length_x % 2 == 0:
        n_windows -= 1 # We'll just make the middle windows larger

    window_width = 1 # Generally, window width is just one

    if n_windows > 4: # Hardcoded: larger windows when building gets wider
        window_width = length_x//4

    if height_y > 4:
        utilityFunctions.setBlock(level, (4,0), door_x, base_y+2, base_z) # Window above the door

    for i in range(base_x+1, length_x, 2): # Windows on ground level
        if i != door_x:
            for j in range(base_y, base_y+window_max_height):
                utilityFunctions.setBlock(level, (4,0), i, j+1, base_z)

    y_r = base_y + height_y + 1
    for floors in range(1, no_floors): # Windows on higher floors
        for i in range(base_x+1, length_x, 2):
            for j in range(window_max_height):
                # print y_r+j
                utilityFunctions.setBlock(level, (4,0), i, y_r+j, base_z)
        y_r += height_y

    # Do something with temp_base_y and the total_height of the building
    y_r = total_height-2
    for x in range(x_center, base_x, -2):
        for y in range(min(window_max_height, y_r-(temp_base_y+2))):
            utilityFunctions.setBlock(level, (20,0), x, base_y+temp_base_y+y+1, base_z)
        y_r -=2


    y_r = total_height-2
    for x in range(x_west, base_x + length_x - 1, +2):
        for y in range(min(window_max_height, y_r-(temp_base_y+2))):
            utilityFunctions.setBlock(level, (20,0), x, base_y+temp_base_y+y+1, base_z)
        y_r -=2


def build_roof(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    for z in range(base_z, base_z + length_z):
        y = base_y+height_y
        for x in range(base_x, x_center):
            utilityFunctions.setBlock(level, (pallete.roof_stair,0), x, y, z)
            y += 1
        adjust = 0
        if length_x % 2 != 0:
            adjust = 1
            utilityFunctions.setBlock(level, pallete.roof_block, x_center, y - 1, z)

        y = base_y+height_y
        for x in range(base_x + length_x - 1, x_west, -1):
            utilityFunctions.setBlock(level, (pallete.roof_stair,1), x, y, z)
            y += 1

    y_r = base_y+height_y
    for x in range(base_x, x_center):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.roof_block, x, y, base_z)
            utilityFunctions.setBlock(level, pallete.roof_block, x, y, base_z + length_z - 1)
        y_r += 1

    if length_x % 2 != 0:
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.roof_block, x_center, y, base_z)
            utilityFunctions.setBlock(level, pallete.roof_block, x_center, y, base_z + length_z - 1)

    y_r = base_y+height_y
    for x in range(base_x + length_x - 1, x_west, -1):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.roof_block, x, y, base_z)
            utilityFunctions.setBlock(level, pallete.roof_block, x, y, base_z + length_z - 1)
        y_r += 1

    return y_r-1


def build_floor(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z, stair_loc, top_offset):
    x = base_x#z-directional wall
    for z in range(base_z + 1, base_z + length_z - 1):
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, pallete.wall, x, y, z)

    z = base_z
    for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, pallete.wall, x, y, z)

    #Other walls:
    x = base_x + length_x - 1#z-directional wall
    for z in range(base_z + 1, base_z + length_z - 1):
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, pallete.wall, x, y, z)

    z = base_z + length_z - 1
    for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, pallete.wall, x, y, z)

    #Corner Pillars:
    for y in range(base_y, base_y+height_y + top_offset):
         utilityFunctions.setBlock(level, pallete.pillar, base_x, y, base_z)
         utilityFunctions.setBlock(level, pallete.pillar, base_x, y, base_z + length_z - 1)
         utilityFunctions.setBlock(level, pallete.pillar, base_x + length_x - 1, y, base_z)
         utilityFunctions.setBlock(level, pallete.pillar, base_x + length_x - 1, y, base_z + length_z - 1)

    if stair_loc == 0:
        #stair on west side, grow to south side
        start_x = base_x + 1
        start_z = base_z + length_z - height_y - 2

        for i in range(height_y):
            utilityFunctions.setBlock(level, (pallete.stair, 2), start_x, base_y+i, start_z+i)
            if i < height_y - 1:
                utilityFunctions.setBlock(level, (pallete.stair, 7), start_x, base_y+i, start_z+i+1)
            else:#one extra floor block for more convenient walking
                utilityFunctions.setBlock(level, pallete.floor, start_x, base_y+i, start_z+i+1)

        y_ceiling = base_y + height_y - 1

        for z in range(base_z + 1, start_z):
            utilityFunctions.setBlock(level, pallete.floor, base_x + 1, y_ceiling, z)
        for x in range (base_x + 2, base_x + length_x - 1):
            for z in range(base_z + 1, base_z + length_z - 1):
                utilityFunctions.setBlock(level, pallete.floor, x, y_ceiling, z)
    #elif stair_loc == 1:
        #stair on north side grow to west side
    elif stair_loc == 2:
        #stair on east side grow to north side
        start_x = base_x + length_x - 2
        start_z = base_z + height_y + 1
        utilityFunctions.setBlock(level, (pallete.stair,1), start_x, base_y, start_z)

        for i in range(height_y):
            utilityFunctions.setBlock(level, (pallete.stair,3), start_x, base_y+i, start_z-i)
            if i < height_y - 1:
                utilityFunctions.setBlockIfEmpty(level, (pallete.stair,6), start_x, base_y+i, start_z-i-1)
            else:#one extra floor block for more convenient walking
                utilityFunctions.setBlockIfEmpty(level, pallete.floor, start_x, base_y+i, start_z-i-1)

        y_ceiling = base_y + height_y - 1

        for z in range(start_z + 1, base_z + length_z - 1):
            utilityFunctions.setBlock(level, pallete.floor, base_x + length_x - 2, y_ceiling, z)
        for x in range (base_x + 1, base_x + length_x - 2):
            for z in range(base_z + 1, base_z + length_z - 1):
                utilityFunctions.setBlock(level, pallete.floor, x, y_ceiling, z)
    #else: #if stair_loc == 3:
        #stair on south side grow to east side

# Start of the Generation script
#  @ level: Minecraft world
#  @ box: selected box by mcedit
#  @ options: user defined inputs from mcedit
def build_house(length_x, height_y, length_z, no_floors, facade_type):
    base_x = 0
    base_y = 1
    base_z = 0
    tot_height = no_floors*height_y + length_x + 1 #/ 2 box too large is not really an issue...
    level = MCSchematic((length_x, tot_height, length_z))#working object
    box = bx.BoundingBox((0,0,0),(length_x, tot_height, length_z))

    pallete = Pallete()

    #level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz))#working object

    #Walls:
    temp_base_y = base_y
    stair_loc = 0
    for i in range(no_floors):
        if i == no_floors - 1:#top most floor
            build_floor(level, pallete, length_x, height_y, length_z, base_x, temp_base_y, base_z, stair_loc, 1)
        else:#middel floor
            build_floor(level, pallete, length_x, height_y, length_z, base_x, temp_base_y, base_z, stair_loc, 0)
        stair_loc += 2
        stair_loc %= 4
        temp_base_y += height_y
    temp_base_y -= height_y - 1

    #floor:
    for x in range (base_x + 1, base_x + length_x - 1):
        for z in range(base_z + 1, base_z + length_z - 1):
            utilityFunctions.setBlock(level, pallete.floor, x, base_y-1, z)


    #else:
        #door in N/S section
    y_r = build_roof(level, pallete, length_x, height_y, length_z, base_x, temp_base_y, base_z)
    facade(level, pallete, length_x, height_y, length_z, base_x, temp_base_y, base_z, facade_type) # TODO: maybe should return the total height of the building, so we can place windows accordingly in the facade front
    door_x = random.randrange(base_x + 1, base_x+length_x - 1, 2)
    door_z = base_z #if door_loc == 1 else base_z + length_z - 1
    #FIXME windows(level, box, length_x, height_y, length_z, base_x, temp_base_y, base_z, facade_type, door_x, base_y, no_floors, y_r)

    #floor block underneeth door:
    utilityFunctions.setBlock(level, pallete.floor, door_x, base_y - 1, door_z)

    #clear blocks for the door:
    utilityFunctions.setBlock(level, (0,0), door_x, base_y, door_z) #air
    utilityFunctions.setBlock(level, (0,0), door_x, base_y + 1, door_z) #air

    #setBlock(x, y, z,"acacia_door")
    #place actual door:
    # "acacia_door"
    #utilityFunctions.setBlock(level, ("acacia_door", door_loc), door_x, base_y, door_z)
    #utilityFunctions.setBlock(level, "acacia_door[half=upper]", door_x, base_y, door_z)

    utilityFunctions.setBlock(level, (pallete.door, 1), door_x, base_y, door_z)
    utilityFunctions.setBlock(level, (pallete.door, 1 + 8), door_x, base_y + 1, door_z)
    #source for door and bed rotations: https://github.com/abrightmoore/ProceduralSettlementsInMinecraft/blob/master/House.py
    #print("level:", level.size)


    return level, box, [door_x, door_z]


def place_house(og_level, length_x, height_y, length_z, base, rotations, no_floors, facade_type):
    scheme, box, door_coords = build_house(length_x, height_y, length_z, no_floors, facade_type)

    if rotations % 2 == 0:
        rot_box = bx.BoundingBox((0,0,0),(box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz))
    else:
        rot_box = bx.BoundingBox((0,0,0),(box.maxz-box.minz,box.maxy-box.miny,box.maxx-box.minx))

    for i in range(rotations):
        scheme.rotateLeft()

    og_level.copyBlocksFrom(scheme, rot_box, base)

    #transform from scheme coords to global coords
    door_coords[0] += base[0]#x
    door_coords[1] += base[2]#z

    return door_coords

def perform(level, box, options):
    height_y = options["height (y)"]
    length_z = options["length (z)"]
    length_x = options["length (x)"]
    base_x = options["offset (x)"]
    base_y = options["offset (y)"]
    base_z = options["offset (z)"]
    rotations = options["door location (N=0, W=1, S=2, E=3)"]
    no_floors = options["number of floors"]
    facade_type = options["facade type (small stairs=0, large stairs=1, bell=2, flat=3)"]
    place_house(level, length_x, height_y, length_z, (base_x, base_y, base_z), rotations, no_floors, facade_type)

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
