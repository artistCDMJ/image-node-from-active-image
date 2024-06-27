import bpy

# Get the active texture node and its size
def get_active_texture_node_image_size():
    if bpy.context.space_data.type == 'NODE_EDITOR':
        node_tree = bpy.context.space_data.node_tree
        if node_tree:
            active_node = node_tree.nodes.active
            if active_node and active_node.type == 'TEX_IMAGE' and active_node.image:
                width = active_node.image.size[0]
                height = active_node.image.size[1]
                return width, height
    return None, None

# Get size of image in image editor
def get_active_image_size():
    if bpy.context.space_data.type == 'IMAGE_EDITOR':
        active_image = bpy.context.space_data.image
        if active_image:
            width = int(active_image.size[0])
            height = int(active_image.size[1])
            return width, height
    return None, None

# Create a new texture node based on the active node size
def create_new_texture_node_with_size(width, height):
    image_name = f"Texture_{width}x{height}"
    new_image = bpy.data.images.new(name=image_name, width=width, height=height)
    
    if bpy.context.space_data.type == 'NODE_EDITOR':
        node_tree = bpy.context.space_data.node_tree
        if node_tree:
            new_texture_node = node_tree.nodes.new(type='ShaderNodeTexImage')
            new_texture_node.image = new_image
            new_texture_node.label = image_name
            
            active_node = node_tree.nodes.active
            if active_node:
                new_texture_node.location = (active_node.location.x, active_node.location.y - 260)

#new image texture node sized to same as active
class D2P_OT_NewTextureNode(bpy.types.Operator):
    bl_idname = "node.new_texture_node"
    bl_label = "New Texture Node from Active Texture"
    
    def execute(self, context):
        width, height = get_active_texture_node_image_size()
        if width and height:
            create_new_texture_node_with_size(width, height)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No active texture node with an image found")
            return {'CANCELLED'}
        
#new image dialog autofilled with size from active image in image editor
class D2P_OT_GetImageSizeOperator(bpy.types.Operator):
    bl_idname = "image.get_image_size"
    bl_label = "New Image from Active Image Size"
    
    width: bpy.props.IntProperty()
    height: bpy.props.IntProperty()
    
    def invoke(self, context, event):
        width, height = get_active_image_size()
        if width and height:
            self.width = width
            self.height = height
            context.window_manager.invoke_props_dialog(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active image found")
            return {'CANCELLED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "width")
        layout.prop(self, "height")
    
    def execute(self, context):
        bpy.ops.image.new(name="New Image", width=self.width, height=self.height)
        return {'FINISHED'}

def draw_node_editor_button(self, context):
    layout = self.layout
    layout.operator("node.new_texture_node", text="New Texture Node from Active Texture")

def draw_image_editor_button(self, context):
    layout = self.layout
    layout.operator("image.get_image_size", text="New Image from Active Image Size")

def register():
    bpy.utils.register_class(D2P_OT_NewTextureNode)
    
    bpy.utils.register_class(D2P_OT_GetImageSizeOperator)
    bpy.types.IMAGE_MT_image.append(draw_image_editor_button)
    bpy.types.NODE_MT_node.append(draw_node_editor_button)

def unregister():
    bpy.utils.unregister_class(D2P_OT_NewTextureNode)
    
    bpy.utils.unregister_class(D2P_OT_GetImageSizeOperator)
    bpy.types.IMAGE_MT_image.remove(draw_image_editor_button)
    bpy.types.NODE_MT_node.remove(draw_node_editor_button)

if __name__ == "__main__":
    register()
