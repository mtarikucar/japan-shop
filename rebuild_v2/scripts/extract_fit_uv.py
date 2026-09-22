import bpy,numpy as np
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'fit_cache';out.mkdir(parents=True,exist_ok=True)
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();v=np.array([v.co[:] for v in m.vertices]);tris=np.array([t.vertices[:] for t in m.loop_triangles]);loops=np.array([t.loops[:] for t in m.loop_triangles]);mi=np.array([m.polygons[t.polygon_index].material_index for t in m.loop_triangles]);uv=np.array([d.uv[:] for d in m.uv_layers.active.data])[loops] if m.uv_layers.active else np.zeros((len(tris),3,2))
 np.savez_compressed(out/(o.name+'.npz'),triangles=v[tris],uv=uv,materials=mi)
