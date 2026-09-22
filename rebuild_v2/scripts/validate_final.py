"""Validate the actual deliverable STL bytes, not intermediate meshes."""
from pathlib import Path
import trimesh,numpy as np,pymeshlab as ml,json,hashlib,sys
root=Path(__file__).resolve().parents[1];out=root.parent/(sys.argv[1] if len(sys.argv)>1 else 'final4');records=[]
for p in sorted((out/'stl_montaj').glob('*.stl')):
 m=trimesh.load_mesh(p);_,counts=np.unique(m.edges_sorted,axis=0,return_counts=True)
 ms=ml.MeshSet();ms.load_new_mesh(str(p));ms.apply_filter('compute_selection_by_self_intersections_per_face')
 parts=m.split(only_watertight=False)
 r={'name':p.name,'triangles':len(m.faces),'watertight':m.is_watertight,'consistent_winding':m.is_winding_consistent,'positive_volume':bool(m.volume>0),'components':len(parts),'open_edges':int((counts==1).sum()),'nonmanifold_edges':int((counts>2).sum()),'degenerate_faces':int((~m.nondegenerate_faces()).sum()),'duplicate_faces':int((~m.unique_faces()).sum()),'self_intersection_faces':ms.current_mesh().selected_face_number(),'dimensions_mm':m.extents.tolist(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 print(r['name'],'closed',r['watertight'],'intersections',r['self_intersection_faces'],flush=True)
 records.append(r)
 assert r['watertight'] and r['consistent_winding'] and r['positive_volume'] and r['components']==1,r
 assert not any(r[k] for k in ['open_edges','nonmanifold_edges','degenerate_faces','duplicate_faces','self_intersection_faces']),r
 # Print STL must differ only by translation. Compare centered triangle vertices.
 q=out/'stl_baski'/p.name;n=trimesh.load_mesh(q,process=False);a=trimesh.load_mesh(p,process=False)
 a.vertices-=np.array([a.bounds[:,0].mean(),a.bounds[:,1].mean(),a.bounds[0,2]])
 assert np.allclose(a.triangles,n.triangles,atol=5e-5),q
 assert abs(n.bounds[0,2])<5e-5,q
 assert n.is_winding_consistent,q
expected={'final5':28,'final6':28,'final7':30}.get(out.name,26)
assert len(records)==expected,len(records)
(out/'kontrol_raporu.json').write_text(json.dumps(records,indent=2))
print('PASS:',expected,'assembly STL files and translated print copies')
