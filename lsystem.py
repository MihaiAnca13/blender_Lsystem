from myutils import *
import math
import numpy as np
from copy import deepcopy


class Lsystem:
    def __init__(self, starting_location=None, starting_rotation=None, step_size=0.1, angle=90):
        self.location = [0, 0, 0]
        self.rotation = [0, 0, 0]
        if starting_location is not None:
            self.location = starting_location
        if starting_rotation is not None:
            self.rotation = starting_rotation

        self.step_size = step_size

        self.locations_done = {}
        self.saved_location = []
        self.saved_rotation = []
        self.first_obj = True
        self.angle = degrees_to_rads(angle)

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

        # keep rotations between [-2*PI, 2*PI]
        self.rotation[1] = abs(self.rotation[1]) % (2 * math.pi) * np.sign(self.rotation[1])

    def handle_F(self):
        new_x = self.location[0] + math.sin(self.rotation[1]) * self.step_size
        new_z = self.location[2] + math.cos(self.rotation[1]) * self.step_size

        if str([new_x, self.location[1], new_z]) not in self.locations_done:
            cylinder_between(self.location[0], self.location[1], self.location[2], new_x, self.location[1], new_z,
                             self.rotation)

            if self.first_obj:
                bpy.ops.object.editmode_toggle()
                self.first_obj = False

        self.location[0] = new_x
        self.location[2] = new_z
        self.locations_done[str(self.location)] = True

    def handle_f(self):
        self.location[0] = self.location[0] + math.sin(self.rotation[1]) * self.step_size
        self.location[2] = self.location[2] + math.cos(self.rotation[1]) * self.step_size
        self.locations_done[str(self.location)] = True

    def handle_plus(self):
        self.rotation[1] += self.angle

    def handle_minus(self):
        self.rotation[1] -= self.angle

    def handle_save(self):
        self.saved_location.append(deepcopy(self.location))
        self.saved_rotation.append(deepcopy(self.rotation))

    def handle_load(self):
        self.location, self.rotation = self.saved_location.pop(), self.saved_rotation.pop()
