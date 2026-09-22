from pathlib import Path
import json,base64,sys
root=Path(__file__).resolve().parents[1]
name=sys.argv[1]
n=int(sys.argv[2]) if len(sys.argv)>2 else 100000
request={'image_url':'data:image/png;base64,'+base64.b64encode((root/'references'/f'{name}.png').read_bytes()).decode(),'ai_model':'meshy-7.1','geometry_resolution':'4k','should_texture':True,'texture_resolution':'4k','enable_pbr':True,'should_remesh':True,'topology':'triangle','target_polycount':n,'save_pre_remeshed_model':True,'image_enhancement':False,'target_formats':['glb','stl'],'multi_view_thumbnails':True}
(root/'raw'/f'{name}_request.json').write_text(json.dumps(request))
print('Prepared',name)
