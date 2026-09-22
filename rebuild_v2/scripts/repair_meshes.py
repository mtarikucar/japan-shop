"""Repair isolated microscopic defects while retaining the generated surfaces."""
from pathlib import Path
import trimesh,numpy as np,pymeshlab as ml,json,sys
root=Path(__file__).resolve().parents[1];out=root/'clean';out.mkdir(exist_ok=True)
records=[]
for p in sorted((root/'raw').glob('*/model.stl')):
 name=p.parent.name
 if len(sys.argv)>1 and name not in sys.argv[1:]:continue
 m=trimesh.load_mesh(p);nf=len(m.faces)
 m=max(m.split(only_watertight=False),key=lambda c:len(c.faces));m.fix_normals();m.fill_holes()
 if not m.is_watertight:
  import pymeshfix
  repair=pymeshfix.MeshFix(m.vertices,m.faces);repair.repair(joincomp=False,remove_smallest_components=True);m=trimesh.Trimesh(repair.points,repair.faces,process=True)
 m.fix_normals();m.export(out/f'{name}.stl')
 ms=ml.MeshSet();ms.load_new_mesh(str(out/f'{name}.stl'));ms.apply_filter('compute_selection_by_self_intersections_per_face')
 if ms.current_mesh().selected_face_number():
  import pymeshfix
  repair=pymeshfix.MeshFix(m.vertices,m.faces);repair.repair(joincomp=False,remove_smallest_components=True);m=trimesh.Trimesh(repair.points,repair.faces,process=True);m.fix_normals();m.export(out/f'{name}.stl')
  ms=ml.MeshSet();ms.load_new_mesh(str(out/f'{name}.stl'));ms.apply_filter('compute_selection_by_self_intersections_per_face')
 r={'asset':name,'source_faces':nf,'faces':len(m.faces),'watertight':m.is_watertight,'winding':m.is_winding_consistent,'intersection_faces':ms.current_mesh().selected_face_number(),'bounds':m.bounds.tolist(),'volume':float(m.volume)};assert r['watertight'] and r['winding'] and r['intersection_faces']==0,r
 records.append(r);print(json.dumps(r),flush=True)
(root/'reports'/('clean_meshes'+('_extra' if len(sys.argv)>1 else '')+'.json')).write_text(json.dumps(records,indent=2))
