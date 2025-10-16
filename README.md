# GR2_importer_for_blender_5
An addon for Blender 5.0 for importing GR2/DAE models that doesn't rely on OpenCOLLADA. 

With OpenCollada support entirely removed from Blender as of 5.0, none of the existing plugins/addons work in current version of Blender. While GR2/DAE files might not be enormously widely used in 2025, I still use them and I know I'm not alone. 

This is a work in progress, please report any issues/suggestions.

# STATE OF THINGS (as of 16/10/2025):
  * Importing GR2/DAE works
  * Preliminary bone rotation fix is implemented
  * Runs as a script in Script Editor directly, with file to be imported named in the code itself.

# TODO:
  * Bone orientation needs some calibration; certain models have attributes not properly managed yet.
  * Imports can be optimised, temp files need management.
  * Should implement support for export even if I don't need it personally.
  * Actual addon with user preferences and UI panel.
