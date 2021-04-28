from Beautiful_meta_analysis import *
from pymclevel.biome_types import biome_types
from pymclevel.box import BoundingBox
from pymclevel import biome_types

inputs = (
    ("Get color palets based on a given box", "label"),
    ("Creator: Elin", "label")
)

ranges_dict = {}

def get_color_palet():
    return None


def perform(level, box, options):
    biom_types = get_block_type_counts(level, box, options)
    print 'Biom types:'
    print biom_types
