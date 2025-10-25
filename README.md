# GR2 Importer for Blender 5.0+

A Blender 5.0 add-on for importing GR2/DAE models that doesn't rely on OpenCOLLADA. 

With OpenCollada support entirely removed from recent versions of Blender, none of the existing GR2/DAE plugins/addons work anymore*. While GR2/DAE files might not be enormously widely used in 2025, I still use them, and while I still use Blender 4.3 primarily, I want it to be possible in 5.0+.

Requires divine.exe and granny2.dll from https://github.com/Norbyte/lslib 

[Uses multiple altered portions of LSLib for the metadata-checker.]

This is a work in progress, please report any issues/suggestions.

# STATE OF THINGS (as of 21/10/2025):
  * Simple GR2/DAE/GLB/GLTF works
  * Basic animation imports works
  * Preliminary bone rotation fix is implemented, still needs some adjustment.
  * Runs as a script in Script Editor directly, with file to be imported named in the code itself.
  * Metadata-checker to get status before import (ie whether the input GR2 includes animation, skeleton, mesh, etc)
  * Converter including the automatic combining of animation GR2s with provided matching Skeleton GR2s (as animations without armatures cannot be imported to Blender)

# TODO:
  * Bone orientation needs some calibration; it's better than importing without fix but is inconsistent, I need to figure out the rules internally for why/when it flips on x/y to compensate.
  * Imports can be optimised, temp files need management. Currently all temp files are simply left in the temp folder. 
		- Need options for autoremoval of temp files and/or designation of output folder.
		- Also the option to name the temp files in accordance with the input file. Currently it just autogenerates a random filename.
  * Should implement support for export even if I don't need it personally.
  * Actual addon with user preferences and UI panel. <- today's priority.

 -- harpoon

 * It turns out I was wrong. `dos2de_collada_importer` still works. I'm going to finish this anyway, because it does some things differently and I think it's worth finishing, but wanted to acknowledge this.
