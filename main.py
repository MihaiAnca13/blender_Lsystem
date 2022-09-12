import sys

sys.path.append('D:/Projects/blender_connection/')

from importlib import reload
import myutils
import lsystem
reload(lsystem)
reload(myutils)

from tqdm import tqdm
from myutils import *
from lsystem import Lsystem
from omegaconf import OmegaConf

DEBUG = False

conf = OmegaConf.load('D:/Projects/blender_connection/configs/config.yaml')

result = conf.axiom
rules = smart_dict(conf.rules)

for n in range(conf.iterations):
    new = ""
    for c in result:
        new = new + rules[c]
    result = new
print(result)

lsystem = Lsystem(angle=conf.angle)

for ix, c in tqdm(enumerate(result), total=len(result)):
    lsystem.interpret(c)

    if DEBUG:
        print(ix, c, lsystem.location, lsystem.rotation)

bpy.ops.object.editmode_toggle()
bpy.ops.object.shade_smooth()
