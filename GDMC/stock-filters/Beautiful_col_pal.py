from Beautiful_meta_analysis import *
from pymclevel.biome_types import biome_types
from pymclevel.box import BoundingBox
from pymclevel import biome_types

inputs = (
    ("Get color palets based on a given box", "label"),
    ("Creator: Elin", "label")
)

ranges_dict = {8: 'NL',
               12: 'desert',
               2: ''}

def get_color_palet():
    return None

def get_most_frequent_block(block_types):
    block_types = block_types.pop(0)
    return max(block_types, key=block_types.get)

def perform(level, box, options):
    block_types = get_block_type_counts(level, box, options)
    # print 'Biom types:'
    # print biom_types

    most_freq_block_type = get_most_frequent_block(block_types)
    print(most_freq_block_type)