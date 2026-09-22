"""Repack loaded textures at the documented delivery resolution."""
from pathlib import Path
import bpy
root=Path(__file__).resolve().parents[1]
for im in bpy.data.images:
 if im.source!='FILE':continue
 original=tuple(im.size)
 if im.packed_file:im.unpack(method='REMOVE')
 size=1024 if im.name.startswith('normal') else (512 if im.name.startswith('Image_1') else 2048)
 if im.size[0]>size:im.scale(size,size)
 fmt='JPEG' if im.name.startswith('Image_0') else 'PNG';ext='jpg' if fmt=='JPEG' else 'png'
 im.file_format=fmt;im.filepath_raw=str(root/'clean'/(im.name+'.'+ext));im.save();im.pack();im.filepath='//textures/'+im.name+'.'+ext
 print(im.name,original,tuple(im.size),len(im.packed_file.data),flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(root.parent/'final4/japan_shop_final.blend'),compress=True)
