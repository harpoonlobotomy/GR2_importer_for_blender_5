# ADDON VERSION

#changing the name: GR2 Importer 2025, instead of 'GR2 Importer for Blender 5'. 
# #Shouldn't be too hard to make it backwards compatible with 4.3~, so a year just to indicate 'this is modern' feels better than a specific blender release.

# Collada import replacement for blender 5.0
# Not perfect, but at present it does successfully import GR2 and DAE, with a start on bone alignment. 
# Still needs more work but it does basically do what I need it to. Meshes + armatures are functional. Animations import, but obviously the bone misalignment is most apparent there.

# No export functionality at all yet, may implement it later but I only need import for myself so that's my focus.
 
#  -- harpoon
  
# 22/10/2025


armaturepath = None # here to make sure there's always something. I kept commenting it out in testing.

import_list = [r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\Resources\Proxy_INTDEV_A.GR2", r"F:\test\gltf_tests\rpremixed anim and skel as skel to mesh.gr2", r"F:\test\gltf_tests\randompeaceintdev defaults copyskel.gr2", r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2", r"F:\test\gltf_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined_copy_skel.gr2", r"F:\test\gltf_tests\random_peace_to_intdev_then_intdev_cin_merged_with_the_combined.gr2", r"F:\test\gltf_tests\random_peace_with_intdev_cin.gr2", 
r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\OwlBear\OWLBEAR_Cub_Rig\_Construction\Owlbear_Cub_Rig_DFLT_CINE_Curious_HeadTilt_01.GR2", r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\OwlBear\OWLBEAR_Cub_Base.GR2", r"F:\test\gltf_tests\owlbear_mesh.dae", r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Rig\INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2", r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Base.GR2", r"F:\BG3 Extract PAKs\PAKs\Models\Generated\Public\Shared\Assets\Characters\_Models\_Creatures\Intellect_Devourer\Resources\INTDEV_CIN.GR2"]

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

#file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Rig\INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2"
#armaturepath =
file_to_import = r"F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Base.GR2"

#inputs = None, None#armaturepath, file_to_import

version = "0.6" # adding console control, only checking for relevant files as needed, making sure the glTF addon is enabled when run via the init.
                    #refixed the armature naming/collections, added custom bone support (either by writing the obj name, or setting the selected obj in the UI.)

#mode = "metadata_only"#"all"
#mode = "mass_metadata" #"all"#"metadata only"  # other options: "all", "metadata only", "mass_metadata"
#metadata = True
#specified_collection = "bulk_anim_test_1"
#fix_bones = True
json_output = False
jsonout_file = f"F:\\test\\gr2_metadata.json" #None

import bpy
from addon_utils import check, enable
import re
import subprocess
import tempfile
from pathlib import Path

#use_existing_collection = True
#custom_bones_on = True

divineexe = r"F:\Blender\Addons etc\Packed\Tools\Divine.exe"
divinedir = str(Path(divineexe).parent) #testing
#divinedir = r"F:\Blender\Addons etc\Packed\Tools"
rootreader = r"D:\Git_Repos\GR2_importer_for_blender_5\rootreader\bin\Debug\net8.0\rootreader.exe"

status_definitions = {
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

def initial_setup(mode, settings):

    print(f"Settings: {settings}")
    if mode == "import":
        path = divineexe#"addon preferences/divine" # these don't exist yet.
    elif mode == "metadata":
        path = rootreader#"addon preferences/metadata_checker"

#--- Check required files exist. --- #
    def check_for_exe(path):
        #for path in [divineexe, rootreader]: # prev just checked both, this time only check the one needed.
        if not Path(path).is_file():
            print(f"Required file not found: {path}. Please check the paths in the script.") # should this be filename instead?
            return list(f"Cannot initialise, required file not found: `{path}`.", "Please add correct path in Add-on Preferences.")

    check_for_exe(path)

### --- Ensure console is visible before running anything. --- ###
    def is_console_visible():
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        return hwnd != 0 and ctypes.windll.user32.IsWindowVisible(hwnd)

    if settings.get("open_console"):  
        if not is_console_visible():
            bpy.ops.wm.console_toggle()

    if mode == "import":
        # Make sure the native glb importer is enabled for later. #
        default, enabled = check("io_scene_gltf2")
        if not enabled:
            try:
                enable("io_scene_gltf2", default_set=True, persistent=True)
            except Exception as e:
                print(f"Failed to enable glTF native importer: {e}")
                print("Please enable the 'glTF 2.0 Format' addon manually in Blender preferences and try again.")
                return list(f"Failed to enable glTF Importer: {e}", "Please enable `glTF 2.0 Format` addon manually in Blender Add-ons and try again.")

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

    if filepath == None or not Path(filepath).is_file(): # test this.
        print(f"No file provided for {origin}.")
        return False

    return True

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
            armatures = 1#len(root_data.get('Skeletons', [])) # making it '1' to work with the binary masking
        if "Meshes" in root_data and root_data.get("Meshes") is not None:
            meshes = 1#len(root_data.get('Meshes', []))
        if "Animations" in root_data and root_data.get("Animations") is not None:
            animations = 1#len(root_data.get('Animations', []))
        if "GR2Tag" in root_data and root_data.get("GR2Tag") is not None: # Does this always exist? I think so. # not sure if this is useful at all  yet. Maybe for partial automation of getting matching skeletons. Need to find out how to match to LSF data.
            extra_data.update({"GR2Tag": root_data.get('GR2Tag')})
        extra_data.update({"Internal_Filename": root_data['FromFileName']}) # I think  this is guaranteed to always exist? Would error in the rootreader if not.
        return meshes, armatures, animations, extra_data
    
    else:
        print_me(printme, f"Failed to get metadata: {result.stderr}")
        return None, None, None, None

def metadata_func(input_file, armaturepath=None, printme=True):

    filename = get_filename_ext(input_file)[1]
    extra_data = {}

    import_exists = check_file_exists(f"metadata: {filename}", input_file)
    if not import_exists:
        print_me(printme, f"Import file `{filename}` does not exist. Aborting metadata check.")
        return 00, None, filename
    
    if input_file == armaturepath:
        print_me(printme, "Testing armature file for metadata:")
        skel_meshes, skel_armatures, skel_animations, extra_data = get_metadata(armaturepath, printme)
        if (skel_meshes, skel_armatures, skel_animations) == (0, 0, 1): # this part feels repetitive with 'get_status' now it's updated. Need to fix.
            return 4, extra_data, filename
    
    print_me(printme, f"Checking metadata for `{filename}`:")
    if armaturepath is not None and not check_file_exists("metadata: armature path", armaturepath): ## Not sure if this works. 'If it says there's a path but the file doesn't exist' is the intent.
        armaturepath = None
        print_me(printme, f"Armature path `{filename}` is not a valid file. Ignoring.")

    if ".dae" in str(input_file).lower(): # check these first, don't bother running them for metadata
        return 7, extra_data, filename
    elif ".glb" in str(input_file).lower() or ".gltf" in str(input_file).lower():
        return 8, extra_data, filename

    def get_status(input_file, armaturepath):
        ARM, MSH, ANIM = 1, 2, 4
        try:
            meshes, armatures, animations, extra_data = get_metadata(input_file, printme)
            mesh = meshes * MSH
            armature = armatures * ARM
            anim = animations * ANIM
            content = mesh + armature + anim

            if content == 4:
                if check_file_exists("metadata: armature path", armaturepath):
                    skel_meshes, skel_armatures, skel_animations, _ = get_metadata(armaturepath, printme)
                    if not skel_armatures:
                        return 42, extra_data
                    if skel_armatures and not (skel_meshes or skel_animations):
                        return 41, extra_data
                    print_me(printme, "Armature file contains more than just armature. Tentatively returning; may fail.")
                    return 43, extra_data
                return 42, extra_data

            return content, extra_data

        except Exception as e:
            print_me(printme, f"FAILED TO GET METADATA: {e}")
            return 0, extra_data

    status, extra_data = get_status(input_file, armaturepath)
    print_me(printme, f"[{filename}] STATUS {status}: {status_definitions.get(status)} \n \n")
    return status, extra_data, filename

def mass_metadata(input_file_list):

    metadata_dict = {}

    for file in input_file_list:
        if "gr2" not in file.lower():
            _, filename, _ = get_filename_ext(file)
            metadata_dict[filename] = {"local_file": file, "status": f"6: {status_definitions.get(6)}"}
        else:
            status, extra_data, filename = metadata_func(file, armaturepath, printme = False) # now prints internally, don't need to print the prologue.
            metadata_dict[filename] = {"local_file": file, "status": f"{status}: {status_definitions.get(status)}", "GR2Tag": extra_data.get("GR2Tag"), "Internal_Filename": extra_data.get("Internal_Filename")} #moved these here, move back to separate 'if extra_data' if it causes errors.

    if json_output:
        import json
        with open(jsonout_file, "w+") as f:
            json.dump(metadata_dict, f, indent=2)
        

#### IMPORT HELPERS ####
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
            #print(f"filepath: {filepath}, armaturepath: {armaturepath}, temppath: {temppath}")
            #print("Divine CLI command for GR2 merge with new skeleton:")
            #print(f'"{divineexe}" --loglevel all -g bg3 -s "{filepath}" -d "{temppath}.{newfile_ext}" -i gr2 -o {newfile_ext} -a convert-model -e conform-copy conform-path "{armaturepath}"')
            subprocess.run(f'"{divineexe}" --loglevel warn -g bg3 -s "{filepath}" -d "{temppath}.{newfile_ext}" -i gr2 -o {newfile_ext} -a convert-model -e conform-copy --conform-path "{armaturepath}"')
        except Exception as e:
            print(f"Failed to generate GR2 with new skeleton. Returning early. Reason: {e}")
            return None

    return f"{temppath}.{newfile_ext}"

def convert_to_DAE(filepath, temppath):
    temppath = str(temppath)
    #print(f"Divine CLI command for GR2 to DAE conversion:")
    #print(f'"{divineexe}" --loglevel all -g bg3 -s {filepath} -d {temppath} -i gr2 -o dae -a convert-model -e flip-uvs')
    try:
            subprocess.run(f'"{divineexe}" --loglevel warn -g bg3 -s "{filepath}" -d "{temppath}" -i gr2 -o dae -a convert-model -e flip-uvs')
    except Exception as e:
        print(f"Failed to generate DAE with Divine. Returning early. Reason: {e}")
        return None

    return temppath

def convert_to_GLB(temppath, fromtype):
    if fromtype.lower() in str(temppath).lower():
        pass
    else:
        temppath = str(temppath)
    temppath2 = str(get_temppath())

    fromtype = fromtype.replace(".", "")
    
    #print(f"Divine CLI command for {fromtype.upper()} to GLB conversion:")
    #print(f'"{divineexe}" --loglevel all -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o glb -a convert-model -e flip-uvs')
    #print()
    try:
        subprocess.run(f'"{divineexe}" --loglevel warn -g bg3 -s "{temppath}" -d "{temppath2}" -i {fromtype} -o glb -a convert-model -e flip-uvs')
        return temppath2
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

def setup_for_import(filepath, settings, armaturepath):
    
    _, filename, _ = get_filename_ext(filepath)
    collection = None

    specified_collection = settings.get("collection_name")
    reuse_existing_collection = settings.get("reuse_existing_collection")
    
    if specified_collection and specified_collection != "":
        trimmed_name = specified_collection
    else:
        import_type = settings.get("import_type")
        if import_type == "bulk_anim":
            armature_name = get_filename_ext(armaturepath)[1]
            trimmed_name = armature_name.split(".")[0]
            specified_collection = True # keeps them all in one collection
        else:
            trimmed_name = filename.split(".")[0]

# need the bool for 'use existing collection or make new w suffix'.

    if specified_collection or reuse_existing_collection: ## Add the option to import to selected/active collection, and/or named collection in the UI once it exists.
        test = bpy.data.collections.get(trimmed_name)
        if test:
            print(f"There is already a collection with this name: {trimmed_name}.")
            collection = test

    print(f"Collection: {collection}")
    if not collection or (collection and not reuse_existing_collection):
#    if not specified_collection and not collection: # this requires both to be true or it runs. 
        collection = bpy.data.collections.new(trimmed_name)
        print(f"Collection: {collection}")

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
    
    has_anim = [4,41,42,43,5,7]
    
    print("\n" *20)
    print("Beginning import process...")
    print()

    status, _, filename = metadata_func(filepath, armaturepath, printme = True)
    ext = get_filename_ext(filepath)[2] # check if this works.
    # if not, go back to // _, filename, ext = get_filename_ext(filepath)

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
            new_status, _, _ = metadata_func(combined_path, armaturepath, printme = True)
            if new_status in [5, 7]:
                print("Attempt direct conversion of armature + anim to glb.")
                glb_path = convert_to_GLB(combined_path, get_filename_ext(combined_path)[2])
                return glb_path, "animation"
            print("Merging of animation + armature did not result in a file with both animation and armature. Will fail.")
            return glb_path, anim_or_static
        return None, anim_or_static

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
                return glb_path, anim_or_static
        else:
            # Assume it's GLTF or GLB at this point. Or unnamed type. Might as well try it. 
            print(f"{filename} is GLB/GLTF. Attempt import directly.")
            return filepath, anim_or_static
    
    else:
        print(f"Anything left at the end of this function: {status}, {filename}")
        
def cleanup(new_objects, status, anim_filename, settings):
    
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
    for obj in non_lod:
        if obj.type == "ARMATURE":
            armature_list.append(obj) # changed back # changed to obj.name from obj.
            if settings.get("custom_bones"):
                new_custom_name = settings.get("custom_bone_obj")
                all_obj = set(bpy.context.scene.objects)
                for test in all_obj: ### this is a terrible way to do this.
                    if test.name == new_custom_name:
                        primary = test
                    #this is going to be a next iter, isn't it. It always is.
                for bone in obj.pose.bones:
                    if bone.custom_shape:
                        scale_custom_bone = settings.get("scale_bone")
                        if scale_custom_bone:
                            bone.use_custom_shape_bone_size = True

                        old_ico = bone.custom_shape
                        bone.custom_shape = primary
                        if old_ico != primary:
                            oldicos.add(old_ico)
                    else:
                        bone.custom_shape = primary
            else:
                for bone in obj.pose.bones:
                    if bone.custom_shape:
                        bone.custom_shape = None # likely won't work. Oh, it does.
                ## NOTE: This does not remove the original created ico or its collection. Those area remnant of the native importer.
                # might delete them later, if they're not used by anything after this point?
                # will look into it. See if they're data linked to anything, if not maybe delete, and then if collection empty, remove it too.
            def fix_bone_orientation():

## NOTE: There are certain dummy bones that don't flip orientation (eg Dummy_R_Foot_01/L, Dummy_R_KneeFX_02/L, Dummy_L_Foot_02/R.) Might be able to use that as a stable reference if it holds across armatures.
# Also: DummyLFoot02 and DummyLFoot01 both start from the same relative position, but DummyLFoot02 is twice as long, with its tail far above  the joint. DummyLFoot01 meets the joint neatly.
# Not sure why and don't know what it means.

                donotmove_bones = ["Root_M", ] # just a hardcoded list of bones that should not reorient.

                # will save an armature from the 4.3.2 native importer and compare like bones. See where it's still not quite right.

                context = bpy.context.object.data.edit_bones
                bpy.ops.object.mode_set(mode='EDIT') # just for set to edit mode, whether it already was or not doesn't seem to error it.
                bpy.context.object.data.show_axes = True # just because it's useful.

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
                    elif parent in donotmove_bones: # think this should work?
                        continue
                    else:
                        siblings = bone_dict.get(parent).get("children")
                        print(f"Number of siblings: {len(siblings)}")

                        if len(siblings) > 1:
                            print("Too many kids.")
                            for sib in siblings:
                                print(sib)
                            continue

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
                no_movement = []
                for name, entry in bone_dict.items():
                    counter += 1
                    if entry.get("new_tail_pos") == entry.get("tail_pos"):
                        no_movement.append(name)
                
                if counter != len(no_movement): ## this whole part is silly. 
                    print(f"Total of {counter} bones, {len(no_movement)} did not move. `({no_movement})`")   
                    for bone in no_movement:
                        if bone in donotmove_bones:
                            continue
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

            #print(f"Object name: {obj.name}")
            obj.name = anim_filename[1].split(".")[0]
            #print(f"Anim filename: {anim_filename}")
            #print(f"New object name: {obj.name}")

            if status != "animation": # for now, just don't apply the fix to animation. I did used to have to retarget because I couldn't fix it automatically. Maybe still true.
                if settings.get("fix_bones"):
                    fix_bone_orientation()

    for ico in oldicos:
        bpy.data.objects.remove(ico,do_unlink=True)

    bpy.ops.object.mode_set(mode='OBJECT')

    for item in armature_list:
        print(f"Imported:  {item.name}")

    return armature_list

def set_up_bulk_convert(armaturepath, anim_dir, settings):

    # testing armature: F:\BG3 Extract PAKs\PAKs\Models\Public\Shared\Assets\Characters\_Anims\_Creatures\Intellect_Devourer\INTDEV_Base.GR2
    # testing dir: #  F:\test\gltf_tests\raw_intdev_anims
    print("Warning: May take a while if there are many files to convert.")
    imported_anims = [f"Armature used: {get_filename_ext(armaturepath)[1]}"]
    #get filelist from dir
    import os
    test_list = os.listdir(anim_dir)
    print(f"Test list: {test_list}")
    for anim in test_list:
        print(f"Anim in test list: {anim}")
        filepath = anim_dir + "\\" + anim
        if check_file_exists("testing animation file before bulk conversion", filepath):
            anim_file = import_process(filepath, armaturepath, settings)
            imported_anims.append(anim_file)
        else:
            print("No animation file(s) found.")
    return imported_anims

def import_process(file_to_import, armaturepath, settings):

    print(f"About to start conversion: file_to_import = {file_to_import}, armaturepath = {armaturepath}")
    if file_to_import is not None:
        print("About to attempt conversion.")
        converted, status = attempt_conversion(file_to_import, armaturepath)
        if converted:
            directory, filename, _ = get_filename_ext(converted)
            existing_objects = setup_for_import(file_to_import, settings, armaturepath)
            imported = import_glb(filename, directory, existing_objects)

            if imported:
                anim_filename =  get_filename_ext(file_to_import) # could do this inline but useful to see clearly that it's the anim skel.
                imported_files = cleanup(imported, status, anim_filename, settings)
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

## I don't need this here but the syntax is useful:
# # metadata == True if import_type == "metadata"
# # ==     metadata = (import_type == "metadata")
# extendable: 
#       metadata = import_type in ("metadata", "meta", "md")

    print(f"File to import: {file}")
    if ".gr2" in str(file).lower():
        print("Checking metadata first.")
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
    #    settings = {"collection_name":props.collection_name_override, "import_type":props.import_type, 
    #                "custom_bones":props.use_custom_bone_obj, "custom_bone_obj":props.custom_bone_obj, 
    #                "remove_all_temp":props.remove_temp, "keep_final":props.keep_final}
        file_list = set_up_bulk_convert(armaturepath, anim_dir, settings)
        return file_list

    else:
        f1_status = assign_files(file_1)
        print(f"f1 status: {f1_status}")
        f2_status = assign_files(file_2)
        print(f"f2 status: {f2_status}")
    #allows for more varied armature files, not sure whether it's good or not.
        if file_1 in has_armature and file_2 not in has_armature and f2_status not in [0, 00, None]: # has armature
            file_to_import = file_2
            armaturepath = file_1
        elif file_2 in has_armature and file_1 not in has_armature and f1_status not in [0, 00, None]: # has armature
            file_to_import = file_1
            armaturepath = file_2
        if file_to_import is None and armaturepath != None:
            file_to_import = armaturepath
        else:
            file_to_import = file_1

        imported_files = import_process(file_to_import, armaturepath, settings)
        file_list = [get_filename_ext(file_to_import)[1], imported_files]
        return file_list

def run(mode, inputs, settings=None):
    metadata_collection = []

    initial_setup(mode, settings)

    if mode == "metadata":
        idx = 1
        for file in inputs:
            if "Secondary file (if needed)" in file:
                metadata_collection.append("[File 2: -- No secondary file --]")
                continue
            if ".gr2" not in str(file).lower() and file.strip() != "": # change this to check if it's a file at all maybe. simple regex? Maybe not worth it.
                print(f"[WARN] Cannot get metadata for non-GR2 files ({str(file)}).")
                metadata_collection.append(f"[File {idx}: [{get_filename_ext(file)[1]}] STATUS 6: {status_definitions.get(6)}] \n \n")
                idx += 1
                continue
            if file.strip() == "":
                print(f"No file in fileline {idx}")
                metadata_collection.append(f"[File {idx}: STATUS 0: No Filepath] \n \n")
                idx += 1
                continue
            status, _, filename = metadata_func(file_to_import, None, False)
            metadata_collection.append(f"[File {idx}: [{filename}] STATUS {status}: {status_definitions.get(status)}] \n \n")
            idx += 1

        for item in metadata_collection:
            print(item)
        return metadata_collection

    if mode == "import":
        [file_1, file_2] = inputs
        file_list = main(file_1, file_2, settings)
        return file_list

