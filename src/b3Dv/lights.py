import bpy

class SunLight:

    def __init__(self, name="Sun", location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), strength=5.0):
        self.data = bpy.data.lights.new(name, 'SUN')
        self.object = bpy.data.objects.new(name, self.data)
        self.object.location = location
        self.object.rotation_euler = rotation
        self.object.scale = scale
        self.data.energy = strength

    def setLocation(self, location):
        self.object.location = location

    def setRotation(self, rotation):
        self.object.rotation_euler = rotation

    def setScale(self, scale):
        self.object.scale = scale

    def setStrength(self, strength):
        self.data.energy = strength