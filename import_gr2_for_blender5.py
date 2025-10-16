# Collada import replacement for blender 5.0
# Not perfect, but at present it does successfully import GR2 and DAE, with a start on bone alignment. 
# Still needs more work but it does basically do what I need it to. Not yet tested for animation but meshes + armatures are functional.
# No export functionality at all yet, may implement it later but I only need import for myself so that's my focus.
# 
#  -- harpoon
#  
# 16/10/2025

version = "0.2.0"

import bpy
from addon_utils import check, enable
import re
import subprocess
import tempfile
from pathlib import Path
import os, sys
#import access_point_scripts.blender.transform_bones as transform_bones
use_existing_collection = True
custom_bones_on = True


SCRIPT_DIR = r"C:\Users\Gabriel\Documents\utilities\access_point_scripts\blender"
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)
    
#import transform_bones
    
divineexe = r"F:\Blender\Addons etc\Packed\Tools\Divine.exe"

default, enabled = check("io_scene_gltf2")
if not enabled:
    enable("io_scene_gltf2", default_set=True, persistent=True)

def get_filename(filename):
    directory, filepath = filename.rsplit("\\", 1)
    return directory, filepath

def get_temppath():
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    tempfile_path = Path(temp.name)
    return tempfile_path

def attemptimport(filepath):

    origname = filepath
    def import_gltf(filepath, directory):
        try:
            bpy.ops.import_scene.gltf(filepath=filepath, directory=directory, files=[{"name":filepath}], loglevel=20)
        except Exception as e:
            print(f"GLTF import failed: {e}")
            return None

    def try_divine(filepath):

        temppath = get_temppath()

        def makedae(temppath):
            temppath = str(temppath) + ".dae"
            print(f"Divine CLI command")
            print(f'"{divineexe}" --loglevel all -g bg3 -s {filepath} -d {temppath} -i gr2 -o dae -a convert-model -e y-up-skeletons')
            try:
                subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}" -i gr2 -o dae -a convert-model -e y-up-skeletons')

            except Exception as e:
                print("Failed to generate DAE with Divine. Returning early.")
                return None

            print("DAE file generated. Moving to generate GLTF.")
            return temppath

        def makegltf(temppath, fromtype):
            if fromtype.lower() in str(temppath).lower():
                pass
            else:
                temppath = str(temppath) + "." + fromtype
            temppath2 = str(get_temppath()) + ".gltf"
            print(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o gltf -a convert-model -e flip-uvs')
            print()
            try:
                subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o gltf -a convert-model -e flip-uvs')
                return temppath2
            except Exception as e:
                print(f"Failed to generate GLTF from {fromtype} with Divine. Returning early.")
                return None        
        
        if "gltf" in str(filepath):
            return filepath

        gltf = makegltf(filepath, "gr2")
        if gltf:
            print("GR2 to GLTF complete.")
            return gltf
        else:
            dae = makedae(temppath)
            if dae:
                gltf = makegltf(filepath, dae, "dae")
                if gltf:
                    print("GLTF made successfully.")
                    return gltf


    collection = None

    directory, filename = get_filename(origname)
    trimmed_name, ext = filename.split(".")

    if use_existing_collection:
        test = bpy.data.collections.get(trimmed_name)
        if test:
            print("There is already a collection with this name.")
            collection = test

    if not use_existing_collection or not collection:
            collection = bpy.data.collections.new(trimmed_name)

    try:
        bpy.context.scene.collection.children.link(collection)
    except:
        pass

    layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
    bpy.context.view_layer.active_layer_collection = layer_collection

    existing_objects = set(bpy.context.scene.objects)

    temppath = try_divine(filepath)
    print("Have finished in try divine.")
    print("Temppath: ", temppath)
    directory, filename = get_filename(temppath)
    import_gltf(filename, directory)

    new_objects = [obj for obj in bpy.context.scene.objects if obj not in existing_objects]
    if new_objects == None:
        print("GLTF import failed, no new objects imported to scene.")
        return None, trimmed_name
    return new_objects, trimmed_name

    
def cleanup(new_objects, trimmed_name):
    
    # Delete LOD objects ending with _LOD\d+
    lod_pattern = re.compile(r'.*_LOD\d+')
    lod_objects = [obj for obj in new_objects if lod_pattern.match(obj.name)]

    for obj in lod_objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    print({'INFO'}, f"Deleted {len(lod_objects)} LOD mesh{'es' if len(lod_objects) != 1 else ''}")

    if not new_objects or all(obj in lod_objects for obj in new_objects):
        print({'WARNING'}, "No non-LOD mesh objects remain after deletion")

    excess_icospheres = []
    for obj in bpy.data.collections["glTF_not_exported"].all_objects:
        if obj.name == "Icosphere":
            primary = obj
        else:
            excess_icospheres.append(obj)
    for obj in excess_icospheres:
        pass# 
    
    non_lod = []
    for item in new_objects:
        if item not in lod_objects:
            non_lod.append(item)

    armature_list = []
    bone_dict = {}
    #counter = 0
    for obj in non_lod:
        if obj.type == "ARMATURE":
            armature_list.append(obj) # changed back # changed to obj.name from obj.
            for bone in obj.pose.bones:
                if bone.custom_shape or custom_bones_on:
                    if bone.custom_shape:
                        old_ico = bone.custom_shape
                        bone.custom_shape = primary
                        bpy.data.objects.remove(old_ico,do_unlink=True)
                    else:
                        bone.custom_shape = primary
    
            def fix_bone_orientation():

                print("OH M YFUCCJI")
                context = bpy.context.object.data.edit_bones
                bpy.ops.object.mode_set(mode='EDIT') # just for set to edit mode, whether it already was or not doesn't seem to error it.
                bpy.context.object.data.show_axes = True # just because it's useful.

                print(f"context: {context}")
                for bone in context:
                    print(f"Bone: {bone}, head: {bone.head}, tail: {bone.tail}")
                    children = []
                    if not bone_dict.get(bone.name):
                        bone_dict[bone.name] = {}
                    entry = bone_dict[bone.name]
                    if bone.parent:
                        entry.update({
                            "parent": bone.parent.name})
                    if bone.children:
                        for child in bone.children:
                            children.append(child.name)
                        entry.update({
                            "children": children})

                parents = set()
                children = set()
                for bone in context:
                    entry = bone_dict.get(bone.name)
                    entry.update({"head_pos": bone.head, "tail_pos": bone.tail.copy(), "new_tail_pos": bone.tail, "roll": bone.roll})
                    parent = entry.get("parent")
                    if not parent:
                        #print(f"No parent for {bone.name}.")
                        pass
                    else:
                        child = bone.name # could skip this and just keep typing bone.name but I need the clarity for now.
                        #print(f"parent: {parent}, child: {child}")
                        children.add(child)
                        parents.add(parent)
                        parent_obj = context.get(parent) ## can just use the dict for this now, no?
                        childhead = entry.get("head_pos")
                        #p2 = parent_obj.head ## i have these here to check for relative length, so if a child is too far away, it doesn't stretch the parent bone. Currently not implemented though.
                        parent_obj.tail = childhead

                #print(bone_dict)
                counter = 0
                nomovement = []
                for name, entry in bone_dict.items():
                    counter += 1
                    if entry.get("new_tail_pos") == entry.get("tail_pos"):
                        nomovement.append(name)
                
                if counter != len(nomovement):
                    print(f"Total of {counter} bones, {len(nomovement)} did not move. `({nomovement})`")   
                    for bone in nomovement:
                        #.print(f"Bone: {bone}")
                        parent = bone_dict[bone].get("parent")
                        parenthead = bone_dict[parent].get("head_pos")
                        parenttail = bone_dict[parent].get("tail_pos")
                        parentnewtail = bone_dict[parent].get("new_tail_pos")
                        vec_before = parenttail - parenthead
                        vec_after  = parentnewtail  - parenthead
                        angle = vec_before.angle(vec_after)
                        axis = vec_before.cross(vec_after)
                        axis.normalize()
                        #print(f"Angle change: {angle}")
                        #print(f"axis: {axis}")
                        
                        childhead = bone_dict[bone].get("head_pos")
                        childtail = bone_dict[bone].get("tail_pos")
                        vec_target = childtail - childhead
                        
                        from mathutils import Quaternion
                        rot_quat = Quaternion(axis, angle)
                        vec_rotated = rot_quat @ vec_target
                        
                        childtail_new = childhead + vec_rotated
                        boneobj = context.get(bone)
                        boneobj.tail = childtail_new
                        
                else:
                    print("No bones moved.")
                    
                for name, entry in bone_dict.items():
                    roll = entry.get("roll")
                    #print("roll: ", roll)
                    if float(roll) < 0:
                        roll = float(roll) * -1
                        bone = context.get(name)
                        bone.roll = roll
                bpy.ops.object.mode_set(mode='OBJECT')

        fix_bone_orientation()
    print(f"armature list: {armature_list}")

    return armature_list
                #if obj.name.startswith("Dummy_Root"):
            #    basename, suffix = obj.name.split(".")
            #    if counter >= 1:
            #        trimmed_name = trimmed_name + "_" + str(counter) 
            #    print(basename, suffix)
            #    obj.name = trimmed_name + "." + suffix
            #    counter += 1
                # Add each bone to dict with parent?
                
            # need to chainlists in order, and connect head>tail.
            # Really just use the bone connections structure from collada, it seems sensible. 
     
## run ##
#file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\Humans\_Hair\Resources\HAIR_HUM_F_Orin.GR2"
#file_to_import = r"F:\\test\\gltf_tests\\badger.gltf"
file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"
imported, trimmed_name = attemptimport(file_to_import)
if imported:
    armature_list = cleanup(imported, trimmed_name)
    #if armature_list:
     #   transform_bones.set_up(armature_list) # moved internally, caused needless complication.


else:
    print("Failed to import through gltf and divine.")
    

# option to replace existing objects with newly imported ones
