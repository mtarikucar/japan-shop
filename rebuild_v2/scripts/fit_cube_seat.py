"""Add a hidden conforming mounting pad behind the projecting lightbox."""
from pathlib import Path
import trimesh,numpy as np,manifold3d as mf,json,pymeshfix
from scipy.spatial import cKDTree
root=Path(__file__).resolve().parents[2];out=root/'final5';cache=root/'rebuild_v2/fit_cache';name='10_kup_tabela'
def solid(m):return mf.Manifold(mf.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
p=out/'stl_montaj'/f'{name}.stl';m=trimesh.load_mesh(p);building=trimesh.load_mesh(out/'stl_montaj/02_bina.stl');changes=json.loads((root/'rebuild_v2/reports/fit/changes.json').read_text());record=next(r for r in changes if r['name']==name and 'faces' in r);x=float(np.load(cache/f'{name}.npz')['triangles'][:,:,0].min())+record['translation_mm'][0]
pad=mf.Manifold.cube((5.5,6,14)).translate((x-4,7,175));s=(solid(m)+pad)-solid(building);a=s.to_mesh();m=trimesh.Trimesh(a.vert_properties[:,:3],a.tri_verts,process=True);m.fix_normals()
if not m.is_watertight:
 m.merge_vertices(digits_vertex=4);m.update_faces(m.nondegenerate_faces());f=pymeshfix.MeshFix(m.vertices,m.faces);f.repair();m=trimesh.Trimesh(f.points,f.faces,process=True)
assert m.is_watertight;m.export(p)
raw=trimesh.load_mesh(p,process=False);shift=np.array([-raw.bounds[:,0].mean(),-raw.bounds[:,1].mean(),-raw.bounds[0,2]]);n=raw.copy();n.apply_translation(shift);n.export(out/'stl_baski'/f'{name}.stl')
changes=json.loads((root/'rebuild_v2/reports/fit/changes.json').read_text());record=next(r for r in changes if r['name']==name and 'faces' in r);delta=np.array(record['translation_mm']);data=np.load(cache/f'{name}.npz');tri=raw.triangles-delta;src=data['triangles'];_,ix=cKDTree(src.mean(1)).query(tri.mean(1));w=trimesh.triangles.points_to_barycentric(np.repeat(src[ix],3,axis=0),tri.reshape(-1,3)).reshape(-1,3,3);w=np.clip(w,0,1);w/=np.maximum(w.sum(axis=2,keepdims=True),1e-15);np.savez_compressed(cache/(name+'_fitted.npz'),triangles=raw.triangles,uv=np.einsum('fij,fjk->fik',w,data['uv'][ix]),materials=data['materials'][ix])
record.update(dimensions_mm=m.extents.tolist(),assembly_bounds_mm=m.bounds.tolist(),print_translation_mm=shift.tolist(),faces=len(m.faces))
(root/'rebuild_v2/reports/fit/changes.json').write_text(json.dumps(changes,indent=2));parts=json.loads((out/'parcalar.json').read_text());parts=[record if r['name']==name else r for r in parts];(out/'parcalar.json').write_text(json.dumps(parts,indent=2));print(name,'mounting seat added',len(m.faces))
