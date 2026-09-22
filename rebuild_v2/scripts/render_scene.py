"""Render the saved deliverable scene without modifying its geometry."""
from pathlib import Path
import bpy
from mathutils import Vector
out=Path(__file__).resolve().parents[2]/'final4';s=bpy.context.scene;cam=s.camera
for name,d in [('izometrik',(-.48,-1,.36)),('on',(0,-1,.05)),('arka',(.6,1,.45)),('mesh_kontrol',(-.48,-1,.36))]:
 cen=Vector((0,7,121));cam.location=cen+Vector(d)*450;cam.rotation_euler=(cen-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=320
 if name=='mesh_kontrol':
  m=bpy.data.materials.new('Inspection clay');m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.22,.26,.3,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.75;s.view_layers[0].material_override=m
 s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
