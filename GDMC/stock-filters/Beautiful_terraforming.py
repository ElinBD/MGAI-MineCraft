import itertools
import numpy as np
import utilityFunctions as utilityFunctions


from Beautiful_meta_analysis import get_height_map, get_surface_type_map

inputs = (
    ("Function to flatten box", "label"),
    ("Creator: Tim", "label"),
    ("Maintain Block Type", False),

)



def flatten_box(level,box, maintain_types = False):
    height_map = get_height_map(level, box)
    surface_type_map = get_surface_type_map(level, box)

    u_height, indices_height = np.unique(height_map.flatten(), return_inverse=True)
    most_freq_height = u_height[np.argmax(np.bincount(indices_height))]

    u_block, indices_block = np.unique(surface_type_map.flatten(), return_inverse=True)
    block_type = u_block[np.argmax(np.bincount(indices_block))]


    pos_top_layer = itertools.product(xrange(box.minx, box.maxx),
                                      xrange(box.minz, box.maxz)
                                     )

    for pos in pos_top_layer:

        height = height_map[pos[0]-box.minx, pos[1]-box.minz]

        if maintain_types:
            block_type = surface_type_map[pos[0]-box.minx, pos[1]-box.minz]


        if height > most_freq_height:

            for y in xrange((box.miny+height), (box.miny+most_freq_height)-1, -1):

                #print(y)
                utilityFunctions.setBlock(level, (0, 0), pos[0], y,
                                          pos[1])

        if height < most_freq_height:

            for y in xrange((box.miny + height), (box.miny + most_freq_height), 1):
                #print(y)
                utilityFunctions.setBlock(level, (block_type, 0), pos[0], y,
                                          pos[1])

        if not maintain_types:
            utilityFunctions.setBlock(level, (block_type, 0), pos[0], box.miny + most_freq_height - 1,
                                  pos[1])


def perform(level, box, options):
    flatten_box(level, box, options['Maintain Block Type'])
