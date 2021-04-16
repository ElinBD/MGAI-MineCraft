import utilityFunctions as utilityFunctions
from pymclevel import biome_types
import random

# Information visible in mcedit, can be used for user-input
inputs = (
	("Settlement Generator", "label"),
	("Creators: me", "label")
	)

# Start of the Generation script
#  @ level: Minecraft world
#  @ box: selected box by mcedit
#  @ options: user defined inputs from mcedit
def perform(level, box, options):
    height = 4
    length_z = 6
    length_x = 8
    base_x = 0
    base_y = 4
    base_z = 0

    #Walls of the house:
    for x in range (base_x, base_x+1):#z-directional wall
        for y in range(base_y, base_y+height):
            for z in range(base_z+1, base_z+length_z):
                utilityFunctions.setBlock(level, (4,0), x, y, z)
    
    for x in range (base_x+1, base_x+length_x):#x-directional wall
        for y in range(base_y, base_y+height):
            for z in range(base_z, base_z+1):
                utilityFunctions.setBlock(level, (4,0), x, y, z)
    
    #other walls:
    for x in range (base_x+length_x, base_x+1+length_x):#z-directional wall
        for y in range(base_y, base_y+height):
            for z in range(base_z+1, base_z+length_z):
                utilityFunctions.setBlock(level, (4,0), x, y, z)
    
    for x in range (base_x+1, base_x+length_x):#x-directional wall
        for y in range(base_y, base_y+height):
            for z in range(base_z+length_z, base_z+1+length_z):
                utilityFunctions.setBlock(level, (4,0), x, y, z)
	
    #Corner Pillars:
    for y in range(base_y, base_y+height):
         utilityFunctions.setBlock(level, (3,0), base_x, y, base_z)
         utilityFunctions.setBlock(level, (3,0), base_x, y, base_z+length_z)
         utilityFunctions.setBlock(level, (3,0), base_x+length_x, y, base_z)
         utilityFunctions.setBlock(level, (3,0), base_x+length_x, y, base_z+length_z)

    #floor:
    for x in range (base_x+1, base_x+length_x):
        for z in range(base_z+1, base_z+length_z):
            utilityFunctions.setBlock(level, (1,0), x, base_y-1, z)

    #doors and windows:
    x_door = random.randint(0, 1)
    #door_x = 0
    #door_z = 0
    if x_door == 1:
        #door in x section
        door_z = random.randint(base_z+2, base_z+length_z-2)
        door_x = random.randint(0, 1)
        if door_x == 0:
            door_x = base_x
        else:
            door_x = base_x+length_x
    else:
        #door in z section
        door_x = random.randint(base_x+2, base_x+length_x-2)
        door_z = random.randint(0, 1)
        if door_z == 0:
            door_z = base_z
        else:
            door_z = base_z+length_z
    
    utilityFunctions.setBlock(level, (8,0), door_x, base_y, door_z)
    utilityFunctions.setBlock(level, (8,0), door_x, base_y+1, door_z)
