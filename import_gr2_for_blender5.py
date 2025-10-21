# Collada import replacement for blender 5.0
# Not perfect, but at present it does successfully import GR2 and DAE, with a start on bone alignment. 
# Still needs more work but it does basically do what I need it to. Meshes + armatures are functional. Animations import, but obviously the bone misalignment is most apparent there.

# No export functionality at all yet, may implement it later but I only need import for myself so that's my focus.
 
#  -- harpoon
  
# 21/10/2025

armaturepath = None # here to make sure there's always something. I kept commenting it out in testing.

import_list = [r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\Resources\Proxy_INTDEV_A.GR2", r"F:\test\gltf_tests\rpremixed anim and skel as skel to mesh.gr2", r"F:\test\gltf_tests\randompeaceintdev defaults copyskel.gr2", r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2", r"F:\test\gltf_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined_copy_skel.gr2", r"F:\test\gltf_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined.gr2", r"F:\test\gltf_tests\random_peace_with_intdev_cin.gr2", 
r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\OwlBear\OWLBEAR_Cub_Rig\_Construction\Owlbear_Cub_Rig_DFLT_CINE_Curious_HeadTilt_01.GR2", r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\OwlBear\OWLBEAR_Cub_Base.GR2", r"F:\test\gltf_tests\owlbear_mesh.dae", r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Rig\INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2", r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Base.GR2", r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"]

#   21/10/25:
# [DEBUG] Using path: F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Base.GR2
# [DEBUG] Using path: F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Rig\INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2
# [DEBUG] Using path: C:\Users\Gabriel\AppData\Local\Temp\tmph9tdjpg_.gr2
# [INFO] Export completed successfully.
# Combined GR2 file created successfully. Updated metadata check:
# Checking metadata for `tmph9tdjpg_.gr2`:
# [tmph9tdjpg_.gr2] STATUS 5: Armature & animation
# 
# Attempt direct conversion of armature + anim to glb.
# [DEBUG] Using path: C:\Users\Gabriel\AppData\Local\Temp\tmph9tdjpg_.gr2
# [DEBUG] Using path: C:\Users\Gabriel\AppData\Local\Temp\tmpbdudw9ih
# [INFO] Export completed successfully.
# 
# 18:00:57 | INFO: Data are loaded, start creating Blender stuff
# 18:00:57 | INFO: glTF import finished in 0.23s
# {'INFO'} Deleted 0 LOD meshes
# armature list: [bpy.data.objects['Armature.191']]
# Import successful.
# 
#     combined armature + animation files as part of the import process without prior setup. yes. Oh that's nice.
# (Although the bone orientation is drastically more broken. Will sort it out.)

# After a little investigation, the 'new' breakage is actually not that recent - it only looked recent because the earlier tests from today had errored before getting to the bone orientation. Good to know.

#file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\Resources\Proxy_INTDEV_A.GR2"

#file_to_import = r"F:\test\glb_tests\rpremixed anim and skel as skel to mesh.gr2" # the name lies, it's just intdev cin.
#file_to_import = r"F:\test\glb_tests\randompeaceintdev defaults copyskel.gr2" ## skel +  animation, no mesh
## file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"
#armaturepath = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"

#file_to_import = r"F:\test\glb_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined_copy_skel.gr2"
#file_to_import = r"F:\test\glb_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined.gr2" # skel + anim, no mesh, made in stage 2 of testing.
#file_to_import = r"F:\test\glb_tests\random_peace_with_intdev_cin.gr2" # done in converterapp, random peace as input file, intdev cin as armature. copy skeleton from and copy skeleton both on. Everyting else at defaults.
#file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\OwlBear\OWLBEAR_Cub_Rig\_Construction\Owlbear_Cub_Rig_DFLT_CINE_Curious_HeadTilt_01.GR2" ## head tilt animation
#armaturepath = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\OwlBear\OWLBEAR_Cub_Base.GR2"

#file_to_import = r"F:\test\glb_tests\owlbear_mesh.dae"

file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Rig\INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2"
armaturepath = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Base.GR2"

# Want to add a db lookup here. Just get the armature automatically if the file to import requires one.

# v i shouldn't be labelling them like this. Should just be 'file1, file2, file3' (well up to 3, anyway) and then we figure it out from there. Clearer when there's a UI.
#mesh_input = r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"

# Also will need a prefs json to store current filepaths in so I won't have to keep re-stating the last used.

# Also the option to batch import animations. Let me select a bunch of them and work through the list, applying the skel to each and importing in turn.
# oop this is starting to get out of hand.

## Oh, if I pull the duration/framerate from the metadata, I could set it to have the frames match the imported anim. Wouldn't need it that often but might be interesting...

version = "0.43" # animations can now be imported; will not have bone fix applied. Will need to replicate existing retargetting setup as per Blender 4.3.2.

mode = "all"
#mode = "mass_metadata" #"all"#"metadata only"  # other options: "all", "metadata only", "mass_metadata"
metadata = True
specified_collection = "fixed_again_21_10_25"
anim_or_static = "static"

## Mass metadata collection/output:
json_output = False
jsonout_file = f"F:\\test\\gr2_metadata.json" #None

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
    00: "File does not exist",
    0: "No reported mesh, animation or armature",
    1: "Has armature & mesh",
    2: "Animation only, no valid armature provided",
    3: "Animation only GR2, valid armature provided",
    33: "Animation file. Armature file provided is not only armature",
    4: "Armature only",
    5: "Armature & animation",
    6: "Mesh, armature & animation",# (Potentially possible, but not necessarily desirable to generate in all circumstances)"
    7: "DAE filetype",
    8: "GLB/GLTF filetype",
    None: "Critical Error" ## will using 'None' here break things? Potentially...
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

# Make sure the native glb importer is enabled for later. # 
default, enabled = check("io_scene_gltf2")
if not enabled:
    try:
        enable("io_scene_gltf2", default_set=True, persistent=True)
    except Exception as e:
        print(f"Failed to enable gltf importer: {e}")
        print("Please enable the 'gltf 2.0 format' addon manually in Blender preferences and try again.")
        exit()

def print_me(status, *args, **kwargs):
    if status:
        print(*args, **kwargs)

def get_filename_ext(filepath = None):
    if not filepath:
        return None, None
    
    directory, filename = str(filepath).rsplit("\\", 1)
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

def get_metadata(filepath, printme):

    extra_data = {"GR2Tag": None, "Internal_Filename": None}
    import json
    result = subprocess.run(
        [rootreader, filepath],
        capture_output=True,
        text=True, cwd=divinedir ### `cwd`:  set to divine dir to ensure any dependent files are found.
    )

    meshes, armatures, animations = 0, 0, 0
    if result.returncode == 0:
        root_data = json.loads(result.stdout)
        
        if "Skeletons" in root_data and root_data.get("Skeletons") is not None:
            armatures = len(root_data.get('Skeletons', []))
        if "Meshes" in root_data and root_data.get("Meshes") is not None:
            meshes = len(root_data.get('Meshes', []))
        if "Animations" in root_data and root_data.get("Animations") is not None:
            animations = len(root_data.get('Animations', []))
        if "GR2Tag" in root_data and root_data.get("GR2Tag") is not None: # not sure if this is useful at all  yet. Maybe for partial automation of getting matching skeletons. Need to find out how to match to LSF data.
            extra_data.update({"GR2Tag": root_data.get('GR2Tag')})
        extra_data.update({"Internal_Filename": root_data['FromFileName']}) # I think  this is guaranteed to always exist? Would error in the rootreader if not.
        return meshes, armatures, animations, extra_data
    
    else:
        print_me(printme, f"Failed to get metadata: {result.stderr}")
        return None, None, None, None

def metadata_func(input_file, armaturepath=None, printme=True): # going to move the metadata print into this function

    filename = get_filename_ext(input_file)[1]
    if input_file == armaturepath:
        print_me(printme, "Testing armature for metadata:")
    
    import_exists = check_file_exists(f"metadata: {filename}", input_file)
    if not import_exists:
        print_me(printme, f"Import file `{filename}` does not exist. Aborting metadata check.")
        return 00
    
    print_me(printme, f"Checking metadata for `{filename}`:")
    if armaturepath is not None and not check_file_exists("metadata: armature path", armaturepath): ## Not sure if this works. 'If it says there's a path but the file doesn't exist' is the intent.
        armaturepath = None
        print_me(printme, f"Armature path `{filename}` is not a valid file. Ignoring.")

    if ".dae" in str(input_file).lower(): # check these first, don't bother running them for metadata
        return 7, extra_data
    elif ".glb" in str(input_file).lower() or "gltf" in str(input_file).lower():
        return 8, extra_data

    def get_status(input_file, armaturepath):
        try:
            meshes, armatures, animations, extra_data = get_metadata(input_file, printme)
            if meshes is None and armatures is None and animations is None:
                return 0, extra_data
            if armatures > 0 and meshes > 0 and animations == 0:
                return 1, extra_data
            if animations > 0 and armatures == 0 and meshes == 0:
                if armaturepath is not None and check_file_exists("metadata: armature path", armaturepath):
                    skel_meshes, skel_armatures, skel_animations, extra_data = get_metadata(armaturepath, printme)
                    if skel_meshes == 0 and skel_animations == 0 and skel_armatures > 0:
                        return 3, extra_data
                    print_me(printme, "Armature file contains more than just armature. Tentatively returning; may fail.")
                    return 33, extra_data
                armaturepath = None
                return 2, extra_data
            if armatures > 0 and animations == 0 and meshes == 0:
                return 4, extra_data
            if animations > 0 and armatures > 0 and meshes == 0:
                return 5, extra_data
            if animations > 0 and armatures > 0 and meshes > 0:
                return 6, extra_data

        except Exception as e:
            print_me(printme, f"FAILED TO GET METADATA: {e}")
            return 0, extra_data

    status, extra_data = get_status(input_file, armaturepath)
    print_me(printme, f"[{filename}] STATUS {status}: {status_definitions.get(status)} \n \n")
    return status, extra_data

def mass_metadata(input_file_list, metadata_dict):
    for file in input_file_list:
        _, filename, _ = get_filename_ext(file)
        metadata_dict[filename] = {"local_file": file, "status": None, "GR2Tag": None, "Internal_Filename": None}
        status, extra_data = metadata_func(file, armaturepath, printme = False) # now prints internally, don't need to print the prologue.
        metadata_dict[filename].update({
            "status": f"{status}: {status_definitions.get(status)}"})
        if extra_data:
            metadata_dict[filename].update({
            "GR2Tag": extra_data.get("GR2Tag"),
            "Internal_Filename": extra_data.get("Internal_Filename")
        })

    if json_output:
        import json
        with open(jsonout_file, "w+") as f:
            json.dump(metadata_dict, f, indent=2)
        

#### IMPORT HELPERS ####

def conformto_armature(filepath, armaturepath):

    ## Changed this to DAE on a whim. Not sure if it's necessary or not, will test more tomorrow.
    # Need to try making it GLB immediately, see if i can skip the middle steps.
    
    newfile_ext = "gr2"#changed back to GR2 so I can check the metadata
    if armaturepath != None:
        try:
            status, _ = metadata_func(armaturepath, armaturepath, printme=True) # Should use logging levels instead of printme but it'll do for now.
            if status not in [1, 4, 5, 6]:
                print("Provided armature path does not contain a skeleton. Aborting conform process.")
                return None
            if status != 4:
                print("Armature file contains more than just an armature. May fail.")
            temppath = get_temppath()
            #print(f"filepath: {filepath}, armaturepath: {armaturepath}, temppath: {temppath}")
            print("Divine CLI command for GR2 merge with new skeleton:")
            print(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}.{newfile_ext}" -i gr2 -o {newfile_ext} -a convert-model -e conform-copy conform-path "{armaturepath}"')
            subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}.{newfile_ext}" -i gr2 -o {newfile_ext} -a convert-model -e conform-copy --conform-path "{armaturepath}"')
        except Exception as e:
            print(f"Failed to generate GR2 with new skeleton. Returning early. Reason: {e}")
            return None

    return f"{temppath}.{newfile_ext}" ## Not sure if this should be ending with the extension or not. I prefer it as a user, but not sure if it needs.

def convertto_DAE(filepath, temppath):
    temppath = str(temppath)
    print(f"Divine CLI command for GR2 to DAE conversion:")
    print(f'"{divineexe}" --loglevel all -g bg3 -s {filepath} -d {temppath} -i gr2 -o dae -a convert-model -e flip-uvs')
    try:
            subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}" -i gr2 -o dae -a convert-model -e flip-uvs')
    except Exception as e:
        print(f"Failed to generate DAE with Divine. Returning early. Reason: {e}")
        return None
    
    return temppath

def convertto_glb(temppath, fromtype):
    if fromtype.lower() in str(temppath).lower():
        pass
    else:
        temppath = str(temppath)
    temppath2 = str(get_temppath())

    if "." in fromtype:
        fromtype = fromtype.replace(".", "")
    
    print(f"Divine CLI command for {fromtype} to GLB conversion:")
    print(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o glb -a convert-model -e flip-uvs')
    print()
    try:
        subprocess.run(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o glb -a convert-model -e flip-uvs')
        return temppath2
    except Exception as e:
        print(f"Failed to generate glb from {fromtype} with Divine. Returning early. Reason: {e}")
        return None

def GR2_to_glb(filepath, ext):
    dae_path = convertto_DAE(filepath, ext)
    if dae_path is not None and check_file_exists("dae conversion", dae_path):
        print("New metadata check after DAE conversion:")
        status, _ = metadata_func(filepath, armaturepath, printme = True) # I have these two here but they don't do anything. Should just delete both, after checking only GR2s can be read this way.
        glb_path = convertto_glb(dae_path, "dae")
        if glb_path is not None and check_file_exists("glb conversion from dae", glb_path):
            print("glb conversion from DAE successful.")
            status, _ = metadata_func(filepath, armaturepath, printme = True) # I have these two here but they don't do anything. Should just delete both, after checking only GR2s can be read this way.
            return glb_path
        print("glb conversion from DAE failed. Aborting import.")
        return None

def import_glb(filename, directory, existing_objects):

    filename = filename + ".glb" if not filename.lower().endswith((".glb", ".gltf")) else filename
    #print("filepath, directory in import_glb: ", filename, directory)
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
            #print(f"There is already a collection with this name: {trimmed_name}.")
            collection = test

    if not use_existing_collection or not collection:
        collection = bpy.data.collections.new(trimmed_name)

    try:
        bpy.context.scene.collection.children.link(collection)  ## NOTE: Will fail if the collection is excluded from the view layer. Even if it passed test.
    except:
        vl_collections = bpy.context.view_layer.layer_collection.children ### Okay. This needs a cleanup but works, at least in this specific case. If the named one is not excluded, it uses that. If it is excluded (should also check for visibility potentially, too), it makes a new collection and uses that.
        for coll in vl_collections:
            if coll.name == collection.name:
                #print("Confirmed: collection exists in view layer.")
                if coll.exclude == True:
                    #print("Collection excluded. Creating new collection.")
                    collection = bpy.data.collections.new(trimmed_name)
                    bpy.context.scene.collection.children.link(collection)
        pass

    layer_collection = bpy.context.view_layer.layer_collection.children[collection.name] ## this will fail if the collection isn't linked to the view layer.
    bpy.context.view_layer.active_layer_collection = layer_collection

    existing_objects = set(bpy.context.scene.objects)

    return existing_objects

def attempt_conversion(filepath, armaturepath):

# I want to add a json output for conversion. The start files/types, successes and failures. Should make it far clearer to find the patterns of what succeeds/fails if I don't have to remember across runs.
    anim_or_static = "static"

    print("\n" *20)
    print("Beginning import process...")
    print()

    status, _ = metadata_func(filepath, armaturepath, printme = True)
    _, filename, ext = get_filename_ext(filepath)

    if status in [2, 3, 33, 5, 6]:
        anim_or_static = "animation"
    
    if status in [0, 00, 2, None]:
        print(f"[{status} : {status_definitions.get(status)}]. Cannot proceed with import.")
        return None, None

    if status == 1:
        print(f"Importing static model: {filename}")
        try:
            glb_path = convertto_glb(filepath, ext)
            if glb_path is None or not check_file_exists("attemptimport: after convertto_glb", glb_path):
                print("Direct GLB conversion failed. Attempting full import process.")
                try:
                    glb_path = GR2_to_glb(filepath, ext)
                except Exception as e:
                    print(f"conversion from GR2 to DAE to GLB failed: {e}")
                if check_file_exists("attemptimport: after convertto_glb", glb_path):
                    return glb_path, anim_or_static
                return None, anim_or_static
            else:
                return glb_path, anim_or_static
        except Exception as e:
            print(f"Direct GLB conversion aborted due to error: {e}")
            return None, anim_or_static

    if status == 3 or status == 33:
        _, armaturename, _ = get_filename_ext(armaturepath) if armaturepath else None
        print(f"Combining {filename} with armature {armaturename}.")
        if status == 33:
            print("Armature contains more than just a skeleton. May fail.")
        combined_path = conformto_armature(filepath, armaturepath)
        if check_file_exists("attemptimport: combined path", combined_path):
            print("Combined GR2 file created successfully. Updated metadata check:")
            new_status, _ = metadata_func(combined_path, armaturepath, printme = True)
            if new_status in [5, 6]:
                print("Attempt direct conversion of armature + anim to glb.")
                glb_path = convertto_glb(combined_path, get_filename_ext(combined_path)[2])
                return glb_path, anim_or_static
            print("Merging of animation + armature did not result in a file with both animation and armature. Will fail.")
            return glb_path, anim_or_static
        return None, anim_or_static

    if status == 7:
        # DAE file, just convert to glb.
        print(f"DAE file detected: {filename}. Converting to glb.")
        glb_path = convertto_glb(filepath, ext)
        if glb_path is None:
            print("Direct glb conversion failed. Attempting full import process.")
            try:
                glb_path = GR2_to_glb(filepath, ext)
            except Exception as e:
                print(f"conversion from gr2 to dae to glb failed: {e}")
                return None, anim_or_static
            return glb_path, anim_or_static
        
    if status == 8:
        print(f"{filename} is GLB/GLTF. Attempt import directly.")
        return filepath, anim_or_static

def cleanup(new_objects, status):
    
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

            if status != "animation": # for now, just don't apply the fix to animation. I did used to ahve to retarget because I couldn't fix it automatically. Maybe still true.
                fix_bone_orientation()

    for ico in oldicos: # delete here to stop structRNA errors when they're deleted before all objs have been observes.
        bpy.data.objects.remove(ico,do_unlink=True)  ### Only needed if there's more that one option. Otherwise it deletes the one it just created and errors.
      
    for item in armature_list:
        print(f"Imported:    {item.name}")

    return armature_list

def main():

# ---------------- get metadata first to determine if skeleton, animation, mesh, etc. ----------------- #
    if metadata and ".gr2" in str(file_to_import): # only test GR2 files (once confirmed they're the only ones that work, pretty sure that's the case.)
        metadata_func(file_to_import)

    converted, status = attempt_conversion(file_to_import, armaturepath)
    if converted:
        directory, filename, _ = get_filename_ext(converted)
        existing_objects = setup_for_import(file_to_import)
        imported = import_glb(filename, directory, existing_objects)

        if imported:
            cleanup(imported, status)
            print("Import successful.")
        else:
            print("No files imported. Terminating process.")
    else:
        print("No files converted, and so no imports. Terminating process.")

if mode == "mass_metadata":
    print("Mass metadata mode: \n")
    metadata_dict = {}
    mass_metadata(import_list, metadata_dict)

if mode == "metadata only":
    print("Metadata only mode, not importing.")
    if ".gr2" not in str(file_to_import).lower():
        print("Cannot get metadata for non-GR2 files. Exiting.")
        exit()
    metadata_func(file_to_import)
    
elif mode == "all":
    main()

# option to replace existing objects with newly imported ones
