exec(open('/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/fest_lib.py').read())
PO=REPO+'product-photos/product-only/'
for k in ('joyboard','classic_tower','color_tower','number_tower'):
    im=Image.open(PO+k+'.jpg').convert('RGB'); a=np.array(im).astype(int)
    bg=tuple(int(v) for v in np.median(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]),0))
    A[k]=key_out(im,bg,18)
def s_three(n,N,col,kick,hl,sub,items):
    im=base(col); kicker(im,kick); y=headline(im,230,hl,96); body(im,y+26,sub)
    for cx,(pid,mh,mw,name) in zip((200,540,880),items):
        product(im,pid,cx,1110,mh,mw); d=ImageDraw.Draw(im)
        for j,ln in enumerate(name.upper().split('|')): d.text(P(cx,1135+j*32),ln,font=MO(700,24),fill=DARK,anchor='ma')
    foot(im,n,N); return im
RT='Ramayan Stacking Tower'
SETS={'christmas-gift-guide':[
 ('01-cover',lambda N: s_cover(N,WHITE_BG,'CHRISTMAS GIFT GUIDE',[[('Gifts they','h')],[('unwrap again','s')],[('and again.','s')]],'Wooden toys for every little one on your list',
   [('color_tower',190,1190,420,300),('ramayan_set',545,1200,440,400),('monkey_easel',895,1190,420,300)])),
 ('02-little-ones',lambda N: s_two(2,N,YEL_BG,'FOR THE LITTLE ONES',[[('Little ','s'),('hands,','h')],[('big ','s'),('discoveries.','h')]],'A steady walker for first steps and a threading board for busy fingers.',('stepbloom',380,420,'Step Bloom'),('joyboard',320,400,'Joyboard'))),
 ('03-little-artists',lambda N: s_two(3,N,WHITE_BG,'FOR LITTLE ARTISTS',[[('Draw ','h'),('a star,','s')],[('then ','s'),('a tree.','h')]],'Whiteboard on one side, blackboard on the other – a gift that grows with them.',('monkey_easel',400,440,'Monkey Easel Board'),('tabletop_easel',400,440,'Tabletop Easel Board'))),
 ('04-stack-it-up',lambda N: s_three(4,N,YEL_BG,'STACK IT UP',[[('Stack, ','h'),('wobble,','s')],[('laugh ','s'),('again.','h')]],'Three towers, endless rounds of who-pulls-next.',[('classic_tower',380,290,'Classic Tumbling|Tower'),('color_tower',380,290,'Colorful Stacking|Tower'),('number_tower',380,290,'Number Stacking|Tower')])),
 ('05-game-night',lambda N: s_two(5,N,WHITE_BG,'HOLIDAY GAME NIGHT',[[('Game ','s'),('night','h')],[('by the ','s'),('tree.','h')]],'Strategy games that bring the whole family to the table.',('barrier',300,420,'Barrier Minds'),('crackcode',300,420,'Crack Code'))),
 ('06-ramayan',lambda N: s_one(6,N,YEL_BG,'A GIFT WITH A STORY',[[('Every ','s'),('block','h')],[('tells a ','s'),('story.','h')]],'A Ramayan question on every block – play, learn and share stories together.',('ramayan_set',500,660),RT,'Questions in English & Hindi')),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Wrap up','h')],[('real play.','h')]],'Wooden toys that are loved long after the wrapping paper is gone.')),
]}
render(SETS,REPO+'festive-posts/carousels/product-only/')
