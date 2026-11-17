import sys, os, numpy as np
SPD='/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/'
src=open(SPD+sys.argv[1]).read().replace('render(SETS,','CAPTURE(SETS,')
OUTROOT='/home/user/2302030430083/festive-posts/carousels/product-only/photoshop/'
import pytoshop
from pytoshop import layers as PL
from pytoshop.enums import ColorMode
import packbits as _pb, pytoshop.codecs as _pc
_pc.packbits=_pb
NAMES={'stepbloom':'Step Bloom','joyboard':'Joyboard','monkey_easel':'Monkey Easel Board','tabletop_easel':'Tabletop Easel Board','barrier':'Barrier Minds','crackcode':'Crack Code','classic_tower':'Classic Tumbling Tower','color_tower':'Colorful Stacking Tower','number_tower':'Number Stacking Tower','ramayan_set':'Ramayan Stacking Tower'}
def CAPTURE(sets,root):
    G=globals(); LAY=[]
    def newL(col=(0,0,0)): return Image.new('RGBA',(W,H),tuple(col)+(0,))
    def push(name,L,im=None):
        LAY.append((name,L))
        if im is not None: im.alpha_composite(L)
    o_base,o_head,o_body,o_kick,o_label,o_foot,o_prod=G['base'],G['headline'],G['body'],G['kicker'],G['label'],G['foot'],G['product']
    def base(col):
        im=Image.new('RGBA',(W,H),col+(255,)); push('Background',im.copy())
        L=newL(); lg=A['logo_y' if col==YEL_BG else 'logo_w']; lg=lg.resize((lg.width*S,lg.height*S),Image.LANCZOS); L.alpha_composite(lg,P(812,36))
        push('Wudly logo',L,im); return im
    def headline(im,y,lines_,size=96,maxw=900):
        L=newL(RED); r=o_head(L,y,lines_,size,maxw); push('Headline',L,im); return r
    def body(im,y,text,col=DARK,size=34,mw=760):
        L=newL(col); r=o_body(L,y,text,col,size,mw); push('Body text',L,im); return r
    def kicker(im,t):
        L=newL(DARK); o_kick(L,t); push('Kicker',L,im)
    def label(im,cx,y,name,sub=''):
        L=newL(DARK); o_label(L,cx,y,name,sub); push('Label - '+name,L,im)
    def foot(im,n,N,swipe=True):
        L=newL(RED); o_foot(L,n,N,swipe); push('Footer (Swipe / page)',L,im)
    def product(im,pid,cx,bottom,mh,mw):
        L=newL(); o_prod(L,pid,cx,bottom,mh,mw); push('Product - '+NAMES.get(pid,pid),L,im)
    def s_three(n,N,col,kick,hl,sub,items):
        im=base(col); kicker(im,kick); y=headline(im,230,hl,96); body(im,y+26,sub)
        for cx,(pid,mh,mw,name) in zip((200,540,880),items):
            product(im,pid,cx,1110,mh,mw)
            L=newL(DARK); d=ImageDraw.Draw(L)
            for j,ln in enumerate(name.upper().split('|')): d.text(P(cx,1135+j*32),ln,font=MO(700,24),fill=DARK,anchor='ma')
            push('Label - '+name.replace('|',' '),L,im)
        foot(im,n,N); return im
    def s_end(N,col,hl,sub,cta1='Explore the collection.',cta2='www.wudlytoys.com'):
        im=base(col); y=headline(im,230,hl,100,560); body(im,y+30,sub,RED,32,520)
        L=newL(RED); d=ImageDraw.Draw(L); d.text(P(66,1200),cta1,font=MO(700,32),fill=RED); d.text(P(66,1244),cta2,font=MO(700,32),fill=RED); push('Call to action',L,im)
        L=newL(); m=A['mascot']; q=m.resize((int(m.width*690*S/m.height),int(690*S)),Image.LANCZOS); L.alpha_composite(q,(int(1058*S-q.width),int(1280*S-q.height))); push('Mascot',L,im)
        return im
    G.update(base=base,headline=headline,body=body,kicker=kicker,label=label,foot=foot,product=product,s_three=s_three,s_end=s_end)
    for folder,S_ in sets.items():
        od=OUTROOT+folder+'/'; os.makedirs(od,exist_ok=True); N=len(S_); worst=0
        for i,(k,f) in enumerate(S_):
            LAY.clear(); full=f(N)
            psd=pytoshop.core.PsdFile(num_channels=3,height=1350,width=1080,color_mode=ColorMode.rgb,compression=1)
            comp=Image.new('RGBA',(1080,1350),(0,0,0,0))
            for name,L in LAY:
                l=L.resize((1080,1350),Image.LANCZOS); comp.alpha_composite(l)
                bb=l.getbbox()
                if not bb: continue
                x0,y0,x1,y1=bb; a=np.array(l.crop(bb))
                ch={-1:a[...,3],0:a[...,0],1:a[...,1],2:a[...,2]}
                psd.layer_and_mask_info.layer_info.layer_records.append(PL.LayerRecord(channels={c:PL.ChannelImageData(image=v,compression=1) for c,v in ch.items()},top=y0,left=x0,bottom=y1,right=x1,name=name))
            ca=np.array(comp.convert('RGB'))
            psd.image_data=pytoshop.image_data.ImageData(channels=np.stack([ca[...,0],ca[...,1],ca[...,2]]),compression=1)
            fn=od+'wudly-%s-%s.psd'%(folder,k)
            with open(fn,'wb') as fh: psd.write(fh)
            ref=np.array(Image.open(root+folder+'/wudly-%s-%s.png'%(folder,k)).convert('RGB')).astype(int)
            worst=max(worst,float(np.abs(ref-ca.astype(int)).mean()))
        print(folder,N,'slides, mean diff vs PNG (worst):',round(worst,2))
exec(src)
