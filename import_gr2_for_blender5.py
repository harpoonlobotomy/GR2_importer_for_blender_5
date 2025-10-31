# for blender 5.0+
# No export functionality at all yet, may implement it later but I only need import for myself so that's my focus.
#  -- harpoon

# 31/10/2025

version = "0.7.1" # fixed the collections again, had an issue where it would always create a collection for the armature name even when another name was specified and used.

import bpy
from addon_utils import check, enable
import re
import subprocess
import tempfile
from pathlib import Path
import os
import json

global settings # not sure about this but going with it for now.

status_definitions = {
    000: "No armature file",
    00: "File does not exist",
    0: "No reported mesh, animation or armature",
    1: "Armature only",
    2: "Mesh only",
    3: "Armature + mesh", 
    4: "Animation only",
    41: "Animation only GR2, valid armature provided",
    42: "Animation only, no valid armature provided",
    43: "Animation file. Armature file provided is not only armature",
    5: "Armature & animation",
    6: "Not a GR2 file",
    7: "Mesh, armature & animation"
}

has_armature = [1,3,5,7]
null_status = [0, 00, 000, None]

## === Helpers === ##
def initial_setup(mode, settings):

### --- Ensure console is visible before running anything. --- ###
    def is_console_visible():
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        return hwnd != 0 and ctypes.windll.user32.IsWindowVisible(hwnd)

    if settings.get("open_console"):  
        if not is_console_visible():
            bpy.ops.wm.console_toggle()

#--- Check required files exist. --- #
    divine = settings.get("divine_path")
    rreader = settings.get("rootreader_path")
    div_state = rr_state = None
    def check_for_exe(name, path):
        if not path or path is None:
            return [f"Cannot initialise, required file not found for {name}.", "Please add the correct path in Add-on Preferences."], "failure"
        elif not Path(path).is_file():
            return [f"Cannot initialise, {name} not found at `{path}`.", "Please add the correct path in Add-on Preferences."], "failure"
        return None, None
    
    if mode == "import":
        text_list, div_state = check_for_exe("divine.exe", divine)
        if div_state == "failure":
            return text_list
        text_list, rr_state = check_for_exe("rootreader.exe", rreader)
        if rr_state == "failure":
            return text_list

    elif mode == "metadata":
        text_list, state = check_for_exe("rootreader.exe", rreader)
        if state == "failure":
            return text_list

    if mode == "import":
        default, enabled = check("io_scene_gltf2")
        if not enabled:
            try:
                enable("io_scene_gltf2", default_set=True, persistent=True) # is this allowed in blender addons? Not sure you're allowed to do this. Might jsut have to make it a warning.
            except Exception as e:
                print(f"Failed to enable glTF native importer: {e}")
                print("Please enable the 'glTF 2.0 Format' addon manually in Blender preferences and try again.")
                return [f"Failed to enable glTF Importer: {e}", "Please enable `glTF 2.0 Format` addon manually in Blender Add-ons and try again."]
            
def print_me(status, *args, **kwargs):
    if status:
        print(*args, **kwargs)

def get_filename_ext(filepath = None):
    if not filepath:
        return None, None, None
    
    #print(filepath)
    if "\\" not in filepath:
        return None, None, None
    directory, filename = str(filepath).rsplit("\\", 1)
    ext = filename.split(".")[-1]
    return directory, filename, ext.lower()

def get_temppath():
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    tempfile_path = Path(temp.name)
    return tempfile_path

def check_file_exists(origin, filepath):

    if filepath == None or not Path(filepath).is_file():
        print(f"No file provided for {origin}.")
        return False
    return True

# MAIN FUNCTIONS #

### METADATA ###
def get_metadata(filepath, printme):

    extra_data = {"GR2Tag": None, "Internal_Filename": None}
    rootreader = settings.get("rootreader_path")
    divinepath = settings.get("divine_path")
    divinedir = os.path.dirname(divinepath)

    result = subprocess.run(
        [rootreader, filepath],
        capture_output=True,
        text=True, cwd=divinedir ### `cwd`:  set to divine dir to ensure any dependent files are found.
    )

    meshes, armatures, animations = 0, 0, 0
    if result.returncode == 0:
        root_data = json.loads(result.stdout)
        if ("Skeletons" in root_data and root_data.get("Skeletons") is not None):
            armatures = 1
        if "Meshes" in root_data and root_data.get("Meshes") is not None:
            meshes = 1
        if "Animations" in root_data and root_data.get("Animations") is not None:
            animations = 1
        extra_data.update({"GR2Tag": root_data.get('GR2Tag')}) # assuming it's always valid. Believe so.
        extra_data.update({"Internal_Filename": root_data.get('FromFileName')})
        return meshes, armatures, animations, extra_data
    
    else:
        print_me(printme, f"Failed to get metadata: {result.stderr}")
        return None, None, None, None

def metadata_func(input_file, armaturepath=None, printme=True): 

    filename = get_filename_ext(input_file)[1]
    extra_data = {}

    if "Secondary file (if needed)" in input_file:
        print_me(printme, f"No secondary input file.")
        return 000, None, filename
    
    import_exists = check_file_exists(f"metadata: {filename}", input_file)
    if not import_exists:
        print_me(printme, f"Import file `{filename}` does not exist. Aborting metadata check.")
        return 00, None, filename
    
    if armaturepath != None:
        if "Secondary file (if needed)" in armaturepath:
            armaturepath = None

    if ".dae" in str(input_file).lower():
        return 7, extra_data, filename
    if ".glb" in str(input_file).lower() or ".gltf" in str(input_file).lower():
        return 8, extra_data, filename
    
    if input_file == armaturepath and input_file is not None:
        print_me(printme, "Testing armature file for metadata:")
        skel_meshes, skel_armatures, skel_animations, extra_data = get_metadata(armaturepath, printme)
        if (skel_meshes, skel_armatures, skel_animations) == (0, 0, 1):
            return 4, extra_data, filename
    
    elif armaturepath is not None and not check_file_exists("metadata: armature path", armaturepath): # this should have caught the default text but it didn't. Why?
        armaturepath = None
        print_me(printme, f"Armature path `{filename}` is not a valid file. Ignoring.")

    def get_status(input_file, armaturepath):
        ARM, MSH, ANIM = 1, 2, 4
        try:
            meshes, armatures, animations, extra_data = get_metadata(input_file, printme)
            mesh = meshes * MSH
            armature = armatures * ARM
            anim = animations * ANIM
            content = mesh + armature + anim
            #print_me(meshes, armatures, animations, extra_data)
            if content == 4:
                if check_file_exists("metadata: armature path", armaturepath):
                    print_me(f"There is an existing file for this animation: {armaturepath}")
                    skel_meshes, skel_armatures, skel_animations, _ = get_metadata(armaturepath, printme)
                    if not skel_armatures:
                        return 42, extra_data
                    if skel_armatures and not (skel_meshes or skel_animations):
                        return 41, extra_data
                    print_me(printme, "Armature file contains more than just armature. Tentatively returning; may fail.")
                    return 43, extra_data
                print_me(f"The armaturepath file does not exist: {armaturepath}")
                return 42, extra_data

            return content, extra_data

        except Exception as e:
            print_me(printme, f"FAILED TO GET METADATA: {e}")
            return 0, extra_data

    print_me(printme, f"Checking metadata for `{filename}`:")
    status, extra_data = get_status(input_file, armaturepath)
    print_me(printme, f"[{filename}] STATUS {status}: {status_definitions.get(status)} \n \n")
    return status, extra_data, filename

### FILE CONVERSION ###
def conform_to_armature(filepath, armaturepath):

    has_armature = [1, 3, 5, 7]
    newfile_ext = "gr2"
    if armaturepath != None:
        try:
            arma_status, _, _ = metadata_func(armaturepath, armaturepath, printme=True) # Should use logging levels instead of printme but it'll do for now.
            if arma_status not in has_armature:#[1, 4, 5, 6]:
                print("Provided armature path does not contain a skeleton. Aborting conform process.")
                return None
            if arma_status != 1:
                print("Armature file contains more than just an armature. May fail.")
            temppath = get_temppath()
            divineexe = settings.get("divine_path")
            #print(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}.{newfile_ext}" -i gr2 -o {newfile_ext} -a convert-model -e conform-copy conform-path "{armaturepath}"')
            subprocess.run(f'"{divineexe}" --loglevel warn -g bg3 -s "{filepath}" -d "{temppath}.{newfile_ext}" -i gr2 -o {newfile_ext} -a convert-model -e conform-copy --conform-path "{armaturepath}"')
        except Exception as e:
            print(f"Failed to generate GR2 with new skeleton. Returning early. Reason: {e}")
            return None
    return f"{temppath}.{newfile_ext}"

def convert_to_DAE(filepath, temppath):
    temppath = str(temppath)
    divineexe = settings.get("divine_path")
    try:
            subprocess.run(f'"{divineexe}" --loglevel warn -g bg3 -s "{filepath}" -d "{temppath}" -i gr2 -o dae -a convert-model -e flip-uvs')
    except Exception as e:
        print(f"Failed to generate DAE with Divine. Returning early. Reason: {e}")
        return None

    return temppath

def convert_to_GLB(frompath, fromtype):
    if fromtype.lower() in str(frompath).lower():
        pass
    else:
        frompath = str(frompath)
    temppath = str(get_temppath())
    fromtype = fromtype.replace(".", "")
    divineexe = settings.get("divine_path")
    try:
        subprocess.run(f'"{divineexe}" --loglevel warn -g bg3 -s "{frompath}" -d "{temppath}" -i {fromtype} -o glb -a convert-model -e flip-uvs mirror-skeletons=true')
        if check_file_exists(f"Conversion from {fromtype} to glb", temppath):
            print(f"Conversion from .{fromtype} to .glb was successful.")
        return temppath
    except Exception as e:
        print(f"Failed to generate glb from {fromtype} with Divine. Returning early. Reason: {e}")
        return None

def GR2_to_DAE_to_GLB(filepath, ext):
    dae_path = convert_to_DAE(filepath, ext)
    if dae_path is not None and check_file_exists("dae conversion", dae_path):
        glb_path = convert_to_GLB(dae_path, "dae")
        if glb_path is not None and check_file_exists("glb conversion from dae", glb_path):
            return glb_path
        print("glb conversion from DAE failed. Aborting import.")
        return None

def attempt_conversion(filepath, armaturepath):

    anim_or_static = "static"
    has_anim = [4,41,42,43,5,7]
    
    print("\n")
    print("Beginning import process...")
    print()

    status, _, filename = metadata_func(filepath, armaturepath, False)
    ext = get_filename_ext(filepath)[2]
    if status in has_anim:
        anim_or_static = "animation"
    
    if status in [0, 00, 42] or status is None:
        print(f"[{status} : {status_definitions.get(status)}]. Cannot proceed with import.")
        return None, None

    if status in [1, 2, 3]:
        print(f"Importing static model...")
        try:
            glb_path = convert_to_GLB(filepath, ext)
            if glb_path is None or not check_file_exists("attemptimport: after convert_to_GLB", glb_path):
                print("Direct GLB conversion failed. Attempting full import process.")
                try:
                    glb_path = GR2_to_DAE_to_GLB(filepath, ext)
                except Exception as e:
                    print(f"conversion from GR2 to DAE to GLB failed: {e}")
                if check_file_exists("attemptimport: after convert_to_GLB", glb_path):
                    return glb_path, anim_or_static
                return None, anim_or_static
            else:
                return glb_path, anim_or_static
        except Exception as e:
            print(f"Direct GLB conversion aborted due to error: {e}")
            return None, anim_or_static

    if status in [4, 41, 43]:
        _, armaturename, _ = get_filename_ext(armaturepath) if armaturepath else None
        print(f"Combining {filename} with armature {armaturename}.")
        if status == 43:
            print("Armature contains more than just a skeleton. May fail.")
        combined_path = conform_to_armature(filepath, armaturepath)
        if check_file_exists("attemptimport: combined path", combined_path):
            print("Combined GR2 file created successfully. Updated metadata check:")
            new_status, _, _ = metadata_func(combined_path, armaturepath, False)
            if new_status in [5, 7]:
                print("Attempt direct conversion of armature + anim to glb.")
                glb_path = convert_to_GLB(combined_path, get_filename_ext(combined_path)[2])
                if glb_path:
                    return glb_path, "animation"
            print("Merging of animation + armature did not result in a file with both animation and armature. Will fail.")
            return glb_path, anim_or_static
        return None, anim_or_static

    if status == 5:
        print("GR2 armature with animation")
        glb_path = convert_to_GLB(filepath, get_filename_ext(filepath)[2])
        return glb_path, anim_or_static

    if status == 6:
        if "dae" in ext:
            # DAE file, just convert to glb.
            print(f"DAE file detected: {filename}. Converting to glb.")
            glb_path = convert_to_GLB(filepath, ext)
            if glb_path is None:
                print("Direct GLB conversion failed. Attempting full import process.")
                try:
                    glb_path = GR2_to_DAE_to_GLB(filepath, ext)
                except Exception as e:
                    print(f"conversion from gr2 to dae to glb failed: {e}")
                    return None, anim_or_static
                if glb_path:
                    return glb_path, anim_or_static
                return None, anim_or_static
        else:
            # Assume it's GLTF or GLB at this point. Or unnamed type. Might as well try it. 
            print(f"{filename} is GLB/GLTF. Attempt import directly.")
            return filepath, anim_or_static
    
    else:
        print(f"Anything left at the end of this function: {status}, {filename}")

def get_collection(settings, trimmed_name, state):

    collection = None
    reuse_existing_collection = settings.get("reuse_existing_collection")

    print(f"STATE: {state}, trimmed name: {trimmed_name}")
    if reuse_existing_collection or state == "bulk_anim":
        test = bpy.data.collections.get(trimmed_name)
        if test:
            collection = test

    if not collection or (collection and not reuse_existing_collection and state == "setup"):
        collection = bpy.data.collections.new(trimmed_name)

    if collection:
        try:
            bpy.context.scene.collection.children.link(collection)  ## NOTE: Will fail if the collection is excluded from the view layer. Even if it passed test.
        except:
            vl_collections = bpy.context.view_layer.layer_collection.children
            for coll in vl_collections:
                if coll.name == collection.name:
                    print(f"Confirmed: collection {coll.name} exists in view layer.")
                    if coll.exclude == True:
                        print(f"Collection {coll.name} excluded. Creating new collection.")
                        collection = bpy.data.collections.new(trimmed_name)
                        bpy.context.scene.collection.children.link(collection)

    return collection

def setup_for_import(filepath, settings, anim_coll):
    
    _, filename, _ = get_filename_ext(filepath)
    collection = None
    import_type = settings.get("import_type")
    specified_collection = settings.get("collection_name")
    
    if import_type == "bulk_anim":
        trimmed_name = anim_coll
        specified_collection = True
    elif (specified_collection and specified_collection != ""):
        trimmed_name = specified_collection   
    else:
        trimmed_name = filename.split(".")[0]

    new_collection = get_collection(settings, trimmed_name, import_type) # uses the preset collection name to stop it producing too many collections during bulk import
    
    collection = new_collection
    print(f"Collection.name: {collection.name}")
    layer_collection = bpy.context.view_layer.layer_collection.children[collection.name] ## this will fail if the collection isn't linked to the view layer (which is why get_collection exists).
    bpy.context.view_layer.active_layer_collection = layer_collection
    existing_objects = set(bpy.context.scene.objects)

    return existing_objects

###  IMPORT ###
def import_glb(filename, directory, existing_objects):

    filename = filename + ".glb" if not filename.lower().endswith((".glb", ".gltf")) else filename
    try:
        bpy.ops.import_scene.gltf(filepath=filename, directory=directory, files=[{"name":filename}], loglevel=20)
    except Exception as e:
        print(f"glb import failed: {e}")
        return None

    new_objects = [obj for obj in bpy.context.scene.objects if obj not in existing_objects]
    if new_objects == None:
        print("glb import failed, no new objects imported to scene.")
        return None
    return new_objects

### POST-IMPORT ###
def cleanup(new_objects, status, anim_filename, settings):
    
    # Delete LOD objects ending with _LOD\d+ ## potentially could change the step before this to exclude LODs (within Divine) but leaving it like this for now.
    lod_pattern = re.compile(r'.*_LOD\d+')

    non_lod = []
    lod_objects = [obj for obj in new_objects if lod_pattern.match(obj.name)]
    for item in new_objects:
        if item not in lod_objects:
            non_lod.append(item)

    for obj in lod_objects: # should be an option instead of mandatory. Will add that today.
        bpy.data.objects.remove(obj, do_unlink=True)

    print({'INFO'}, f"Deleted {len(lod_objects)} LOD mesh{'es' if len(lod_objects) != 1 else ''}")

    if not new_objects or all(obj in lod_objects for obj in new_objects):
        print({'WARNING'}, "No non-LOD mesh objects remain after deletion")

    excess_icospheres = []
    
    for obj in bpy.data.collections["glTF_not_exported"].all_objects:
        if obj.name == "Icosphere" or len(bpy.data.collections["glTF_not_exported"].all_objects) == 1: # stops it freaking out if the last icosphere left has the wrong name. Not ideal but okay for placeholder.
            primary = obj
        else:
            excess_icospheres.append(obj)   

    emp_dict = {}
    for obj in non_lod:
        if obj.type == "EMPTY": # have to run this first before any bones have a chance  to move.
            emp_dict.update({obj.name: {"name": obj.name, "obj":obj, "location": obj.matrix_world.translation.copy()}})
    
    armature_list = []
    bone_dict = {}
    for obj in non_lod:
        if obj.type == "ARMATURE":
            bone_names = []
            armature_list.append(obj)
            if settings.get("show_axes"):
                bpy.context.object.data.show_axes = True

            if settings.get("custom_bones"):
                new_custom_name = settings.get("custom_bone_obj")
                scale_custom_bone = settings.get("scale_custom_bone")
                if new_custom_name and new_custom_name.lower() != "ico":
                    if bpy.data.objects.get(new_custom_name):
                        primary=bpy.data.objects.get(new_custom_name)

                for bone in obj.pose.bones:
                    if scale_custom_bone:
                        bone.use_custom_shape_bone_size = True
                    old_ico = bone.custom_shape
                    bone.custom_shape = primary
                    if old_ico != primary:
                        if old_ico not in excess_icospheres:
                            excess_icospheres.add(old_ico)
            else:
                for bone in obj.pose.bones:
                    bone_names.append(bone.name)
                    if bone.custom_shape:
                        bone.custom_shape = None

            def fix_bone_orientation():
                track_bones = []#"Finger2_R", "Finger_R_Endbone"]

                donotmove_bones = ["Root_M"]
                context = bpy.context.object.data.edit_bones
                bpy.ops.object.mode_set(mode='EDIT')

                for bone in context:
                    if bone.name in track_bones:
                        print(f"Bone: {bone.name}, head: {bone.head}, tail: {bone.tail}")
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

                EPSILON = 1e-6 # change this if needed but seems to work okay.
                parents = set()
                children = set()
                for bone in context:
                    entry = bone_dict.get(bone.name)
                    entry.update({"head_pos": bone.head, "tail_pos": bone.tail.copy(), "new_tail_pos": bone.tail, "roll": bone.roll})
                    if bone.name in track_bones:
                        print(f"\n \n Bone: {bone.name}")
                        print("Before anything moves.")
                        for key, value in entry.items():
                            print(key, value)
                    parent = entry.get("parent")
                    if not parent:
                        pass
                    elif parent in donotmove_bones:
                        continue
                    else:
                        siblings = bone_dict.get(parent).get("children")
                        if len(siblings) > 1:
                            continue

                        child = bone.name # could skip this and just keep typing bone.name but I need the clarity for now.
                        if child in track_bones or parent in track_bones in track_bones:
                            print(f"parent: {parent}, child: {child}")
                        children.add(child)
                        parents.add(parent)
                        parent_obj = context.get(parent)
                        childhead = entry.get("head_pos")
                        
                        if (childhead - parent_obj.head).length <= EPSILON:
                            pass
                        else:
                            parent_obj.tail = childhead
                        if bone.name in track_bones:
                            print(f"\n \n Bone: {bone.name}. \n After initial movements:")
                            for key, value in entry.items():
                                print(key, value)

                from mathutils import Quaternion
                counter = 0
                no_movement = []
                bone_angle_dict = {}
                for name, entry in bone_dict.items():
                    counter += 1
                    if entry.get("new_tail_pos") == entry.get("tail_pos"):
                        no_movement.append(name)
            
                for bone in no_movement:
                    parent = bone_dict[bone].get("parent")
                    if bone in donotmove_bones or not parent:
                        continue
                    parenthead = bone_dict[parent].get("head_pos")
                    parenttail = bone_dict[parent].get("tail_pos")
                    parentnewtail = bone_dict[parent].get("new_tail_pos")
                    vec_before = parenttail - parenthead
                    vec_after = parentnewtail - parenthead

                    if bone in track_bones or parent in track_bones:
                        print(f"Before grandparents: bone: {bone}, tail, head: {parenttail}, {parenthead}, newtail, head: {parentnewtail}, {parenthead}, vecbefore: {vec_before}, vecafter: {vec_after}")

                    if vec_after.length <= EPSILON:
                        grandparent = bone_dict[parent].get("parent")
                        parenthead = bone_dict[grandparent].get("head_pos")
                        parenttail = bone_dict[grandparent].get("tail_pos")
                        parentnewtail = bone_dict[grandparent].get("new_tail_pos")
                        
                        vec_before = parenttail - parenthead
                        vec_after = parentnewtail - parenthead
                        if bone in track_bones or parent in track_bones:
                            print("Bone: ", bone, "Parent: ", bone_dict[bone].get("parent"))
                            print("Grandparent: ", bone_dict[parent].get("parent"))
                            print(f"After grandparents: bone: {bone}, tail, head: {parenttail}, {parenthead}, newtail, head: {parentnewtail}, {parenthead}, vecbefore: {vec_before}, vecafter: {vec_after}")
    
                    angle = vec_before.angle(vec_after)
                    axis = vec_before.cross(vec_after)
                    axis.normalize()
 
                    bone_angle_dict[bone] = {
                        "bone": bone,
                        "Angle change": angle,
                        "axis": axis,
                        "dot": vec_before.dot(vec_after)
                    }
                    bone_dict[bone].update({"angle":angle, "axis": axis})

                    childhead = bone_dict[bone].get("head_pos")
                    childtail = bone_dict[bone].get("tail_pos")
                    vec_target = childtail - childhead
                    rot_quat = Quaternion(axis, angle)
                    vec_rotated = rot_quat @ vec_target
                    
                    childtail_new = childhead + vec_rotated
                    if childtail_new <= EPSILON:
                        continue
                    boneobj = context.get(bone)
                    boneobj.tail = childtail_new

                    if bone in track_bones:
                        print(f"\n \n Bone: {bone} \n After all movements.")
                        entry = bone_dict[bone]
                        for key, value in entry.items():
                            print(key, value)

            obj.name = anim_filename[1].split(".")[0]

            if status != "animation" and settings.get("fix_bones"): # I want to implement retargeting directly if I can, but the retargeter I'm used to doesn't work on 5.0 yet and animation seems to be hit-and-miss in the current release version. So for now we just don't apply the fix to anims.
                fix_bone_orientation()

    for ico in excess_icospheres:
        bpy.data.objects.remove(ico,do_unlink=True)

    bpy.ops.object.mode_set(mode='OBJECT')

    if status != "animation" and settings.get("fix_bones"): # this will have to change is full object reorientation comes into play. But that should be done after this, if so. Or before; either way will be fine.
        for empty in emp_dict.keys(): 
            orig_loc = emp_dict.get(empty).get("location")
            empty_object = emp_dict.get(empty).get("obj")
            global_coord = empty_object.matrix_world.translation
            if orig_loc != global_coord:
                empty_object.matrix_world.translation = orig_loc # works
        
    for item in armature_list:
        print(f"Imported:  {item.name}")

    return armature_list

### SET-UP ###

def set_up_bulk_convert(armaturepath, anim_dir, settings):

    print("Warning: May take a while if there are many files to convert.")
    armature_name = get_filename_ext(armaturepath)[1]
    imported_anims = [f"Armature used: {armature_name}"]
    test_list = os.listdir(anim_dir)
    print(f"Test list: {test_list}")
    specified = settings.get("collection_name")
    if specified and specified != "":
        trimmed_name = specified
    else:
        trimmed_name = armature_name.split(".")[0] 
    print(f"Trimmed name for bulk collection: {trimmed_name}")
    bulk_collection = get_collection(settings, trimmed_name, "setup")
    print(f"bulk collection name: {bulk_collection.name}")
    for anim in test_list:
        #print(f"Anim file in provided directory: {anim}")
        filepath = anim_dir + "\\" + anim
        if check_file_exists("testing animation file before bulk conversion", filepath):
            anim_file = import_process(filepath, armaturepath, settings, bulk_collection.name)
            imported_anims.append(anim_file)
        else:
            print("No animation file(s) found.")
    return imported_anims

def import_process(file_to_import, armaturepath, settings, anim_coll):

    if file_to_import is not None:
        converted, status = attempt_conversion(file_to_import, armaturepath)
        if converted:
            directory, filename, _ = get_filename_ext(converted)
            existing_objects = setup_for_import(file_to_import, settings, anim_coll)
            imported = import_glb(filename, directory, existing_objects)

            if imported:
                anim_filename =  get_filename_ext(file_to_import)
                imported_files = cleanup(imported, status, anim_filename, settings)

                ### Add custom properties with import settings (y-up, flip mesh, etc etc) to armature/mesh
                # see 'paper trailing' here: https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x

                print("Import successful.")
                return imported_files
            else:
                print("No files imported. Terminating process.")
                return "No files imported. Terminating process."
        else:
            print("No files converted, and so no imports. Terminating process.")
            return "No files converted, and so no imports. Terminating process."
    else:
        print("File to import is None. Exiting.")
        return "No file to import."

def assign_files(file):

    if "Secondary file (if needed)" in file:
        return 000
    if ".gr2" in str(file).lower():
        print(f"File to import: {file}")
        status, _, _ = metadata_func(file)
        return status
    return 6

def main(file_1, file_2, settings):

    f1_status = f2_status = file_to_import = armaturepath = None
    import_type = settings.get("import_type")

    if import_type == "bulk_anim":
        print("Bulk Anim Mode.")
        if assign_files(file_1) == 1:
            armaturepath = file_1
        elif assign_files(file_1) in has_armature:
            print("Armature file is not just armature: may fail.")
            armaturepath = file_1
        else:
            print("Armature file does not contain a viable armature. Returning.")
            return f"No viable armature in {file_1}"
        anim_dir = file_2
        file_list = set_up_bulk_convert(armaturepath, anim_dir, settings)
        return file_list

    else:
        f1_status = assign_files(file_1)
        #print(f"f1 status: {f1_status}")
        f2_status = assign_files(file_2)
        #print(f"f2 status: {f2_status}")
        if f1_status not in null_status and f2_status in null_status:
            file_to_import = file_1
            print("Only File 1 available; continuing with import.")
        elif f1_status in has_armature and f2_status not in has_armature and f2_status not in null_status: # has armature 
            file_to_import = file_2
            armaturepath = file_1
            print("File 1 has armature, file 2 doesn't.")
        elif f2_status in has_armature and f1_status not in has_armature and f1_status not in null_status: # has armature
            file_to_import = file_1
            armaturepath = file_2
            print("File 2 has armature, file 1 doesn't.")
        elif file_to_import is None and armaturepath != None:
            file_to_import = armaturepath
            print("File 1 doesn't exist, armature does.")
        else:
            file_to_import = file_1
            print("Nothing else applies, assigning file 1 as file to import.")

        #print(f"About to enter import process. File to import: {file_to_import}. Armaturepath: {armaturepath}")
        imported_files = import_process(file_to_import, armaturepath, settings, None)
        file_list = [get_filename_ext(file_to_import)[1], imported_files]
        return file_list

def run(mode, inputs, imp_settings):

    global settings
    settings = imp_settings
    metadata_collection = []
    text_report = initial_setup(mode, settings)
    if text_report and text_report != None:
        return text_report

    armaturepath = None
    if mode == "metadata":
        for file in inputs:
            if metadata_func(file, file, True)[0] == 1: # run this first just to see. Later rewrite it to test 'is one of these an armature' after the initial check, right now the order's all wrong. Going with this for now because I need to test something else first.
                armaturepath = file
        idx = 1
        for file in inputs:
            if "Secondary file (if needed)" in file:
                metadata_collection.append("[File 2: -- No secondary file --]")
                continue
            if ".gr2" not in str(file).lower() and file.strip() != "":
                print(f"[WARN] Cannot get metadata for non-GR2 files ({str(file)}).")
                metadata_collection.append(f"[File {idx}: [{get_filename_ext(file)[1]}] STATUS 6: {status_definitions.get(6)}] \n \n")
                idx += 1
                continue
            if file.strip() == "":
                print(f"No file in fileline {idx}")
                metadata_collection.append(f"[File {idx}: STATUS 0: No Filepath] \n \n")
                idx += 1
                continue

            status, _, filename = metadata_func(file, armaturepath, True) #temporarily true for troubleshooting.
            metadata_collection.append(f"[File {idx}: [{filename}] STATUS {status}: {status_definitions.get(status)}] \n \n")
            idx += 1

        for item in metadata_collection:
            print(item)
        return metadata_collection

    if mode == "import":
        [file_1, file_2] = inputs
        file_list = main(file_1, file_2, settings)
        return file_list
    