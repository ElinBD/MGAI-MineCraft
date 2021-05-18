from Beautiful_meta_analysis import get_block_type_counts, get_biom_type_counts
from pymclevel.biome_types import biome_types
from pymclevel.box import BoundingBox
from pymclevel import biome_types
import random

inputs = (
    ("Get color palets based on a given box", "label"),
    ("Creator: Elin", "label")
)

stairs = [(53, 0), (67, 0), (108, 0), (109, 0), (128, 0),
          (134, 0), (135, 0), (136, 0),
          (156, 0), (163, 0), (164, 0), (203, 0)]
# alphaMaterials.WoodenStairs = alphaMaterials[53, 0]
# alphaMaterials.StoneStairs = alphaMaterials[67, 0]
# alphaMaterials.BrickStairs = alphaMaterials[108, 0]
# alphaMaterials.StoneBrickStairs = alphaMaterials[109, 0]
# alphaMaterials.SandstoneStairs = alphaMaterials[128, 0]
# alphaMaterials.SpruceWoodStairs = alphaMaterials[134, 0]
# alphaMaterials.BirchWoodStairs = alphaMaterials[135, 0]
# alphaMaterials.JungleWoodStairs = alphaMaterials[136, 0]
# alphaMaterials.QuartzStairs = alphaMaterials[156, 0]
# alphaMaterials.AcaciaStairs = alphaMaterials[163, 0]
# alphaMaterials.DarkOakStairs = alphaMaterials[164, 0]
# alphaMaterials.PurpurStairs = alphaMaterials[203, 0]

slabs = [(43, 0), (43, 1), (43, 2), (43, 3), (43, 4), (43, 5),
         (44, 0), (44, 1), (44, 2), (44, 3), (44, 4), (44, 5),
         (125, 0), (125, 1), (125, 2), (125, 3),
         (126, 0), (126, 1), (126, 2), (126, 3),
         (181, 0), (182, 0), (205, 0)]
# alphaMaterials.DoubleStoneSlab = alphaMaterials[43, 0]
# alphaMaterials.DoubleSandstoneSlab = alphaMaterials[43, 1]
# alphaMaterials.DoubleWoodenSlab = alphaMaterials[43, 2]
# alphaMaterials.DoubleCobblestoneSlab = alphaMaterials[43, 3]
# alphaMaterials.DoubleBrickSlab = alphaMaterials[43, 4]
# alphaMaterials.DoubleStoneBrickSlab = alphaMaterials[43, 5]
# alphaMaterials.StoneSlab = alphaMaterials[44, 0]
# alphaMaterials.SandstoneSlab = alphaMaterials[44, 1]
# alphaMaterials.WoodenSlab = alphaMaterials[44, 2]
# alphaMaterials.CobblestoneSlab = alphaMaterials[44, 3]
# alphaMaterials.BrickSlab = alphaMaterials[44, 4]
# alphaMaterials.StoneBrickSlab = alphaMaterials[44, 5]
# alphaMaterials.OakWoodDoubleSlab = alphaMaterials[125, 0]
# alphaMaterials.SpruceWoodDoubleSlab = alphaMaterials[125, 1]
# alphaMaterials.BirchWoodDoubleSlab = alphaMaterials[125, 2]
# alphaMaterials.JungleWoodDoubleSlab = alphaMaterials[125, 3]
# alphaMaterials.OakWoodSlab = alphaMaterials[126, 0]
# alphaMaterials.SpruceWoodSlab = alphaMaterials[126, 1]
# alphaMaterials.BirchWoodSlab = alphaMaterials[126, 2]
# alphaMaterials.JungleWoodSlab = alphaMaterials[126, 3]
# alphaMaterials.DoubleRedSandstoneSlab = alphaMaterials[181, 0]
# alphaMaterials.RedSandstoneSlab = alphaMaterials[182, 0]
# alphaMaterials.PurpurSlab = alphaMaterials[205, 0]

# pillars = [(202, 0)]
# alphaMaterials.PurpurPillar = alphaMaterials[202, 0]

windows = [(95, 0), (102, 0), (160, 0)]
# alphaMaterials.StainedGlass = alphaMaterials[95, 0]
# alphaMaterials.GlassPane = alphaMaterials[102, 0]
# alphaMaterials.StainedGlassPane = alphaMaterials[160, 0]

doors = [(64 ,0), (71 ,0), (96 ,0), (167 ,0), (193 ,0), (194 ,0), (195 ,0),
         (196 ,0), (197 ,0)]
# alphaMaterials.WoodenDoor = alphaMaterials[64, 0]
# alphaMaterials.IronDoor = alphaMaterials[71, 0]
# alphaMaterials.Trapdoor = alphaMaterials[96, 0]
# alphaMaterials.IronTrapdoor = alphaMaterials[167, 0]
# alphaMaterials.SpruceDoor = alphaMaterials[193, 0]
# alphaMaterials.BirchDoor = alphaMaterials[194, 0]
# alphaMaterials.JungleDoor = alphaMaterials[195, 0]
# alphaMaterials.AcaciaDoor = alphaMaterials[196, 0]
# alphaMaterials.DarkOakDoor = alphaMaterials[197, 0]

floors = [(70, 0), (72, 0)]
# alphaMaterials.StoneFloorPlate = alphaMaterials[70, 0]
# alphaMaterials.WoodFloorPlate = alphaMaterials[72, 0]

walls = [(1,0)]

# alphaMaterials.Stone = alphaMaterials[1, 0]
# alphaMaterials.Grass = alphaMaterials[2, 0]
# alphaMaterials.Dirt = alphaMaterials[3, 0]
# alphaMaterials.Cobblestone = alphaMaterials[4, 0]
# alphaMaterials.WoodPlanks = alphaMaterials[5, 0]
# alphaMaterials.Sapling = alphaMaterials[6, 0]
# alphaMaterials.SpruceSapling = alphaMaterials[6, 1]
# alphaMaterials.BirchSapling = alphaMaterials[6, 2]
# alphaMaterials.Bedrock = alphaMaterials[7, 0]
# alphaMaterials.WaterActive = alphaMaterials[8, 0]
# alphaMaterials.Water = alphaMaterials[9, 0]
# alphaMaterials.LavaActive = alphaMaterials[10, 0]
# alphaMaterials.Lava = alphaMaterials[11, 0]
# alphaMaterials.Sand = alphaMaterials[12, 0]


blocks_dict = {2: 'NL',
               8: 'NL',
               12: 'desert'}

bioms_dict = {6: 'NL',
               2: 'desert'}

color_palets = {'wall': walls,
                'staircase': stairs,
                'rooftop staircase': stairs,
                # 'pilar': pillars,
                'windows': windows,
                'door': doors,
                'floor': floors,
                'roofslab': slabs,
                'decoslab': slabs #,
                # 'lights':
                }
                

def get_most_frequent_block(block_types):
    if 0 in block_types.keys():
        block_types.pop(0)
    return max(block_types, key=block_types.get)

def sample_palet(col_pal):
    sampled_palet = {}
    for key, value in col_pal.items():
        sampled_palet[key] = random.sample(value, 1)[0]

    return sampled_palet

def get_color_palet(level, box):
    # biom_types = get_biom_type_counts(level, box, options)
    block_types = get_block_type_counts(level, box)
    # print 'Biom types:'
    # print biom_types

    most_freq_block_type = get_most_frequent_block(block_types)

    # most_freq_biom_type = get_most_frequent_block(biom_types))
    # print(most_freq_biom_type)

    landscape_type = blocks_dict.get(most_freq_block_type, 'NL')
    # landscape_biom = bioms_dict[most_freq_block_type]

    palet_ranges = color_palets[landscape_type]
    palet = sample_palet(palet_ranges)

    return palet


class Pallete():
    def __init__(self, pillars=False):
        self.quartz_stair = 156
        self.quartz_block = (155, 0)
        self.quartz_slab = (44, 7)

        rng_wall = random.randint(0, 5)
        if rng_wall == 0:#white
            self.wall = (251, 0)
        elif rng_wall == 1:#gray
            self.wall = (251, 7)
        elif rng_wall == 2:#light gray
            self.wall = (251, 8)
        elif rng_wall == 3:#brown
            self.wall = (251, 12)
        elif rng_wall == 4:#orange
            self.wall = (251, 1)
        elif rng_wall == 5:#gray bricks
            self.wall = (98, 0)
        elif rng_wall == 6:#orange bricks
            self.wall = (45, 0)

        #self.wall = (45, 0)#FIXME hardcoded
        self.pillar = self.wall#(251, 0)TODO if pillars == True...

        rng_plank = random.randint(0, 2)
        #print('plank = ', rng_plank)
        if rng_plank == 0:#oak
            self.stair = 53
            self.floor = (5, 0)
        elif rng_plank == 1:#spruce
            self.stair = 134
            self.floor = (5, 1)
        elif rng_plank == 2:#birch
            self.stair = 135
            self.floor = (5, 2)

        rng_door = random.randint(0, 4)
        #print('door = ', rng_door)
        if rng_door == 0:#oakw
            self.door = 64
        elif rng_door == 1:#spruce
            self.door = 193
        elif rng_door == 2:#birch
            self.door = 194
        elif rng_door == 3:#jungle
            self.door = 195
        elif rng_door == 4:#dark oak
            self.door = 197

        rng_roof = random.randint(0, 3)
        #print('roof = ', rng_roof)
        if rng_roof == 0:#red bricks
            self.roof_stair = 108
            self.roof_block = (45, 0)
            self.roof_slab = (44, 4)
        elif rng_roof == 1:#gray bricks
            self.roof_stair = 109
            self.roof_block = (98, 0)
            self.roof_slab = (44, 5)
        elif rng_roof == 2:#nether bricks
            self.roof_stair = 114
            self.roof_block = (112, 0)
            self.roof_slab = (44, 6)
        elif rng_roof == 3:#dark oak
            self.roof_stair = 164
            self.roof_block = (5, 5)
            self.roof_slab = (126, 5)

        #self.decoration_slab #TODO add if nescassary TODO
        raam = random.randint(0, 2)
        #print('raam = ', raam)
        if raam == 0:#vanilla
            self.window = (102, 0)
        elif raam == 1:#gray
            self.window = (160, 7)
        elif raam == 2:#black
            self.window = (160, 15)
    
    