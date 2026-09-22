"""Map texture corners from the source triangles to the locally repaired surface."""
from pathlib import Path
import trimesh,numpy as np
from scipy.spatial import cKDTree
root=Path(__file__).resolve().parents[1]
for p in sorted((root/'clean').glob('*.stl')):
 if not (root/'raw'/p.stem/'model.glb').exists():continue
 target=p.with_suffix('.npz')
 if target.exists() and target.stat().st_mtime>p.stat().st_mtime:continue
 src=trimesh.load(root/'raw'/p.stem/'model.glb').to_geometry()
 # glTF is Y-up; generated STL and Blender scene are Z-up.
 src.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]));src.apply_scale(1000)
 dst=trimesh.load_mesh(p,process=False)
 _,indices=cKDTree(src.triangles_center).query(dst.triangles_center)
 tris=src.triangles[indices];uv=src.visual.uv[src.faces[indices]]
 weights=trimesh.triangles.points_to_barycentric(np.repeat(tris,3,axis=0),dst.triangles.reshape(-1,3)).reshape(-1,3,3)
 weights=np.clip(weights,0,1);weights/=weights.sum(axis=2,keepdims=True)
 result=np.einsum('fij,fjk->fik',weights,uv)
 np.savez_compressed(target,triangles=dst.triangles,uv=result)
 print(p.stem,'UV saved',flush=True)
