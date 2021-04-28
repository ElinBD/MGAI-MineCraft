from Beautiful_meta_analysis import get_block_type_counts, get_biom_type_counts
from pymclevel.biome_types import biome_types
from pymclevel.box import BoundingBox
from pymclevel import biome_types

inputs = (
    ("Get color palets based on a given box", "label"),
    ("Creator: Elin", "label")
)

ranges_dict = {8: 'NL',
               12: 'desert',
               2: 'field'}

#color_palets = {'NL': {'wall': ,
#                       'roof':  ,
#},
#                'desert': {'wall': ,
#                       'roof':  },
#                'field': {'wall': ,
#                       'roof':  }
                }


def get_most_frequent_block(block_types):
    block_types = block_types.pop(0)
    return max(block_types, key=block_types.get)

def perform(level, box, options):
    block_types = get_block_type_counts(level, box, options)
    # print 'Biom types:'
    # print biom_types

    most_freq_block_type = get_most_frequent_block(block_types)
    landscape_type = ranges_dict[most_freq_block_type]
    return color_palets[landscape_type]
    # print(most_freq_block_type)