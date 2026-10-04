import struct,json,hashlib
from pathlib import Path
from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM
p=Path(__file__).parent;b=bytearray((p/'app-check.bin').read_bytes());orig=bytes(b)
k=Ks(KS_ARCH_ARM,KS_MODE_ARM)
code='''
push {r0-r6,lr}
mov r5,r1
bl 0x2b4a0
sub sp,sp,#32
mov r0,#24
bl 0x1ea54
mov r6,r0
mov r1,r5
mov r2,#0
bl 0x1e7f0
movw r0,#906
str r0,[sp]
mov r0,#6
str r0,[sp,#4]
movw r0,#1020
str r0,[sp,#8]
mov r0,#38
str r0,[sp,#12]
mov r0,r6
mov r1,sp
bl 0x20330
mov r0,sp
movw r1,#0x400
movt r1,#0x14
mvn r2,#0
bl 0x2ad94
mov r0,r6
mov r1,sp
bl 0x1e754
mov r0,sp
bl 0x2aee4
mov r0,sp
movw r1,#0x440
movt r1,#0x14
mvn r2,#0
bl 0x2ad94
mov r0,r6
mov r1,sp
bl 0x1eae4
mov r0,sp
bl 0x2aee4
mov r0,r6
mov r1,#0x84
bl 0x203c0
add sp,sp,#32
pop {r0-r6,pc}
'''
c=bytes(k.asm(code,addr=0x140200)[0]);assert len(c)<0x200
ph=struct.unpack_from('<I',b,28)[0]+6*32;off=struct.unpack_from('<I',b,ph+4)[0];assert off==0x146000
b.extend(b'\0'*max(0,off+0x500-len(b)));b[off+0x200:off+0x200+len(c)]=c
for a,t in [(0x400,b'Hamtech\nM0FXB Mod\0'),(0x440,b'color: #49dff3; font-size: 11px; background: transparent;\0')]:b[off+a:off+a+len(t)]=t
struct.pack_into('<II',b,ph+16,0x500,0x500)
a=0x2ff10-0x10000;assert orig[a:a+4]==bytes(k.asm('bl 0x2b4a0',addr=0x2ff10)[0]);b[a:a+4]=bytes(k.asm('bl 0x140200',addr=0x2ff10)[0])
(p/'app-branded.bin').write_bytes(b)
changes=[i for i in range(len(orig)) if orig[i]!=b[i]];assert all(i in range(a,a+4) or i in range(ph+16,ph+24) for i in changes)
(p/'runtime-brand-manifest.json').write_text(json.dumps({'text':'Hamtech M0FXB Mod','display_lines':['Hamtech','M0FXB Mod'],'geometry':[906,6,115,33],'font_pixels':11,'original_sha256':hashlib.sha256(orig).hexdigest(),'branded_sha256':hashlib.sha256(b).hexdigest(),'hook_vaddr':'0x2ff10','wrapper_vaddr':'0x140200','radio_patch_bytes_unchanged':True},indent=2)+'\n')
print('Built runtime label',len(c),'bytes')
