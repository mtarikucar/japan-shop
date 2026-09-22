"""Split the base and the building in two so each half can be printed tilted on a resin printer.

Target printer: ELEGOO Saturn 4 Ultra, 218.88 x 122.88 x 220 mm. Unsplit, the base does not
fit the plate at all and the building can only lean ~19 degrees; each half fits at 45 degrees.

Cuts follow lines that already exist on the model:
  building  x=-1.3 below the saçak (door leaves meet, between the handles),
            x=-3.3 across the saçak (a board joint), x=-2.0 on the window floor (inner edge
            of the window stile); the jogs sit at the saçak bottom and top edges.
  base      x=-0.1, a curb-stone joint.
The right halves get pegs, the left halves matching holes, for glue alignment.

  python rebuild_v2/scripts/split_for_tilt.py            # final6 -> final7
"""
from pathlib import Path
import json,shutil,sys
import numpy as np

PEG_R,PEG_LEN,CHAMFER=2.0,5.0,0.5          # mm; peg on the right half
HOLE_R,HOLE_DEPTH=2.2,5.5                  # 0.2 mm radial and 0.5 mm depth clearance
SEG=48
BIG=1000.0
# (name, source, left-region boxes [x_max, z_min, z_max], pins [(x_cut, y, z)], new names)
SPLITS=[
 ('01_tabla',[(-0.1,-BIG,BIG)],[(-0.1,-47.0,5.5),(-0.1,10.0,7.5),(-0.1,55.0,7.5)],('01a_tabla_sol','01b_tabla_sag')),
 ('02_bina',[(-1.3,-BIG,166.0),(-3.3,166.0,198.9),(-2.0,198.9,BIG)],
  [(-1.3,40.0,40.0),(-1.3,40.0,95.0),(-1.3,40.0,150.0),(-3.3,35.0,182.0),(-2.0,35.0,205.0)],('02a_bina_sol','02b_bina_sag')),
]

def to_manifold(m):
 s=mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices,dtype=np.float32),tri_verts=np.asarray(m.faces,dtype=np.uint32)))
 assert s.status()==mf.Error.NoError,s.status();return s
def to_trimesh(s):
 g=s.to_mesh();return trimesh.Trimesh(np.asarray(g.vert_properties)[:,:3],np.asarray(g.tri_verts),process=True)
def box(x0,x1,z0,z1):
 return mf.Manifold.cube([x1-x0,2*BIG,z1-z0]).translate([x0,-BIG,z0])
def along_x(s,x,y,z):
 """Cylinder built along +Z from 0 -> axis along -X starting at x."""
 return s.rotate([0,-90,0]).translate([x,y,z])
def peg(x,y,z):
 body=mf.Manifold.cylinder(PEG_LEN-CHAMFER+.5,PEG_R,PEG_R,SEG)
 tip=mf.Manifold.cylinder(CHAMFER,PEG_R,PEG_R-CHAMFER,SEG).translate([0,0,PEG_LEN-CHAMFER+.5])
 return along_x(body+tip,x+.5,y,z)       # starts 0.5 mm inside the right half
def hole(x,y,z):
 return along_x(mf.Manifold.cylinder(HOLE_DEPTH+.5,HOLE_R,HOLE_R,SEG),x+.5,y,z)

def check_pins_inside(m,pins,margin=1.0):
 """Hole plus margin must lie inside the original solid on both sides of the cut."""
 a=np.linspace(0,2*np.pi,24,endpoint=False)
 for x,y,z in pins:
  for r in [0,HOLE_R+margin]:
   for dx in np.linspace(-HOLE_DEPTH-margin,margin+.5,8):
    pts=np.column_stack([np.full(len(a),x+dx),y+r*np.cos(a),z+r*np.sin(a)])
    assert m.contains(pts).all(),('pin not inside solid',x,y,z)

def write_stl(p,m):
 tri=np.asarray(m.triangles,dtype=np.float32);rec=np.zeros(len(tri),dtype=[('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')])
 rec['v']=tri;rec['normal']=np.asarray(m.face_normals,dtype=np.float32)
 p.write_bytes(bytes(80)+len(tri).to_bytes(4,'little')+rec.tobytes())

if __name__=='__main__':
 import trimesh,manifold3d as mf   # not needed when Blender imports SPLITS
 root=Path(__file__).resolve().parents[2]
 src=root/(sys.argv[1] if len(sys.argv)>1 else 'final6');out=root/(sys.argv[2] if len(sys.argv)>2 else 'final7')
 for d in ['stl_montaj','stl_baski']:
  (out/d).mkdir(parents=True,exist_ok=True)
  for p in (out/d).glob('*.stl'):p.unlink()
  for p in sorted((src/d).glob('*.stl')):
   if p.stem not in [s[0] for s in SPLITS]:shutil.copy2(p,out/d/p.name)
 parts=json.loads((src/'parcalar.json').read_text());records=[]
 for name,boxes,pins,(lname,rname) in SPLITS:
  m=trimesh.load_mesh(src/'stl_montaj'/(name+'.stl'));check_pins_inside(m,pins);s=to_manifold(m)
  left_region=mf.Manifold.batch_boolean([box(-BIG,x,z0,z1) for x,z0,z1 in boxes],mf.OpType.Add)
  left=s^left_region;right=s-left_region
  left=left-mf.Manifold.batch_boolean([hole(*p) for p in pins],mf.OpType.Add)
  right=right+mf.Manifold.batch_boolean([peg(*p) for p in pins],mf.OpType.Add)
  base=next(r for r in parts if r['name']==name)
  for new,solid,side in [(lname,left,'sol'),(rname,right,'sag')]:
   t=to_trimesh(solid);assert t.is_watertight and t.is_winding_consistent and t.volume>0,new
   assert len(t.split(only_watertight=False))==1,(new,'components')
   write_stl(out/'stl_montaj'/(new+'.stl'),t)
   lo,hi=t.bounds;shift=-np.array([(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]])
   q=t.copy();q.apply_translation(shift);write_stl(out/'stl_baski'/(new+'.stl'),q)
   records.append({'name':new,'dimensions_mm':(hi-lo).tolist(),'assembly_bounds_mm':[lo.tolist(),hi.tolist()],'print_translation_mm':shift.tolist(),
    'translation_mm':base['translation_mm'],'faces':len(t.faces),'split_from':name,'side':side,
    'cut_x_mm':[[x,z0,z1] for x,z0,z1 in boxes],'alignment':('holes' if side=='sol' else 'pegs'),
    'pins_mm':[{'x':x,'y':y,'z':z} for x,y,z in pins],'peg_diameter_mm':2*PEG_R,'peg_length_mm':PEG_LEN,'hole_diameter_mm':2*HOLE_R,'hole_depth_mm':HOLE_DEPTH})
   print(new,'faces',len(t.faces),'volume_ml',round(t.volume/1000,1),'size',np.round(hi-lo,2),flush=True)
 merged=[]
 for r in parts:
  if r['name'] in [s[0] for s in SPLITS]:merged+=[x for x in records if x['split_from']==r['name']]
  else:merged.append(r)
 (out/'parcalar.json').write_text(json.dumps(merged,indent=2))
