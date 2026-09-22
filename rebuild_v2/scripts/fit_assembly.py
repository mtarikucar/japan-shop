"""Seat the existing model parts on measured surfaces and restore the legacy planters."""
from pathlib import Path
import sys,json,numpy as np,trimesh,manifold3d as mf,pymeshfix
from scipy.spatial import cKDTree
root=Path(__file__).resolve().parents[2];out=root/'final5';cache=root/'rebuild_v2/fit_cache'
sys.argv=['contacts',str(root/'final4/stl_montaj')]
from check_contacts import gaps
meshes={p.stem:trimesh.load_mesh(p) for p in (root/'final4/stl_montaj').glob('*.stl')};names={k[:2]:k for k in meshes};original={k:m.copy() for k,m in meshes.items()};trans={k:np.zeros(3) for k in meshes};records=[]
def mesh(i):return meshes[names[i]]
def solid(m):return mf.Manifold(mf.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def box(lo,hi):return mf.Manifold.cube(tuple(np.subtract(hi,lo))).translate(lo)
def weld(m,tol=.0001):
 pairs=cKDTree(m.vertices).query_pairs(tol,output_type='ndarray');parent=np.arange(len(m.vertices))
 for a,b in pairs:
  while parent[a]!=a:a=parent[a]
  while parent[b]!=b:b=parent[b]
  parent[max(a,b)]=min(a,b)
 for i in range(len(parent)):
  while parent[i]!=parent[parent[i]]:parent[i]=parent[parent[i]]
 m.faces=parent[m.faces];m.update_faces(m.nondegenerate_faces());m.update_faces(m.unique_faces());m.remove_unreferenced_vertices();return m
def setsolid(i,s):
 assert s.status()==mf.Error.NoError,(i,s.status())
 a=s.to_mesh();m=trimesh.Trimesh(a.vert_properties[:,:3],a.tri_verts,process=True);m.fix_normals();meshes[names[i]]=m
 print('SOLID',i,len(m.faces),m.is_watertight,flush=True)
def move(i,delta):mesh(i).apply_translation(delta);trans[names[i]]+=delta
# Create a level, full-area foot on the building rather than resting on isolated corners.
level=float(mesh('03').bounds[1,2]);s=solid(mesh('02'));section=s.slice(level+3)
shoe=section.extrude(3.08).translate((0,0,level));setsolid('02',s+shoe)
# The step follows the existing sidewalk underneath while retaining a flat top.
setsolid('03',solid(mesh('03'))-solid(mesh('01')))
# Flatten only the hidden mating surfaces of the two rows of barrels.
for i in range(15,19):
 key=f'{i:02}';m=mesh(key);bottom=m.bounds[0,2]+.35;top=m.bounds[1,2]-1.15;c=m.bounds.mean(0)
 s=solid(m)^box((-200,-200,bottom),(200,200,top))
 seat=mf.Manifold.cylinder(2.5,5.2,5.2,64).translate((c[0],c[1],top-2.5));s=s+seat
 setsolid(key,s);move(key,np.array([0,0,level-bottom]))
 upper=f'{i+4:02}';u=mesh(upper);ub=u.bounds[0,2]+.35
 setsolid(upper,solid(u)^box((-200,-200,ub),(200,200,300)))
 move(upper,np.array([0,0,mesh(key).bounds[1,2]-ub]))
# Clear the left jamb and keep the threshold mat outside the barrel footprint.
for i in range(15,23):move(f'{i:02}',np.array([4.,0,0]))
move('23',np.array([12.,0,0]))
# Bring all lanterns clear of the wooden frame. Their rear seats are modeled below.
for i in range(6,10):move(f'{i:02}',np.array([0,-5.0,0]))
# Fit ceiling plates to the actual slope of the soffit.
for i in range(11,14):setsolid(f'{i:02}',solid(mesh(f'{i:02}'))-solid(mesh('02')))
# Noren ends and rear face must not run through the wooden jambs.
curtain=solid(mesh('05'))^box((-76.53,-100,0),(76.53,100,300));setsolid('05',curtain-solid(mesh('02')))
# The projecting lightbox mounts against the right side, not inside the fascia.
m=mesh('10');move('10',np.array([8.0,0,0]));g=gaps(mesh('10'),mesh('02'),0,.25);move('10',np.array([-g['min_gap_mm'],0,0]));setsolid('10',solid(mesh('10'))-solid(mesh('02')))
# Continuous backing and crossbar with matching seats for sign, lanterns and facade.
back=box((-44.5,10.9,124.4),(44.5,25,153.1))+box((-79,5.5,152),(79,25,154.5))
for i in ['02','04','06','07','08','09','11','12','13']:back=back-solid(mesh(i))
setsolid('26',back)
# Bollard sits on the road just in front of the curb, with its full foot exposed.
move('25',np.array([0,-5.5,0]));g=gaps(mesh('25'),mesh('01'),2,.25);move('25',np.array([0,0,-g['min_gap_mm']]))
# Drape the thin pavement mat to the real pavement height.
m=mesh('24');v=m.vertices.copy();orig=np.column_stack([v[:,:2],np.full(len(v),30.)]);d=np.tile([0,0,-1.],(len(v),1));loc,idx,_=mesh('01').ray.intersects_location(orig,d,multiple_hits=True);h=np.full(len(v),-np.inf);np.maximum.at(h,idx,loc[:,2]);assert np.isfinite(h).all();m.vertices[:,2]+=h-original[names['24']].bounds[0,2]
setsolid('24',solid(m)-solid(mesh('01')))
# Original final3 planters, uniformly scaled; shaped foot adapters meet the pavement.
for key,old,scale,x,y in [('27','04_sol_saksi_bambu',.65,-108.3,10),('28','05_sag_saksi_akcaagac',.48,108.3,7)]:
 p=trimesh.load_mesh(root/'final3'/f'{old}.stl');p.apply_scale(scale);lo,hi=p.bounds;delta=np.array([x-(lo[0]+hi[0])/2,y-(lo[1]+hi[1])/2,20-lo[2]]);p.apply_translation(delta)
 name=key+('_sol_saksi_bambu' if key=='27' else '_sag_saksi_akcaagac');names[key]=name;meshes[name]=p;original[name]=p.copy();trans[name]=np.zeros(3)
 s=solid(p);foot=s.slice(20.4).extrude(6).translate((0,0,14.45));setsolid(key,(s+foot)-solid(mesh('01')))
 records.append({'name':name,'source':f'final3/{old}.stl','uniform_scale':scale,'translation_mm':delta.tolist()})
# Export and map the retained UVs. New hidden contact surfaces use adjacent material.
for name,m in sorted(meshes.items()):
 m.fix_normals();p=out/'stl_montaj'/f'{name}.stl';m.export(p);m=trimesh.load_mesh(p)
 for attempt in range(3):
  if m.is_watertight and m.nondegenerate_faces().all():break
  m=weld(m)
  if not m.is_watertight:
   f=pymeshfix.MeshFix(m.vertices,m.faces);f.repair();m=trimesh.Trimesh(f.points,f.faces,process=True)
  m.fix_normals();m.export(p);m=trimesh.load_mesh(p)
 assert m.is_watertight,(name,'open');assert m.nondegenerate_faces().all(),(name,'degenerate')
 meshes[name]=m
 raw=trimesh.load_mesh(p,process=False);shift=np.array([-raw.bounds[:,0].mean(),-raw.bounds[:,1].mean(),-raw.bounds[0,2]]);raw.apply_translation(shift);raw.export(out/'stl_baski'/f'{name}.stl')
 records.append({'name':name,'dimensions_mm':m.extents.tolist(),'assembly_bounds_mm':m.bounds.tolist(),'print_translation_mm':shift.tolist(),'translation_mm':trans[name].tolist(),'faces':len(m.faces)})
 if name[:2] in ['27','28']:continue
 data=np.load(cache/f'{name}.npz');dst=trimesh.load_mesh(p,process=False);tri=dst.triangles-trans[name];src=data['triangles'];_,ix=cKDTree(src.mean(1)).query(tri.mean(1));w=trimesh.triangles.points_to_barycentric(np.repeat(src[ix],3,axis=0),tri.reshape(-1,3)).reshape(-1,3,3);w=np.clip(w,0,1);w/=np.maximum(w.sum(axis=2,keepdims=True),1e-15);uv=np.einsum('fij,fjk->fik',w,data['uv'][ix]);np.savez_compressed(cache/(name+'_fitted.npz'),triangles=dst.triangles,uv=uv,materials=data['materials'][ix])
 print('EXPORTED',name,len(m.faces),flush=True)
(out/'parcalar.json').write_text(json.dumps([r for r in records if 'faces' in r],indent=2));(root/'rebuild_v2/reports/fit/changes.json').write_text(json.dumps(records,indent=2))
