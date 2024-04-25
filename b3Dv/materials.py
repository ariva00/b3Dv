import bpy

class ColorRampAttributeMaterial:
    def __init__(self, name="ColorRampEmissionMaterial", colors = [(0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)], emission_color=(0.0, 0.0, 0.0, 1.0), color_attribute = "color", emission_attribute = "emission") -> None:
        self.data = bpy.data.materials.new(name)
        self.data.use_nodes = True
        self.node_group = self.data.node_tree
        self.node_group.nodes.clear()
        self.nodes = {}
        self.links = {}

        self.nodes['output'] = self.node_group.nodes.new(type="ShaderNodeOutputMaterial")
        self.nodes['principledBSDF'] = self.node_group.nodes.new(type="ShaderNodeBsdfPrincipled")
        self.nodes['colorAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")
        self.nodes['emissionAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")
        self.nodes['colorRamp'] = self.node_group.nodes.new(type="ShaderNodeValToRGB")

        self.links['colorAttributeToColorRamp'] = self.node_group.links.new(self.nodes['colorAttribute'].outputs['Fac'], self.nodes['colorRamp'].inputs['Fac'])
        self.links['colorRampToPrincipledBSDF'] = self.node_group.links.new(self.nodes['colorRamp'].outputs['Color'], self.nodes['principledBSDF'].inputs['Base Color'])
        self.links['emissionAttributeToPrincipledBSDF'] = self.node_group.links.new(self.nodes['emissionAttribute'].outputs['Fac'], self.nodes['principledBSDF'].inputs['Emission Strength'])
        self.links['principledBSDFToOutput'] = self.node_group.links.new(self.nodes['principledBSDF'].outputs['BSDF'], self.nodes['output'].inputs['Surface'])

        for i, c in enumerate(colors):
            if i == 0:
                self.nodes['colorRamp'].color_ramp.elements[i].color = c
                self.nodes['colorRamp'].color_ramp.elements[-1].color = colors[-1]
            elif i == len(colors)-1:
                break
            elem = self.nodes['colorRamp'].color_ramp.elements.new(i * 1/(len(colors)-1))
            elem.color = c

        self.nodes['colorAttribute'].attribute_name = color_attribute
        self.nodes['emissionAttribute'].attribute_name = emission_attribute
        self.nodes['principledBSDF'].inputs['Roughness'].default_value = 0.75
        self.nodes['principledBSDF'].inputs['Emission Color'].default_value = emission_color


class ColorAttributeMaterial:
    def __init__(self, name="ColorMaterial", emission_color=(0.0, 0.0, 0.0, 1.0), color_attribute = "color_attr", emission_attribute = "emission_attr") -> None:
        self.data = bpy.data.materials.new(name)
        self.data.use_nodes = True
        self.node_group = self.data.node_tree
        self.node_group.nodes.clear()
        self.nodes = {}
        self.links = {}

        self.nodes['output'] = self.node_group.nodes.new(type="ShaderNodeOutputMaterial")
        self.nodes['principledBSDF'] = self.node_group.nodes.new(type="ShaderNodeBsdfPrincipled")
        self.nodes['colorAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")
        self.nodes['emissionAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")

        self.links['colorAttributeToPrincipledBSDF'] = self.node_group.links.new(self.nodes['colorAttribute'].outputs['Color'], self.nodes['principledBSDF'].inputs['Base Color'])
        self.links['emissionAttributeToPrincipledBSDF'] = self.node_group.links.new(self.nodes['emissionAttribute'].outputs['Fac'], self.nodes['principledBSDF'].inputs['Emission Strength'])
        self.links['principledBSDFToOutput'] = self.node_group.links.new(self.nodes['principledBSDF'].outputs['BSDF'], self.nodes['output'].inputs['Surface'])

        self.nodes['colorAttribute'].attribute_name = color_attribute
        self.nodes['emissionAttribute'].attribute_name = emission_attribute
        self.nodes['principledBSDF'].inputs['Roughness'].default_value = 0.75
        self.nodes['principledBSDF'].inputs['Emission Color'].default_value = emission_color

class ColorMaterial:
    def __init__(self, name="ColorMaterial", color = (1.0, 1.0, 1.0, 1.0), emission_color=(0.0, 0.0, 0.0, 1.0), emission_attribute = "emission_attr") -> None:
        self.data = bpy.data.materials.new(name)
        self.data.use_nodes = True
        self.node_group = self.data.node_tree
        self.node_group.nodes.clear()
        self.nodes = {}
        self.links = {}

        self.nodes['output'] = self.node_group.nodes.new(type="ShaderNodeOutputMaterial")
        self.nodes['principledBSDF'] = self.node_group.nodes.new(type="ShaderNodeBsdfPrincipled")
        self.nodes['emissionAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")

        self.links['emissionAttributeToPrincipledBSDF'] = self.node_group.links.new(self.nodes['emissionAttribute'].outputs['Fac'], self.nodes['principledBSDF'].inputs['Emission Strength'])
        self.links['principledBSDFToOutput'] = self.node_group.links.new(self.nodes['principledBSDF'].outputs['BSDF'], self.nodes['output'].inputs['Surface'])

        self.nodes['emissionAttribute'].attribute_name = emission_attribute
        self.nodes['principledBSDF'].inputs['Base Color'].default_value = color
        self.nodes['principledBSDF'].inputs['Emission Color'].default_value = emission_color
