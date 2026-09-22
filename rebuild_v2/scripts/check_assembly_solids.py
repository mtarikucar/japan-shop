"""Check inter-part penetration volume, separately from each part's topology."""
from pathlib import Path
import trimesh,numpy as np,manifold3d as mf,json
root=Path(__file__).resolve().parents[2];out=root/'final5'
items=[]
for p in sorted((out/'stl_montaj').glob('*.stl')):
 m=trimesh.load_mesh(p);s=mf.Manifold(mf.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)));assert s.status()==mf.Error.NoError,p.name;items.append((p.stem,m,s))
records=[]
for i,(n,a,sa) in enumerate(items):
 for name,b,sb in items[i+1:]:
  overlap=np.minimum(a.bounds[1],b.bounds[1])-np.maximum(a.bounds[0],b.bounds[0])
  if np.any(overlap<=.00001):continue
  inter=sa^sb;vol=max(0.,inter.volume());r={'a':n,'b':name,'overlap_volume_mm3':vol};records.append(r);print(n,name,round(vol,6),flush=True)
(out/'parcalar_arasi_kontrol.json').write_text(json.dumps(records,indent=2))
# Numerical slivers below 0.005 cubic mm are below the weld/export tolerance.
bad=[r for r in records if r['overlap_volume_mm3']>.005]
assert not bad,bad
print('PASS: no inter-part penetration above 0.005 mm3')
