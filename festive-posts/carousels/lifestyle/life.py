exec(open('/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/fest_lib.py').read())
LROOT=REPO+'festive-posts/carousels/lifestyle/'
def photo_card(im,path,y,x=66,w=948,maxh=None):
    p=Image.open(path).convert('RGB'); h=w*p.height/p.width
    if maxh and h>maxh:
        nh=int(p.width*maxh/w); t=(p.height-nh)//2; p=p.crop((0,t,p.width,t+nh)); h=maxh
    pw,ph=int(w*S),int(h*S); p=p.resize((pw,ph),Image.LANCZOS)
    m=Image.new('L',(pw,ph),0); ImageDraw.Draw(m).rounded_rectangle((0,0,pw-1,ph-1),radius=int(26*S),fill=255)
    L=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(L).rounded_rectangle(P(x,y+12,x+w,y+h+12),radius=int(26*S),fill=(60,40,30,70))
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(16*S)))
    pr=p.convert('RGBA'); pr.putalpha(m); im.alpha_composite(pr,P(x,y)); return y+h
def tag(im,x,y,t):
    d=ImageDraw.Draw(im); f=MO(700,22); tw=d.textlength(t,font=f)/S
    d.rounded_rectangle(P(x,y-40,x+tw+38,y),radius=int(20*S),fill=(255,255,255)); d.text(P(x+19,y-20),t,font=f,fill=DARK,anchor='lm')
def v_slide(n,N,col,kick,hl,sub,photo,tg,cover=False):
    im=base(col); kicker(im,kick); y=headline(im,230,hl,104 if cover else 96)
    y=body(im,y+(30 if cover else 24),sub,RED if cover else DARK,34 if cover else 32,900)
    b=photo_card(im,photo,y+28,maxh=1250-(y+28))
    if tg: tag(im,88,b-20,tg.upper())
    foot(im,n,N); return im
