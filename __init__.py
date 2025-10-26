# 2025 HarpoonLobotomy

import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import Panel, Operator, OperatorFileListElement, AddonPreferences, PropertyGroup
from datetime import datetime

version = 0.32
#22/10/25.
# Initial functions in progress.
# - harpoon

bl_info = {
    "name": "GR2 Importer",
    "author": "harpoonLobotomy",
    "description": "Import GR2/DAE models and animations into Blender without Collada (Blender 5.0 compatible)",
    "blender": (5, 0, 0), #will make it backwards compatible once it's fully working in 5, will just need to adapt the api.
    "version": (0, 3, 2),
    "category": "Import-Export",
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

def show_popup(text_lines, title=""):

    if text_lines == None:
        text_lines = "Nothing to display."

    if isinstance(text_lines, str):
        lines = text_lines.split("\n")
    else:
        lines = list(text_lines)

    def _draw(self, context):
        
        layout = self.layout
        for ln in lines:
            layout.label(text=str(ln) if ln != "" else " ")
        layout.separator()
        layout.label(text="(Esc or anywhere outside to close)")

    props = bpy.context.scene.gr2_importer_props
    if props.no_popups:
        return

    bpy.context.window_manager.popup_menu(_draw, title=title, icon='INFO')


def set_selected_as_custom(self, context):

    ## maybe include a couple of premade custom bones? 
    selected_objects = set(context.selected_objects)

    if selected_objects:
        if len(selected_objects) == 1:
            for selection in selected_objects:
                if selection.type == "MESH":
                    return selection.name, 1
                return selection.name, 0
        objects_queue = [] # should only run if >1 mesh
        for selection in selected_objects:
            if selection.type != "MESH":
                print("Non mesh object selected; only mesh can be custom bone, ignoring.")
                continue
            else:
                objects_queue.append(selection.name)
    else:
        print("No objects selected.")
        #show_popup("No objects selected,")
        return "No objects selected.", 0

    if len(objects_queue) == 1:
        for selection in objects_queue:
            return selection.name, 1
        
    if len(objects_queue) > 1:
        print(f"{len(objects_queue)} meshes selected; please select only one object to set as custom bone.")
        #show_popup(f"{len(objects_queue)} objects selected; please select only one object to set as custom bone.", title="")
        return f"{len(objects_queue)} objects selected; please select just one mesh.", 0
    
    return "No suitable objects", 0 # just in case anything slips through. Shouldn't be necessary.

# === PROPERTY GROUP ===
class GR2_ImporterProps(PropertyGroup):

    remove_temp: bpy.props.BoolProperty(
        name="Remove temp files",
        description="Remove all temp files generated in the process.",
        default=False, update=remove_temp_cb)

    keep_final: bpy.props.BoolProperty(
        name="Keep final file only",
        description="Keep the final .glb file, remove any other generated temp files.",
        default=False, update=keep_final_cb)
    
    import_type: EnumProperty(
        name="Import Type",
        items=(
            ("default", "Default", "Default import (1 GR2 file with optional armature)"),
            ("bulk_anim", "Bulk Animation", "Import multiple animations with a common armature"),
        ), description="", default="default")
    
    file_1: StringProperty(
        name="",
        default=r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2",
        description="Primary import file", subtype='FILE_PATH')
    
    file_2: StringProperty(     # add a third later maybe ### Would love the option of selecting multiple, instead of just single or dir.
        name="", default="Secondary file (if needed)",
        description="Secondary import file", subtype="FILE_PATH")
    
    armature_file_for_bulk: StringProperty(
        name="", 
        default=r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Base.GR2",
        description="Armature file to conform animation files to",
        subtype="FILE_PATH")
    
    anim_dir: StringProperty(
        name="",
        default=r"F:\test\gltf_tests\raw_intdev_anims",
        description="Directory of armature files", subtype="DIR_PATH")
    
    show_advanced_options: BoolProperty(
        name="Show Advanced Options", description="Show or hide advanced options", default=False)
    
    test_files: BoolProperty(name="test_file_components", default=False)
    collection_name_override: StringProperty(name="Collection Name (optional)", default="", description="Collection Name (optional); if not used, the primary input filename will be used for the collection name.")
    reuse_existing_collection: BoolProperty(name="Reuse Coll.", default=True, description="Reuse an existing collection with the correct name if found.")
    custom_bone_obj: StringProperty(name="Custom Bone Object", default="Ico", description="Select an object to use as a custom bone.")
    use_custom_bone_obj: BoolProperty(name="Use custom bones", default=True)
    scale_custom_bone: BoolProperty(name="Scale custom bones", default=False)
    temp_folder: StringProperty(name="Temp folder", default="") # should be in prefs, not here.
    delete_temp: BoolProperty(name="Delete temp files", default=True, description="Delete temporary files")
    fix_bones: BoolProperty(name="Fix Bone Orientation", default=True, description="Try to reorient bones into proper alignment.")
    open_console: BoolProperty(name="Open console on run", default=True, description="Open Terminal before running import.")
    set_selected_as_custom: StringProperty(name="Set selected object as custom bone", default="", description="Set the selected object as 'custom bone' for the next import . [Can be changed afterwards in Pose Mode: Bone Properties > Viewport Display, Custom Shape > Custom Object]")
    no_popups: BoolProperty(name="no_popups", default=False, description="No popup messages. (Messages will still be printed to terminal.)")

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
        def_col.prop(props, "file_1")
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
        bulk_col.prop(props, "armature_file_for_bulk")
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
        row1 = col2.row()
        row1.prop(props, "collection_name_override")
        row1.prop(props, "reuse_existing_collection")
        row3 = col2.row()
        row3.prop(props, "remove_temp")
        row3.prop(props, "keep_final")
        col2.prop(props, "temp_folder")
        row4 = col2.row()
        row4.prop(props, "use_custom_bone_obj")
        row4.prop(props, "scale_custom_bone")
        if props.use_custom_bone_obj:
            row5 = col2.row()
            row5.prop(props, "custom_bone_obj")
            row5.operator("gr2.set_custom_bone", text="Set selection as custom bone")
        col2.prop(props, "fix_bones")
        row5 = col2.row()
        row5.prop(props, "open_console")
        row5.prop(props, "no_popups")
        col2.separator()

class GR2_PT_Importer_ShaderPanel(Panel):
    bl_label = "GR2 Importer"
    bl_idname = "GR2_PT_Importer_ShaderPanel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'GR2 Importer'

    def draw(self, context):
        draw_GR2import_panel(self, context)

class GR2_PT_Importer_3DViewPanel(Panel):
    bl_label = "GR2 Importer"
    bl_idname = "GR2_PT_Importer_3DViewPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GR2 Importer'

    def draw(self, context):
        draw_GR2import_panel(self, context)

# === BUTTON HANDLERS ===

class GR2_OT_Importer_Run_Import(Operator):

    bl_idname = "gr2.run_importer"
    bl_label = "Run Importer Logic"
    bl_description = "Run the importer with the selected files and settings."

    def execute(self, context):
        
        import_start = datetime.now()
        debug_print("general_setup", f"\n" * 12)
        debug_print("general_setup", f" " * 13 + "=" * 40)
        print("  === Import process started at", import_start, "===")
        debug_print("general_setup", f" " * 17 + "=" *32 + "\n")

        props = context.scene.gr2_importer_props
        
        if props.import_type == "bulk_anim":
            inputs = [props.armature_file_for_bulk, props.anim_dir]
        else:
            inputs = [props.file_1, props.file_2]
        
        settings = {"collection_name":props.collection_name_override, "import_type":props.import_type, 
                    "custom_bones":props.use_custom_bone_obj, "custom_bone_obj":props.custom_bone_obj, 
                    "remove_all_temp":props.remove_temp, "keep_final":props.keep_final, "fix_bones":props.fix_bones,
                    "open_console":props.open_console, "reuse_existing_collection":props.reuse_existing_collection}
        
        from . import (import_gr2_for_blender5)
        imported_files = import_gr2_for_blender5.run("import", inputs, settings)

        show_popup(imported_files, title="Imported:")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class GR2_OT_Test_Files(Operator):
    # run the rootreader for any filepaths in file1/file2, no imports.
    
    bl_idname = "gr2.test_files"
    bl_label = "Test File(s) for Components"
    bl_description = "Run the metadata checker on the specified file(s)."
    
    def execute(self, context):
        metadata_collection = None
        props = context.scene.gr2_importer_props
        file_1 = props.file_1
        file_2 = props.file_2

        inputs = [file_1, file_2]
        settings = {"open_console":props.open_console}

        from . import (import_gr2_for_blender5)
        metadata_collection = import_gr2_for_blender5.run("metadata", inputs, settings)
        if metadata_collection == None:
            metadata_collection.append("No viable files")    
        metadata_collection.append("  -------- DONE --------    ")

        show_popup(metadata_collection, title="GR2 Metadata Results:")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class GR2_OT_set_custom_bone(Operator):
    
    bl_idname = "gr2.set_custom_bone"
    bl_label = "Set selection as as custom bone"
    bl_description = "Select a mesh object to set as a custom bone for the next import."
    
    def execute(self, context):

        custom_bone, success = set_selected_as_custom(self, context)
        props = context.scene.gr2_importer_props
        if success == 1:
            props.custom_bone_obj = custom_bone
        else:
            props.custom_bone_obj = ""
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)

# === REGISTRATION ===
classes = (
    GR2_ImporterProps,
    GR2_OT_Importer_Run_Import,
    GR2_OT_Test_Files,
    GR2_PT_Importer_ShaderPanel,
    GR2_PT_Importer_3DViewPanel,
    GR2_OT_set_custom_bone
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
