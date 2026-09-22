"""Measure the minimum horizontal clearance from the jamb, then move the whole group."""
from pathlib import Path
import trimesh,numpy as np,manifold3d as mf,json
root=Path(__file__).resolve().parents[2];out=root/'final5';cache=root/'rebuild_v2/fit_cache';files={p.stem[:2]:p for p in (out/'stl_montaj').glob('*.stl')}
def solid(m):return mf.Manifold(mf.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
b=solid(trimesh.load_mesh(files['02']));barrels=[solid(trimesh.load_mesh(files[i])) for i in ['15','19']]
def volume(dx):return sum(max(0,(s.translate((dx,0,0))^b).volume()) for s in barrels)
dx=0.
while volume(dx)>.0001:
 dx+=.25
 assert dx<15,'Unexpected jamb clearance'
if dx:dx+=.2
parts=json.loads((out/'parcalar.json').read_text());changes=json.loads((root/'rebuild_v2/reports/fit/changes.json').read_text())
def translate(key,shift):
 p=files[key];m=trimesh.load_mesh(p,process=False);m.apply_translation(shift);m.export(p);m=trimesh.load_mesh(p,process=False);offset=np.array([-m.bounds[:,0].mean(),-m.bounds[:,1].mean(),-m.bounds[0,2]]);copy=m.copy();copy.apply_translation(offset);copy.export(out/'stl_baski'/p.name)
 q=cache/(p.stem+'_fitted.npz');data=np.load(q);np.savez_compressed(q,triangles=m.triangles,uv=data['uv'],materials=data['materials'])
 for rows in [parts,changes]:
  for r in rows:
   if r['name']==p.stem and 'faces' in r:r.update(translation_mm=(np.array(r['translation_mm'])+shift).tolist(),assembly_bounds_mm=m.bounds.tolist(),print_translation_mm=offset.tolist())
if dx:
 for i in range(15,23):translate(f'{i:02}',np.array([dx,0,0]))
barrel=trimesh.load_mesh(files['18']);mat=trimesh.load_mesh(files['23']);matshift=max(0,barrel.bounds[1,0]+1.2-mat.bounds[0,0])
if matshift:translate('23',np.array([matshift,0,0]))
(out/'parcalar.json').write_text(json.dumps(parts,indent=2));(root/'rebuild_v2/reports/fit/changes.json').write_text(json.dumps(changes,indent=2));print('Measured additional barrel shift',dx,'mm; mat shift',matshift,'mm')
