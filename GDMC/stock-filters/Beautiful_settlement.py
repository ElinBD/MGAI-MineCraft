# Generates a beautiful settlement given a level and box

import utilityFunctions as utility
import numpy as np
import random
import math

from Beautiful_settings import *


inputs = (
	("Beautiful Settlement Generator", "label"),
	("Creators: Koen, Elin, Tim, Sem, Jerry", "label")
	)


# Stores data about one building
class Building:
  def __init__(self, P, length, width, front):
    self.P = P
    self.length = length
    self.width = width
    self.front = front  # North = 0, West = 1, South = 2, East = 3


# Create settlement
class Settlement:
  def __init__(self, level, box):
    self.level = level
    self.box = box

    self.box_origin_height = self.box.origin[1]  # Height of origin block in box

    # Centerpoint of settlement
    self.origin = (0,3,0)  # TODO
    self.x_origin = self.origin[0]
    self.y_origin = self.origin[1]
    self.z_origin = self.origin[2]

    # Relative height map of given box
    self.height_map = np.zeros((box.size[0], box.size[2]), dtype=int) # TODO

    # Meta information
    self.buildings = []  # Plots of the buildings


  # Place a grid of 3x3 blocks at given (x,z)
  def __place_grid(self, block, x, z, y_offset):
    for i in range(-1, 2):
      for j in range(-1, 2):
        y = self.__get_height(x+i, z+j) + y_offset
        utility.setBlock(self.level, block, x+i, y, z+j)


  # Get absolute height at point (x,z)
  def __get_height(self, x, z):
    return self.box_origin_height + self.height_map[x][z]


  # Generate canal from P0 to P1
  def __generate_canal(self, P0, P1):
    lst = utility.raytrace(P0, P1)
    for block in lst:
      self.__place_grid(WATER, block[0], block[2], 0)
      self.__place_grid(AIR, block[0], block[2], 1)


  # Generate inner canals from P1 and P2 to center, then to P0
  def __generate_inner_canals(self, P0, P1, P2):
    cross_x = self.x_origin+random.randint(-OFFSET_CROSSPOINT, OFFSET_CROSSPOINT)
    cross_z = self.z_origin+random.randint(-OFFSET_CROSSPOINT, OFFSET_CROSSPOINT)
    crosspoint = (cross_x, self.__get_height(cross_x, cross_z), cross_z)
    
    self.__generate_canal(P1, crosspoint)
    self.__generate_canal(P2, crosspoint)
    self.__generate_canal(P0, crosspoint)


  # Generate canals surrounding the settlement, has a gear-like shape
  # Also preparations for the three smaller canals
  def __generate_canals(self, outer_r, inner_r):
    length = 0   # Current length of a gear-segment
    outer = bool(random.randint(0,1))  # Start with inner/outer part
    init_outer = outer  # Save value of first outer

    # Angle at which the inner canal starts
    R0 = random.randint(0, MAX_L_INNER)  # Left inner canal
    R1 = random.randint(MIN_T_INNER, MAX_T_INNER)  # Top inner canal
    R2 = random.randint(MIN_B_INNER, MAX_B_INNER)  # Bottom inner canal

    # Generate canals
    for alpha in range(0, 360):
      x_outer = int(self.x_origin + outer_r * math.cos(math.pi*alpha/180))
      z_outer = int(self.z_origin + outer_r * math.sin(math.pi*alpha/180))
      y_outer = self.__get_height(x_outer, z_outer)

      x_inner = int(self.x_origin + inner_r * math.cos(math.pi*alpha/180))
      z_inner = int(self.z_origin + inner_r * math.sin(math.pi*alpha/180))
      y_inner = self.__get_height(x_inner, z_inner)

      # Switch between inner and outer circle
      if length >= MIN_LENGTH_C and 360-alpha > MIN_LENGTH_C and random.uniform(0,1) <= P_SWITCH:
        outer = not outer
        length = 0

        # Connect outer and inner parts
        lst = utility.raytrace((x_outer, y_outer, z_outer), (x_inner, y_inner, z_inner))
        for block in lst:
          self.__place_grid(WATER, block[0], block[2], 0)
      
      if outer:
        self.__place_grid(WATER, x_outer, z_outer, 0)
      else:
        self.__place_grid(WATER, x_inner, z_inner, 0)

      # Record points from which there will be canals within the gear shape
      if alpha == R0:
        P0 = (x_outer, y_outer, z_outer) if outer else (x_inner, y_inner, z_inner)
      elif alpha == R1:
        P1 = (x_outer, y_outer, z_outer) if outer else (x_inner, y_inner, z_inner)
      elif alpha == R2:
        P2 = (x_outer, y_outer, z_outer) if outer else (x_inner, y_inner, z_inner)
            
      length += 1
    
    # Connect ends of canals if current is not the same as the initial
    if not outer == init_outer:
      lst = utility.raytrace((x_outer, y_outer, z_outer), (x_inner, y_inner, z_inner))
      for block in lst:
        self.__place_grid(WATER, block[0], block[2], 0)

    return P0, P1, P2
  

  # Count number of water blocks surrounding the given coordinates
  # Grid: 5x5
  def __count_water(self, x, z):
    count = 0
    for i in range(-2, 3):
      for j in range(-2, 3):
        if i == 0 and j == 0:
          continue
        y = self.__get_height(x+i, z+j)
        if self.level.blockAt(x+i, y, z+j) == WATER[0]:
          count += 1
    return count


  # Generates the foundation of the settlement and adds walls surrounding it
  # Outer_r is necessary to know how far to look
  def __foundation_and_walls(self, outer_r):
    max_radius = np.full(360, outer_r, dtype=int)  # Max radius at which water is found per alpha

    for r in range(1, outer_r):
      for alpha in range(0, 360):
        if r > max_radius[alpha]:  # Skip, water found
          continue
        
        x = int(self.x_origin + r * math.cos(math.pi*alpha/180))
        z = int(self.z_origin + r * math.sin(math.pi*alpha/180))
        
        # Manual placement of 3x3 grid
        for i in range(-1, 2):
          for j in range(-1, 2):
            y = self.__get_height(x+i, z+j)
            if not self.level.blockAt(x+i, y, z+j) == WATER[0]:
              if self.__count_water(x+i, z+j) > 0:  # Create wall
                utility.setBlock(self.level, OUTER_WALL, x+i, y, z+j)  # TODO
              else:  # Foundation floor
                utility.setBlock(self.level, ROAD, x+i, y, z+j)

        if self.level.blockAt(x, self.__get_height(x, z), z) == WATER[0]:
          max_radius[alpha] = r  # Inner ring found for current alpha, update max_radius
        

  # Check if space between points P1 and P2 is available
  # Available -> no buildings
  def __available(self, P1, P2):
    for x in range(P1[0], P2[0]):
      for z in range(P1[1], P2[1]):
        y = self.__get_height(x, z)
        if not self.level.blockAt(x, y, z) == ROAD[0]:  # Not road -> not empty
          return False
    return True


  # Compute number of free blocks in every direction around building
  # Returns optimal direction
  def __compute_space(self, building):
    P1_x, P1_y, P1_z = building[0][0], building[0][1], building[0][2]
    length, width = building[1][0], building[1][1]

    space = np.zeros(4, dtype=int)
    indices = range(4)

    for x in range(P1_x-3, P1_x+length+3):
      for z in range(P1_z-3, P1_x+width+3):
        y = self.__get_height(x, z)
        block = self.level.blockAt(x, y, z)
        if not P1_x <= x < P1_x+length:
          if x < P1_x and (block == ROAD[0] or block == WATER[0]):  # EAST
            space[1] += 1
            if block == WATER[0]:  # Point towards canal
              space[1] += CANAL_VALUE
          elif x > P1_x+length-1 and (block == ROAD[0] or block == WATER[0]):  # WEST
            space[3] += 1
            if block == WATER[0]:  # Point towards canal
              space[3] += CANAL_VALUE
        if not P1_z <= z < P1_z+width:
          if z < P1_z and (block == ROAD[0] or block == WATER[0]):  # SOUTH
            space[2] += 1
            if block == WATER[0]:  # Point towards canal
              space[2] += CANAL_VALUE
          elif z > P1_z+width-1 and (block == ROAD[0] or block == WATER[0]):  # NORTH
            space[0] += 1
            if block == WATER[0]:  # Point towards canal
              space[0] += CANAL_VALUE
    
    # If multiple indices have max value, shuffle indices and space with same seed
    R = random.randint(0, 10000)  # Create random seed
    random.seed(R)
    random.shuffle(space)
    random.seed(R)
    random.shuffle(indices)
    return indices[np.argmax(space)]


  # Determine front of every building based on space around it
  # Also creates a new Building object, storing all necessary data
  def __determine_front(self, temp):
    for building in temp:
      # NORTH = 0, EAST = 1, SOUTH = 2, WEST = 3
      i = self.__compute_space(building)

      # TODO: remove =====================================================
      P1_x, P1_y, P1_z = building[0][0], building[0][1], building[0][2]
      length, width = building[1][0], building[1][1]
      if i == 1:
        for z in range(0, width):
          y = self.__get_height(P1_x, P1_z+z)
          utility.setBlock(self.level, (57,0), P1_x, 3, P1_z+z)
      elif i == 0:
        for x in range(0, length):
          y = self.__get_height(P1_x+x, P1_z+width+1)
          utility.setBlock(self.level, (57,0), P1_x+x, 3, P1_z+width-1)
      elif i == 2:
        for x in range(0, length):
          y = self.__get_height(P1_x+x, P1_z)
          utility.setBlock(self.level, (57,0), P1_x+x, 3, P1_z)
      elif i == 3:
        for z in range(0, width):
          y = self.__get_height(P1_x+length-1, P1_z+z)
          utility.setBlock(self.level, (57,0), P1_x+length-1, 3, P1_z+z)
      # ==================================================================

      self.buildings.append(Building(building[0], length, width, i))  # Add new building


  # Create plots on which the buildings can be generated
  def __place_plots(self, outer_r):
    temp = []  # Temporal storage of buildings

    for z in range(-1*outer_r, outer_r, 2):
      width_plot = random.randint(MIN_WIDTH, MAX_WIDTH)
      for x in range(-1*outer_r, outer_r, 1):
        length_plot = random.randint(MIN_LENGTH, MAX_LENGTH)
        if self.__available((x-1, z-1), (x+length_plot+1, z+width_plot+1)):
          if random.uniform(0,1) <= P_PLOT:
            y = self.__get_height(x,z)
            # TODO: remove when done? OR EASTER EGG -> diamond foundation
            for i in range(x, x+length_plot):  # Mark plot
              for j in range(z, z+width_plot):
                utility.setBlock(self.level, (35,12), i, self.__get_height(i,j), j)
            # ===========================================================
            temp.append( [(x, y, z), (length_plot, width_plot)] )
    
    self.__determine_front(temp)
  

  # Generate a building on top of each plot
  def __generate_buildings(self):
    for building in self.buildings:
      pass
      # TODO: generate(self.level, building.P, building.length, building.width, building.front)


  # Generates the settlement
  def generate(self):
    # Radius of outer and inner circles, forming the gear-shape 
    outer_r, inner_r = random.randint(MIN_OUTER, MAX_OUTER), random.randint(MIN_INNER, MAX_INNER)

    P0, P1, P2 = self.__generate_canals(outer_r, inner_r)  # Canals surrounding the settlement
    self.__foundation_and_walls(outer_r)  # Foundation of settlement + walls
    self.__generate_inner_canals(P0, P1, P2)  # Three inner canals

    self.__place_plots(outer_r)  # Generate random plots for the buildings
    self.__generate_buildings()


# Starting point of generating the beautiful settlement
def perform(level, box, options):
  S = Settlement(level, box)
  S.generate()