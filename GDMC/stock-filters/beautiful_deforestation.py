import utilityFunctions as utilityFunctions
from pymclevel import box as boundingBox
from pymclevel import materials

inputs = (
	("Deforestation of given box", "label"),
	("Creator: Jerry", "label")
	)

# Remove a single tree
def remove_tree(level, loc, biome):
  # Travel downwards until end of log is reached
  # Wood-ID=17 | Leave-ID=18
  step = boundingBox.Vector(0, 1, 0)
  while level.blockAt(loc[0], loc[1]-1, loc[2]) == 17 or \
        level.blockAt(loc[0], loc[1]-1, loc[2]) == 18:
    loc = loc.__sub__(step)
  utilityFunctions.setBlock(level, (2,0), loc[0], loc[1]-1, loc[2]) # Dirt -> Grass

  # TODO TODO TODO TODO TODO TODO TODO
  for i in range(10): # Replace blocks of tree with air
    utilityFunctions.setBlock(level, (0,0), loc[0], loc[1]+i, loc[2])
  # TODO TODO TODO TODO TODO TODO TODO

# Start of the Deforestation
def perform(level, box, options):
  tree_map = utilityFunctions.treeMap(level, box) # Column = x, Row = z

  # Search through given box for trees
  for z, row in enumerate(tree_map):
    for x, pos in enumerate(row):
      if not pos == 0: # Coordinates (x,z) contains a log-block
        loc = box.origin.__add__(boundingBox.Vector(x, box.height, z))
        remove_tree(level, loc, level.biomeAt(loc[0], loc[1]))