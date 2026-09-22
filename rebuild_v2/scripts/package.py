"""Package the deliverables; verify every entry can be decompressed."""
from pathlib import Path
import hashlib,zipfile,sys
root=Path(__file__).resolve().parents[2];out=root/(sys.argv[1] if len(sys.argv)>1 else 'final4')
files=sorted(p for p in out.rglob('*') if p.is_file() and p.suffix in {'.stl','.blend','.png','.md','.json'})
checks=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(out).as_posix()+'\n' for p in files)
(out/'dosya_hashleri.sha256').write_text(checks)
archive=out/f'yagami_{out.name}_tum_modeller.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[out/'dosya_hashleri.sha256']:z.write(p,'yagami_'+out.name+'/'+p.relative_to(out).as_posix())
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print('Verified',len(files)+1,'files',archive.stat().st_size,'bytes',flush=True)
