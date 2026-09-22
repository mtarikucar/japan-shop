"""Replace 01_tabla and 02_bina in the final6 scene with the final7 halves; UVs come from the old surface.

  blender -b final6/japan_shop_final.blend --python rebuild_v2/scripts/split_scene.py
"""
from pathlib import Path
import sys,bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here))
from split_for_tilt import SPLITS
root=here.parents[1];out=root/'final7'
cut=bpy.data.materials.new('Kesim yuzeyi');cut.use_nodes=True;cut.diffuse_color=(.62,.6,.56,1)
b=next(n for n in cut.node_tree.nodes if n.type=='BSDF_PRINCIPLED');b.inputs['Base Color'].default_value=(.62,.6,.56,1);b.inputs['Roughness'].default_value=.8
for name,_,_,halves in SPLITS:
 old=bpy.data.objects[name];om=old.data;om.calc_loop_triangles();ouv=om.uv_layers.active.data
 tris=[[om.vertices[i].co.copy() for i in t.vertices] for t in om.loop_triangles]
 uvs=[[Vector((*ouv[l].uv,0)) for l in t.loops] for t in om.loop_triangles]
 mats=[om.polygons[t.polygon_index].material_index for t in om.loop_triangles]
 bvh=BVHTree.FromPolygons([v.co for v in om.vertices],[t.vertices[:] for t in om.loop_triangles])
 for new in halves:
  bpy.ops.wm.stl_import(filepath=str(out/'stl_montaj'/(new+'.stl')));o=bpy.context.object;o.name=new;m=o.data
  for mat in om.materials:m.materials.append(mat)
  m.materials.append(cut);ci=len(m.materials)-1
  layer=m.uv_layers.new(name='UVMap')
  for p in m.polygons:
   # Cut faces and pins are not on the old surface: plain cut material, hidden once glued.
   _,_,i,d=bvh.find_nearest(p.center);a,b,c=tris[i];p.material_index=mats[i] if d<1e-4 else ci
   for li in p.loop_indices:
    q=barycentric_transform(m.vertices[m.loops[li].vertex_index].co,a,b,c,*uvs[i]);layer.data[li].uv=(q.x,q.y)
  print('SPLIT',new,len(m.polygons),flush=True)
 bpy.data.objects.remove(old,do_unlink=True)
bpy.data.orphans_purge(do_recursive=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'japan_shop_final.blend'),compress=True)
