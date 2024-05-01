import bpy

class Material:
    def __init__(
            self, name="Material",
            color=(1.0, 1.0, 1.0, 1.0),
            emission_color=(0.0, 0.0, 0.0, 1.0),
            roughness=0.75,
            emission_strenght=0.0,
            color_attribute=None,
            color_attribute_colors=None,
            emission_color_attribute=None,
            emission_color_attribute_colors=None,
            emission_strength_attribute=None
            ) -> None:
        self.data = bpy.data.materials.new(name)
        self.data.use_nodes = True
        self.node_group = self.data.node_tree
        self.node_group.nodes.clear()
        self.nodes = {}
        self.links = {}

        self.nodes['output'] = self.node_group.nodes.new(type="ShaderNodeOutputMaterial")
        self.nodes['principledBSDF'] = self.node_group.nodes.new(type="ShaderNodeBsdfPrincipled")

        self.links['principledBSDFToOutput'] = self.node_group.links.new(self.nodes['principledBSDF'].outputs['BSDF'], self.nodes['output'].inputs['Surface'])

        self.setColor(color)
        self.setRoughness(roughness)
        self.setEmissionStrength(emission_strenght)
        self.setEmissionColor(emission_color)

        if color_attribute is not None:
            if color_attribute_colors is not None:
                assert len(color_attribute_colors) > 1, "Color attribute colors must have at least 2 colors"
                self.setFloatAttributeAsColor(color_attribute, color_attribute_colors)
            else:
                self.setColorAttributeAsColor(color_attribute)
        
        if emission_color_attribute is not None:
            if emission_color_attribute_colors is not None:
                assert len(emission_color_attribute_colors) > 1, "Emission color attribute colors must have at least 2 colors"
                self.setFloatAttributeAsEmissionColor(emission_color_attribute, emission_color_attribute_colors)
            else:
                self.setColorAttributeAsEmissionColor(emission_color_attribute)

        if emission_strength_attribute is not None:
            self.setFloatAttributeAsEmissionStrength(emission_strength_attribute)

    def setColor(self, color):
        self.nodes['principledBSDF'].inputs['Base Color'].default_value = color

    def setRoughness(self, roughness):
        self.nodes['principledBSDF'].inputs['Roughness'].default_value = roughness

    def setEmissionStrength(self, emission_strenght):
        self.nodes['principledBSDF'].inputs['Emission Strength'].default_value = emission_strenght

    def setEmissionColor(self, emission_color):
        self.nodes['principledBSDF'].inputs['Emission Color'].default_value = emission_color
    
    def setColorAttributeAsColor(self, attribute_name):
        self._removeAttributeAsColor()

        self.nodes['colorAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")
        self.links['colorAttributeToPrincipledBSDF'] = self.node_group.links.new(self.nodes['colorAttribute'].outputs['Color'], self.nodes['principledBSDF'].inputs['Base Color'])

        self.nodes['colorAttribute'].attribute_name = attribute_name

    def setFloatAttributeAsColor(self, attribute_name, colors = [(0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)]):
        self._removeAttributeAsColor()

        self.nodes['colorAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")
        self.nodes['colorRamp'] = self.node_group.nodes.new(type="ShaderNodeValToRGB")
        self.links['colorAttributeToColorRamp'] = self.node_group.links.new(self.nodes['colorAttribute'].outputs['Fac'], self.nodes['colorRamp'].inputs['Fac'])
        self.links['colorRampToPrincipledBSDF'] = self.node_group.links.new(self.nodes['colorRamp'].outputs['Color'], self.nodes['principledBSDF'].inputs['Base Color'])

        self.nodes['colorAttribute'].attribute_name = attribute_name

        for i, c in enumerate(colors):
            if i == 0:
                self.nodes['colorRamp'].color_ramp.elements[i].color = c
                self.nodes['colorRamp'].color_ramp.elements[-1].color = colors[-1]
            elif i == len(colors)-1:
                break
            elem = self.nodes['colorRamp'].color_ramp.elements.new(i * 1/(len(colors)-1))
            elem.color = c

    def setColorAttributeAsEmissionColor(self, attribute_name):
        self._removeAttributeAsEmissionColor()

        self.nodes['emissionColorAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")
        self.links['emissionColorAttributeToPrincipledBSDF'] = self.node_group.links.new(self.nodes['emissionColorAttribute'].outputs['Color'], self.nodes['principledBSDF'].inputs['Emission Color'])

        self.nodes['emissionColorAttribute'].attribute_name = attribute_name

    def setFloatAttributeAsEmissionColor(self, attribute_name, colors = [(0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)]):
        self._removeAttributeAsEmissionColor()

        self.nodes['emissionColorAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")
        self.nodes['emissionColorRamp'] = self.node_group.nodes.new(type="ShaderNodeValToRGB")
        self.links['emissionColorAttributeToEmissionColorRamp'] = self.node_group.links.new(self.nodes['emissionColorAttribute'].outputs['Fac'], self.nodes['emissionColorRamp'].inputs['Fac'])
        self.links['emissionColorRampToPrincipledBSDF'] = self.node_group.links.new(self.nodes['emissionColorRamp'].outputs['Color'], self.nodes['principledBSDF'].inputs['Emission Color'])
        
        self.nodes['emissionColorAttribute'].attribute_name = attribute_name

        for i, c in enumerate(colors):
            if i == 0:
                self.nodes['emissionColorRamp'].color_ramp.elements[i].color = c
                self.nodes['emissionColorRamp'].color_ramp.elements[-1].color = colors[-1]
            elif i == len(colors)-1:
                break
            elem = self.nodes['emissionColorRamp'].color_ramp.elements.new(i * 1/(len(colors)-1))
            elem.color = c

    def setFloatAttributeAsEmissionStrength(self, attribute_name):
        self._removeAttributeAsEmissionStrength()

        self.nodes['emissionStrengthAttribute'] = self.node_group.nodes.new(type="ShaderNodeAttribute")
        self.links['emissionStrengthAttributeToPrincipledBSDF'] = self.node_group.links.new(self.nodes['emissionStrengthAttribute'].outputs['Fac'], self.nodes['principledBSDF'].inputs['Emission Strength'])

        self.nodes['emissionStrengthAttribute'].attribute_name = attribute_name

    def _removeAttributeAsColor(self):
        self._removeLink('colorAttributeToPrincipledBSDF')
        self._removeLink('colorAttributeToColorRamp')
        self._removeLink('colorRampToPrincipledBSDF')
        self._removeNode('colorAttribute')
        self._removeNode('colorRamp')

    def _removeAttributeAsEmissionColor(self):
        self._removeLink('emissionColorAttributeToPrincipledBSDF')
        self._removeLink('emissionColorAttributeToEmissionColorRamp')
        self._removeLink('emissionColorRampToPrincipledBSDF')
        self._removeNode('emissionColorAttribute')
        self._removeNode('emissionColorRamp')

    def _removeAttributeAsEmissionStrength(self):
        self._removeLink('emissionStrengthAttributeToPrincipledBSDF')
        self._removeNode('emissionStrengthAttribute')

    def _removeLink(self, link_name):
        if link_name in self.links.keys():
            self.node_group.links.remove(self.links[link_name])
            self.links.pop(link_name)

    def _removeNode(self, node_name):
        if node_name in self.nodes.keys():
            self.node_group.nodes.remove(self.nodes[node_name])
            self.nodes.pop(node_name)
