from __future__ import division

import itertools
import numpy as np
import utilityFunctions as utilityFunctions

from Beautiful_meta_analysis import get_height_map, analyze_height_map
from skimage.filters.rank import mean, gradient, gradient_percentile
from skimage.morphology import (square, rectangle, diamond, disk,
                                octagon, star)


inputs = (
    ("Function to search for optimal starting point to start a settlement by iterating through height map", "label"),
    ("Creator: Tim", "label"),
    ("shape (0=square, 1=rectangle, 2=disk, 3=diamond", (0, 0, 3)),
    ("size_1", (0, 0, 256)),
    ("size_2 (only applicable for rectangle)", (20, 0, 256))
)


def find_starting_point(height_map, box, level, area, offset):
    ##not finished yet
    # height_map_centred = height_map - np.mean(height_map)
    print(height_map)

    excl_perc = 0
    gradient_map = gradient(height_map.astype('uint8'), area)
    print(gradient_map)

    while not np.any(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset] == 0):
        excl_perc += 1
        gradient_map = gradient_percentile(height_map.astype('uint8'), area, p0=((0 + (excl_perc / 2)) / 100),
                                           p1=((100 - (excl_perc / 2)) / 100) )

        if (excl_perc >= 20):

            candidates = np.where(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset]
                                  == np.amin(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset]))
            elev = np.amin(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset])
            print('no perfectly flat area of given size in box, area with {} elevation excluding {} percent of area chosen instead'.format(
                    elev, excl_perc))
            print('{} candidate(s) found'.format(len(candidates[0])))

            return(candidates)



    print(np.where(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset]
                                  == 0))

    while (excl_perc > 0) and np.any(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset] == 0):
        excl_perc -= 0.1
        gradient_map = gradient_percentile(height_map.astype('uint8'), area, p0=(((0 + (excl_perc / 2)) / 100)),
                                           p1=(((100 - (excl_perc / 2))) / 100))

    while not np.any(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset] == 0):
        excl_perc += 0.01
        gradient_map = gradient_percentile(height_map.astype('uint8'), area, p0=(((0 + (excl_perc / 2)) / 100)),
                                           p1=(((100 - (excl_perc / 2))) / 100))

    candidates = np.where(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset] == 0)
    if excl_perc == 0:
        print('perfectly flat area found')
    else:
        print('no perfectly flat area of given size in box, area with no elevation excluding {} percent of area chosen instead'.format(excl_perc))

    print('{} candidate(s) found'.format(len(candidates[0])))
    return (candidates)


def perform(level, box, options):
    shape = options["shape (0=square, 1=rectangle, 2=disk, 3=diamond"]
    size = options["size_1"]


    if shape == 0:
        area = square(size)
        offset = int(size/2)
    if shape == 1:
        size_2 = options['size_2 (only applicable for rectangle)']
        area =  rectangle(size,size_2)
        offset = int((max(size, size_2))/2)
    if shape == 2:
        area = disk(size)
        offset = int(size)
    if shape == 3:
        area = diamond(size)
        offset = int(size)

    if (box.size[0] < 2*offset) or (box.size[2] < 2*offset):
        print('box smaller than area')
        return

    height_map = get_height_map(level, box)
    candidates = find_starting_point(height_map, box, level, area = area, offset = offset)


    for i in range(0, 100):
       utilityFunctions.setBlock(level, (4, 0), box.minx+offset+candidates[0][0], i, box.minz+offset+candidates[1][0])
