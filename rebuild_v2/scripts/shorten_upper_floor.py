"""Remove 24 mm from the building's upper window floor and write the final6 STL set.

The upper floor (saçak top to roof, Z 198.9-240) is only ~41 mm tall, so one
contiguous 24 mm cut would take out the window sills or the roof edge. Instead
the height is taken from the Z bands whose cross-section is constant on all four
sides (plain wall under the sills, window glass), and the sill/frame and side
cornice bands are shortened slightly. Only Z is remapped, strictly increasing,
so the triangle topology, watertightness and UVs of the mesh are untouched.
Everything below Z 198.9 (saçak, storefront, the cube sign mount) is unchanged.

  python rebuild_v2/scripts/shorten_upper_floor.py            # final5 -> final6
"""
from pathlib import Path
import json,shutil,sys
import numpy as np

# (original Z, new Z) control points. Bands between them are mapped linearly.
KNOTS=np.array([
 (0.0,0.0),
 (198.9,198.9),   # top of the saçak box: fixed
 (213.3,200.7),   # plain wall under sills 14.4 -> 1.8 mm
 (219.9,206.1),   # sill + lower frame rail 6.6 -> 5.4 mm
 (228.5,207.7),   # window glass 8.6 -> 1.6 mm
 (231.5,210.1),   # side/back cornice 3.0 -> 2.4 mm
 (234.5,210.5),   # window glass 3.0 -> 0.4 mm
 (240.0,216.0),   # roof edge, upper frame, parapet: shifted only
 (1000.0,976.0),
])
BUILDING='02_bina'

def remap_z(z):
 z=np.asarray(z,dtype=np.float64)
 return np.interp(z,KNOTS[:,0],KNOTS[:,1])

def remap_vertices(v):
 """float32 (...,3) -> float32 (...,3); identical inputs give identical outputs."""
 v=np.asarray(v,dtype=np.float32);out=v.copy()
 out[...,2]=remap_z(v[...,2]).astype(np.float32)
 return out

STL=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')])
def read_stl(p):
 data=p.read_bytes();n=int.from_bytes(data[80:84],'little')
 return np.frombuffer(data,offset=84,dtype=STL,count=n)['v'].copy()
def write_stl(p,tri):
 tri=np.asarray(tri,dtype=np.float32);rec=np.zeros(len(tri),dtype=STL);rec['v']=tri
 nrm=np.cross(tri[:,1].astype(np.float64)-tri[:,0],tri[:,2].astype(np.float64)-tri[:,0]);l=np.linalg.norm(nrm,axis=1,keepdims=True);l[l==0]=1
 rec['normal']=(nrm/l).astype(np.float32)
 p.write_bytes(bytes(80)+len(tri).to_bytes(4,'little')+rec.tobytes())

if __name__=='__main__':
 root=Path(__file__).resolve().parents[2]
 src=root/(sys.argv[1] if len(sys.argv)>1 else 'final5');out=root/(sys.argv[2] if len(sys.argv)>2 else 'final6')
 assert np.all(np.diff(KNOTS[:,0])>0) and np.all(np.diff(KNOTS[:,1])>0)
 for d in ['stl_montaj','stl_baski']:
  (out/d).mkdir(parents=True,exist_ok=True)
  for p in sorted((src/d).glob('*.stl')):
   if p.stem!=BUILDING:shutil.copy2(p,out/d/p.name)
 tri=read_stl(src/'stl_montaj'/(BUILDING+'.stl'));new=remap_vertices(tri)
 write_stl(out/'stl_montaj'/(BUILDING+'.stl'),new)
 lo=new.reshape(-1,3).min(0).astype(np.float64);hi=new.reshape(-1,3).max(0).astype(np.float64)
 shift=-np.array([(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]])
 write_stl(out/'stl_baski'/(BUILDING+'.stl'),(new.astype(np.float64)+shift).astype(np.float32))
 parts=json.loads((src/'parcalar.json').read_text())
 for r in parts:
  if r['name']==BUILDING:
   r.update(dimensions_mm=(hi-lo).tolist(),assembly_bounds_mm=[lo.tolist(),hi.tolist()],print_translation_mm=shift.tolist(),upper_floor_z_map_mm=KNOTS[1:-1].tolist())
 (out/'parcalar.json').write_text(json.dumps(parts,indent=2))
 print(BUILDING,'height',float(hi[2]-lo[2]),'top',float(hi[2]),'removed',float(tri[...,2].max()-hi[2]))
