import utilityFunctions as utilityFunctions
import math
import random

from Beautiful_meta_analysis import get_height_map

inputs = (
	("Beautiful roads", "label"),
	("Creator: Jerry", "label")
	)

P_ROAD = 0.01
THRESHOLD = 60

def normalize(x, z):
  if abs(x) > abs(z):
    return x/abs(x), z/abs(x)
  else:
    return x/abs(z), z/abs(z)


# Draw main road, starting from point of circle
def draw_main_road(level, x_origin, z_origin, y_origin, dx, dz):
  dx, dz = normalize(dx, dz)
  R1 = random.randint(0,1)
  factor = [-1, 1]

  for i in range(40):
    R2 = random.randint(0,1)
    if R1 == 0:  # Make the road curve a bit
      dx += 0.05*factor[R2]
    else:
      dz += 0.05*factor[R2]

    x = x_origin+round(i*dx)
    z = z_origin+round(i*dz)

    utilityFunctions.setBlock(level, (35,10), x+1, y_origin, z)
    utilityFunctions.setBlock(level, (35,10), x-1, y_origin, z)
    utilityFunctions.setBlock(level, (35,10), x+1, y_origin, z+1)
    utilityFunctions.setBlock(level, (35,10), x-1, y_origin, z-1)
    utilityFunctions.setBlock(level, (35,10), x, y_origin, z+1)
    utilityFunctions.setBlock(level, (35,10), x, y_origin, z-1)
    utilityFunctions.setBlock(level, (35,10), x, y_origin, z)


# If len=360 -> draw full circle
def draw_circle(level, x_origin, z_origin, y_origin, r, scalar_x, scalar_z, len, start, block, main_road, connect):
  angle_between = THRESHOLD
  for alpha in range(start, len+start):
    x = round(x_origin + scalar_x * r * math.cos(math.pi*alpha/180))
    z = round(z_origin - scalar_z * r * math.sin(math.pi*alpha/180))
    
    if main_road and angle_between == THRESHOLD:
      angle_between = 0
      dx = x - x_origin
      dz = z - z_origin
      draw_main_road(level, x, z, y_origin, dx, dz)
    
    prev_x = x
    prev_z = z
    
    angle_between += 1
    utilityFunctions.setBlock(level, block, x, y_origin, z)

  if main_road:
    dx = x - x_origin
    dz = z - z_origin
    draw_main_road(level, x, z, y_origin, dx, dz)


def perform(level, box, options):
  utilityFunctions.setBlock(level, (1,0), 0, 3, 0)
  scalar_x = 1  # TODO: create list from which scalars can be chosen
  scalar_z = 1
  len = random.randint(270, 360)
  start = random.randint(1, 270)
  draw_circle(level, 0, 0, 3, 7, scalar_x, scalar_z, len, start, (1,0), False, False)
  draw_circle(level, 0, 0, 3, 8, scalar_x, scalar_z, len, start, (1,0), False, False)
  draw_circle(level, 0, 0, 3, 9, scalar_x, scalar_z, len, start, (1,0), True, False)

  # Outer wall
  draw_circle(level, 0, 0, 3, 40, scalar_x, scalar_z, 360, 0, (35,3), False, True)
  draw_circle(level, 0, 0, 3, 41, scalar_x, scalar_z, 360, 0, (35,3), False, True)