## CHANGELOG

[I haven't been very good at this kind of documentation. Working on it.]


# CURRENT:
	Version 0.43:
	  * Stopped the bone orientation from being applied to animations. 
	  * Improved tolerance for DAE/GLB/GLTF file imports.
	  
          ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ 	  
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
	As of 21/10/25:
	  * Add a database lookup for anim/skel combinations. If not 'GR2Tag', can just use the filename or potentially internal filename. (Probably the former more than the latter.)
	  * Set up a prefs json for current filepaths once the UI is in.
	  * Add the option to batch import animations from a folder or list.
	  * If I pull the duration/framerate from the metadata, I could set it to have the frames match the imported anim. Wouldn't need it that often but might be interesting...
	  * Find out how "GR2Tag" applies in the LSF files, see if it can be used for assigning correct skeleton file to anim files.
	  * Automate parentage of imported animations to mesh/obj (optional)
	  * Test for 0-size generated files. Currently they're discovered with the metadata checker, but return the same failure error as viable non-GR2 inputs.
	  * Bone orientation needs calibration; currently is better than importing without fix but is inconsistent. Need to figure out the rules internally for why/when it flips on x/y to be able to compensate.
			- Refer to "bpy.ops.wm.collada_import(filepath=str(collada_path), fix_orientation=True)" from Blender 4.3.2 for the original orientation fixes.
	  * Imports can be optimised, temp files need management. Currently all temp files are simply left in the temp folder. 
			- Need options for autoremoval of temp files and/or designation of output folder.
			- Also the option to name the temp files in accordance with the input file. Currently it just autogenerates a random filename.
	  * Should implement support for export even if I don't need it personally.
	  * Check if 'Game' LS file is actually needed/used at all anymore.
	  * Actual addon with user preferences and UI panel. <- today's priority.


	As of 20/10/2025:
	  DONE Fix import of models without meshes (Tried twice to get strikethrough to work in markdown. Apparently neither worked. Oh well.)
	  DONE Rework import script to explicitly account for object-types found by the rootreader.
	  * Blender UI/Addon
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