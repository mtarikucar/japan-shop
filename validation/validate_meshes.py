"""Validate exported STL solids. Run: python validation/validate_meshes.py"""
from pathlib import Path
import json
import numpy as np
import trimesh

root = Path(__file__).resolve().parents[1]
results = {}
for path in sorted((root / 'final3').glob('*.stl')):
    mesh = trimesh.load_mesh(path)
    counts = np.bincount(mesh.edges_unique_inverse)
    components = len(trimesh.graph.connected_components(mesh.face_adjacency, nodes=np.arange(len(mesh.faces))))
    result = {
        'triangles': len(mesh.faces),
        'watertight': bool(mesh.is_watertight),
        'consistent_winding': bool(mesh.is_winding_consistent),
        'positive_volume': bool(mesh.is_volume),
        'boundary_edges': int(np.count_nonzero(counts == 1)),
        'nonmanifold_edges': int(np.count_nonzero(counts > 2)),
        'degenerate_triangles': int(np.count_nonzero(mesh.area_faces < 1e-12)),
        'components': components,
        'bounds_mm': mesh.bounds.tolist(),
        'dimensions_mm': mesh.extents.tolist(),
        'volume_mm3': float(mesh.volume),
    }
    results[path.name] = result
    assert result['watertight'] and result['consistent_winding'] and result['positive_volume'], (path.name, result)
    assert components == 1 and result['degenerate_triangles'] == 0, (path.name, result)
    print(path.name, 'PASS', len(mesh.faces), flush=True)
assert len(results) == 12
(root / 'validation' / 'after.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print('12/12 STL files passed. Physical printing and minimum wall thickness are not tested.')
