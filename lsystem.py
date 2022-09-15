from myutils import *
import math
import numpy as np
from copy import deepcopy
from scipy.spatial.transform import Rotation as R


class Lsystem:
    def __init__(self, starting_location=None, starting_rotation=None, step_size=0.1, angle=90):
        location = [0, 0, 0]
        rotation = [0, 0, 0]
        if starting_location is not None:
            location = starting_location
        if starting_rotation is not None:
            rotation = starting_rotation

        self.transform = np.eye(4)
        rotation_matrix = R.from_euler('xyz', rotation, degrees=True)
        self.transform[:3, :3] = rotation_matrix.as_matrix()
        self.transform[:3, -1] = location

        self.step_size = step_size

        # TODO: add a way to check if segment there already
        self.saved_transform = []
        self.first_obj = True
        self.angle = degrees_to_rads(angle)

    def rotation_around(self, axis, angle):
        m = np.eye(4)
        m[:3, :3] = R.from_euler(axis, angle, degrees=False).as_matrix()
        self.transform = np.matmul(self.transform, m)

    def interpret(self, symbol):
        match symbol:
            case 'F':
                self.handle_F()
            case 'f':
                self.handle_f()
            case '+':
                self.handle_plus()
            case '-':
                self.handle_minus()
            case '[':
                self.handle_save()
            case ']':
                self.handle_load()

    def handle_F(self):
        m = np.eye(4)
        m[2, -1] = self.step_size
        new_transform = np.matmul(self.transform, m)

        rotation = R.from_matrix(self.transform[:3, :3]).as_euler('xyz', degrees=False)
        old_location = self.transform[:3, -1]
        new_location = new_transform[:3, -1]
        cylinder_between(*old_location, *new_location, rotation)

        if self.first_obj:
            bpy.ops.object.editmode_toggle()
            self.first_obj = False

        self.transform = new_transform

    def handle_f(self):
        m = np.eye(4)
        m[2, -1] = self.step_size
        self.transform = np.matmul(m, self.transform)

    def handle_plus(self):
        self.rotation_around('y', self.angle)

    def handle_minus(self):
        self.rotation_around('y', -self.angle)

    def handle_save(self):
        self.saved_transform.append(deepcopy(self.transform))

    def handle_load(self):
        self.transform = self.saved_transform.pop()
