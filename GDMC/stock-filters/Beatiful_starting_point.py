import itertools
import numpy as np
from Beautiful_meta_analysis import get_height_map, analyze_height_map
from skimage.filters.rank import mean
from skimage.morphology import square



inputs = (
    ("Function to search for optimal starting point to start a settlement by iterating through height map", "label"),
    ("Creator: Tim", "label")
)

def find_starting_point(height_map, box, level, square_size):

    ##not finished yet
    height_map_centred = height_map - np.mean(height_map)
    smoothed = mean(height_map_centred.astype('uint8'), square(square_size))

    return smoothed



def perform(level, box, options):

    square_size = 1
    height_map = get_height_map(level, box)
    print find_starting_point(height_map, box, level, square_size)

