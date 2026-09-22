"""Transfer original UVs onto repaired surfaces and build the printable assembly."""
from pathlib import Path
import bpy,json,math,numpy as np
from mathutils import Vector,Matrix
root=Path(__file__).resolve().parents[1];out=root.parent/'final4';out.mkdir(exist_ok=True)
for d in ['stl_montaj','stl_baski']: (out/d).mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001
objects=[];manifest=[]
def activate(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o

def mat(name,color,rough=.65):
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;return m
cream=mat('Ivory',(.82,.75,.57,1));ink=mat('Black ink',(.017,.013,.01,1));wood=mat('Wood trims',(.29,.115,.025,1));red=mat('Vermilion',(.64,.025,.012,1));gold=mat('Noodles',(.87,.47,.02,1));paper=mat('Menu paper',(.83,.79,.68,1))

def fit(o,dims,lo):
 bpy.context.view_layer.update();corners=[o.matrix_world@Vector(c) for c in o.bound_box];oldlo=Vector([min(c[i] for c in corners) for i in range(3)]);oldhi=Vector([max(c[i] for c in corners) for i in range(3)]);scale=Vector([dims[i]/(oldhi[i]-oldlo[i]) for i in range(3)])
 for v in o.data.vertices:v.co=(v.co-oldlo)*scale+Vector(lo)
 o.data.update()

def repaired(asset,name,dims,lo):
 bpy.ops.import_scene.gltf(filepath=str(root/'raw'/asset/'model.glb'));imported=list(bpy.context.selected_objects);src=next(o for o in imported if o.type=='MESH');activate(src);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 bpy.ops.wm.stl_import(filepath=str(root/'clean'/f'{asset}.stl'));dst=bpy.context.object;dst.name=name
 for v in dst.data.vertices:v.co*=.001
 dst.data.update();dst.data.materials.clear()
 for m in src.data.materials:dst.data.materials.append(m)
 data=np.load(root/'clean'/f'{asset}.npz');layer=dst.data.uv_layers.new(name='UVMap')
 vertices=np.empty(len(dst.data.vertices)*3,dtype=np.float32);dst.data.vertices.foreach_get('co',vertices);vertices=vertices.reshape(-1,3)
 loops=np.empty(len(dst.data.loops),dtype=np.int32);dst.data.loops.foreach_get('vertex_index',loops)
 actual=vertices[loops].reshape(-1,3,3)*1000
 assert np.allclose(actual,data['triangles'],atol=.002),asset+' triangle order changed'
 layer.data.foreach_set('uv',data['uv'].astype(np.float32).reshape(-1))
 for o in imported:bpy.data.objects.remove(o,do_unlink=True)
 fit(dst,dims,lo);objects.append(dst);print('ASSEMBLED',name,flush=True);return dst

repaired('base','01_tabla',(280,150,22),(-140,-65,0))
building=repaired('building','02_bina',(210,70,250),(-105,0,26))
glass=mat('Window blinds',(.2,.25,.28,1),.38)
wave=glass.node_tree.nodes.new('ShaderNodeTexWave');wave.wave_type='BANDS';wave.bands_direction='X';wave.inputs['Scale'].default_value=50
ramp=glass.node_tree.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.12,.16,.19,1);ramp.color_ramp.elements[1].color=(.26,.30,.32,1)
glass.node_tree.links.new(wave.outputs['Fac'],ramp.inputs[0]);glass.node_tree.links.new(ramp.outputs['Color'],glass.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
building.data.materials.append(glass)
for p in building.data.polygons:
 x,y,z=p.center
 if abs(y-10.88)<.06 and 252.45<z<271.85 and any(a-.02<x<b+.02 for a,b in [(-75.5,-46.5),(-39.3,-2.5),(36.4,66.1),(73.7,88.2)]):p.material_index=len(building.data.materials)-1
repaired('sign','04_yagami_tabela',(106,5,34),(-53,8,141))
for i,x in enumerate([-84,-61,61,84],1):repaired(f'lantern{i}',f'{5+i:02d}_fener_{i}',(18,18,44),(x-9,1,134))
templates={}
barrel_layout=[['barrel_red','barrel_blue','barrel_blue','barrel_red'],['barrel_blue','barrel_red','barrel_sun','barrel_blue']]
for row in range(2):
 for col in range(4):
  asset=barrel_layout[row][col];name=f'{15+row*4+col:02d}_fici_'+('alt' if row==0 else 'ust')+f'_{col+1}'
  lo=(-85+col*17.5,4,26+row*18.7)
  if asset not in templates:
   o=repaired(asset,name,(17,16.5,19),lo);templates[asset]=(o,Vector(lo))
  else:
   source,oldlo=templates[asset];o=source.copy();o.data=source.data.copy();bpy.context.collection.objects.link(o);o.name=name;o.data.transform(Matrix.Translation(Vector(lo)-oldlo));objects.append(o)
for r in json.loads((root/'reports'/'accessory_materials.json').read_text()):
 bpy.ops.wm.stl_import(filepath=str(root/'accessories'/(r['name']+'.stl')));o=bpy.context.object;o.name=r['name'];o.data.materials.append(mat(o.name,r['color']));objects.append(o)
 if 'perde' in o.name:
  o.data.materials.append(cream)
  for p in o.data.polygons:
   if p.center.y<18.45:p.material_index=1
 if 'kup' in o.name:
  for m in [ink,wood,red,gold]:o.data.materials.append(m)
  for p in o.data.polygons:
   x,y,z=p.center
   if z<192.55 or z>227.45:p.material_index=2
   elif y < -17.1 or (x<96.95 and z<209):p.material_index=1
   if y < -17.1 and z>210 and z<217:p.material_index=3 if z<216 else 4
 if 'menu' in o.name:
  for m in [paper,red,ink]:o.data.materials.append(m)
  rot=Matrix.Rotation(math.radians(-35),4,'X')
  for p in o.data.polygons:
   a=rot@(p.center-Vector((78,1,85)))
   if abs(a.x)<11.7 and abs(a.y)<8.7 and a.z>.7:p.material_index=1
   if a.z>1.25 and abs(a.x)<10 and abs(a.y)<7:p.material_index=2
# Overall height remains 240 mm; the base fits a 256 mm print bed.
for o in objects:o.data.transform(Matrix.Scale(240/276,4))
# STL exports preserve assembly coordinates; print copies only translate XY and Z.
for o in sorted(objects,key=lambda o:o.name):
 activate(o);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 bpy.ops.wm.stl_export(filepath=str(out/'stl_montaj'/(o.name+'.stl')),export_selected_objects=True,apply_modifiers=True)
 corners=[Vector(c) for c in o.bound_box];lo=Vector([min(c[i] for c in corners) for i in range(3)]);hi=Vector([max(c[i] for c in corners) for i in range(3)]);offset=Vector((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,-lo.z))
 manifest.append({'name':o.name,'dimensions_mm':list(hi-lo),'assembly_bounds_mm':[list(lo),list(hi)],'print_translation_mm':list(offset),'faces':len(o.data.polygons)})
 o.location=offset;bpy.ops.wm.stl_export(filepath=str(out/'stl_baski'/(o.name+'.stl')),export_selected_objects=True,apply_modifiers=True);o.location=(0,0,0)
(out/'parcalar.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# Texture compression only; retained geometry is identical to the STL assembly.
for im in bpy.data.images:
 if im.source!='FILE':continue
 _=tuple(im.size)
 if im.packed_file:im.unpack(method='REMOVE')
 size=1024 if im.name.startswith('normal') else (512 if im.name.startswith('Image_1') else 2048)
 if im.size[0]>size:im.scale(size,size)
 fmt='JPEG' if im.name.startswith('Image_0') else 'PNG';ext='jpg' if fmt=='JPEG' else 'png'
 im.file_format=fmt;im.filepath_raw=str(root/'clean'/(im.name+'.'+ext));im.save();im.pack()
 im.filepath='//textures/'+im.name+'.'+ext
bpy.data.orphans_purge(do_recursive=True)
s.render.engine='CYCLES';s.cycles.samples=32;s.render.resolution_x=1400;s.render.resolution_y=1400;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.16,.17,.19,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.65
for loc,power,size in [((-280,-360,500),3000000,300),((300,-160,360),2000000,220),((10,300,450),2600000,230)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=size;o.rotation_euler=(Vector((0,20,130))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';cam.data.clip_end=10000;s.camera=cam

def camera(d,scale=320,center=(0,7,121)):
 cen=Vector(center);cam.location=cen+Vector(d)*450;cam.rotation_euler=(cen-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
camera((-.48,-1,.36))
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.clip_end=10000;area.spaces.active.region_3d.view_distance=400;area.spaces.active.region_3d.view_location=(0,0,140);area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion();area.spaces.active.shading.color_type='MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'japan_shop_final.blend'),compress=True)
for name,d in [('izometrik',(-.48,-1,.36)),('on',(0,-1,.05)),('arka',(.6,1,.45))]:
 camera(d);s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
clay=mat('Mesh inspection',(.22,.26,.3,1));s.view_layers[0].material_override=clay;camera((-.48,-1,.36));s.render.filepath=str(out/'mesh_kontrol.png');bpy.ops.render.render(write_still=True)
print('COMPLETE',len(objects),'parts',flush=True)
