
import utilityFunctions as utilityFunctions
import numpy as np
import sys

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
  def __init__(self, height_map, size, start, end):
    self.graph = []
    self.size_x, self.size_z = size[0], size[2]

    self.x1, self.z1 = start  # Starting point
    self.x2, self.z2 = end    # End point

    self.shortest_found = 0   # Blocks for which shortest path is found

    # Create the graph, each node is a block which contains the height difference with its surrounding blocks
    for x in range(self.size_x):
      column = []
      for z in range(self.size_z):
        top, bottom, left, right = None, None, None, None
        height = height_map[x][z]

        if self.on_map(x-1, z): # Top
          top = abs(height - height_map[x-1][z])
        if self.on_map(x+1, z): # Bottom
          bottom = abs(height - height_map[x+1][z])
        if self.on_map(x, z-1): # Left
          left = abs(height - height_map[x][z-1])
        if self.on_map(x, z+1): # Right
          right = abs(height - height_map[x][z+1])
        
        column.append(Block(top, bottom, left, right))
      self.graph.append(column)
  
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
    # Initialization
    self.graph[self.x1][self.z1].set_dst(0)

    x, z = self.get_new_block()  # Get starting block
    # Terminate when shortest path is found to the end point
    while self.shortest_found != self.size_x*self.size_z and \
          not self.graph[self.x2-1][self.z2-1].get_shortest():
      self.graph[x][z].set_shortest()
      self.shortest_found += 1

      # Update min distance for surrounding blocks
      dx = [-1, 0, 1, 0]  # Top, Right, Bottom, Left
      dz = [0, 1, 0, -1]
      for i in range(4):  # 4 potential neighbours for each block
        if self.graph[x][z].get_neighbour(i):
          dst = self.graph[x][z].get_dst() + self.graph[x][z].get_neighbour(i)
          self.graph[x+dx[i]][z+dx[i]].set_dst(min(self.graph[x+dx[i]][z+dx[i]].get_dst(), dst))

      x, z = self.get_new_block()  # Get next block
  

  def Prim(self):
    selected = np.zeros((self.size_x, self.size_x), dtype=int)
    selected[self.x1][self.z1] = True
    n_nodes = 0
    total_nodes = self.size_x*self.size_z

    adlist = [ [ [] for _ in range(self.size_z) ] for _ in range(self.size_x) ]  # Adjacency list

    dx = [-1, 0, 1, 0]  # Top, Right, Bottom, Left
    dz = [0, 1, 0, -1]

    while n_nodes < self.size_x*self.size_z - 1:
      minimum = sys.maxsize
      i, j = 0, 0
      # Walk through all blocks
      for x in range(self.size_x):
        for z in range(self.size_z):
          if selected[x][z]:
            # Walk through all neighbours of selected block
            for k in range(4):
              if self.on_map(x+dx[k], z+dz[k]) and not selected[x+dx[k]][z+dz[k]]:  # Neighbour should not already be selected
                if minimum > self.graph[x][z].get_neighbour(k):
                  minimum = self.graph[x][z].get_neighbour(k)
                  i, j = (x,z), (x+dx[k], z+dz[k])

      adlist[i[0]][i[1]].append(j)  # Add to adjacency list

      selected[j[0]][j[1]] = True
      n_nodes += 1
    
    return adlist


# Connect points p1 and p2 with a road
# Road is based on Dijkstra's shortests path algorithm
def connect_points(level, box, p1, p2):
  # Convert absolute points to relative points
  start = (p1[0] - box.origin[0], p1[2] - box.origin[2])
  end = (p2[0] - box.origin[0], p2[2] - box.origin[2])

  height_map = get_height_map(level, box)
  G = Graph(height_map, box.size, start, end)
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
    utilityFunctions.setBlock(level, (35,10), 
                              box.origin[0]+block[0], 
                              box.origin[1]+height_map[block[0]][block[1]]-1,
                              box.origin[2]+block[1])

def perform(level, box, options):
  connect_points(level, box, box.origin, box.maximum)