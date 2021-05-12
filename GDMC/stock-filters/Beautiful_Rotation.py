from pymclevel import schematic, block_copy

def perform(level, box, options):
    scheme = schematic.extractSchematicFrom(level, box)
    print("pre:")
    print("length", scheme.Length)
    print("width", scheme.Width)
    print("height", scheme.Height)
    
    #scheme.rotateLeft()
    print("post:")
    print("length", scheme.Length)
    print("width", scheme.Width)
    print("height", scheme.Height)

    block_copy.copyBlocksFrom(scheme, level, box, (20, 4, 20)) #I've tested this on a superflat world 