import bpy
import numpy as np
import open3d as o3d
import os

from b3Dv import Scene
from b3Dv import Mesh
from b3Dv import SunLight

suzanne = o3d.io.read_triangle_mesh('smooth_suzanne.obj')

V = np.asarray(suzanne.vertices)
V = np.column_stack((V[:, 0], V[:, 2], V[:, 1]))
F = np.asarray(suzanne.triangles)

float_attr = V[:, 2]
color_attr = np.hstack((V, np.ones((V.shape[0], 1))))

scene = Scene(resolution=(1080, 1080))

mesh = Mesh("numpyMesh", V, [], F, scale=(0.5,0.5,0.5))
mesh.addColorAttribute(color_attr, "color_attr")
mesh.addFloatAttribute(float_attr, "float_attr")

mesh.material.setColorAttributeAsColor("color_attr")
mesh.material.setFloatAttributeAsEmissionColor("float_attr")
mesh.material.setEmissionStrength(10)

mesh.setShadeSmooth()
mesh.asPointCloud()
scene.addObject(mesh)

floor = mesh.getFloor()
scene.addObject(floor)

sun = SunLight(rotation=(-30 * np.pi/180, 0, -10 * np.pi/180))
scene.addObject(sun)

camera = mesh.getCamera(azimuth=70 * np.pi/180, elevation=20 * np.pi/180, distance=2.5)
scene.addCamera(camera)

scene.setSamples(8)

scene.renderToFile(os.path.join(os.getcwd(), "output.png"))

bpy.ops.wm.save_mainfile(filepath = 'test.blend')
