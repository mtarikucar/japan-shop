import bpy, numpy as np, hashlib, json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
def signature(tri):
    tri=np.asarray(tri,dtype='<f4').copy()
    tri[tri==0]=0
    vertices=tri.reshape(-1,3).view('V12').reshape(-1,3)
    vertices.sort(axis=1)
    faces=vertices.reshape(-1).view('V36').copy();faces.sort()
    return hashlib.sha256(faces.tobytes()).hexdigest()
results={}
for path in sorted((Path(bpy.data.filepath).parent/'stl_montaj').glob('*.stl')):
    obj=bpy.data.objects[path.stem];mesh=obj.data;mesh.calc_loop_triangles()
    v=np.empty(len(mesh.vertices)*3,dtype=np.float32);mesh.vertices.foreach_get('co',v);v=v.reshape(-1,3)
    f=np.empty(len(mesh.loop_triangles)*3,dtype=np.int32);mesh.loop_triangles.foreach_get('vertices',f);f=f.reshape(-1,3)
    assert obj.matrix_world.is_identity
    data=path.read_bytes();n=int.from_bytes(data[80:84],'little');dtype=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')]);tri=np.frombuffer(data,offset=84,dtype=dtype,count=n)['v']
    assert signature(v[f])==signature(tri),path.name
    results[path.name]={'matches_stl':True,'triangles':n,'sha256':hashlib.sha256(data).hexdigest()}
    print(path.name,'scene matches STL')
assert len([o for o in bpy.context.scene.objects if o.type=='MESH'])=={'final5':28,'final6':28,'final7':30}.get(Path(bpy.data.filepath).parent.name,26)
(Path(bpy.data.filepath).parent/'sahne_kontrolu.json').write_text(json.dumps(results,indent=2))
