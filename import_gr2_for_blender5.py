# Collada import replacement for blender 5.0
# Not perfect, but at present it does successfully import GR2 and DAE, with a start on bone alignment. 
# Still needs more work but it does basically do what I need it to. Meshes + armatures are functional.

# Animations not currently functional. Fails after combining animation GR2 with skeleton GR2. Recursion in one of the bones, not sure why.

# No export functionality at all yet, may implement it later but I only need import for myself so that's my focus.
# 
#  -- harpoon
#  
# 18/10/2025
#

# NOTE: FAILED TO GET METADATA: Expecting value: line 1 column 1 (char 0)
# This: | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
# probably means you added print statements in the exe.

armaturepath = None
    # mesh + armature in same GR2
    #file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\Resources\Proxy_INTDEV_A.GR2"
    #file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"

#file_to_import = r"F:\test\gltf_tests\rpremixed anim and skel as skel to mesh.gr2" # the name lies, it's just intdev cin.
#file_to_import = r"F:\test\gltf_tests\randompeaceintdev defaults copyskel.gr2" ## skel + armaturem, no mesh
file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"

#file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Rig\INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2"
#armaturepath = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"

version = "0.3.2"

mode = "all"#"metadata only"  # other options: "all", "metadata only"
metadata = True


print("\n" *20)
import bpy
from addon_utils import check, enable
import re
import subprocess
import tempfile
from pathlib import Path

use_existing_collection = True
custom_bones_on = True

divineexe = r"F:\Blender\Addons etc\Packed\Tools\Divine.exe"
divinedir = r"F:\Blender\Addons etc\Packed\Tools"
rootreader = r"D:\Git_Repos\GR2_importer_for_blender_5\rootreader\bin\Debug\net8.0\rootreader.exe"

#--- Check required files exist. --- #
for path in [divineexe, rootreader]:
    if not Path(path).is_file():
        print(f"Required file not found: {path}. Please check the paths in the script.")
        print("Press 'Enter' to continue, type 'Exit' to exit.")
        user_input = input()
        if user_input.lower() == 'exit':
            exit()

### --- Ensure console is visible before running anything. --- ###
def is_console_visible():
    import ctypes
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    return hwnd != 0 and ctypes.windll.user32.IsWindowVisible(hwnd)
    
if not is_console_visible():
    bpy.ops.wm.console_toggle()

# Make sure the native GLTF importer is enabled for later. # 
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

### Check what object types are contained in the initial GR2 file. Had to make an exe for this, need to find a simpler way. ###



def get_metadata(filepath):

    import json
    result = subprocess.run(
        [rootreader, filepath],
        capture_output=True,
        text=True, cwd=divinedir ### `cwd`:  set to divine dir to ensure any dependent files are found.
    )

    meshes, armatures, animations = 0, 0, 0
    if result.returncode == 0:
        root_data = json.loads(result.stdout)
        print(root_data['FromFileName'])
        
        if "Skeletons" in root_data and root_data.get("Skeletons") is not None:
            armatures = len(root_data.get('Skeletons', []))
        if "Meshes" in root_data and root_data.get("Meshes") is not None:
            meshes = len(root_data.get('Meshes', []))
        if "Animations" in root_data and root_data.get("Animations") is not None:
            animations = len(root_data.get('Animations', []))

        print(f"Number of Meshes: {meshes}")
        print(f"Number of Skeletons: {armatures}")
        print(f"Number of Animations: {animations}")
        return meshes, armatures, animations
    else:
        print(f"Failed to get metadata: {result.stderr}")
        return None, None, None

def metadata_func(file_to_import):
    try:
        meshes, armatures, animations = get_metadata(file_to_import)
    # this is from chatgpt. I wrote the rest myself so I feel like I should mention the lack of authorship here.
        if meshes is None and armatures is None and animations is None:
            print("Failed to get metadata from GR2 file. Aborting import.")
            exit()
        print(f"Metadata - Meshes: {meshes}, Armatures: {armatures}, Animations: {animations}")

        if animations is not None and armatures is None:
            if armaturepath == None:
                print("File must have a skeleton in order to convert GR2. Please provide filepath to armature GR2 file.")
            else:
                print("Proceeding with conversion, conforming to provided armature file.")
    except Exception as e:
        print(f"FAILED TO GET METADATA: {e}")

def attemptimport(filepath, armaturepath):

    origname = filepath
    def import_gltf(filepath, directory):
        try:
            bpy.ops.import_scene.gltf(filepath=filepath, directory=directory, files=[{"name":filepath}], loglevel=20)
        except Exception as e:
            print(f"GLTF import failed: {e}")
            return None

    def try_divine(filepath, armaturepath):

        temppath = get_temppath()

        def add_armature(filepath, armaturepath):
            print("Adding armature to animation. Armature metadata:: ")
            temppath = get_temppath()
            if armaturepath != None:
                if not Path(armaturepath).is_file():
                    print("Provided armature path is not a valid file. Ignoring.")
                    armaturepath = None
                try:
                    get_metadata(armaturepath)
                    print(f"filepath: {filepath}, armaturepath: {armaturepath}, temppath: {temppath}")
                    print("Divine CLI command for GR2 generation with new skeleton:")
                    print(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}.gr2" -i gr2 -o gr2 -a convert-model -e conform-copy conform-path "{armaturepath}"')
                    subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}.gr2" -i gr2 -o gr2 -a convert-model -e conform-copy --conform-path "{armaturepath}"')
                except Exception as e:
                    print(f"Failed to generate GR2 with new skeleton. Returning early. Reason: {e}")
                    return None
            get_metadata(f"{temppath}.gr2")
            return f"{temppath}.gr2"

        def makedae(filepath, temppath):
            temppath = str(temppath)
            #get_metadata(temppath)
            print(f"Divine CLI command for DAE generation:")
            print(f'"{divineexe}" --loglevel all -g bg3 -s {filepath} -d {temppath} -i gr2 -o dae -a convert-model -e flip-uvs')
            try:
                    subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}" -i gr2 -o dae -a convert-model -e flip-uvs')
            except Exception as e:
                print(f"Failed to generate DAE with Divine. Returning early. Reason: {e}")
                return None

            print("DAE file generated. Moving to generate GLTF.")
            return temppath

        def makegltf(temppath, fromtype):
            if fromtype.lower() in str(temppath).lower():
                pass
            else:
                temppath = str(temppath)
            temppath2 = str(get_temppath())
            
            print(f"Divine CLI command for GLTF generation:")
            print(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o glb -a convert-model -e flip-uvs')
            print()
            try:
                subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o glb -a convert-model -e flip-uvs')
                return temppath2
            except Exception as e:
                print(f"Failed to generate GLTF from {fromtype} with Divine. Returning early. Reason: {e}")
                return None        
        
        if ".gltf" in str(filepath).lower():
            return filepath

        if armaturepath != None:
            print("Armaturepath exists.")
            print("Shouldn't be based on this though. Should be based on the metadata.")
            print("Armaturepath metadata::    ")
            get_metadata(armaturepath)
            print("Filepath metadata:: ")
            get_metadata(filepath)
            new_filepath = add_armature(filepath, armaturepath)
            if new_filepath is None:
                print(("Failed to add armature, returning early."))
                return None
            else:
                print("Armature added successfully.")
                filepath = new_filepath
                
        if "gr2" in str(filepath).lower():
            get_metadata(filepath)

        print()
        #if armaturepath is None:
        #    gltf = makegltf(filepath, "gr2")
        #    if gltf is not None:
        #        print("GR2 to GLTF complete.")
        #        return gltf

        dae = makedae(filepath, temppath)
        if dae:
            gltf = makegltf(dae, "dae")
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

    temppath = try_divine(filepath, armaturepath)
    print("Have finished in try divine.")
    print("Temppath: ", temppath)
    
    temppath2 = temppath + ".glb"
    if not Path(temppath2).is_file():
        temppath2 = temppath
    directory, filename = get_filename(temppath2)
    import_gltf(filename, directory)

    new_objects = [obj for obj in bpy.context.scene.objects if obj not in existing_objects]
    if new_objects == None:
        print("GLTF import failed, no new objects imported to scene.")
        return None, trimmed_name
    return new_objects, trimmed_name

    
def cleanup(new_objects, trimmed_name):
    
    # Delete LOD objects ending with _LOD\d+
    lod_pattern = re.compile(r'.*_LOD\d+')

    non_lod = []
    lod_objects = [obj for obj in new_objects if lod_pattern.match(obj.name)]
    for item in new_objects:
        if item not in lod_objects:
            non_lod.append(item)

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

    armature_list = []
    bone_dict = {}
    oldicos = set()
    #counter = 0
    for obj in non_lod:
        if obj.type == "ARMATURE":
            armature_list.append(obj) # changed back # changed to obj.name from obj.
            for bone in obj.pose.bones:
                if bone.custom_shape or custom_bones_on:
                    if bone.custom_shape:
                        old_ico = bone.custom_shape
                        bone.custom_shape = primary
                        if old_ico != primary:
                            oldicos.add(old_ico)
                    else:
                        bone.custom_shape = primary
 
            def fix_bone_orientation():

                context = bpy.context.object.data.edit_bones
                bpy.ops.object.mode_set(mode='EDIT') # just for set to edit mode, whether it already was or not doesn't seem to error it.
                bpy.context.object.data.show_axes = True # just because it's useful.

                print(f"context: {context}")
                for bone in context:
                    #print(f"Bone: {bone}, head: {bone.head}, tail: {bone.tail}")
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
                        #print(f"Bone: {bone}")
                        parent = bone_dict[bone].get("parent")
                        if not parent:
                            continue
                        parenthead = bone_dict[parent].get("head_pos")
                        parenttail = bone_dict[parent].get("tail_pos")
                        parentnewtail = bone_dict[parent].get("new_tail_pos")
                        vec_before = parenttail - parenthead
                        vec_after  = parentnewtail  - parenthead
                        #print(f"bone: {bone}, tail, head: {parenttail}, {parenthead}, newtail, head: {parentnewtail}, {parenthead}, vecbefore: {vec_before}, vecafter: {vec_after}")
                        
                        if vec_after.length == 0:
                            grandparent = bone_dict[parent].get("parent")
                            parenthead = bone_dict[grandparent].get("head_pos")
                            parenttail = bone_dict[grandparent].get("tail_pos")
                            parentnewtail = bone_dict[grandparent].get("new_tail_pos")
                            
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
                    #print(f"entry: {name}, {entry}, roll: ", roll)
                    if float(roll) < 0:
                        roll = float(roll) * -1
                        bone = context.get(name)
                        if bone:
                            bone.roll = roll
                bpy.ops.object.mode_set(mode='OBJECT')

            fix_bone_orientation()

    for ico in oldicos: # delete here to stop structRNA errors if they're deleted before all objs have been observes.
        bpy.data.objects.remove(ico,do_unlink=True)  ### Only needed if there's more that one option. Otherwise it deletes the one it just created and errors.
           
    print(f"armature list: {armature_list}")

    return armature_list

def main():

# ---------------- try to get metadata first to determine if skeleton, animation, mesh, etc. ----------------- #
    if metadata:

        metadata_func(file_to_import)
    # ----------------- end metadata check ------------------ #

    imported, trimmed_name = attemptimport(file_to_import, armaturepath)
    if imported:
        cleanup(imported, trimmed_name)
        print("Import successful.")

    else:
        print("Failed to import through gltf and divine.")
        
if mode == "metadata only":
    print("Metadata only mode, not importing.")
    metadata_func(file_to_import)
    
elif mode == "all":
    main()

# option to replace existing objects with newly imported ones
