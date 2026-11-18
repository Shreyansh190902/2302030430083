exec(open('/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/life.py').read())
PH=LROOT+'photos/winter-evenings/'
O='/home/user/2302030430083/festive-posts/posts/winter-evenings/'
im=base(WHITE_BG); kicker(im,'WINTER EVENINGS')
y=headline(im,230,[[('Cold outside,','s')],[('cosy ','h'),('inside.','h')]],104)
y=body(im,y+26,'Swap screen time for blanket time this winter.',DARK,32,900)
b=photo_card(im,PH+'cover.jpg',y+28,maxh=1220-(y+28))
tag(im,88,b-20,'COLORFUL STACKING TOWER')
d=ImageDraw.Draw(im); f=MO(700,30); t='Shop at www.wudlytoys.com'
tw=d.textlength(t,font=f)/S
d.rounded_rectangle(P(66,1258,66+tw+56,1316),radius=int(29*S),fill=RED); d.text(P(66+28+tw/2,1287),t,font=f,fill=(255,255,255),anchor='mm')
im.convert('RGB').resize((1080,1350),Image.LANCZOS).save(O+'wudly-winter-evenings-post.png')
