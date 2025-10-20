# TODO for Blender 5 GR2/DAE Importer

# 20/10/2025

* Fix import of models without meshes
* Fix bone orientation; it's better than baseline but needs adjustment
* Rework import script to explicitly account for object-types found by the rootreader.
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

Parts of these files have been culled, rearranged and otherwise amended to suit my specific needs. Please refer to the original LSLib repo for anything other than my weird little project - this is in no way a replacement for the original.

-- harpoon