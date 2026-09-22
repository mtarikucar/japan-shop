"""Run with Blender: blender -b --python validation/remesh_plants.py -- SOURCE OUTPUT."""
import sys
from pathlib import Path
import bpy

source, output = map(Path, sys.argv[sys.argv.index('--') + 1:])
output.mkdir(parents=True, exist_ok=True)
for name in ['04_sol_saksi_bambu.stl', '05_sag_saksi_akcaagac.stl']:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.stl_import(filepath=str(source / name))
    obj = bpy.context.object
    modifier = obj.modifiers.new('Volume repair', 'REMESH')
    modifier.mode = 'VOXEL'
    modifier.voxel_size = 0.12
    modifier.use_smooth_shade = False
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.ops.wm.stl_export(filepath=str(output / name), export_selected_objects=True)
