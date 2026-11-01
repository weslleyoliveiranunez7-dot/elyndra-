# ELYNDRA v1.6 - gera os sprites e texturas em www/img a partir de EXPLOIT/ (protagonista.png, Jordana.png, Flowey).
# Uso: python3 tools/build_assets.py <pasta EXPLOIT> <pasta www/img>
import sys, glob, re, colorsys, random
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
SRC=sys.argv[1] if len(sys.argv)>1 else 'exploit/EXPLOIT'
OUT=sys.argv[2] if len(sys.argv)>2 else 'www/img'
HTML=sys.argv[3] if len(sys.argv)>3 else 'www/index.html'
import os; os.makedirs(OUT,exist_ok=True)
CELLBG=(195,134,255)
def hexrgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def keyout(im,col=CELLBG):
    a=np.array(im.convert('RGBA')); m=(np.abs(a[:,:,:3].astype(int)-np.array(col)).sum(2)<8)|(np.abs(a[:,:,:3].astype(int)-np.array((138,90,157))).sum(2)<8); a[m,3]=0; return Image.fromarray(a,'RGBA')
# ---------- protagonista (Frisk): 4 colunas x 3 linhas (baixo, esquerda, cima), 22x32; direita = espelho no jogo
P=Image.open(f'{SRC}/protagonista.png').convert('RGB'); CW,CH=20,30
prot=Image.new('RGBA',(4*CW,3*CH),(0,0,0,0))
for r in range(3):
    for c in range(4):
        x=3+c*23; y=3+r*33
        prot.alpha_composite(keyout(P.crop((x,y,x+CW,y+CH))),(c*CW,r*CH))
prot.save(f'{OUT}/prot.png')
# ---------- NPCs: Frisk recolorido (2 quadros: parado, passo), uma linha por personagem
S=open(HTML,encoding='utf8').read()
npcs=dict(re.findall(r"n:'([^']*)',x:\d+,y:\d+,c:'(#[0-9a-fA-F]+)'",S))
for skip in ('Floris','Jordana'): npcs.pop(skip,None)
npcs['Rainha']='#d58cff'   # so aparece em batalha/dialogo
names=sorted(npcs)
HAIR=[(43,26,16),(107,58,26),(217,184,74),(138,138,153),(194,90,42),(26,26,42),(232,224,208),(90,40,60)]
SKIN=[(241,201,160),(224,176,136),(201,139,96),(168,106,68)]
def recolor(cell,col,i):
    a=np.array(cell).astype(int); out=a.copy(); rgb=a[:,:,:3]
    def sel(c): return (np.abs(rgb-np.array(c)).sum(2)<10)&(a[:,:,3]>0)
    base=np.array(col); stripe=np.clip(base*1.35+25,0,255); dark=np.clip(base*.55,0,255)
    out[sel((103,164,224))][:]=0
    for src,dst in(((103,164,224),base),((230,7,248),stripe),((255,201,14),SKIN[i%4]),((61,18,14),HAIR[(i*3)%8])):
        m=sel(src); out[m,:3]=dst
    return Image.fromarray(out.astype(np.uint8),'RGBA')
npc=Image.new('RGBA',(2*CW,max(1,len(names))*CH),(0,0,0,0))
for i,n in enumerate(names):
    for f in range(2):
        cell=prot.crop((f*CW,0,f*CW+CW,CH))   # coluna 0 e 1 da linha "baixo"
        npc.alpha_composite(recolor(cell,hexrgb(npcs[n]),i),(f*CW,i*CH))
npc.save(f'{OUT}/npc.png')
# ---------- Flowey (Floris): 2 quadros 'Talk'
F=Image.open(glob.glob(f'{SRC}/*Non-Playable Characters - Flowey.png')[0]).convert('RGB')
fa=np.array(F); m=(np.abs(fa.astype(int)-np.array(CELLBG)).sum(2)<8)
lab,n=ndi.label(m); objs=ndi.find_objects(lab)
cells=sorted([(s[0].start,s[1].start,s[0].stop,s[1].stop) for s in objs if (s[0].stop-s[0].start)>20 and (s[1].stop-s[1].start)>20])
rows={}
for c in cells: rows.setdefault(round(c[0]/12),[]).append(c)
rk=sorted(rows); cells=rows[rk[0]][:2]+rows[rk[2]][:3]   # Talk x2 (amigavel) + Laugh x3 (malvado)
FW,FH=32,40; fl=Image.new('RGBA',(5*FW,FH),(0,0,0,0))
for i,(y0,x0,y1,x1) in enumerate(cells):
    c=keyout(F.crop((x0,y0,x1,y1))); bb=c.getbbox(); c=c.crop(bb)
    fl.alpha_composite(c,(i*FW+(FW-c.width)//2,FH-c.height))
fl.save(f'{OUT}/floris.png'); FLS=fl
# ---------- Jordana: sprites 4 dir x (parado, andando, correndo), retrato (6) e batalha
J=Image.open(f'{SRC}/Jordana.png').convert('RGB'); ja=np.array(J).astype(int)
def clean(c):
    a=np.array(c).astype(int); lab,n=ndi.label(a.sum(2)<70)
    edge=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0)
    bg=np.isin(lab,list(edge)); return Image.fromarray(np.dstack([a.astype(np.uint8),np.where(bg,0,255).astype(np.uint8)]),'RGBA')
def fit(im,h):
    bb=im.getbbox(); im=im.crop(bb); w=max(1,round(im.width*h/im.height)); r=im.resize((w,h),Image.BOX)
    a=np.array(r); a[:,:,3]=np.where(a[:,:,3]>110,255,0); return Image.fromarray(a,'RGBA')
BOX=[(22,51,142,236),(149,51,249,236),(259,51,364,236),(373,51,480,236),(523,51,642,234),(649,52,751,235),(759,51,865,236),(873,51,979,236),(1028,51,1151,234),(1161,52,1263,232),(1271,51,1381,236),(1393,52,1504,232)]
JW,JH,JS=28,38,34
jo=Image.new('RGBA',(4*JW,3*JH),(0,0,0,0))
for i,b in enumerate(BOX):
    s=fit(clean(J.crop(b)),JS); r,c=divmod(i,4); jo.alpha_composite(s,(c*JW+(JW-s.width)//2,r*JH+JH-s.height))
jo.save(f'{OUT}/jordana.png')
PB=[(566,813,719,967),(723,813,876,967),(880,813,1033,967),(1036,813,1189,967),(1193,813,1346,967),(1350,813,1502,967)]
po=Image.new('RGBA',(6*48,48),(0,0,0,0))
for i,b in enumerate(PB): po.paste(J.crop(b).resize((48,48),Image.BOX).convert('RGBA'),(i*48,0))
po.save(f'{OUT}/jordana_face.png')
bt=fit(clean(J.crop((40,538,190,773))),76); bt.save(f'{OUT}/jordana_bat.png')
# ---------- texturas (16x16, repetiveis): linha = capitulo 0..8, coluna 0 = chao, 1 = parede
def vnoise(rng,sz,cell):
    g=np.array([[rng.random() for _ in range(sz//cell)] for _ in range(sz//cell)]); return np.kron(g,np.ones((cell,cell)))
PAL={ # chao(a,b,detalhe) parede(a,b,topo) estilo
0:('#13201a','#1b2d23','#24402f','#3a2a1d','#4a3626','#5a4230','moss'),
1:('#13201a','#1b2d23','#24402f','#3a2a1d','#4a3626','#5a4230','moss'),
2:('#221a1a','#2c2220','#3a2e2a','#3a2a2a','#2a1d1d','#5a4040','ash'),
3:('#1d1830','#262040','#3a3070','#2a2a50','#1d1d3a','#5a5aa0','tile'),
4:('#2a1d28','#33232f','#4a3040','#3a2418','#2c1b12','#6a4430','parquet'),
5:('#2a3044','#343b55','#4c5878','#4a4f6a','#3a3f58','#8a94b8','marble'),
6:('#15122a','#1b1735','#2a2250','#1d1830','#141024','#3a3070','stone'),
7:('#0d0c12','#11101a','#1a1826','#14121c','#0d0c14','#2a2438','void'),
8:('#0d1020','#121830','#1c2a50','#10162c','#0a0e20','#2a4a7a','circuit')}
tiles=Image.new('RGB',(32,9*16))
for k,(f0,f1,f2,w0,w1,w2,st) in PAL.items():
    rng=random.Random(100+k); f0,f1,f2,w0,w1,w2=map(hexrgb,(f0,f1,f2,w0,w1,w2))
    fl=np.zeros((16,16,3),np.uint8); wl=np.zeros((16,16,3),np.uint8)
    for y in range(16):
        for x in range(16):
            r=rng.random(); fl[y,x]=f0 if r<.6 else f1 if r<.92 else f2
            wl[y,x]=w0 if (x+y*2)%7 else w1
    if st=='moss':
        for _ in range(5): x,y=rng.randrange(14),rng.randrange(14); fl[y,x]=f2; fl[y,x+1]=f2
        for y in range(16): wl[y,(y*3)%16]=w1; wl[y,(y*3+8)%16]=w1   # veios de casca
    if st=='ash':
        for _ in range(8): fl[rng.randrange(16),rng.randrange(16)]=(80,66,60)
        for y in (5,11): wl[y,:]=w1
    if st in('tile','parquet','marble','stone','circuit'):
        for i in range(16): fl[0,i]=f0 if st!='marble' else f2; fl[i,0]=f0 if st!='marble' else f2
        if st=='parquet':
            for y in range(16):
                for x in range(16):
                    if ((x//8)+(y//8))%2: fl[y,x]=np.clip(fl[y,x].astype(int)+10,0,255)
        if st=='marble':
            for i in range(16): fl[(i+3)%16,i]=f1
        if st=='circuit':
            for i in range(4,12): fl[8,i]=f2; fl[i,4]=f2
            fl[8,12]=(90,160,255)
        for y in (0,8): wl[y,:]=w1
        for y in range(16): wl[y,0 if y<8 else 8]=w1
    if st=='void':
        for _ in range(3): fl[rng.randrange(16),rng.randrange(16)]=f2
    tiles.paste(Image.fromarray(fl),(0,k*16)); tiles.paste(Image.fromarray(wl),(16,k*16))
tiles.save(f'{OUT}/tiles.png')
# ---------- rostos de dialogo (48x48): cabecas dos NPCs ampliadas 3x, protagonista, Floris amigavel e malvado
FN=['Você']+names+['Floris','Floris!']
faces=Image.new('RGBA',(len(FN)*48,48),(0,0,0,0))
def head(cell): return cell.crop((2,0,18,16)).resize((48,48),Image.NEAREST)
for i,n in enumerate(FN):
    if n=='Você': h=head(prot.crop((0,0,CW,CH)))
    elif n.startswith('Floris'):
        fc=FLS.crop(((2 if n.endswith('!') else 0)*FW,0,(2 if n.endswith('!') else 0)*FW+FW,FH)); bb=fc.getbbox(); fc=fc.crop(bb)
        side=max(fc.width,min(fc.height,fc.width)); sq=Image.new('RGBA',(side,side),(0,0,0,0)); sq.alpha_composite(fc.crop((0,0,fc.width,min(fc.height,side))),(0,0)); h=sq.resize((48,48),Image.NEAREST)
    else: h=head(npc.crop((0,names.index(n)*CH,CW,names.index(n)*CH+CH)))
    bg=Image.new('RGBA',(48,48),(26,20,40,255)); bg.alpha_composite(h); faces.paste(bg,(i*48,0))
faces.save(f'{OUT}/faces.png')
open(f'{OUT}/faces_names.txt','w',encoding='utf8').write('\n'.join(FN)+'\n@@'+repr({**npcs,'Você':'#67a4e0'}))
open(f'{OUT}/npc_names.txt','w',encoding='utf8').write('\n'.join(names))
print('ok',len(names),'npcs; flowey cells',len(cells))
