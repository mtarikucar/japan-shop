"""Build the editable scene and preview renders from the checked STL files."""
from pathlib import Path
import bpy
from mathutils import Vector

root=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.render.resolution_x=1300;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True
bg=next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs[0].default_value=(.10,.12,.15,1);bg.inputs[1].default_value=.5
colors={'01':(.3,.33,.36,1),'02':(.48,.52,.55,1),'03':(.64,.54,.39,1),'04':(.27,.42,.26,1),'05':(.42,.47,.25,1),'06':(.68,.32,.23,1),'07':(.68,.32,.23,1),'08':(.68,.32,.23,1),'09':(.75,.65,.39,1),'10':(.35,.27,.2,1),'11':(.82,.58,.13,1)}
objects=[]
for path in sorted((root/'final3').glob('*.stl')):
    bpy.ops.wm.stl_import(filepath=str(path))
    obj=bpy.context.object;obj.name=path.stem
    mat=bpy.data.materials.new(path.stem);mat.diffuse_color=colors[path.name[:2]];mat.use_nodes=True
    shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');shader.inputs['Base Color'].default_value=mat.diffuse_color;shader.inputs['Roughness'].default_value=.8
    obj.data.materials.append(mat);obj.color=mat.diffuse_color;objects.append(obj)
for loc,power,size in [((-250,-350,500),2600000,260),((300,-100,300),1300000,200),((50,350,400),1700000,220)]:
    bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((0,0,100))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;scene.camera=camera;camera.data.type='ORTHO';camera.data.clip_end=10000

def render(name,direction,targets):
    for obj in objects:obj.hide_render=obj not in targets
    corners=[o.matrix_world@Vector(c) for o in targets for c in o.bound_box]
    lo=Vector(tuple(min(v[i] for v in corners) for i in range(3)));hi=Vector(tuple(max(v[i] for v in corners) for i in range(3)));center=(lo+hi)/2
    size=max(hi-lo);camera.location=center+Vector(direction).normalized()*size*3
    camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=size*1.5
    scene.render.filepath=str(root/'final3'/name);bpy.ops.render.render(write_still=True)
render('onarilmis_on.png',(-.65,-1,.55),objects)
render('onarilmis_arka.png',(.65,1,.55),objects)
render('onarilmis_bina.png',(-.65,-1,.6),[o for o in objects if o.name=='02_bina'])
render('onarilmis_tabla.png',(-.65,-1,.8),[o for o in objects if o.name=='01_tabla'])
for obj in objects:obj.hide_render=False
center=Vector((0,0,120));camera.location=(-360,-500,350);camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=410
bpy.ops.object.select_all(action='DESELECT')
for obj in objects:obj.select_set(True)
bpy.context.view_layer.objects.active=next(o for o in objects if o.name=='02_bina')
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active;space.clip_end=10000;space.shading.color_type='MATERIAL';space.shading.show_cavity=True
            space.region_3d.view_distance=400;space.region_3d.view_location=center;space.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
bpy.ops.wm.save_as_mainfile(filepath=str(root/'final3/japan_shop_repaired.blend'),compress=True)
print('Saved scene with',len(objects),'STL mesh objects')
