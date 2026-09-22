from pathlib import Path
import numpy as np, trimesh, manifold3d as mf
import argparse
parser=argparse.ArgumentParser(description='Repair structural surfaces from the ae6af10 STL set.')
parser.add_argument('source', type=Path)
parser.add_argument('output', type=Path)
args=parser.parse_args()
SRC=args.source; OUT=args.output; OUT.mkdir(parents=True,exist_ok=True)
def solid(m):
 return mf.Manifold(mf.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def box(lo,hi):
 return mf.Manifold.cube(tuple(np.array(hi)-lo)).translate(lo)
def wedge(x0,x1,yz):
 pts=np.array([[x,y,z] for x in (x0,x1) for y,z in yz]);return solid(trimesh.convex.convex_hull(pts))
def union(items):return mf.Manifold.batch_boolean(items,mf.OpType.Add)
def export(s,name):
 assert s.status()==mf.Error.NoError,(name,s.status())
 t=s.to_mesh();m=trimesh.Trimesh(t.vert_properties[:,:3],t.tri_verts,process=True);m.export(OUT/name);print(name,len(m.faces),m.is_watertight,m.volume,flush=True)
m=trimesh.load_mesh(SRC/'02_bina.stl');old=solid(m)
# Retain original door fittings, lettering and upper windows; rebuild damaged structural surfaces.
core=wedge(-108,88,[(19,18),(61,18),(61,229),(32,240),(19,240)])
front=box((-108,13,18),(88,23,240))
front=front-box((-84,0,202),(-13,24,228))
front=front-box((25,0,202),(69,24,228))
front=front-box((-68,0,18),(66,24,108))
front=front-box((-91,0,109),(87,24,155))
window_parts=[]
for x0,x1 in [(-88,-9),(21,73)]:
 frame=box((x0,9.2,198),(x1,23,233))-box((x0+4,8,202),(x1-4,18.4,229))
 for t in ([1/3,2/3] if x0<0 else [.5]):
  x=x0+(x1-x0)*t
  frame=frame+box((x-.6,16.7,202),(x+.6,20,229))
 window_parts.append(frame)
windows=union(window_parts)
doors=old^box((-8,-5,55),(8,15,85))
panels=union([box((-64,14,18),(-.6,22,104)),box((.6,14,18),(62,22,104)),box((-67,12.8,18),(-64,22,107)),box((62,12.8,18),(65,22,107)),box((-67,12.8,104),(65,22,107)),box((-67,12.8,18),(65,22,20))])
sign=old^box((-91,-5,109),(87,24,155))
# Fill structural wall behind signage without covering its relief.
sign_wall=box((-91,12.9,108),(87,24,151))
canopy=wedge(-107,88,[(-12,155),(20,155),(20,191),(-12,179)])
grooves=[]
for x in np.arange(-93,88,14):
 grooves.append(wedge(x-.22,x+.22,[(-12.5,178.8),(20.5,191.175),(20.5,193),(-12.5,181)]))
canopy=canopy-union(grooves)
pillar=box((88,13,18),(110,46,160))+box((86,11,158),(111.695526,48,166))
building=union([core,front,windows,doors,panels,sign,sign_wall,canopy,pillar])
# Shallow, regular masonry joints on the repaired rear and side walls.
grooves=[]
for row,z in enumerate(np.arange(28,228,10)):
 grooves.append(box((-109,60.65,z-.25),(89,62,z+.25)))
 grooves.append(box((-109,23,z-.25),(-107.65,61,z+.25)))
 grooves.append(box((87.65,48,z-.25),(89,61,z+.25)))
 for x in np.arange(-108+(10 if row%2 else 0),88,25):
  grooves.append(box((x-.25,60.65,z+.25),(x+.25,62,z+9.75)))
 y=41 if row%2 else 31
 grooves.append(box((-109,y-.25,z+.25),(-107.65,y+.25,z+9.75)))
building=building-union(grooves)
bmesh=building.to_mesh()
bmesh=trimesh.Trimesh(bmesh.vert_properties[:,:3],bmesh.tri_verts,process=True)
# Remove the tiny sealed internal cavity left behind the original sign.
bmesh=max(bmesh.split(only_watertight=False),key=lambda m:len(m.faces))
export(solid(bmesh),'02_bina.stl')
# Lightbox: restore planar faces; retain its existing mounting foot.
m=trimesh.load_mesh(SRC/'09_isikli_tabela.stl');old=solid(m)
body=box((68.8,-40.5,159),(96.9,-12.6,188.0))
foot=old^box((65,-43,155),(100,-10,160))
export(body+foot,'09_isikli_tabela.stl')
# Bollard: replace collapsed face with a smooth arch, preserving footprint and through-hole.
m=trimesh.load_mesh(SRC/'11_baba_sari.stl');lo,hi=m.bounds;cx=(lo[0]+hi[0])/2
points=[[lo[0],lo[1],lo[2]],[hi[0],lo[1],lo[2]]]
rx=(hi[0]-lo[0])/2;rz=hi[2]-lo[2]
outline=[(cx+rx*np.cos(a),lo[2]+rz*np.sin(a)) for a in np.linspace(0,np.pi,129)]
verts=np.array([[x,y,z] for y in (lo[1],hi[1]) for x,z in outline]);arch=solid(trimesh.convex.convex_hull(verts))
hole=mf.Manifold.cylinder(hi[1]-lo[1]+4,3.35,3.35,64).rotate((90,0,0)).translate((cx,hi[1]+2,lo[2]+12.0))
# Two shallow horizontal reflector recesses, cleanly cut into the face.
cut=[hole,box((cx-16,lo[1]-1,lo[2]+10),(cx-7,lo[1]+.5,lo[2]+10.7)),box((cx+7,lo[1]-1,lo[2]+10),(cx+16,lo[1]+.5,lo[2]+10.7))]
export(arch-union(cut),'11_baba_sari.stl')
# Menu board: planar inset and square border at the original tilt; keep the stem.
m=trimesh.load_mesh(SRC/'10_menu_standi.stl');old=solid(m)
center=np.array([58.725,-11.2,66.9]);angle=np.degrees(np.arctan2(.58,.814))
def panel_box(lo,hi):return box(lo,hi).rotate((angle,0,0)).translate(center)
panel=panel_box((-12,-10,-1.2),(12,10,.8))-panel_box((-10.8,-8.8,.25),(10.8,8.8,2))
# Keep a shallow 3-by-2 layout on the menu face.
for x in [-3.6,3.6]:panel=panel-panel_box((x-.08,-8.6,.12),(x+.08,8.6,.4))
panel=panel-panel_box((-10.6,-.08,.12),(10.6,.08,.4))
stem=old^box((40,-30,17),(80,10,58))
pole=m.vertices[(m.vertices[:,2]>35)&(m.vertices[:,2]<45),:2].mean(axis=0)
bridge=mf.Manifold.cylinder(10,1.5,1.5,48).translate((pole[0],pole[1],58))
bridge=bridge^panel_box((-50,-50,-100),(50,50,0))
export(union([panel,stem,bridge]),'10_menu_standi.stl')
# Restore the two creased lanterns using their median radial profile.
from scipy.ndimage import gaussian_filter1d
for name,top in [('06_fener_sol_1.stl',143.6),('07_fener_sol_2.stl',141.8)]:
 m=trimesh.load_mesh(SRC/name);lo,hi=m.bounds;c=(lo[:2]+hi[:2])/2;v=m.vertices
 zs=np.linspace(lo[2]+.05,top,300);rad=np.linalg.norm(v[:,:2]-c,axis=1)
 rs=[]
 for z in zs:
  mask=np.abs(v[:,2]-z)<.15
  if mask.sum()<5:mask=np.abs(v[:,2]-z)<.35
  rs.append(np.median(rad[mask]))
 rs=gaussian_filter1d(rs,.65)
 profile=np.vstack(([0,lo[2]],np.column_stack((rs,zs)),[0,top]))
 revolved=trimesh.creation.revolve(profile,sections=128);revolved.apply_translation([*c,0]);revolved.fix_normals()
 hook=solid(m)^box((lo[0]-1,lo[1]-1,top-.25),(hi[0]+1,hi[1]+1,hi[2]+1))
 export(solid(revolved)+hook,name)
