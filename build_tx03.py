"""TX02 -> TX03: palette-only executable revision."""
from pathlib import Path
import struct,json,hashlib
p=Path(__file__).parent;source=p.parent/'b4-build/gsoc_app_v1';original=source.read_bytes();b=bytearray(original)
expected='1f87e4b4426088d400e8329f07abd8b55b4c4ae6d93095a1182de04f49767a92'
assert hashlib.sha256(b).hexdigest()==expected,'Unexpected TX02 input'
anchors=[(0,(0,8,90)),(32,(4,22,140)),(80,(10,36,185)),(112,(14,44,210)),(127,(16,48,220)),(128,(190,175,10)),(160,(225,205,30)),(208,(255,245,110)),(255,(255,255,210))]
colors=[]
for i in range(256):
 lo,hi=next((a,z) for a,z in zip(anchors,anchors[1:]) if a[0]<=i<=z[0]);f=(i-lo[0])/(hi[0]-lo[0]);r,g,blue=[round(a+(z-a)*f) for a,z in zip(lo[1],hi[1])];colors.append((r<<16)|(g<<8)|blue)
a,z=0x146800,0x146c00;b[a:z]=struct.pack('<256I',*colors)
assert len(b)==len(original) and b[:a]==original[:a] and b[z:]==original[z:]
(p/'gsoc_app_v1').write_bytes(b)
manifest={'build':'HamTech V1.4beta TX03','change':'Waterfall palette only; royal-blue lower range with yellow from midrange','input_sha256':expected,'output_sha256':hashlib.sha256(b).hexdigest(),'palette_file_range':[hex(a),hex(z)],'anchors':anchors,'all_other_executable_bytes':'identical to TX02','hardware_test':'New palette has not been tested on GSOC'}
(p/'TX03-patch-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(manifest['output_sha256'])
