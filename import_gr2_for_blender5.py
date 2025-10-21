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

##Testing mesh/armature/animation combinations.##

# stage 1:
#   input file: INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2
#   armaturepath: INTDEV_CIN.GR2
#   output:
#    F:\test\gltf_tests\random_peace_to_intdev.gr2 == Internal filename:  C:/Users/Merel.Beers/Perforce/beers_merelfw4main/ASSETS/Art/GUSTAV/Data/Public/Shared/Assets/Characters/_Anims/_Creatures/Intellect_Devourer/INTDEV_Rig/INTDEV_Rig_DFLT_IDLE_Random_Peace_01.ma
                            #Metadata - Meshes: 0, Armatures: 1, Animations: 1

# stage 2:
#   input file: INTDEV_CIN.GR2
#   armaturepath: F:\test\gltf_tests\random_peace_to_intdev.gr2
#   output:
#    F:\test\gltf_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined.gr2 == Internal filename:  c:\FW4\ASSETS\Art\GUSTAV\Data\Public\Shared\Assets\Characters\_Rigs\_Creatures\Intellect_Devourer\INTDEV_Rig_Skinning.ma
#                           Metadata - Meshes: 5, Armatures: 1, Animations: 0

#stage 3:
#    this time, same input/armature files, but with 'copy skeleton' on:
#        F:\test\gltf_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined_copy_skel.gr2

#  input file: F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2 (mesh, armature)

#So I can't get metadata if it's not GR2. So I can't test the DAE files in the same way I can the GR2s. Need to make those checks contitional.

armaturepath = None
    # mesh + armature in same GR2
#file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\Resources\Proxy_INTDEV_A.GR2"

#file_to_import = r"F:\test\gltf_tests\rpremixed anim and skel as skel to mesh.gr2" # the name lies, it's just intdev cin.
#file_to_import = r"F:\test\gltf_tests\randompeaceintdev defaults copyskel.gr2" ## skel +  animation, no mesh
#file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"

#file_to_import = r"F:\test\gltf_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined_copy_skel.gr2"
#file_to_import = r"F:\test\gltf_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined.gr2" # skel + anim, no mesh, made in stage 2 of testing.
#file_to_import = r"F:\test\gltf_tests\random_peace_with_intdev_cin.gr2" # done in converterapp, random peace as input file, intdev cin as armature. copy skeleton from and copy skeleton both on. Everyting else at defaults.
#           1 armature, 1 animation, 0 meshes.

#file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\OwlBear\OWLBEAR_Cub_Rig\_Construction\Owlbear_Cub_Rig_DFLT_CINE_Curious_HeadTilt_01.GR2" ## head tilt animation
#armaturepath = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\OwlBear\OWLBEAR_Cub_Base.GR2"

#file_to_import = r"F:\test\gltf_tests\owlbear_mesh.dae"
file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Rig\INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2"
armaturepath = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Base.GR2"

#armaturepath = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"

version = "0.4" # animations can now be imported. ::TODO: potentially automate parentage of imported anim + mesh pairings.
#                                                          :: eg: "Animation file: ___", "Armature file: _____", "Mesh file: _______" and then combine them. 
#                                                            Also the ability to combine existing parts. If i have a good mesh body, let me apply the skeleton to it in some way. Previously Iv'e had to do it with retargeting but maybe I can find a better way now, idk.
#                               If not any of that at least I can just set the collection. Maybe if a skeleton obj is specified, pick that collection automatically. That'd be nice. So if I'm
            #                       importing animations for the Mindflayer, and have a mindflayer model already set up, I can tell it 'this is the model I'm using' and either have it allocate the actions to that figure, 
            #                           some level of retargeting, or simply put it into the same collection so I can do the rest myself more conveniently.

mode = "all"#"metadata only"  # other options: "all", "metadata only"
metadata = False
specified_collection = "intdev_with_proper_skel"#IDLE_Random_Peace_01_20_10_25_02"

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

status_definitions = {
    0: "failed to get metadata",
    1: "armature + mesh (default for static models)",
    2: "animation only, needs armature to work (default for animated models)",
    3: "animation only GR2, armature file provided.",
    4: "armature + animation (merged) (currently cannot be imported due to lack of mesh)",
    5: "mesh, armature, animation (fully combined.)",# (Potentially possible but not necessarily desirable in all circumstances)"
    6: "no metadata results but is .dae filetype",
    7: "armature only"
}

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
    try:
        enable("io_scene_gltf2", default_set=True, persistent=True)
    except Exception as e:
        print(f"Failed to enable GLTF importer: {e}")
        print("Please enable the 'glTF 2.0 format' addon manually in Blender preferences and try again.")
        exit()

def get_filename_ext(filepath = None):
    if not filepath:
        return None, None
    #print("Filepath in get_filename_ext: ", filepath)
    directory, filename = filepath.rsplit("\\", 1)
    ext = filename.split(".")[-1]
    return directory, filename, ext.lower()

def get_temppath():
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    tempfile_path = Path(temp.name)
    return tempfile_path

def check_file_exists(origin, filepath):

    if filepath == None:
        print(f"No file provided for {origin}.")
        return False
    if not Path(filepath).is_file():
        print(f"File in `{origin}` does not exist: {filepath}")
        return False
    return True

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
        print()
        print("Internal filename: ", root_data['FromFileName'])
        
        if "Skeletons" in root_data and root_data.get("Skeletons") is not None:
            armatures = len(root_data.get('Skeletons', []))
        if "Meshes" in root_data and root_data.get("Meshes") is not None:
            meshes = len(root_data.get('Meshes', []))
        if "Animations" in root_data and root_data.get("Animations") is not None:
            animations = len(root_data.get('Animations', []))

        return meshes, armatures, animations
    else:
        print(f"Failed to get metadata: {result.stderr}")
        return None, None, None

def metadata_func(input_file, armaturepath=None):

    if input_file == armaturepath:
        print("Testing armature for metadata:")
        

    # this should be broken up into multiple parts. I'm checking the armaturepath each time, I should just make that a bool and have the input file be the one I'm testing. Sounds better.

    # Check that both files exists before proceeding.
    import_exists = check_file_exists("metadata: input file", input_file)
    if not import_exists:
        print("Import file does not exist. Aborting metadata check.")
        return 0
    
    print(f"Checking metadata for file to import: { get_filename_ext(input_file)[1] }")
    if armaturepath is not None and not check_file_exists("metadata: armature path", armaturepath): ## Not sure if this works. 'If it says there's a path but the file doesn't exist' is the intent.
        armaturepath = None
        print("Provided armature path is not a valid file. Ignoring.")

 ## LEGEND:    ##       
    # 0 = failed to get metadata
    # 1 = armature + mesh (default for static models)
    # 2 = animation only, needs armature to work (default for animated models)
    # 3 = animation only GR2, armature file provided.

    # 4 = armature + animation (merged) (currently cannot be imported due to lack of mesh)
    # 5 = mesh, armature, animation (fully combined.) (Potentially possible but not necessarily desirable in all circumstances)
    # 6 = no results but is .dae filetype
    # 7 = armature only

    try:
        meshes, armatures, animations = get_metadata(input_file)
        
        if meshes is None and armatures is None and animations is None:
            if ".dae" in str(input_file).lower():
                print("DAE file detected, cannot get metadata but assuming valid for import.")
                return 6
            print("No reported mesh, armature or animation; cannot read metadata.")
            return 0
        print(f"Metadata - Meshes: {meshes}, Armatures: {armatures}, Animations: {animations}")

        if armatures > 0 and meshes > 0 and animations == 0:
            return 1
        if animations > 0 and armatures == 0 and meshes == 0:
            if armaturepath is None or not check_file_exists("metadata: armature path", armaturepath):
                armaturepath = None
                return 2
            return 3
        if animations > 0 and armatures > 0 and meshes == 0:
            return 4
        if animations > 0 and armatures > 0 and meshes > 0:
            return 5
        if armatures > 0 and animations == 0 and meshes == 0:
            return 7

    except Exception as e:
        print(f"FAILED TO GET METADATA: {e}")

#### IMPORT HELPERS ####

def conformto_armature(filepath, armaturepath):

    ## Changed this to DAE on a whim. Not sure if it's necessary or not, will test more tomorrow.
    newfile_ext = "dae"
    if armaturepath != None:
        try:
            print("Metadata for armaturepath: (must contain skeleton)")
            status = metadata_func(armaturepath, armaturepath)
            print(f"Status {status}: `{status_definitions.get(status)}`")
            if status not in [1,4,5,7]:
                print("Provided armature path does not contain a skeleton. Aborting conform process.")
                return None
            print()
            temppath = get_temppath()
            print(f"filepath: {filepath}, armaturepath: {armaturepath}, temppath: {temppath}")
            print("Divine CLI command for GR2 generation with new skeleton:")
            print(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}.{newfile_ext}" -i gr2 -o {newfile_ext} -a convert-model -e conform-copy conform-path "{armaturepath}"')
            subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}.{newfile_ext}" -i gr2 -o {newfile_ext} -a convert-model -e conform-copy --conform-path "{armaturepath}"')
        except Exception as e:
            print(f"Failed to generate GR2 with new skeleton. Returning early. Reason: {e}")
            return None
    
    return f"{temppath}.{newfile_ext}" ## Not sure if this should be ending with GR2, it often omits its own temp file extensions.

def convertto_DAE(filepath, temppath):
    temppath = str(temppath)
    print(f"Divine CLI command for DAE generation:")
    print(f'"{divineexe}" --loglevel all -g bg3 -s {filepath} -d {temppath} -i gr2 -o dae -a convert-model -e flip-uvs') ## if I turn flip uvs off, does it drop the requirement for mesh dict in import?
    try:
            subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}" -i gr2 -o dae -a convert-model -e flip-uvs')
    except Exception as e:
        print(f"Failed to generate DAE with Divine. Returning early. Reason: {e}")
        return None

    return temppath

def convertto_GLTF(temppath, fromtype):
    if fromtype.lower() in str(temppath).lower():
        pass
    else:
        temppath = str(temppath)
    temppath2 = str(get_temppath())

    if "." in fromtype:
        fromtype = fromtype.replace(".", "")
    
    print(f"Divine CLI command for GLTF generation:")
    print(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o glb -a convert-model -e flip-uvs')
    print()
    try:
        subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o glb -a convert-model -e flip-uvs')
        return temppath2
    except Exception as e:
        print(f"Failed to generate GLTF from {fromtype} with Divine. Returning early. Reason: {e}")
        return None

def GR2_to_gltf(filepath, ext):
    dae_path = convertto_DAE(filepath, ext)
    if dae_path is not None and check_file_exists("dae conversion", dae_path):
        print("New metadata check after DAE conversion:")
        status = metadata_func(filepath, armaturepath)
        print(f"Status {status}: `{status_definitions.get(status)}`")
        gltf_path = convertto_GLTF(dae_path, "dae")
        if gltf_path is not None and check_file_exists("gltf conversion from dae", gltf_path):
            print("GLTF conversion from DAE successful.")
            status = metadata_func(filepath, armaturepath)
            print(f"Status {status}: `{status_definitions.get(status)}`")
            return gltf_path
        print("GLTF conversion from DAE failed. Aborting import.")
        return None

def import_gltf(filename, directory, existing_objects):

    filename = filename + ".glb" if not filename.lower().endswith((".gltf", ".glb")) else filename
    print("filepath, directory in import_gltf: ", filename, directory)
    try:
        bpy.ops.import_scene.gltf(filepath=filename, directory=directory, files=[{"name":filename}], loglevel=20)
    except Exception as e:
        print(f"GLTF import failed: {e}")
        return None

    new_objects = [obj for obj in bpy.context.scene.objects if obj not in existing_objects]
    if new_objects == None:
        print("GLTF import failed, no new objects imported to scene.")
        return None
    return new_objects


def setup_for_import(filepath):
    
    _, filename, _ = get_filename_ext(filepath)
    collection = None

    if specified_collection:
        trimmed_name = specified_collection
    else:
        trimmed_name = filename.split(".")[0]

    if use_existing_collection: ## Add the option to import to selected/active collection, and/or named collection in the UI once it exists.
        test = bpy.data.collections.get(trimmed_name)
        if test:
            print(f"There is already a collection with this name: {trimmed_name}.")
            collection = test

    if not use_existing_collection or not collection:
        collection = bpy.data.collections.new(trimmed_name)

    try:
        bpy.context.scene.collection.children.link(collection)  ## NOTE: Will fail if the collection is excluded from the view layer. Even if it passed test.
    except:
        vl_collections = bpy.context.view_layer.layer_collection.children ### Okay. This needs a cleanup but works, at least in this specific case. If the named one is not excluded, it uses that. If it is excluded (should also check for visibility potentially, too), it makes a new collection and uses that.
        for coll in vl_collections:
            if coll.name == collection.name:
                print("Confirmed: collection exists in view layer.")
                if coll.exclude == True:
                    print("Collection excluded. Creating new collection.")
                    collection = bpy.data.collections.new(trimmed_name)
                    bpy.context.scene.collection.children.link(collection)
        else:
            print("Really failed this time. Apparently the layer collection exists in the  view layer but linking still failed.")
        pass

    layer_collection = bpy.context.view_layer.layer_collection.children[collection.name] ## this will fail if the collection isn't linked to the view layer.
    bpy.context.view_layer.active_layer_collection = layer_collection

    existing_objects = set(bpy.context.scene.objects)

    return existing_objects

def attempt_conversion(filepath, armaturepath):

    print("\n" *20)
    print("Beginning import process...")
    print()

    status = metadata_func(filepath, armaturepath)
    print()
    _, filename, ext = get_filename_ext(filepath)
    print(f"Status {status}: `{status_definitions.get(status)}`")

    if status in [0, None]:
        print("Metadata check failed, cannot proceed with import.")
        return None

    if status == 1:
        print(f"Importing static model: {filename}")
        try:
            gltf_path = convertto_GLTF(filepath, ext)
            if gltf_path is None:
                print("Direct GLTF conversion failed. Attempting full import process.")
                try:
                    gltf_path = GR2_to_gltf(filepath, ext)
                except Exception as e:
                    print(f"conversion from gr2 to dae to gltf failed: {e}")
                    return None
                return gltf_path
            else:
                print("New metadata check after direct GLTF conversion:")
                status = metadata_func(gltf_path, armaturepath)
                print(f"Status {status}: `{status_definitions.get(status)}`") ## Is there any point in having this here? It's not a GR2 anymore so this can't read it, right?
                return gltf_path
        except Exception as e:
            print(f"Direct GLTF conversion aborted due to error: {e}")
            return None

    if status == 3:
        _, armaturename, _ = get_filename_ext(armaturepath) if armaturepath else None
        print(f"Combining {filename} with armature {armaturename}.")
        combined_path = conformto_armature(filepath, armaturepath)
        if check_file_exists("attemptimport: combined path", combined_path):
            print("Combined GR2 file created successfully. Updated metadata check:")
            new_status = metadata_func(combined_path, armaturepath)
            print(f"{new_status}: {status_definitions.get(new_status)}")
            # Metadata - Meshes: 0, Armatures: 1, Animations: 1
            if new_status in [4, 6]:
                print("Attempt direct conversion of armature + anim to GLTF.")
                _, _, ext = get_filename_ext(combined_path)
                gltf_path = convertto_GLTF(combined_path, ext)
                return gltf_path
        return None

    if status == 6:
        # DAE file, just convert to GLTF.
        print(f"DAE file detected: {filename}. Converting to GLTF.")
        gltf_path = convertto_GLTF(filepath, ext)
        if gltf_path is None:
            print("Direct GLTF conversion failed. Attempting full import process.")
            try:
                gltf_path = GR2_to_gltf(filepath, ext)
            except Exception as e:
                print(f"conversion from gr2 to dae to gltf failed: {e}")
                return None
            return gltf_path
    print()

def cleanup(new_objects):
    
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

    converted = attempt_conversion(file_to_import, armaturepath)
    if converted:
        directory, filename, _ = get_filename_ext(converted)
        existing_objects = setup_for_import(file_to_import)
        imported = import_gltf(filename, directory, existing_objects)

        if imported:
            cleanup(imported)
            print("Import successful.")
        else:
            print("No files imported. Terminating process.")
    else:
        print("No files converted, and so no imports. Terminating process.")
        
if mode == "metadata only":
    print("Metadata only mode, not importing.")
    metadata_func(file_to_import)
    
elif mode == "all":
    main()

# option to replace existing objects with newly imported ones
