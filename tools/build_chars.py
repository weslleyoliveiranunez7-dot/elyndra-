# ELYNDRA v1.8 - personagens com design proprio (pixel art procedural, estilo Undertale: contorno preto, sombra em 2 tons, cabeca grande).
# Uso: python3 tools/build_chars.py www/img   (substitui npc.png e faces.png; mantem Voce, Floris e Floris! do faces.png antigo)
import sys, math, colorsys
from PIL import Image
OUT=sys.argv[1] if len(sys.argv)>1 else 'www/img'
NAMES=['Anubis','Aro','Athena','Bento','Cain','Dante','Dom','Erro Original','Guardião','Hades','Helena','Herdeiros','Joca','Judas','Kael','Lúcia','Matriarca','Mira','Morpheus','Nilo','Persephone','Primeiro Autor','Prometheus','Rainha','Rufo','Sira','Tobias','Vael','Vera','Zeus','Íris']
def H(h):
    h=h.lstrip('#'); h=''.join(c*2 for c in h) if len(h)==3 else h
    return tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,)
def sh(c,f): return tuple(min(255,int(v*f)) for v in c[:3])+(255,)
OL=(14,10,22,255)
SK={'p':'#f6d2b0','t':'#d9a273','b':'#a8704a','d':'#7a4a30','g':'#c9d6c0','w':'#f2efff','y':'#c9b87a','k':'#4a4660'}
# nome: (pele, cabelo, estilo cabelo, olhos, boca, corpo, cor1, cor2, extras)
S={
'Anubis':('k','#2a2230','jackal','glow','flat','robe','#d4b050','#2a2230',['collar:#ffd84a']),
'Aro':('t','#cfcfd8','short','dot','flat','coat','#9a9a9a','#5a5a66',['beard:#e4e4ea','brows']),
'Athena':('p','#6a4a30','long','dot','smile','armor','#9fd0ff','#e8f4ff',['helm:#c8d8ea','owl']),
'Bento':('t','#5a3a22','short','dot','smile','tunic','#6a8a5a','#e0c070',['hat:#d9b96a','freck']),
'Cain':('g','#2a2a34','hood','dot','flat','robe','#8a8a99','#3a3a48',['scar','mark:#c0303a']),
'Dante':('p','#3a2a24','short','dot','smirk','coat','#3a8a8a','#c0303a',['laurel:#6fbf5a']),
'Dom':('t','#3a3040','short','dot','flat','coat','#7a8aa0','#e8e8f0',['glasses']),
'Erro Original':('k','#7a6a8a','spiky','glitch','flat','robe','#7a6a8a','#ff3a8a',['glitch']),
'Guardião':('y','#2f7a3c','leaf','glow','flat','armor','#4a6a3a','#8a6a3a',['moss']),
'Hades':('g','#1a1630','spiky','glow','frown','robe','#3a3060','#8ab8ff',['collar:#8ab8ff','brows']),
'Helena':('p','#c06a8a','long','dot','smile','tunic','#d98ca8','#fff0f6',['ribbon:#ff6a9a','blush']),
'Herdeiros':('k','#3a2a50','hood','glow','flat','robe','#3a2a50','#b08aff',['mask:#e8e0ff']),
'Joca':('t','#4a3020','short','dot','open','tunic','#6a8aa0','#e8c04a',['cap:#e04a4a','freck','kid']),
'Judas':('y','#2a2218','hood','dot','smirk','coat','#8a7a66','#d9b030',['coin','stub']),
'Kael':('t','#ff7a2a','flame','sharp','smirk','coat','#d9482f','#ffd84a',['scarf:#ffb36b']),
'Lúcia':('p','#f0c84a','pony','dot','smile','tunic','#e0b84a','#fff4c0',['blush','lantern']),
'Matriarca':('t','#d8d0d8','bun','dot','smile','robe','#a86a6a','#e8c8c8',['shawl:#7a4a5a','specs']),
'Mira':('b','#2a1a14','braids','dot','smile','tunic','#c9a06a','#6a4a2a',['band:#e0503a']),
'Morpheus':('w','#e8d9ff','long','closed','flat','robe','#2a2050','#ffd84a',['hood:#1d1640','stars']),
'Nilo':('g','#8a9ab0','bald','dot','frown','coat','#9a9ab0','#4a5a70',['drops']),
'Persephone':('p','#7a5a3a','long','dot','smile','robe','#7ed8a0','#ff9ac0',['flowers']),
'Primeiro Autor':('w','#f4f0ff','long','hollow','none','robe','#e8d9ff','#6a5a9a',['quill']),
'Prometheus':('d','#ff6a1a','flame','dot','smirk','tunic','#ff9a5a','#8a8a99',['chain']),
'Rainha':('p','#2a1a3a','long','sharp','flat','robe','#d58cff','#fff0ff',['mask:#f8f0ff','blush']),
'Rufo':('t','#6a4a30','short','dot','flat','armor','#6a8aa0','#4a5a6a',['beard:#6a4a30','wide']),
'Sira':('t','#2a1a1a','buns','dot','open','tunic','#ff8a6a','#fff0d0',['blush']),
'Tobias':('t','#3a2a1a','short','dot','smile','coat','#8a6a3a','#e0e0e0',['cap:#3a5a8a','whistle']),
'Vael':('p','#8a2a2a','spiky','sharp','smirk','coat','#d95a5a','#f0e0c0',['scarf:#f0e0c0']),
'Vera':('b','#7a3a1a','bob','dot','smile','tunic','#c98b6a','#8a4a30',['blush']),
'Zeus':('t','#f0f0f8','long','dot','flat','armor','#ffe066','#e8e8f0',['beard:#f0f0f8','brows','wide']),
'Íris':('p','#4a2a7a','long','dot','smile','tunic','#7a5ac8','#ff6a9a',['rainbow','blush']),
}
class Cv:
    def __init__(s,w,h): s.w,s.h=w,h; s.p=[[None]*w for _ in range(h)]
    def px(s,x,y,c):
        x,y=int(x),int(y)
        if 0<=x<s.w and 0<=y<s.h and c is not None: s.p[y][x]=c
    def rect(s,x,y,w,h,c):
        for j in range(h):
            for i in range(w): s.px(x+i,y+j,c)
    def ell(s,cx,cy,rx,ry,c):
        for y in range(int(cy-ry)-1,int(cy+ry)+2):
            for x in range(int(cx-rx)-1,int(cx+rx)+2):
                if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1: s.px(x,y,c)
    def get(s,x,y): return s.p[y][x] if 0<=x<s.w and 0<=y<s.h else None
    def finish(s,shade=True):
        # sombra: pixel cujo vizinho da direita/baixo esta vazio fica mais escuro; depois contorno preto externo
        q=[r[:] for r in s.p]
        if shade:
            for y in range(s.h):
                for x in range(s.w):
                    c=s.p[y][x]
                    if c and c!=OL and (s.get(x+1,y) is None) and (s.get(x,y+1) is not None) : q[y][x]=sh(c,.78)
        o=[r[:] for r in q]
        for y in range(-1,s.h+1):
            for x in range(-1,s.w+1):
                if s.get(x,y) is None and any(s.get(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))) and 0<=x<s.w and 0<=y<s.h: o[y][x]=OL
        s.p=o; return s
    def img(s):
        im=Image.new('RGBA',(s.w,s.h),(0,0,0,0)); pm=im.load()
        for y in range(s.h):
            for x in range(s.w):
                if s.p[y][x]: pm[x,y]=s.p[y][x]
        return im
def head(cv,sp,ox,oy,big):
    sk,hc,hs,eye,mo,body,c1,c2,ex=sp; skin=H(SK[sk]); hair=H(hc); X=lambda x:ox+x; Y=lambda y:oy+y
    def P(x,y,c): cv.px(X(x),Y(y),c)
    def R(x,y,w,h,c): cv.rect(X(x),Y(y),w,h,c)
    jack=hs=='jackal'
    # costas do cabelo comprido / capuz (atras da cabeca)
    if hs in('long','hood','braids','bob','pony'):
        R(0,3,14,9,hair) if hs!='hood' else cv.ell(X(6.5),Y(5.5),7.6,6.8,hair)
    if hs=='buns' or hs=='bun':
        cv.ell(X(6.5),Y(-1),2.6,2.2,hair)
        if hs=='buns': cv.ell(X(0),Y(1),2,2,hair); cv.ell(X(13),Y(1),2,2,hair)
    cv.ell(X(6.5),Y(5.5),7,6,skin)
    if jack:
        cv.ell(X(6.5),Y(6),6,5,hair); R(3,9,8,4,H('#4a3a44'))
        for k in(0,1):
            for i in range(5): P(1+k*11+(1 if k else 0),-1+i,hair) if i else None
            for i in range(6): P(2+k*9+(i>3),-4+i,hair); P(3+k*9+(i>3),-3+i,hair)
    top=hair
    if hs in('short','long','bob','pony','braids','bun','buns','bald') and hs!='bald':
        for y in range(0,4):
            for x in range(0,14):
                if ((x-6.5)/7)**2+((y-5.5)/6)**2<=1 and (y<2 or (y==2 and not 3<x<10) or (y==3 and (x<3 or x>10))): P(x,y,top)
        R(0,3,2,3,top); R(12,3,2,3,top); R(2,2,4,1,top)
        if hs in('long','bob','braids'): R(0,3,2,11 if hs=='long' else 6,top); R(12,3,2,11 if hs=='long' else 6,top)
        if hs=='pony': R(12,3,2,2,top); cv.rect(X(14),Y(3),2,6,top)
        if hs=='braids':
            for k in range(4): P(0+(k%2),11+k,top); P(13-(k%2),11+k,top)
    if hs in('spiky','flame'):
        base=hair if hs=='spiky' else H('#ff7a2a')
        for x in range(0,14,2):
            h=3+(x%4==0)*2+(x in(6,8))
            for y in range(-h+2,3): P(x,y,base); P(x+1,y+1,base)
        R(0,2,14,2,base); R(0,4,2,2,base); R(12,4,2,2,base)
        if hs=='flame':
            for x in(3,6,9): P(x,-2,H('#ffd84a')); P(x,-1,H('#ffd84a'))
    if hs=='leaf':
        R(0,0,14,3,H('#3a8a3c')); [P(x,-1-(x%3==0),H('#58c05a')) for x in range(1,13,2)]; [P(x,-2,H('#58c05a')) for x in(3,7,10)]
    if hs=='hood':
        for y in range(0,4):
            for x in range(0,14):
                if ((x-6.5)/7.6)**2+((y-5.5)/6.8)**2<=1 and (y<3 or x<2 or x>11): P(x,y,hair)
        R(0,3,2,8,hair); R(12,3,2,8,hair); R(2,3,10,1,sh(hair,.7)); R(3,4,8,2,sh(skin,.55))
    # extras de cabeca
    for e in ex:
        k,_,v=e.partition(':'); col=H(v) if v else None
        if k in('hat','cap'):
            R(1,0,12,3,col); R(0,2,14,1,sh(col,.8)); R(-2 if k=='hat' else 9,2,16 if k=='hat' else 6,1,sh(col,.7)); R(3,-1,8,1,col) if k=='hat' else None
        if k=='crown': [P(x,-1-(x%4==0),col) for x in range(1,13)]; R(1,-1,12,1,col)
        if k=='laurel': [cv.px(X(x),Y(1+(x%2)),col) for x in range(0,14,1)]; [P(x,2,sh(col,.7)) for x in(1,4,9,12)]
        if k=='helm': R(0,0,14,3,col); R(5,-3,4,3,H('#d04a4a')); R(0,3,2,5,col); R(12,3,2,5,col)
        if k=='band': R(0,2,14,1,col)
        if k=='ribbon': R(10,0,4,2,col); R(9,1,2,3,col); R(13,1,2,3,col)
        if k=='flowers': [P(x,1,H(c)) for x,c in((1,'#ff9ac0'),(4,'#ffe066'),(8,'#ff9ac0'),(11,'#ffe066'))]; [P(x,0,H('#7ed8a0')) for x in(2,6,10)]
        if k=='rainbow':
            for i,c in enumerate(('#ff5a5a','#ffb03a','#ffe066','#6ad86a','#5ab0ff','#9a6aff')): P(2+i*2,0,H(c)); P(3+i*2,0,H(c))
        if k=='glitch':
            for i in range(6): R(i*3-1,(i*5)%11,5,1,H(('#ff3a8a','#3affd0','#fff')[i%3]))
    # rosto
    ey=6 if not jack else 6
    ec=OL
    if eye=='dot': R(3,ey,2,2 if not big else 3,ec); R(9,ey,2,2 if not big else 3,ec); big and (P(3,ey,H('#fff')),P(9,ey,H('#fff')))
    if eye=='closed': R(2,ey+1,4,1,ec); R(8,ey+1,4,1,ec)
    if eye=='sharp': [P(3+i,ey+(1-i//2 if i<4 else 0),ec) for i in range(3)]; [P(8+i,ey+(i//2),ec) for i in range(3)]; R(3,ey+1,2,2,ec); R(9,ey+1,2,2,ec)
    if eye=='glow': gc=H(c2) if 'jack' not in hs else H('#ffd84a'); gc=H('#ffd84a') if hs=='jackal' else gc; R(2,ey,3,2,gc); R(9,ey,3,2,gc); P(3,ey,OL); P(10,ey,OL)
    if eye=='hollow': R(2,ey-1,4,4,H('#fff')); R(8,ey-1,4,4,H('#fff')); R(3,ey,2,2,OL); R(9,ey,2,2,OL)
    if eye=='glitch': R(2,ey,4,2,H('#3affd0')); R(8,ey,4,2,H('#ff3a8a')); R(5,ey+3,5,1,OL)
    my=10
    if mo=='smile': R(5,my,4,1,OL); P(4,my-1,OL); P(9,my-1,OL)
    if mo=='flat': R(5,my,4,1,OL)
    if mo=='frown': R(5,my,4,1,OL); P(4,my+1,OL); P(9,my+1,OL)
    if mo=='open': R(5,my,4,2,OL); R(6,my+1,2,1,H('#e0506a'))
    if mo=='smirk': R(5,my,4,1,OL); P(9,my-1,OL); P(10,my-1,OL)
    for e in ex:
        k,_,v=e.partition(':'); col=H(v) if v else None
        if k=='blush': R(1,8,2,1,H('#ff8a9a')); R(11,8,2,1,H('#ff8a9a'))
        if k=='freck': [P(x,8,sh(skin,.7)) for x in(2,4,9,11)]
        if k=='beard': R(1,8,12,5,col); R(4,8,6,2,skin); R(5,my,4,1,OL); R(1,12,12,2,col) if big else None
        if k=='brows': R(2,ey-2,4,1,OL); R(8,ey-2,4,1,OL)
        if k=='glasses' or k=='specs': [R(1,ey-1,5,4,None) for _ in()]; R(1,ey-1,5,1,H('#e8e8f0')); R(8,ey-1,5,1,H('#e8e8f0')); R(1,ey+2,5,1,H('#e8e8f0')); R(8,ey+2,5,1,H('#e8e8f0')); R(6,ey,2,1,H('#e8e8f0'))
        if k=='scar': R(10,4,1,6,H('#c05a5a')); R(9,6,3,1,H('#c05a5a'))
        if k=='mark': R(6,2,2,2,col)
        if k=='stub': [P(x,11,sh(skin,.6)) for x in range(3,11,2)]
        if k=='mask': R(1,ey-2,12,5 if big else 4,col); R(2,ey,3,2,OL); R(9,ey,3,2,OL); R(6,ey-3,2,1,col)
        if k=='moss': [P(x,y,H('#58c05a')) for x,y in((1,7),(12,9),(11,3),(2,10))]
        if k=='stars': [P(x,y,H('#ffd84a')) for x,y in((2,1),(11,2),(6,0),(12,6))]
        if k=='drops': P(12,4,H('#8ad8ff')); P(12,5,H('#8ad8ff'))
        if k=='collar': pass
    return cv
def body(cv,sp,ox,oy,step,big=False):
    sk,hc,hs,eye,mo,bd,c1,c2,ex=sp; skin=H(SK[sk]); a=H(c1); b=H(c2)
    wide='wide' in ex; tx=5-(1 if wide else 0); tw=10+(2 if wide else 0); y0=oy+13
    leg=H('#3a3048') if bd!='robe' else a
    if bd=='robe':
        for y in range(y0,y0+13):
            w=tw+ (y-y0)//2; cv.rect(ox+ 10-w//2-ox%1+ (0), y, w, 1, a)
        cv.rect(ox+tx-1,y0,tw+2,2,sh(a,1.15)); cv.rect(ox+9,y0,2,12,b)
        cv.rect(ox+tx-4,y0+1,3,6,a); cv.rect(ox+tx+tw+1,y0+1,3,6,a); cv.rect(ox+tx-4,y0+7,3,2,skin); cv.rect(ox+tx+tw+1,y0+7,3,2,skin)
    else:
        lx=ox+tx
        # pernas e sapatos
        up=1 if step else 0
        cv.rect(lx+1,y0+10,3,4-up,leg); cv.rect(lx+tw-4,y0+10,3,4-(0 if step else 1),leg)
        cv.rect(lx,y0+13-up,5,2,H('#2a2030')); cv.rect(lx+tw-5,y0+13-(0 if step else 1),5,2,H('#2a2030'))
        cv.rect(lx,y0,tw,11 if bd!='tunic' else 8,a)
        if bd=='tunic': cv.rect(lx-1,y0+8,tw+2,3,sh(a,.85))
        if bd=='coat': cv.rect(ox+9,y0,2,11,b); cv.rect(lx,y0+7,tw,1,b)
        if bd=='armor': cv.rect(lx-2,y0,3,3,b); cv.rect(lx+tw-1,y0,3,3,b); cv.rect(lx+2,y0+1,tw-4,2,sh(a,1.2)); cv.rect(lx,y0+8,tw,1,b)
        cv.rect(lx-2,y0+1,2,7,a); cv.rect(lx+tw,y0+1,2,7,a); cv.rect(lx-2,y0+8,2,2,skin); cv.rect(lx+tw,y0+8,2,2,skin)
    for e in ex:
        k,_,v=e.partition(':'); col=H(v) if v else None
        if k=='collar': cv.rect(ox+5,y0-1,10,2,col)
        if k=='scarf': cv.rect(ox+4,y0-1,12,3,col); cv.rect(ox+13,y0+2,3,5,col)
        if k=='shawl': cv.rect(ox+3,y0,14,3,col)
        if k=='owl': cv.rect(ox+9,y0+3,2,2,H('#f0d080'))
        if k=='chain': [cv.px(ox+4+i,y0+4+(i%2),H('#c8c8d8')) for i in range(12)]
        if k=='coin': cv.rect(ox+12,y0+6,3,3,H('#ffd84a'))
        if k=='whistle': cv.rect(ox+8,y0+3,3,2,H('#e0e0e0'))
        if k=='lantern': cv.rect(ox+16,y0+5,3,4,H('#ffd84a')); cv.px(ox+17,y0+4,OL)
        if k=='quill': cv.rect(ox+16,y0+4,2,7,H('#ffffff')); cv.px(ox+17,y0+3,H('#6a5a9a'))
        if k=='stars': [cv.px(ox+x,y0+y,H('#ffd84a')) for x,y in((6,3),(13,6),(8,9),(12,10))]
        if k=='glitch': [cv.rect(ox+i*3,y0+(i*5)%9,4,1,H(('#ff3a8a','#3affd0','#fff')[i%3])) for i in range(6)]
        if k=='rainbow': [cv.rect(ox+4+i*2,y0+8,2,1,H(c)) for i,c in enumerate(('#ff5a5a','#ffe066','#6ad86a','#5ab0ff','#9a6aff'))]
def sprite(n,step):
    sp=S[n]; cv=Cv(20,30); oy=2-(1 if step else 0)
    body(cv,sp,0,oy,step); head(cv,sp,3,oy,False)
    return cv.finish().img()
def face(n):
    sp=S[n]; cv=Cv(16,16); head(cv,sp,1,2,True)
    # ombros
    c=H(sp[6]); cv.rect(1,14,14,2,c)
    for e in sp[8]:
        k,_,v=e.partition(':')
        if k in('collar','scarf','shawl'): cv.rect(1,14,14,2,H(v))
    cv.finish(); fc=cv.img()
    bg=Image.new('RGBA',(16,16),(26,20,40,255)); bg.alpha_composite(fc); return bg.resize((48,48),Image.NEAREST)
npc=Image.new('RGBA',(40,len(NAMES)*30),(0,0,0,0))
for i,n in enumerate(NAMES):
    for f in range(2): npc.alpha_composite(sprite(n,f),(f*20,i*30))
npc.save(f'{OUT}/npc.png')
old=Image.open(f'{OUT}/faces.png'); FN=['Você']+NAMES+['Floris','Floris!']
fs=Image.new('RGBA',(len(FN)*48,48),(0,0,0,0))
for i,n in enumerate(FN):
    f=old.crop((i*48,0,i*48+48,48)) if n in('Você','Floris','Floris!') else face(n)
    fs.paste(f,(i*48,0))
fs.save(f'{OUT}/faces.png'); print('ok',len(NAMES),'personagens')
