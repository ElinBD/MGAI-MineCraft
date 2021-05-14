from pymclevel import schematic, block_copy, box as bx

def perform(og_level, og_box, options):
    scheme = schematic.extractSchematicFrom(og_level, og_box)

    level = og_level.extractSchematic(og_box)#schematic.MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz))
    box = bx.BoundingBox((0,0,0),(scheme.Length, scheme.Height, scheme.Width))

    level.copyBlocksFrom(og_level, og_box, (og_box.minx, og_box.miny, og_box.minz ))
    #level.copyBlocksFrom(shape, bbox, (box.minx,box.miny,box.minz))
    '''
    shape = PalladioBuilding(box,options)#insert foundationSchematic a schematic
	bbox = BoundingBox((0,0,0),(width,height,depth))
	level.copyBlocksFrom(shape, bbox, (box.minx,box.miny,box.minz))

    	# Create the lower foundation.
	foundationSchematic = MCSchematic((width,height,foundationHeight+depth))
	for x in xrange(0,width):
		for z in xrange(0,depth):
			# Check the source model for a block, if found, there's a foundation here
			for y in xrange(0,height):
				if getBlock(level,x,y,z) != AIR:
					for fy in xrange(0, foundationHeight):
						setBlock(foundationSchematic, WALLBLOCK, x, fy, z)
					break
	foundationSchematic.copyBlocksFrom(level, box, (0,foundationHeight,0))
    '''
    print("pre:")
    print("length", scheme.Length)
    print("width", scheme.Width)
    print("height", scheme.Height)

    print("level length", level.Length)
    print("level width", level.Width)
    print("level height", level.Height)

    print("og level length", og_level.Length)
    print("og level width", og_level.Width)
    print("og level height", og_level.Height)

    print("box length", box.length)
    print("box height", box.height)
    print("box width", box.width)

    print("og_box length", og_box.length)
    print("og_box height", og_box.height)
    print("og_box width", og_box.width)
    
    scheme.rotateLeft()
    print("post:")
    print("length", scheme.Length)
    print("width", scheme.Width)
    print("height", scheme.Height)
    
    print("box length", box.length)
    print("box height", box.height)
    print("box width", box.width)

    print("og_box length", og_box.length)
    print("og_box height", og_box.height)
    print("og_box width", og_box.width)

    print("level length", level.Length)
    print("level width", level.Width)
    print("level height", level.Height)

    print("og level length", og_level.Length)
    print("og level width", og_level.Width)
    print("og level height", og_level.Height)
    

    #print("level length", level)
    
    og_level.copyBlocksFrom(scheme, box, (box.minx, box.miny, box.minz))

    #copyBlocksFrom(destLevel, sourceLevel, sourceBox, destinationPoint)

    
