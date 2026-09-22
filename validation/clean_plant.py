from pathlib import Path
import sys,pymeshlab as ml, trimesh,numpy as np
s=ml.MeshSet();s.load_new_mesh(sys.argv[1]);print('loaded',s.current_mesh().face_number(),flush=True)
s.apply_filter('meshing_remove_connected_component_by_face_number',mincomponentsize=10000)
s.apply_filter('meshing_remove_null_faces');s.apply_filter('meshing_remove_unreferenced_vertices')
s.apply_filter('meshing_decimation_quadric_edge_collapse',targetfacenum=850000,preservetopology=True,preservenormal=True,optimalplacement=False,autoclean=True)
s.apply_filter('compute_selection_by_self_intersections_per_face');print('intersections',s.current_mesh().selected_face_number(),flush=True)
s.save_current_mesh(sys.argv[2])
m=trimesh.load_mesh(sys.argv[2]);print('topology',len(m.faces),m.is_watertight,m.is_winding_consistent,m.volume,flush=True)
