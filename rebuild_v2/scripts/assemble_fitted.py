"""Use fitted STL geometry with original materials, and add the two legacy planters."""
from pathlib import Path
import bpy,numpy as np
root=Path(__file__).resolve().parents[2];out=root/'final5';cache=root/'rebuild_v2/fit_cache'
def material(name,color):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=color;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=color;m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.75;return m
pot=material('Planter stone',(.32,.28,.23,1));soil=material('Soil',(.075,.045,.025,1));bamboo=material('Bamboo foliage',(.14,.27,.07,1));maple=material('Maple foliage',(.42,.075,.025,1))
for p in sorted((out/'stl_montaj').glob('*.stl')):
 old=bpy.data.objects.get(p.stem);materials=list(old.data.materials) if old else []
 if old:bpy.data.objects.remove(old,do_unlink=True)
 bpy.ops.wm.stl_import(filepath=str(p));o=bpy.context.object;o.name=p.stem
 if p.stem[:2] in ['27','28']:
  for m in [pot,soil,bamboo if p.stem[:2]=='27' else maple]:o.data.materials.append(m)
  scale=.65 if p.stem[:2]=='27' else .48
  for poly in o.data.polygons:
   poly.material_index=0 if poly.center.z<20+13*scale else (1 if poly.center.z<20+16*scale else 2)
 else:
  for m in materials:o.data.materials.append(m)
  data=np.load(cache/(p.stem+'_fitted.npz'));layer=o.data.uv_layers.new(name='UVMap');v=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',v);v=v.reshape(-1,3);f=np.empty(len(o.data.loops),dtype=np.int32);o.data.loops.foreach_get('vertex_index',f);assert np.allclose(v[f].reshape(-1,3,3),data['triangles'],atol=2e-5),p.stem
  layer.data.foreach_set('uv',data['uv'].astype(np.float32).reshape(-1));o.data.polygons.foreach_set('material_index',data['materials'].astype(np.int32))
 print('FITTED',p.stem,flush=True)
bpy.data.orphans_purge(do_recursive=True);bpy.context.scene.view_layers[0].material_override=None
bpy.ops.wm.save_as_mainfile(filepath=str(out/'japan_shop_final.blend'),compress=True)
