import utilityFunctions as utilityFunctions
import itertools
import numpy as np

from pymclevel.biome_types import biome_types
from pymclevel.box import BoundingBox


inputs = (
    ("Utility functions to obtain access to meta data for a given box", "label"),
    ("Creator: Tim", "label")
)

def get_block_type_counts(level, box, options):

    block_type_count = {}

    for pos in box.positions:
        block = level.blockAt(pos[0], pos[1] , pos[2])
        if block not in block_type_count.keys():
            block_type_count[block] = 0
        block_type_count[block] += 1
    return(block_type_count)

def get_biom_type_counts(level, box, options):
    biom_type_count = {}

    for pos in box.positions:
        biom = biome_types.biome_types[level.biomeAt(pos[0], pos[2])]
        # biom = level.biomAt(pos[0], pos[1] , pos[2])
        if biom not in biom_type_count.keys():
            biom_type_count[biom] = 0
        biom_type_count[biom] += 1
    return(biom_type_count)

def get_height_map(level, box):

    #think of way to deal with caves

    size = box.size
    pos_top_layer = itertools.product(xrange(box.minx, box.maxx),
                                      xrange(box.minz, box.maxz)
                                     )

    height_map = np.empty([size[0], size[2]], dtype=int)
    for pos in pos_top_layer:
        height = 0
        for y in xrange(box.miny, box.maxy, +1):
            if level.blockAt(pos[0], y, pos[1]) != 0:
                height += 1
            if y == box.maxy:
                height = box.maxy
                continue
            else:
                height_map[pos[0]-box.minx, pos[1]-box.minz] = height
                continue

    #do you think underground tiles will be relevant, or will a box be placed in a way that its lowest point
    #is underground for all blocks? Then, we could do:
    # height_map = height_map - np.min(height_map)

    return(height_map)

def analyze_height_map(height_map):
    meta_dict = {}

    min_altitude, max_altitude, sd_altitude = np.min(height_map), np.max(height_map), np.round(np.std(height_map), 2)
    quantiles = (np.quantile(height_map, (0.1, 0.25, 0.75, 0.9)))
    return min_altitude, max_altitude, sd_altitude, quantiles

def perform(level, box, options):
    block_types = get_block_type_counts(level, box, options)
    print 'Block types:'
    print block_types
    height_map = get_height_map(level, box)
    print 'Height map'
    print height_map
    height_map_data = analyze_height_map(height_map)
    print 'Summary'
    print height_map_data


