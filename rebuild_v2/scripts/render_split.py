"""Render the split base/building halves opened like a book so cut faces, pegs and holes show.

Does not save the scene.  blender -b final7/japan_shop_final.blend --python rebuild_v2/scripts/render_split.py
"""
from pathlib import Path
import bpy,math
from mathutils import Matrix,Vector
s=bpy.context.scene;out=Path(bpy.data.filepath).parent
left,right=['01a_tabla_sol','02a_bina_sol'],['01b_tabla_sag','02b_bina_sag']
for o in s.objects:
 if o.type=='MESH' and o.name not in left+right:o.hide_render=True
hinge=Vector((-1.0,74.0,0))
for names,angle,dx in [(left,-32,-28),(right,32,28)]:
 m=Matrix.Translation(hinge+Vector((dx,0,0)))@Matrix.Rotation(math.radians(angle),4,'Z')@Matrix.Translation(-hinge)
 for n in names:bpy.data.objects[n].matrix_world=m
cam=s.camera;cen=Vector((0,-10,112));cam.location=cen+Vector((.18,-1,.42))*600
cam.rotation_euler=(cen-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=440
s.render.resolution_x=1800;s.render.resolution_y=1300;s.cycles.samples=24;s.view_layers[0].material_override=None
s.render.filepath=str(out/'bolunmus_parcalar.png');bpy.ops.render.render(write_still=True)
