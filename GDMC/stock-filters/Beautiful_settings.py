# Contains settings for generating the settlement


# ==== Canal settings ====
MIN_LENGTH_C = 30  # Min length of each section of the gear-like shape

MAX_L_INNER = 10   # Angle between which the left inner canal should be

MIN_T_INNER = 200  # Angle between which the top inner canal should be
MAX_T_INNER = 230

MIN_B_INNER = 130  # Angle between which the bottom inner canal should be
MAX_B_INNER = 160

P_SWITCH = 0.4  # Probability to switch between inner and outer, when MIN_LENGTH is reached

OFFSET_CROSSPOINT = 5  # Maximum offset of the crosspoint of the three inner canals

# Radius of the outer and inner circles, forming the gear-shape
MIN_OUTER = 40
MAX_OUTER = 45
MIN_INNER = MIN_OUTER - 8
MAX_INNER = MIN_OUTER - 5


# ==== Plot generation settings ====
MIN_WIDTH = 4
MAX_WIDTH = 8
MIN_LENGTH = 4
MAX_LENGTH = 8

P_PLOT = 0.7  # Probability to place plot when it is available

CANAL_VALUE = 100  # Added value to direct the buildings nearby a canal to it


# ==== Street light specific ====
LEN_POLE = 4    # Length of street light pole
SPARSITY = 9    # Area (NxN) where at most one street light can be


# ==== Block-specifications (with the exception of the buildings) ====
AIR = (0,0)
WATER = (9,0)
ROAD = (13,0)
OUTER_WALL = (35,14)
POLE = (139,0)  # Cobblestone wall