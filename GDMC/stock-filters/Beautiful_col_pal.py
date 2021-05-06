from Beautiful_meta_analysis import get_block_type_counts, get_biom_type_counts
from pymclevel.biome_types import biome_types
from pymclevel.box import BoundingBox
from pymclevel import biome_types

inputs = (
    ("Get color palets based on a given box", "label"),
    ("Creator: Elin", "label")
)

stairs = [(53, 0), (67, 0), (108, 0), (109, 0), (128, 0), (134, 0), (135, 0), (136, 0),
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

pillars = [(202, 0)]
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

blocks_dict = {8: 'NL',
               12: 'desert'}

bioms_dict = {6: 'NL',
               2: 'desert'}

color_palets = {'NL': {'Wall': slabs,
                'staircase': stairs,
                'rooftop staircase': stairs,
                'pilar': pillars,
                'windows': windows,
                'door': doors,
                'floor': floors,
                'roofslab': slabs,
                'decoslab': slabs #,
                # 'lights':
                }
                }

def get_most_frequent_block(block_types):
    block_types.pop(0)
    print(block_types)
    return max(block_types, key=block_types.get)

def sample_palet(col_pal):
    sampled_palet = {}
    for key, value in col_pal.items():
        sample_palet[key] = value.sample()

    return sample_palet

def perform(level, box, options):
    # biom_types = get_biom_type_counts(level, box, options)
    block_types = get_block_type_counts(level, box, options)
    # print 'Biom types:'
    # print biom_types

    most_freq_block_type = get_most_frequent_block(block_types)
    print(most_freq_block_type)

    # most_freq_biom_type = get_most_frequent_block(biom_types))
    # print(most_freq_biom_type)

    landscape_type = blocks_dict[most_freq_block_type]
    # landscape_biom = bioms_dict[most_freq_block_type]

    palet_ranges = color_palets[landscape_type]
    palet = sample_palet(palet_ranges)

    return palet