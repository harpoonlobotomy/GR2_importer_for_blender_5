# gr2_importer_shell

from typing import Self
import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Panel
from datetime import datetime

version = 0.2
#22/10/25.
# Initial functions in progress.
# - harpoon

bl_info = {
    "name": "GR2_Importer",
    "description": "GR2/DAE importer for Blender 5.0+",
    "version": (0, 2, 0),
    "blender": (5, 0, 0),
    "category": "Object",
    "location": "Property Panel, Press N in Viewport",
}

DEBUG_GROUPS = {
    "general_setup": True,
    "errors": True
}

def debug_print(groups, *args, **kwargs):
    if isinstance(groups, str):
        groups = [groups]
    if any(DEBUG_GROUPS.get(g, False) for g in groups):
        print(*args, **kwargs)

def remove_temp_cb(self, context):
    if self.remove_temp + self.keep_final <= 1:
        return None
    self.keep_final = not(self.remove_temp)

def keep_final_cb(self, context):
    if self.remove_temp + self.keep_final <= 1:
        return None
    self.remove_temp = not(self.keep_final)

# === PROPERTY GROUP ===
class GR2_ImporterProps(bpy.types.PropertyGroup):

    remove_temp: bpy.props.BoolProperty(
        name="Remove temp files",
        description="Remove all temp files generated in the process.",
        default=False,
        update=remove_temp_cb,
    )
    keep_final: bpy.props.BoolProperty(
        name="Keep final file only",
        description="Keep the final .glb file, remove any other generated temp files.",
        default=False,
        update=keep_final_cb,
    )
    import_type: EnumProperty(
        name="Import Type",
        items=(
            ("default", "Default", "Default import (1 GR2 file with optional armature)"),
            ("bulk_anim", "Bulk Animation", "Import multiple animations with a common armature"),
        ),
        description="",
        default="default",
    )
    file_1: StringProperty(
        name="",
        default="Primary input file",
        description="Primary import file",
        subtype='FILE_PATH'
    )
    file_2: StringProperty(     # add a third later maybe ### Would love the option of selecting multiple, instead of just single or dir.
        name="",
        default="Secondary file (if needed)",
        description="Secondary import file",
        subtype="FILE_PATH"
    )
    anim_dir: StringProperty(
        name="",
        default="folder/somewhere/",
        description="Directory of armature files",
        subtype="DIR_PATH"
    )
    show_advanced_options: BoolProperty(
        name="Show Advanced Options",
        description="Show or hide advanced options",
        default=False)
    test_files: BoolProperty(name="test_file_components", default=False) # actually want it to be a button
    collection_name_override: StringProperty(name="Collection Name (optional)", default="Collection Name (optional); if not used, the primary input filename will be used for the collection name.")
    custom_bone_obj: StringProperty(name="Custom Bone Object", default="Ico", description="Select an object to use as a custom bone.") # select from current blend? From file? 
    use_custom_bone_obj: BoolProperty(name="Use custom bones", default=True)
    temp_folder: StringProperty(name="Temp folder", default="")

    # === PANELS ===
def draw_GR2import_panel(self, context):
    layout = self.layout
    scn = context.scene
    props = scn.gr2_importer_props

    # === IMPORT TYPE ===
    box = layout.box()
    row = box.row()
    col = box.column(align=True)

    row.label(text="Import type:")
    row = col.row()
    row.prop(props, "import_type", expand=True)
    
    if props.import_type == "default":
        default=layout.box()
        def_col = default.column(align=True)
        def_col.label(text="Primary file to import:")
        row1 = def_col.row()
        row1.prop(props, "file_1")
        def_col.separator()
        def_col.label(text="Secondary file if needed (eg armature):")
        def_col.prop(props, "file_2")
        def_col.separator()
        def_col.separator()
        def_col.operator("gr2.test_files", text="Test file(s) for components")
        def_col.separator()

    if props.import_type == "bulk_anim":
        bulk_anim=layout.box()
        bulk_col = bulk_anim.column(align=True)
        bulk_col.label(text="Common armature:")
        bulk_col.prop(props, "file_1")
        bulk_col.separator()
        bulk_col.label(text="Animation files folder:")
        bulk_col.prop(props, "anim_dir")
        bulk_col.separator()
        bulk_col.separator()

    layout.operator("gr2.run_importer", text="Run Importer")

    optionsbox = layout.box()
    optionsbox.prop(props, "show_advanced_options", icon="TRIA_DOWN" if props.show_advanced_options else "TRIA_RIGHT", icon_only=False, emboss=True)
    if props.show_advanced_options:
        col2 = optionsbox.column(align=True)
        col2.prop(props, "collection_name_override")
        row2 = col2.row()
        row2.prop(props, "remove_temp")
        row2.prop(props, "keep_final")
        col2.prop(props, "temp_folder")
        col2.prop(props, "use_custom_bone_obj")
        if props.use_custom_bone_obj:
            col2.prop(props, "custom_bone_obj")

class GR2_PT_Importer_ShaderPanel(Panel):
    bl_label = "GR2 Importer"
    bl_idname = "GR2_PT_Importer_ShaderPanel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'GR2_Importer'

    def draw(self, context):
        draw_GR2import_panel(self, context)

class GR2_PT_Importer_3DViewPanel(Panel):
    bl_label = "GR2 Importer"
    bl_idname = "GR2_PT_Importer_3DViewPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GR2_Importer'

    def draw(self, context):
        draw_GR2import_panel(self, context)

# === BUTTON HANDLERS ===

class GR2_OT_Importer_Run_Import(bpy.types.Operator):
    # run import_gr2_for_blender5.py, once amended accordingly.

    bl_idname = "gr2.run_importer"
    bl_label = "Run Importer Logic"

    def execute(self, context):
        
        import_start = datetime.now()
        debug_print("general_setup", f"\n" * 12)
        debug_print("general_setup", f" " * 13 + "=" * 40)
        print("  === Import process started at", import_start, "===")
        debug_print("general_setup", f" " * 17 + "=" *32 + "\n")


        props = context.scene.gr2_importer_props
        file_1 = props.file_1
        file_2 = props.file_2
        inputs = [file_1, file_2]

        if "bpy" in locals():
            import importlib
            reloadable_modules = [
                "import_gr2_for_blender5",
                ""
            ]
            for module in reloadable_modules:
                if module in locals():
                    importlib.reload(locals()[module])

        from . import (import_gr2_for_blender5)
                        
        import_gr2_for_blender5.run("import", inputs)

    def invoke(self, context, event):
        return self.execute(context)

class GR2_OT_Test_Files(bpy.types.Operator):
    # run the rootreader for any filepaths in file1/file2, no imports.
    
    bl_idname = "gr2.test_files"
    bl_label = "Test File(s) for Components"
    
    def execute(self, context):
    
        filetest_start = datetime.now()
        debug_print("general_setup", f"\n" * 12)
        debug_print("general_setup", f" " * 13 + "=" * 40)
        print("  === GR2 Test process started at", filetest_start, "===")
        debug_print("general_setup", f" " * 17 + "=" *32 + "\n")

        props = context.scene.gr2_importer_props

        file_1 = props.file_1
        file_2 = props.file_2

        inputs = [file_1, file_2]
        #import_gr2_for_blender5.run("metadata_only", inputs)

    def invoke(self, context, event):
        return self.execute(context)

# === REGISTRATION ===
classes = (
    GR2_ImporterProps,
    GR2_OT_Importer_Run_Import,
    GR2_OT_Test_Files,
    GR2_PT_Importer_ShaderPanel,
    GR2_PT_Importer_3DViewPanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.gr2_importer_props = bpy.props.PointerProperty(type=GR2_ImporterProps)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.gr2_importer_props

if __name__ == "__main__":
    register()
