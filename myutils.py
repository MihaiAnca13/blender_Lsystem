import math
import bpy

def degrees_to_rads(angle):
    return angle * math.pi / 180


class smart_dict(dict):
    @staticmethod
    def __missing__(key):
        return key


def cylinder_between(x1, y1, z1, x2, y2, z2, rot, r=0.03, verts=6):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    dist = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=r,
        depth=dist,
        vertices=verts,
        location=(dx / 2 + x1, dy / 2 + y1, dz / 2 + z1),
        rotation=rot
    )
