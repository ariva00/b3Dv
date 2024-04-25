import bpy

class Mesh:
    def __init__(self, name="Mesh", vertices=[], edges=[], faces=[], location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)) -> None:
        self.data = bpy.data.meshes.new(name=name)
        self.data.from_pydata(vertices, [], faces)
        self.data.update()
        self.data.validate()
        self.object = bpy.data.objects.new(name, self.data)
        self.object.location = location
        self.object.rotation_euler = rotation
        self.object.scale = scale

    def addFloatAttribute(self, data, name="value", domain="POINT"):
        attribute = self.object.data.attributes.new(name=name, type='FLOAT', domain=domain)
        attribute.data.foreach_set('value', data.ravel())

    def addColorAttribute(self, data, name="value", domain="POINT"):
        attribute = self.object.data.attributes.new(name=name, type='FLOAT_COLOR', domain=domain)
        attribute.data.foreach_set('color', data.ravel())

    def getMinZ(self):
        minz = float('inf')
        for vert in self.data.vertices:
            if vert.co[2] < minz:
                minz = vert.co[2]
        return minz
    
    def getMaxZ(self):
        maxz = -float('inf')
        for vert in self.data.vertices:
            if vert.co[2] > maxz:
                maxz = vert.co[2]
        return maxz
    
    def setLocation(self, location=(0, 0, 0)):
        self.object.location = location

    def getFloor(self,  size = (10,10), shadow_catcher = True):
        minz = self.getMinZ()
        verices = [
            (-size[0]/2, -size[0]/2, 0),
            (-size[0]/2, size[0]/2, 0),
            (size[0]/2, size[0]/2, 0),
            (size[0]/2, -size[0]/2, 0),
        ]
        faces = [
            (0, 1, 2, 3)
        ]
        floor = Mesh("Floor", vertices=verices, faces=faces, location=(0,0, minz + self.object.location.z))
        floor.object.is_shadow_catcher = shadow_catcher
        return floor