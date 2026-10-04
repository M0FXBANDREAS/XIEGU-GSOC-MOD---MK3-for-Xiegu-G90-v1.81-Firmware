"""TX01 -> TX02: palette-only executable revision."""
from pathlib import Path
import struct,json,hashlib
p=Path(__file__).parent;source=p.parent/'b3-build/gsoc_app_v1';original=source.read_bytes();b=bytearray(original)
expected='f94325aeccfeb1cf4bc02561ee303b775e29d9c070c607a66c98209d9649630f'
assert hashlib.sha256(b).hexdigest()==expected,'Unexpected TX01 input'
anchors=[(0,(0,0,10)),(16,(0,12,45)),(48,(0,55,130)),(96,(0,140,230)),(144,(70,215,255)),(184,(170,240,255)),(208,(235,250,160)),(232,(255,252,150)),(255,(255,255,210))]
colors=[]
for i in range(256):
 lo,hi=next((a,z) for a,z in zip(anchors,anchors[1:]) if a[0]<=i<=z[0]);f=(i-lo[0])/(hi[0]-lo[0]);r,g,blue=[round(a+(z-a)*f) for a,z in zip(lo[1],hi[1])];colors.append((r<<16)|(g<<8)|blue)
a,z=0x146800,0x146c00;b[a:z]=struct.pack('<256I',*colors)
assert len(b)==len(original) and b[:a]==original[:a] and b[z:]==original[z:]
(p/'gsoc_app_v1').write_bytes(b)
manifest={'build':'HamTech V1.4beta TX02','change':'Waterfall palette only; brighter weak signals and pale-yellow strong signals','input_sha256':expected,'output_sha256':hashlib.sha256(b).hexdigest(),'palette_file_range':[hex(a),hex(z)],'anchors':anchors,'all_other_executable_bytes':'identical to working TX01','hardware_test':'TX01 reported working by user; new palette not yet tested on GSOC'}
(p/'TX02-patch-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(manifest['output_sha256'])
