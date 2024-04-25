import bpy

class Camera:

    def __init__(self, name="Camera", location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.data = bpy.data.cameras.new(name)
        self.object = bpy.data.objects.new(name, self.data)
        self.object.location = location
        self.object.rotation_euler = rotation
        self.object.scale = scale
    
    def setFocalLength(self, focal_length):
        self.data.lens = focal_length

    def setLocation(self, location):
        self.object.location = location

    def setRotation(self, rotation):
        self.object.rotation_euler = rotation

    def setScale(self, scale):
        self.object.scale = scale