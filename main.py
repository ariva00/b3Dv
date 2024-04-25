import bpy
import numpy as np
import open3d as o3d

from scipy.io import loadmat

from b3Dv.scene import Scene
from b3Dv.camera import Camera
from b3Dv.pointCloudNodes import MeshToPointCloudNodeTree
from b3Dv.mesh import Mesh
from b3Dv.materials import ColorAttributeMaterial, ColorRampAttributeMaterial
from b3Dv.lights import SunLight

bpy.ops.wm.read_homefile()
bpy.ops.object.select_all(action = 'SELECT')
bpy.ops.object.delete()

scene = Scene(resolution=(1080, 1080))
camera = Camera()
scene.addCamera(camera)

world = bpy.data.worlds.new("World")
scene.data.world = world
scene.data.render.filepath = "output.png"

suzanne = o3d.io.read_triangle_mesh('smooth_suzanne.obj')

V = np.asarray(suzanne.vertices)
V = np.column_stack((V[:, 0], V[:, 2], V[:, 1]))
F = np.asarray(suzanne.triangles)

pc = bpy.data.pointclouds.new(name='numpy point cloud')

mesh = Mesh("numpyMesh", V, [], F, scale=(0.5,0.5,0.5))

attr = V[:, 0]
mesh.addColorAttribute(np.ones((V.shape[0], 4)), "color_attr")
mesh.addFloatAttribute(attr, "float_attr")

material = ColorRampAttributeMaterial(color_attribute="float_attr", colors = [(0.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0,1,0,1), (1.0, 1.0, 1.0, 1.0)])

modifier = MeshToPointCloudNodeTree(material=material)
mesh.object.modifiers.new('MeshToPointCloud', 'NODES')
mesh.object.modifiers['MeshToPointCloud'].node_group = modifier.node_group
mesh.setLocation((0, 0, 1.4))
scene.addObject(mesh)

floor = mesh.getFloor()
scene.addObject(floor)

sun = SunLight(rotation=(-30 * np.pi/180, 0, -10 * np.pi/180))
scene.addObject(sun)

camera.setLocation((2,2,1.8))
camera.setRotation((80 * np.pi/180, 0 * np.pi/180, 135 * np.pi/180))

scene.data.cycles.samples = 60

bpy.ops.render.render(write_still = True, scene = scene.data.name)

bpy.ops.wm.save_mainfile(filepath = 'test.blend')
