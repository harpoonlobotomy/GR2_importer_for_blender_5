## CHANGELOG


# CURRENT:
	Version 0.66
	  * Removed temp file mentions from import script
	  * Fixed the bulk import creating one collection per anim if the intended collection was hidden; now it creates one new collection (suffixed) and uses that for all.
          ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ 
	  
	Version 0.65
	  * Fixed bone scaling and custom bones. (Custom bones default to icospheres if not otherwise selected.)
	  * Fixed an issue where the bone orientation fix would disappear control bones.
	  * Updated the UI panel to make it a bit more organised.
	  * Removed temp file options, will look to reimplement later.	
		  
	Version 0.6:
	  (* Made so many little commmits on the test branch, but then merged commits instead of squashing so I may as well have done them on the main branch from the start. Ah well.)
	  * Added open-console bool, use existing collection, disable popups, custom bone bool + 'set from selection' to UI, all working.
	  * Added initial setup to run from the addon (checking for required files, checking import addon is enabled etc)
	  * Fixed the Collection naming; now defaults to the armature name unless something else is specified.
	  * Fixed armature naming; non-animation are named for the primary import object, animation GR2s are named for the animation file.
	  
	Version 0.55:
	  * Improvement to bone orientation, no longer moves towards an arbitrary child. Also added the option in the UI to turn off the bone fix for the current import.
	  * Now allows for custom bones by looking for a named obj in the blend file. Needs a far better way of doing it but it does work, so it's a placeholder.
		  
	Version 0.54:
	  * Bulk importing of animations is now fully supported.
	  * Import and metadata check now works via the UI panel.
		  
	Version 0.5:
	  * Basic functionality of the Blender addon is implemented.
	  * Changed the status enums to work with binary mask, much neater now.
		  
	Version 0.43:
	  * Stopped the bone orientation from being applied to animations. 
	  * Improved tolerance for DAE/GLB/GLTF file imports.	  
	  
	Version 0.41:
	  * Added mass metadata checker; optionally outputs to JSON with status (has armature,  has mesh, etc), internal filename, GR2Tag and local filepath. 
		Currently uses a hardcoded file list. Will add folders later for collecting data en masse, but after the UI panel is done.

	Version 0.4:
	  * Simple GR2/DAE/GLB/GLTF works
	  * Basic animation imports works
	  * Preliminary bone rotation fix is implemented, still needs some adjustment.
	  * Runs as a script in Script Editor directly, with file to be imported named in the code itself.
	  * Metadata-checker to get status before import (ie whether the input GR2 includes animation, skeleton, mesh, etc)
	  * Converter including the automatic combining of animation GR2s with provided matching Skeleton GR2s (as animations without armatures cannot be imported to Blender)
 
	Version 0.3.28:
	  * Fixed Collection naming/allocation: correctly names the Collection either after the import object, or as specified. If the allocated collection is not available, it creates a new collection with '.001' style suffix.

	Version 0.3.2:
	  * Fixed some of the CLI issues with inconsistent filenames.

# TODO:
	As of 25/10/25:
	  * Fix/reimplement Addon Preferences
	  * Looked into the adding retargeting as a post-import option, but Blender 5's animation system is... well broken. so I'm leaving that off the todo list for now.
	  * Delete imported objects of type (eg, delete all but the action data of animation imports (potentially assigning them to a specific one? Not sure.) Maybe. dos2de importer has something like this, worth looking at.
	  DONE Figure out why Finger2_R is pointing in a random direction. It's strange, and every other bone is fine... (Had to use an epsilion, == was too strict.)
	  * Move control empties with bone orientation fix; currently they're left where the bone tail originally was. 
	  * Save UI settings to prefs. 
	  * Sample .blend with custom bones maybe.
	  DONE The panel options have gotten a bit busy. Need to subcategorise.
	  
	As of 22/10/25:
	  * Prefs json is in the works, Blender addon is baseline functional.
	As of 21/10/25:
	  * Add a database lookup for anim/skel combinations. If not 'GR2Tag', can just use the filename or potentially internal filename. (Probably the former more than the latter.)
	  * Set up a prefs json for current filepaths once the UI is in.
	  * If I pull the duration/framerate from the metadata, I could set it to have the frames match the imported anim. Wouldn't need it that often but might be interesting...
	  * Find out how "GR2Tag" applies in the LSF files, see if it can be used for assigning correct skeleton file to anim files.
	  * Automate parentage of imported animations to mesh/obj (optional)
	  * Bone orientation needs calibration; currently is better than importing without fix but is inconsistent. Need to figure out the rules internally for why/when it flips on x/y to be able to compensate.
			- Refer to "bpy.ops.wm.collada_import(filepath=str(collada_path), fix_orientation=True)" from Blender 4.3.2 for the original orientation fixes.
	  * Imports can be optimised, temp files need management. Currently all temp files are simply left in the temp folder. 
			- Need options for autoremoval of temp files and/or designation of output folder.
			- Also the option to name the temp files in accordance with the input file. Currently it just autogenerates a random filename.
	  * Should implement support for export even if I don't need it personally.

	As of 20/10/2025:
	  * Licence details for the portions from LSLib.

	  // Licence notes (temp, will do it properly later)
	    The following files in this repo were taken from [LSLib](https://github.com/Norbyte/lslib) and adjusted to fit this project. Licencing and the relevant copyright for the original content of these files remains with Norbyte.
		- Format.cs
		- Helpers.cs
		- Reader.cs
		- Writer.cs
		- Root.cs
		- Vertex.cs
		- ColladaSchema.cs
		- Common.cs
		- Game.cs
		- granny2wrapper.cpp
		- granny2wrapper.h

	  Portions of GR2Utils.cs were adapted into RootReader.cs

	  Parts of these files have been culled, rearranged and otherwise amended to suit my specific needs. Please refer to the original LSLib repo for anything other than my weird little project - this is in no way a replacement for   the original.

	  -- harpoon