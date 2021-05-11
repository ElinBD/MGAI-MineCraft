
import utilityFunctions as utilityFunctions
import numpy as np
import sys

from pymclevel import box as boundingBox
from Beautiful_meta_analysis import get_height_map


inputs = (
	("Beautiful short path", "label"),
	("Creator: Jerry", "label")
	)

class Block:
  def __init__(self, top, bottom, left, right):  
    # Absolute height difference between itself and surrounding blocks
    self.surroundings = [top, right, bottom, left]

    self.dst = sys.maxsize  # Minimum distance found (default -> not reachable)
    self.shortest = False   # Has shortest path been found
  
  # ==== Various Getter and Setter methods ====
  def get_neighbour(self, i):
    return self.surroundings[i]
  
  def set_dst(self, d):
    self.dst = d
  
  def get_dst(self):
    return self.dst

  def set_shortest(self):
    self.shortest = True

  def get_shortest(self):
    return self.shortest
  # ===========================================


class Graph:
  ROAD = (35, 10)  # Road block
  FACTOR = 1

  dx = [-1, 0, 1, 0]  # Top, Right, Bottom, Left
  dz = [0, 1, 0, -1]

  def __init__(self, level, box, height_map, size, start, end):
    self.graph = []
    self.size_x, self.size_z = size[0], size[2]

    self.x1, self.z1 = start  # Starting point
    self.x2, self.z2 = end    # End point

    self.shortest_found = 0   # Blocks for which shortest path is found

    origin = box.origin
    utilityFunctions.setBlock(level, (5,0), origin[0], 10, origin[2])

    # Create the graph, each node is a block which contains the height difference with its surrounding blocks
    # If pre-existing road block found -> subtract FACTOR to enforce that those paths are reused
    for x in range(self.size_x):
      column = []
      for z in range(self.size_z):
        top, bottom, left, right = None, None, None, None
        height = height_map[x][z]

        if self.on_map(x-1, z): # Top
          block = origin.__add__(boundingBox.Vector(x-1, height_map[x-1][z], z))
          top = 1 + abs(height - height_map[x-1][z]) - self.FACTOR * self.is_road_block(level, block)

        if self.on_map(x+1, z): # Bottom
          block = origin.__add__(boundingBox.Vector(x+1, height_map[x+1][z], z))
          bottom = 1 + abs(height - height_map[x+1][z]) - self.FACTOR * self.is_road_block(level, block)
        
        if self.on_map(x, z-1): # Left
          block = origin.__add__(boundingBox.Vector(x, height_map[x][z-1], z-1))
          left = 1 + abs(height - height_map[x][z-1]) - self.FACTOR * self.is_road_block(level, block)
        
        if self.on_map(x, z+1): # Right
          block = origin.__add__(boundingBox.Vector(x, height_map[x][z+1], z+1))
          right = 1 + abs(height - height_map[x][z+1]) - self.FACTOR * self.is_road_block(level, block)
        
        column.append(Block(top, bottom, left, right))
      self.graph.append(column)

  # Check if given (x,z) is already a road block
  def is_road_block(self, level, block):
    return int(level.blockAt(block[0], block[1]-1, block[2]) == self.ROAD[0])
  
  # Checks whether the given (relative) coordinates are in the box
  def on_map(self, x, z):
    if x < 0 or x >= self.size_x:
      return False
    if z < 0 or z >= self.size_z:
      return False
    return True
  
  # Retrieve new block with lowest distance where shortest=false
  def get_new_block(self):
    min_dst = sys.maxsize
    coordinates = (-1, -1)
    for x in range(self.size_x):
      for z in range(self.size_z):
        if not self.graph[x][z].get_shortest() and self.graph[x][z].get_dst() < min_dst:
          min_dst = self.graph[x][z].get_dst()
          coordinates = (x, z)
    return coordinates

  # Update minimum distance for each of the blocks in the graph
  def Dijkstra(self):
    print "NOT WORKING RIGHT NOW DUE TO PRIM"
    return

    # Initialization
    self.graph[self.x1][self.z1].set_dst(0)

    x, z = self.get_new_block()  # Get starting block
    # Terminate when shortest path is found to the end point
    while self.shortest_found != self.size_x*self.size_z and \
          not self.graph[self.x2-1][self.z2-1].get_shortest():
      self.graph[x][z].set_shortest()
      self.shortest_found += 1

      # Update min distance for surrounding blocks
      
      for i in range(4):  # 4 potential neighbours for each block
        if self.graph[x][z].get_neighbour(i):
          dst = self.graph[x][z].get_dst() + self.graph[x][z].get_neighbour(i)
          self.graph[x+self.dx[i]][z+self.dz[i]].set_dst(min(self.graph[x+self.dx[i]][z+self.dz[i]].get_dst(), dst))

      x, z = self.get_new_block()  # Get next block
  
  # Determine shortest path between two points
  def Prim(self):
    selected = np.zeros((self.size_x, self.size_z), dtype=bool)
    selected[self.x1][self.z1] = True
    self.graph[self.x1][self.z1].set_dst(0)
    n_nodes = 0
    total_nodes = self.size_x*self.size_z

    adlist = [ [ [] for _ in range(self.size_z) ] for _ in range(self.size_x) ]  # Adjacency list

    while n_nodes < total_nodes - 1 and not selected[self.x2-1][self.z2-1]:
      minimum = sys.maxsize
      i, j = (-1,-1), (-1,-1)  # i = node added to adlist | j = new selected node
      # Walk through all blocks
      for x in range(self.size_x):
        for z in range(self.size_z):
          if selected[x][z]:
            # Walk through all neighbours of selected block
            for k in range(4):
              if self.on_map(x+self.dx[k], z+self.dz[k]) and not selected[x+self.dx[k]][z+self.dz[k]]:  # Neighbour should not already be selected
                dist = self.graph[x][z].get_neighbour(k) + self.graph[x][z].get_dst()
                if minimum > dist:
                  minimum = dist
                  i, j = (x,z), (x+self.dx[k], z+self.dz[k])  # i = node added to adlist | j = new selected node
      
      adlist[i[0]][i[1]].append(j)  # Add to adjacency list

      selected[j[0]][j[1]] = True
      self.graph[j[0]][j[1]].set_dst(minimum)
      n_nodes += 1
    
    return adlist


# Connect points p1 and p2 with a road
# Road is based on Dijkstra's shortests path algorithm
def connect_points(level, box, p1, p2):
  # Convert absolute points to relative points
  start = (p1[0] - box.origin[0], p1[2] - box.origin[2])
  end = (p2[0] - box.origin[0], p2[2] - box.origin[2])

  height_map = get_height_map(level, box)
  G = Graph(level, box, height_map, box.size, start, end)
  adlist = G.Prim()

  """ PRINTS THE ADJACENCY LIST
  for x in range(box.size[0]):
    for z in range(box.size[2]):
      point = (x,z)
      string = ""
      for item in adlist[x][z]:
        string += str(item)
      print str(point) + " -> " + string
  """
  
  # Find path from end -> start with the adlist
  cur = (end[0]-1, end[1]-1)
  path = [cur]
  while not cur == start:
    for x in range(box.size[0]):
      for z in range(box.size[2]):
        if cur in adlist[x][z]:
          cur = (x,z)
          path.append((x,z))

  # Create pathblocks 
  for block in path:
    utilityFunctions.setBlock(level, G.ROAD, 
                              box.origin[0]+block[0], 
                              box.origin[1]+height_map[block[0]][block[1]]-1,
                              box.origin[2]+block[1])

def perform(level, box, options):
  connect_points(level, box, box.origin, box.maximum)