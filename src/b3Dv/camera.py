import bpy
import numpy as np

class Camera:

    def __init__(self, name="Camera", location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), focal_length=50):
        self.data = bpy.data.cameras.new(name)
        self.object = bpy.data.objects.new(name, self.data)
        self.setLocation(location)
        self.setRotation(rotation)
        self.setScale(scale)
        self.setFocalLength(focal_length)
    
    def setFocalLength(self, focal_length):
        self.data.lens = focal_length

    def setLocation(self, location):
        self.object.location = location

    def setRotation(self, rotation):
        self.object.rotation_euler = rotation

    def setScale(self, scale):
        self.object.scale = scale

    def focusOnPoint(self, point, azimuth=np.pi/4, elevation=np.pi/9, distance=3):
        x = distance * np.cos(azimuth) * np.cos(elevation)
        y = distance * np.sin(azimuth) * np.cos(elevation)
        z = distance * np.sin(elevation)
        coords = np.array((x, y, z)) + point
        rotation = (np.pi/2 - elevation, 0, azimuth + np.pi/2)
        self.setLocation(coords)
        self.setRotation(rotation)
