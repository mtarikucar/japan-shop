"""Apply the final6 upper-floor Z map to the saved final5 scene; UVs and materials stay as they are.

  blender -b final5/japan_shop_final.blend --python rebuild_v2/scripts/shorten_scene.py
"""
from pathlib import Path
import sys,bpy,numpy as np
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here))
from shorten_upper_floor import BUILDING,remap_vertices
root=here.parents[1];out=root/'final6'
mesh=bpy.data.objects[BUILDING].data
v=np.empty(len(mesh.vertices)*3,dtype=np.float32);mesh.vertices.foreach_get('co',v)
mesh.vertices.foreach_set('co',remap_vertices(v.reshape(-1,3)).reshape(-1));mesh.update()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'japan_shop_final.blend'),compress=True)
print('SHORTENED',BUILDING,'->',out/'japan_shop_final.blend',flush=True)
