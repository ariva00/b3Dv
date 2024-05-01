import bpy

from b3Dv.camera import Camera

class Scene:

    def __init__(self, name="Scene", engine="CYCLES", device="GPU", resolution=(1920, 1080), transparent=True) -> None:
        self.data = bpy.data.scenes.new(name)
        self.setRenderEngine(engine=engine)
        self.setDevice(device=device)
        self.setResolution(resolution)
        self.data.render.film_transparent = transparent

        world = bpy.data.worlds.new("World")
        self.data.world = world

    def setRenderEngine(self, engine):
        self.data.render.engine = engine

    def setDevice(self, device):
        self.data.cycles.device = device

    def setResolution(self, resolution):
        self.data.render.resolution_x = resolution[0]
        self.data.render.resolution_y = resolution[1]

    def setSamples(self, samples):
        self.data.cycles.samples = samples
        self.data.eevee.taa_render_samples = samples

    def addCamera(self, camera:Camera):
        self.data.collection.objects.link(camera.object)
        self.data.camera = camera.object

    def addObject(self, object):
        self.data.collection.objects.link(object.object)

    def renderToFile(self, filepath):
        self.data.render.filepath = filepath
        bpy.ops.render.render(write_still=True, scene=self.data.name)
