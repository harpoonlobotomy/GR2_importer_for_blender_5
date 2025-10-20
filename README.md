# GR2_importer_for_blender_5

A Blender 5.0 add-on for importing GR2/DAE models that doesn't rely on OpenCOLLADA. 

With OpenCollada support entirely removed from recent versions of Blender, none of the existing GR2/DAE plugins/addons work in current version of Blender. While GR2/DAE files might not be enormously widely used in 2025, I still use them, and I know I'm not entirely alone in that. 

Requires divine.exe and granny2.dll from https://github.com/Norbyte/lslib 

[Uses multiple portions of LSLib for the metadata-checker; currently testing how much I can cull it back to only scrape the specific data it needs.]

This is a work in progress, please report any issues/suggestions.

# STATE OF THINGS (as of 20/10/2025):
  * Importing GR2/DAE works, although imperfectly. Basic armatures + meshes import nicely, aside from some bone orientation issues.
  * Preliminary bone rotation fix is implemented, still needs some adjustment.
  * Runs as a script in Script Editor directly, with file to be imported named in the code itself.
  * Made a metadata-checker to get status before import (ie GR2 includes animation, includes skeleton, etc) so I can modify the args as needed.


# TODO:
  * Implementing automatic conform-copy to target skeleton now to prevent the same issue that the native Collada import had, that required animations to have the skeleton merged manually beforehand. Theoretically exists currently but unreliable.
  * Bone orientation needs some calibration; certain models have attributes not properly managed yet.
  * Imports can be optimised, temp files need management.
  * Should implement support for export even if I don't need it personally.
  * Actual addon with user preferences and UI panel.
