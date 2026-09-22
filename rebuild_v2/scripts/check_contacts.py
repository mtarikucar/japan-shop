"""Measure signed gaps along the attachment axis on actual mesh surfaces."""
from pathlib import Path
import trimesh,numpy as np,json,sys
src=Path(sys.argv[1]) if len(sys.argv)>1 else Path('final4/stl_montaj')
meshes={p.stem[:2]:trimesh.load_mesh(p) for p in src.glob('*.stl')}
# child, support, axis: +Z support below; +Y support behind.
pairs=[('02','03',2),('03','01',2),('04','26',1),('05','02',1),('26','02',1),('10','02',0),('14','03',2),('23','03',2),('24','01',2),('25','01',2)]+[(f'{i:02}', '03' if i<19 else f'{i-4:02}',2) for i in range(15,23)]+[(f'{i:02}','26',1) for i in range(6,10)]+[(f'{i:02}','02',-2) for i in range(11,14)]
for i in ['27','28']:
 if i in meshes:pairs.append((i,'01',2))
def gaps(child,parent,axis,step=.5):
 if axis==-2:return gaps(parent,child,2,step)
 a=[i for i in range(3) if i!=axis];lo=np.maximum(child.bounds[0,a],parent.bounds[0,a]);hi=np.minimum(child.bounds[1,a],parent.bounds[1,a])
 if np.any(hi<=lo):return None
 g=np.meshgrid(*[np.linspace(lo[j]+.01,hi[j]-.01,min(220,max(3,int((hi[j]-lo[j])/step)+1))) for j in range(2)]);xy=np.column_stack([v.ravel() for v in g]);orig=np.zeros((len(xy),3));orig[:,a]=xy
 vals=[]
 # Bottom of child and top of support for Z; rear child and front support for Y.
 for mesh,sign in [(child,-1 if axis in [0,2] else 1),(parent,1 if axis in [0,2] else -1)]:
  o=orig.copy();o[:,axis]=mesh.bounds[1,axis]+10 if sign==1 else mesh.bounds[0,axis]-10
  d=np.zeros_like(o);d[:,axis]=-sign
  loc,idx,_=mesh.ray.intersects_location(o,d,multiple_hits=True)
  v=np.full(len(o),-np.inf if sign==1 else np.inf)
  if sign==1:np.maximum.at(v,idx,loc[:,axis])
  else:np.minimum.at(v,idx,loc[:,axis])
  vals.append(v)
 good=np.isfinite(vals[0])&np.isfinite(vals[1]);delta=(vals[0]-vals[1]) if axis in [0,2] else (vals[1]-vals[0]);delta=delta[good]
 if len(delta)==0:return None
 return {'min_gap_mm':float(delta.min()),'median_gap_mm':float(np.median(delta)),'max_gap_mm':float(delta.max()),'samples':len(delta),'contact_samples_within_0_025_mm':int((np.abs(delta)<.025).sum()),'closest_sample_mm':float(np.abs(delta).min())}
if __name__=='__main__':
 records=[]
 for c,p,a in pairs:
  r={'child':c,'support':p,'axis':a,'contact':gaps(meshes[c],meshes[p],a)};records.append(r);print(json.dumps(r),flush=True)
 if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(records,indent=2))
 if src.parent.name in ('final5','final6'):
  assert all(r['contact'] and r['contact']['contact_samples_within_0_025_mm']>=3 for r in records),[r for r in records if not r['contact'] or r['contact']['contact_samples_within_0_025_mm']<3]
  print('PASS: measured seating contacts on every required connection')
