from __future__ import division

import itertools
import numpy as np
import utilityFunctions as utilityFunctions

from Beautiful_meta_analysis import get_height_map, get_surface_type_map, get_biome_map
from skimage.filters.rank import modal, gradient, gradient_percentile, maximum
from skimage.morphology import (square, rectangle, diamond, disk,
                                octagon, star)


inputs = (
    ("Function to search for optimal starting point to start a settlement by iterating through height map", "label"),
    ("Creator: Tim", "label"),
    ("shape (0=square, 1=rectangle, 2=disk, 3=diamond", (0, 0, 3)),
    ("size_1", (5, 0, 256)),
    ("size_2 (only applicable for rectangle)", (0, 0, 256))
)


def find_starting_point(height_map, surface_type_map, biome_map, box, level, area, offset, plains = True):

    excl_perc = 0
    gradient_map = gradient(height_map.astype('uint8'), area)

    surface_type_map[surface_type_map == 9] = surface_type_map[surface_type_map == 9] + 100
    surface_max_map = maximum(surface_type_map, area)
    if plains:
        biome_maj_map = modal(biome_map, area)


    #increase value of centres of areas that include water to avoid selecting them
    gradient_map[surface_max_map > 99] += 50
    #increase value of centres whose majority biome is not plains
    if plains:
        gradient_map[biome_maj_map != 1] += 50

    while not np.any(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset] == 0):
        excl_perc += 1
        gradient_map = gradient_percentile(height_map.astype('uint8'), area, p0=((0 + (excl_perc / 2)) / 100),
                                           p1=((100 - (excl_perc / 2)) / 100) )

        gradient_map[surface_max_map > 99] += 50
        if plains:
            gradient_map[biome_maj_map != 1] += 50

        if (excl_perc >= 50):

            candidates = np.where(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset]
                                  == np.amin(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset]))
            elev = np.amin(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset])
            if elev >= 50:
                raise ValueError('No suitable area found. Try smaller size or different box')

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
        gradient_map[surface_max_map > 99] += 50
        if plains:
            gradient_map[biome_maj_map != 1] += 50

    while not np.any(gradient_map[offset:box.size[0] - offset, offset:box.size[2] - offset] == 0):
        excl_perc += 0.01
        gradient_map = gradient_percentile(height_map.astype('uint8'), area, p0=(((0 + (excl_perc / 2)) / 100)),
                                           p1=(((100 - (excl_perc / 2))) / 100))
        gradient_map[surface_max_map > 99] += 50
        if plains:
            gradient_map[biome_maj_map != 1] += 50

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

    if (box.size[0] <= 2*offset) or (box.size[2] <= 2*offset):
        print('box smaller than area')
        return

    height_map = get_height_map(level, box)
    surface_type_map = get_surface_type_map(level, box)
    biome_map = get_biome_map(level, box)

    candidates = find_starting_point(height_map, surface_type_map, biome_map, box, level, area = area, offset = offset,
                                     plains = True)
    index = np.random.randint(len(candidates[0]))

    for i in range(0, 100):
       utilityFunctions.setBlock(level, (4, 0), box.minx+offset+candidates[0][index], i, box.minz+offset+candidates[1][index])
