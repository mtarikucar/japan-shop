"""Package the deliverables; verify every entry can be decompressed."""
from pathlib import Path
import hashlib,zipfile
root=Path(__file__).resolve().parents[2];out=root/'final4'
files=sorted(p for p in out.rglob('*') if p.is_file() and p.suffix in {'.stl','.blend','.png','.md','.json'})
checks=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(out).as_posix()+'\n' for p in files)
(out/'dosya_hashleri.sha256').write_text(checks)
archive=out/'yagami_final4_tum_modeller.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[out/'dosya_hashleri.sha256']:z.write(p,'yagami_final4/'+p.relative_to(out).as_posix())
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print('Verified',len(files)+1,'files',archive.stat().st_size,'bytes',flush=True)
