import bpy
import math
import numpy as np
from collections import defaultdict

import sys

sys.path.append('//')


class smart_dict(dict):
    @staticmethod
    def __missing__(key):
        return key


def cylinder_between(x1, y1, z1, x2, y2, z2, rot, r = 0.2, verts = 8):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    dist = math.sqrt(dx**2 + dy**2 + dz**2)

    bpy.ops.mesh.primitive_cylinder_add(
        radius = r,
        depth = dist,
        vertices = verts,
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1),
        rotation= rot
    )


result = '-L'
rules = smart_dict({
    'L': "LF+RFR+FL-F-LFLFL-FRFR+",
    'R': "-LFLF+RFRFR+F+RF-LFL-FR"
})
angle = math.pi / 2
iterations = 3
new = ""
for n in range(iterations):
    for c in result:
        new = new + rules[c]
    result = new
print(result)

location = [0, 0, 0]
rotation = [0, 0, 0]

locations_done = {}

first_obj = True
for ix, c in enumerate(result):
    if c == 'F':
        new_x = location[0] + math.sin(rotation[1])
        new_z = location[2] + math.cos(rotation[1])

        if str([new_x, location[1], new_z]) not in locations_done:
            cylinder_between(location[0], location[1], location[2], new_x, location[1], new_z, rotation)

            if first_obj:
                bpy.ops.object.editmode_toggle()
                first_obj = False

        location[0] = new_x
        location[2] = new_z
        locations_done[str(location)] = True
    elif c == '+':
        rotation[1] += angle
    elif c == '-':
        rotation[1] -= angle
    rotation[1] = abs(rotation[1]) % (2 * math.pi) * np.sign(rotation[1])

    print(ix, c, location, rotation)

bpy.ops.object.editmode_toggle()
bpy.ops.object.shade_smooth()
