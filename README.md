# GR2 Importer for Blender 5.0+

GR2 Importer for Blender 5 is a Blender add-on for importing GR2 models and animations directly into Blender 5, without relying on the (now removed) Collada support.

With OpenCollada support entirely removed from recent versions of Blender, none of the existing GR2/DAE plugins/addons work anymore*. While GR2/DAE files might not be enormously widely used in 2025, I still use them, and while I still use Blender 4.3 primarily, I want it to be possible in 5.0+.

It handles:

Armature & animation merging: automatically combines animation-only GR2s with armature-containing GR2s.

Simple import: Armature-only, armature+mesh and armature+animation all supported.

Bulk animation import: import entire folders of animations for a single armature in one go.

Automatic renaming & collections: imported animations rename the armature and organize objects into dedicated collections for clarity.

Metadata inspection: a lightweight helper (`rootreader`) analyzes GR2 files before import, detecting object types (armature, animation, mesh) to streamline the workflow.

This add-on is designed to be self-contained, and user-friendly, enabling GR2 assets even without Collada. Made for modders, animators, and anyone working with older game models in Blender.


[Casual disclaimers: 
	All my testing so far has been done with GB3 models, as that's what I have access to at present.
	I've only been coding a few months, and I'm still figuring it out. Please let me know of any issues that aren't in the changelog.]

Requires `divine.exe` and `granny2.dll` from https://github.com/Norbyte/lslib 

[Uses multiple altered portions of LSLib for the metadata-checker.]

## This is a work in progress, please report any issues/suggestions.

 STATE OF THINGS (as of 25/10/2025):
  * Basic GR2/DAE/GLB/GLTF import
  * Basic animation imports work but requires manual retargeting - working on this
  * Bulk animation import: multiple animations with a common armature can be imported at once
  * Preliminary bone rotation fix is implemented (still needs some adjustment)
  * Runs as an addon, installed from a .zip
  * Metadata-checker to get status before import (ie whether the input GR2 includes animation, skeleton, mesh, etc)
  * Converter including the automatic combining of animation GR2s with provided armature GR2s (as animations without armatures cannot be imported to Blender)

 -- harpoon


[[ It turns out I was wrong. `dos2de_collada_importer` still works. I'm going to finish this anyway, because it does some things differently and I think it's worth finishing, but wanted to acknowledge this. ]]

