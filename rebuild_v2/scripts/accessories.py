"""Closed solids for the small architectural accessories, in millimetres."""
from pathlib import Path
import numpy as np,trimesh,manifold3d as mf,json
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
root=Path(__file__).resolve().parents[1];out=root/'accessories';out.mkdir(exist_ok=True)
records=[]
def box(lo,hi):return mf.Manifold.cube(tuple(np.subtract(hi,lo))).translate(lo)
def cylinder(h,r,loc):return mf.Manifold.cylinder(h,r,r,48).translate(loc)
def union(items):return mf.Manifold.batch_boolean(items,mf.OpType.Add)
def textsolid(text,width,height,depth,loc,font='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'):
 paths=TextPath((0,0),text,size=10,prop=FontProperties(fname=font)).to_polygons()
 allv=np.concatenate(paths);lo=allv.min(0);span=np.ptp(allv,axis=0)
 paths=[(p-lo)*[width/span[0],height/span[1]] for p in paths]
 return mf.CrossSection(paths,mf.FillRule.EvenOdd).extrude(depth).rotate((90,0,0)).translate(loc)
def save(s,name,color):
 assert s.status()==mf.Error.NoError,(name,s.status())
 a=s.to_mesh();m=trimesh.Trimesh(a.vert_properties[:,:3],a.tri_verts,process=True);m.fix_normals();assert m.is_watertight,name
 m.export(out/f'{name}.stl');records.append({'name':name,'color':color});print(name,len(m.faces),flush=True)
# Raised stone footing: continuous level seating surface, projecting beyond pillars.
save(box((-108,-7,18),(108,74,26)),'03_esik',[.075,.08,.085,1])
# Noren panel and attached wave relief. Each wave overlaps the backing panel.
wave=[box((-88,18.5,124),(88,23.6,140))]
for cx in range(-94,96,22):
 for radius in [3,5.8,8.6,11.4]:
  ring=mf.CrossSection.circle(radius,64)-mf.CrossSection.circle(max(.2,radius-.65),64)
  arc=ring.extrude(.7).rotate((90,0,0)).translate((cx,18.8,125))
  wave.append(arc ^ box((-88,17,124),(88,20,140)))
# Stylized curling wave crests repeated along the strip.
for cx in range(-78,89,33):
 for j in range(3):
  r=2.3-j*.4;wave.append(cylinder(.7,r,(0,0,0)).rotate((90,0,0)).translate((cx+j*2.8,18.8,137-j*1.4)))
save(union(wave),'05_dalga_perde',[.06,.055,.04,1])
# Solid lightbox with raised labels; printable faces remain planar and closed.
parts=[box((97,-17,192),(132,16,228)),box((96,-18,191),(133,17,192.5)),box((96,-18,227.5),(133,17,229))]
parts.append(textsolid('Ramen',29,6,.55,(100,-16.9,202)))
parts.append(textsolid('ヤガミ',18,3.6,.55,(106,-16.9,195),'/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'))
# Bowl silhouette and noodle rings on the front face.
bowl=mf.CrossSection([[(102,216),(105,211),(125,211),(128,216)]]).extrude(.55).rotate((90,0,0)).translate((0,-16.9,0));parts.append(bowl)
for x in [109,115,121]:
 ring=mf.CrossSection.circle(2.1,40)-mf.CrossSection.circle(1.25,40)
 parts.append(ring.extrude(.6).rotate((90,0,0)).translate((x,-16.9,216)))
# Side lettering faces left, visible from the reference camera.
side=textsolid('Sushi',25,6,.55,(0,0,0)).rotate((0,0,-90)).translate((97.1,12,202));parts.append(side)
save(union(parts),'10_kup_tabela',[.86,.84,.77,1])
# Three spotlights with integrated mounting plates and stems.
for i,x in enumerate([-42,-6,32],1):
 s=union([cylinder(1.4,3.7,(x,6,186)),cylinder(3.5,1.1,(x,6,182.8)),cylinder(6,2.15,(x,6,177.5))])
 s=s-cylinder(.6,1.65,(x,6,177.3))
 save(s,f'{10+i:02d}_spot_{i}',[.028,.029,.03,1])
# Menu stand: foot, continuous stem, angled framed plaque, six shallow plate reliefs.
angle=35;center=(78,1,85)
def tilt(s):return s.rotate((angle,0,0)).translate(center)
plaque=tilt(box((-13,-10,-1.3),(13,10,1)))
frame=tilt(box((-13,-10,.6),(13,10,2))-box((-11.7,-8.7,.5),(11.7,8.7,2.5)))
parts=[box((68,-7,26),(88,10,27.6)),box((76.8,1,27.5),(79.2,3.8,85)),plaque,frame]
for x in [-7.5,0,7.5]:
 for y in [-4.6,4.2]:
  parts.append(tilt(cylinder(.55,2.3,(x,y,.85))))
  parts.append(tilt(box((x-2.3,y-3,.85),(x+2.3,y-2.65,1.25))))
save(union(parts),'14_menu_standi',[.43,.35,.23,1])
# Two distinct mats, shallow ridges integral with their backing.
for name,lo,hi in [('23_paspas_esik',(-22,-6,26),(43,17,27.2)),('24_paspas_kaldirim',(-27,-35,18),(62,-13,19.2))]:
 items=[box(lo,hi)]
 for x in np.arange(lo[0]+.6,hi[0]-.4,1.2):items.append(box((x,lo[1]+.4,hi[2]-.1),(x+.38,hi[1]-.4,hi[2]+.25)))
 save(union(items),name,[.45,.018,.028,1])
# Half-ellipse roadside bollard with through-hole.
arc=[(12+14*np.cos(a),11+22*np.sin(a)) for a in np.linspace(0,np.pi,97)]
s=mf.CrossSection([arc]).extrude(5.5).rotate((90,0,0)).translate((0,-44,0))
hole=mf.Manifold.cylinder(9,1.65,1.65,48).rotate((90,0,0)).translate((12,-42,24))
save(s-hole,'25_sari_baba',[.88,.51,.025,1])
save(union([box((-50,12.6,143),(50,24,173)),box((-89,18.4,170),(89,24,176))]),'26_tabela_montaj_destegi',[.29,.115,.025,1])
(root/'reports'/'accessory_materials.json').write_text(json.dumps(records,indent=2))
