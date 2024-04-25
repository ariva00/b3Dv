import bpy

class Scene:

    def __init__(self, name="Scene", engine="CYCLES", device="GPU", resolution=(1920, 1080), transparent=True) -> None:
        self.data = bpy.data.scenes.new(name)
        self.setRenderEngine(engine=engine)
        self.setDevice(device=device)
        self.setResolution(resolution)
        self.data.render.film_transparent = transparent

    def setRenderEngine(self, engine):
        self.data.render.engine = engine

    def setDevice(self, device):
        self.data.cycles.device = device

    def setResolution(self, resolution):
        self.data.render.resolution_x = resolution[0]
        self.data.render.resolution_y = resolution[1]

    def addCamera(self, camera):
        self.data.collection.objects.link(camera.object)
        self.data.camera = camera.object

    def addObject(self, object):
        self.data.collection.objects.link(object.object)