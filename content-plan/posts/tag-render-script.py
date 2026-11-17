exec(open('/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/fest_lib.py').read())
PO=REPO+'product-photos/product-only/'
im=Image.open(PO+'classic_tower.jpg').convert('RGB'); a=np.array(im).astype(int)
bg=tuple(int(v) for v in np.median(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]),0)); A['classic_tower']=key_out(im,bg,18)
img=base(WHITE_BG); kicker(img,'FAMILY GAME NIGHT')
y=headline(img,230,[[('Tag a ','s'),('parent','h')],[('who never lets','s')],[('the tower ','s'),('fall.','h')]],100,960)
body(img,y+26,'Steady hands, calm nerves and a very competitive spirit.',DARK,34,500)
product(img,'classic_tower',770,1165,500,480)
label(img,770,1185,'Classic Tumbling Tower')
d=ImageDraw.Draw(img)
# CTA pill
f=MO(700,34); t='Tag them below'; tw=d.textlength(t,font=f)/S
x0,y0=66,1150; d.rounded_rectangle(P(x0,y0,x0+tw+120,y0+80),radius=int(40*S),fill=RED)
d.text(P(x0+40,y0+40),t,font=f,fill=(255,255,255),anchor='lm')
ax=x0+tw+62; ay=y0+40
d.line([P(ax,ay-12),P(ax,ay+10)],fill=(255,255,255),width=int(5*S)); d.polygon([P(ax-12,ay+4),P(ax+12,ay+4),P(ax,ay+18)],fill=(255,255,255))
d.text(P(66,1260),'www.wudlytoys.com',font=MO(700,28),fill=DARK)
img.convert('RGB').resize((1080,1350),Image.LANCZOS).save(REPO+'content-plan/posts/wudly-tag-a-parent.png')
