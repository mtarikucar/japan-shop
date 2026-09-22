"""Local architectural details: planar window openings and engraved wood joints."""
from pathlib import Path
import trimesh,numpy as np,manifold3d as mf,shutil
root=Path(__file__).resolve().parents[1];p=root/'clean/building.stl';backup=root/'clean/building_original.stl'
if not backup.exists():shutil.copyfile(p,backup)
m=trimesh.load_mesh(backup);lo=m.bounds[0];scale=np.array([210,70,250])/m.extents
m.vertices=(m.vertices-lo)*scale+[-105,0,26]
s=mf.Manifold(mf.Mesh(np.array(m.vertices,dtype=np.float32),np.array(m.faces,dtype=np.uint32)))
def box(lo,hi):return mf.Manifold.cube(tuple(np.subtract(hi,lo))).translate(lo)
cut=[]
for x0,x1 in [(-75.5,-46.5),(-39.3,-2.5),(36.4,66.1),(73.7,88.2)]:cut.append(box((x0,8,252.5),(x1,10.88,271.8)))
for x in np.arange(-99,103,6.8):cut.append(box((x-.14,-.5,191),(x+.14,1.7,219)))
s=s-mf.Manifold.batch_boolean(cut,mf.OpType.Add)
assert s.status()==mf.Error.NoError
r=s.to_mesh();m=trimesh.Trimesh(r.vert_properties[:,:3],r.tri_verts,process=True);m.vertices=(m.vertices-[-105,0,26])/scale+lo;m.fix_normals();m.export(p)
print('Refined building',len(m.faces),m.is_watertight)
