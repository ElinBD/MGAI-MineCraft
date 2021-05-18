import numpy as np
from random import sample
from Beautiful_meta_analysis import get_surface_type_map
import utilityFunctions as utilityFunctions
from pymclevel import biome_types
from pymclevel.box import BoundingBox

# Information visible in mcedit, can be used for user-input
inputs = (
	("Bridge placer", "label"),
	("Creator: Elin", "label"))

def get_waterpoints(level, box):
    """Get all coordinates where blocktype is water"""
    surfacemap = get_surface_type_map(level, box)
    waterpoints = np.argwhere(surfacemap == 9)
    return waterpoints

def generate_candidates(waterpoints):
    """Generate 50 candidates where each candidates contains the x,z coordinates
        of 2 bridges."""
    num_bridges = 3
    num_candidates = 20

    candidates = []
    for i in range(num_candidates):
        # sample 3 indeces from the waterpoints
        idxs = np.random.randint(len(waterpoints), size=num_bridges)
        bridges = waterpoints[idxs].flatten()
        candidates.append(bridges)

    return np.asarray(candidates)

def fitness_function(candidate, doors):
    """"Calculates the fitness value for a single candidate"""
    def f(door, candidate, bridge):
        return np.linalg.norm(door - candidate[bridge])
    
    # split candidate in the 3 bridge locations
    bridge_loca = np.split(candidate, len(candidate)/doors.shape[1])

    #for each bridge, calculcate the distance to each door
    dists = np.empty((len(bridge_loca), len(doors)))
    for bridge in range(len(bridge_loca)):
        dists[bridge] = np.apply_along_axis(f, 1, doors, bridge_loca, bridge)

    # for each door, save the minimal distance to a bridge
    min_dists = dists.min(axis = 0)

    return min_dists.sum()
       
def sort_by_fitness(candidates, doors):
    """Sort the candidates by their respective fitness"""
    fitness = np.apply_along_axis(fitness_function, 1, candidates, doors)
    sorted_idx = np.argsort(fitness)
    return candidates[sorted_idx], fitness[sorted_idx]

def selection(candidates, fitness):
    """select parents with a p equivalent to their fitness"""
    norm_fitness = [float(i)/sum(fitness) for i in fitness]
    candidate_draw = np.random.choice(range(len(candidates)), 10,
              p=norm_fitness)

    return candidates[candidate_draw].tolist()

def crossover(parents):
    """perform crossover between the parents"""
    children = []
    while len(parents) > 2:
        p1idx = np.random.randint(low = 0, high=len(parents)-1, size=1)
        p1 = parents.pop(p1idx)
        p2idx = np.random.randint(low = 0, high=len(parents)-1, size=1)
        p2 = parents.pop(p2idx)

        first_point_crossover = (np.random.uniform() < 0.2)
        second_point_crossover = (np.random.uniform() < 0.2)

        if first_point_crossover and second_point_crossover:
            child1 = p1[0:2] + p2[2:4] + p1[4:6]
            child2 = p2[0:2] + p1[2:4] + p2[4:6]
            children.append(child1)
            children.append(child2)
        elif first_point_crossover and not second_point_crossover:
            child1 = p1[0:2] + p2[2:6]
            child2 = p2[0:2] + p1[2:6]
            children.append(child1)
            children.append(child2)
        elif not first_point_crossover and second_point_crossover:
            child1 = p2[0:4] + p1[4:6]
            child2 = p1[0:4] + p2[4:6]
            children.append(child1)
            children.append(child2)
        else:
            children.append(p1)
            children.append(p2)

    return np.array(children)

def mutation(offspring, waterpoints):
    """randomly replace one bridge location for another"""
    for i in range(len(offspring)):
        child = offspring[i]

        for bridge in [0, 1, 2]:
            mutation = np.random.uniform() < 0.1
            if mutation:
                new_bridge = sample(waterpoints, 1)[0]

                #substitute new bridge for old bridge
                child[bridge*2] = new_bridge[0]
                child[bridge*2+1] = new_bridge[1]
        offspring[i] = child

    return offspring

def get_bridge_locations(level, box, doors):
    waterpoints = get_waterpoints(level, box)
    candidates = generate_candidates(waterpoints)

    # placeholder for list of doors
    surfacemap = get_surface_type_map(level, box)
    doordummy = np.argwhere(surfacemap == 2)
    idxs = np.random.randint(len(doordummy), size=5)
    doors = doordummy[idxs]

    # evaluate initial population
    sorted_candidates, sorted_fitness = sort_by_fitness(candidates, doors)
    best_fitness = -np.inf
    # average_fitness = -np.inf
    # worst_fitness = np.inf

    num_iterations = 10
    i = 0
    consecutive_same_best = 0
    while i < num_iterations and consecutive_same_best < 5:
        # generate offspring
        selected_parents = selection(sorted_candidates, sorted_fitness)
        offspring = crossover(selected_parents)
        offspring = mutation(offspring, waterpoints)

        # new_population = np.append(sorted_candidates, offspring)
        print(offspring.shape)
        print(sorted_candidates.shape)

        new_population = np.append(sorted_candidates, offspring, axis=0)

        # calculate fitness of new population
        sorted_candidates, sorted_fitness = sort_by_fitness(new_population, doors)
        sorted_candidates = sorted_candidates[:20]
        sorted_fitness = sorted_fitness[:20]

        # determine if population has converged
        new_best = sorted_fitness[0]
        if abs(new_best - best_fitness) < 0.5:
            consecutive_same_best += 1
        else:
            consecutive_same_best = 0
        if new_best > best_fitness:
            best_fitness = new_best

        print("Best fitness found: ")
        print(best_fitness)
        i+=1

    return sorted_candidates[0]

def find_bridge_box(level, box, bridge):
    coords = []
    surfacemap = get_surface_type_map(level, box)

    first_grass_n = np.argwhere(surfacemap[bridge[0,]] == 2)
    first_grass_e = np.argwhere(surfacemap[bridge[1,]] == 2)
    first_grass_s = np.argwhere(surfacemap[bridge[0,]] == 2)
    first_grass_w = np.argwhere(surfacemap[bridge[0,]] == 2)

    is first_grass_e - first_grass_w > first_grass_n - first_grass_s:
        horizontal = True
        for step in range(box.minx, box.maxx):
            coords.append([step, bridge[1]])

    else:
        horizontal = False 
        for step in range(box.minz, box.maxz):
            coords.append([bridge[0], step])
    return coords

def place_bridges(level, box, doors):
    bridge_coords = get_bridge_locations(level, box, doors)
    
    # split candidate in the 3 bridge locations
    bridge_loca = np.split(bridge_coords, 3)
    
    # find the rest of the bridgebox for each bridge
    for bridge in bridge_loca:
        box_coords = find_bridge_box(level, box, bridge)

        

def perform(level, box, options):
    place_bridges(level, box, [])