import bpy

class MeshToPointCloudNodeTree:
    def __init__(self, name="Pointcloud", radius = 0.01, subdivison = 3, material = None) -> None:
        self.node_group = bpy.data.node_groups.new(type="GeometryNodeTree", name=name)
        self.node_group.nodes.clear()
        self.nodes = {}
        self.links = {}

        self.nodes['input'] = self.node_group.nodes.new(type="NodeGroupInput")
        self.nodes['output'] = self.node_group.nodes.new(type="NodeGroupOutput")
        self.nodes['meshToPoints'] = self.node_group.nodes.new(type="GeometryNodeMeshToPoints")
        self.nodes['instanceOnPoints'] = self.node_group.nodes.new(type="GeometryNodeInstanceOnPoints")
        self.nodes['icoSphere'] = self.node_group.nodes.new(type="GeometryNodeMeshIcoSphere")
        self.nodes['setShadeSmooth'] = self.node_group.nodes.new(type="GeometryNodeSetShadeSmooth")
        self.nodes['setMaterial'] = self.node_group.nodes.new(type="GeometryNodeSetMaterial")
        self.nodes['realizeInstances'] = self.node_group.nodes.new(type="GeometryNodeRealizeInstances")

        self.node_group.interface.new_socket(name="Geometry", description="", in_out="INPUT", socket_type="NodeSocketGeometry")
        self.node_group.interface.new_socket(name="Geometry", description="", in_out="OUTPUT", socket_type="NodeSocketGeometry")

        self.links['inputToMeshToPoints'] = self.node_group.links.new(self.nodes['input'].outputs['Geometry'], self.nodes['meshToPoints'].inputs['Mesh'])
        self.links['meshToPointsToInstanceOnPoints'] = self.node_group.links.new(self.nodes['meshToPoints'].outputs['Points'], self.nodes['instanceOnPoints'].inputs['Points'])
        self.links['icoSphereToSetShadeSmooth'] = self.node_group.links.new(self.nodes['icoSphere'].outputs['Mesh'], self.nodes['setShadeSmooth'].inputs['Geometry'])
        self.links['setShadeSmoothToInstanceOnPoints'] = self.node_group.links.new(self.nodes['setShadeSmooth'].outputs['Geometry'], self.nodes['instanceOnPoints'].inputs['Instance'])
        self.links['instanceOnPointsToSetMaterial'] = self.node_group.links.new(self.nodes['instanceOnPoints'].outputs['Instances'], self.nodes['setMaterial'].inputs['Geometry'])
        self.links['setMaterialToRealizeInstances'] = self.node_group.links.new(self.nodes['setMaterial'].outputs['Geometry'], self.nodes['realizeInstances'].inputs['Geometry'])
        self.links['realizeInstancesToOutput'] = self.node_group.links.new(self.nodes['realizeInstances'].outputs['Geometry'], self.nodes['output'].inputs['Geometry'])

        self.nodes['icoSphere'].inputs['Radius'].default_value = radius
        self.nodes['icoSphere'].inputs['Subdivisions'].default_value = subdivison
        if material is not None:
            self.nodes['setMaterial'].inputs['Material'].default_value = material.data

    def setPointsRadius(self, radius):
        self.nodes['icoSphere'].inputs['Radius'].default_value = radius
