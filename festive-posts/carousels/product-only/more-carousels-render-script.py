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
SETS={
'why-wooden-toys':[
 ('01-cover',lambda N: s_cover(N,WHITE_BG,'WHY WOODEN TOYS?',[[('Real wood,','h')],[('real play.','s')]],'5 reasons parents are switching to wood',
   [('classic_tower',190,1190,420,300),('stepbloom',545,1200,440,400),('tabletop_easel',895,1190,420,300)])),
 ('02-safe',lambda N: s_one(2,N,YEL_BG,'01 · SAFE FOR LITTLE HANDS',[[('Natural ','h'),('wood,','s')],[('smooth ','s'),('edges.','h')]],'Made from natural wood and finished smooth, so little hands can explore freely.',('stepbloom',500,600),'Step Bloom')),
 ('03-lasts',lambda N: s_three(3,N,WHITE_BG,'02 · BUILT TO LAST',[[('Made for ','s'),('years,','h')],[('not ','s'),('weeks.','h')]],'Sturdy blocks that survive every tumble – and get passed on.',[('classic_tower',380,290,'Classic Tumbling|Tower'),('color_tower',380,290,'Colorful Stacking|Tower'),('number_tower',380,290,'Number Stacking|Tower')])),
 ('04-imagination',lambda N: s_two(4,N,YEL_BG,'03 · SPARKS IMAGINATION',[[('No ','s'),('batteries.','h')],[('Just ','s'),('ideas.','h')]],'Open-ended toys let children decide what happens next.',('monkey_easel',400,440,'Monkey Easel Board'),('joyboard',320,400,'Joyboard'))),
 ('05-together',lambda N: s_two(5,N,WHITE_BG,'04 · BRINGS FAMILIES TOGETHER',[[('Screens ','s'),('off,','h')],[('faces ','s'),('up.','h')]],'Games the whole family can play around one table.',('barrier',300,420,'Barrier Minds'),('crackcode',300,420,'Crack Code'))),
 ('06-learning',lambda N: s_two(6,N,YEL_BG,'05 · LEARNING HIDDEN IN PLAY',[[('Count, ','h'),('match,','s')],[('crack the ','s'),('code.','h')]],'Numbers, colours and patterns – learning that feels like a game.',('number_tower',380,300,'Number Stacking Tower'),('crackcode',300,420,'Crack Code'))),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Choose','h')],[('real wood.','h')]],'Safe, natural toys made to be loved for years.')),
],
'play-that-builds-skills':[
 ('01-cover',lambda N: s_cover(N,WHITE_BG,'PLAY THAT BUILDS SKILLS',[[('Every toy','h')],[('teaches','s')],[('something.','s')]],'Find the right toy for the skill you want to grow',
   [('joyboard',190,1190,360,300),('barrier',545,1200,360,360),('number_tower',895,1190,420,300)])),
 ('02-motor',lambda N: s_two(2,N,YEL_BG,'MOTOR SKILLS',[[('Steady ','h'),('steps,','s')],[('busy ','s'),('fingers.','h')]],'Walking, balancing, threading – big and small movements get stronger.',('stepbloom',380,420,'Step Bloom'),('joyboard',320,400,'Joyboard'))),
 ('03-creativity',lambda N: s_two(3,N,WHITE_BG,'CREATIVITY',[[('Big ','s'),('ideas,','h')],[('blank ','s'),('boards.','h')]],'Drawing, writing and pretend play – whiteboard on one side, blackboard on the other.',('monkey_easel',400,440,'Monkey Easel Board'),('tabletop_easel',400,440,'Tabletop Easel Board'))),
 ('04-focus',lambda N: s_three(4,N,YEL_BG,'FOCUS & PATIENCE',[[('Steady ','s'),('hands,','h')],[('calm ','s'),('minds.','h')]],'Every careful pull builds concentration – and counting too.',[('classic_tower',380,290,'Classic Tumbling|Tower'),('color_tower',380,290,'Colorful Stacking|Tower'),('number_tower',380,290,'Number Stacking|Tower')])),
 ('05-thinking',lambda N: s_two(5,N,WHITE_BG,'LOGIC & STRATEGY',[[('Think ','h'),('ahead,','s')],[('play ','s'),('smart.','h')]],'Plan moves, crack patterns and outsmart the family.',('barrier',300,420,'Barrier Minds'),('crackcode',300,420,'Crack Code'))),
 ('06-culture',lambda N: s_one(6,N,YEL_BG,'STORIES & CULTURE',[[('Learn ','s'),('the','s')],[('Ramayan.','h')]],'A question on every block – stories passed down through play.',('ramayan_set',500,660),'Ramayan Stacking Tower','Questions in English & Hindi')),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Play that','h')],[('grows','h')],[('with them.','h')]],'Find the right wooden toy for every skill.')),
],
'screen-free-weekend':[
 ('01-cover',lambda N: s_cover(N,WHITE_BG,'YOUR WEEKEND PLAN',[[('A screen-free','h')],[('weekend,','s')],[('sorted.','s')]],'Simple play ideas from morning to night',
   [('monkey_easel',190,1190,420,300),('crackcode',545,1200,330,360),('color_tower',895,1190,420,300)])),
 ('02-morning',lambda N: s_two(2,N,YEL_BG,'SATURDAY MORNING',[[('Start ','s'),('with','s')],[('art.','h')]],'Draw the weekend plan together on the easel.',('monkey_easel',400,440,'Monkey Easel Board'),('tabletop_easel',400,440,'Tabletop Easel Board'))),
 ('03-afternoon',lambda N: s_three(3,N,WHITE_BG,'SATURDAY AFTERNOON',[[('Tower ','h'),('challenge!','s')]],'Who can pull the most blocks before it tumbles?',[('classic_tower',380,290,'Classic Tumbling|Tower'),('color_tower',380,290,'Colorful Stacking|Tower'),('number_tower',380,290,'Number Stacking|Tower')])),
 ('04-evening',lambda N: s_two(4,N,YEL_BG,'SATURDAY NIGHT',[[('Family ','s'),('game','h')],[('night.','h')]],'Phones in a basket, games on the table.',('barrier',300,420,'Barrier Minds'),('crackcode',300,420,'Crack Code'))),
 ('05-sunday',lambda N: s_two(5,N,WHITE_BG,'SUNDAY MORNING',[[('Slow ','h'),('play','s')],[('for little ','s'),('ones.','h')]],'Wobbly first steps and calm threading time.',('stepbloom',380,420,'Step Bloom'),('joyboard',320,400,'Joyboard'))),
 ('06-sunday-evening',lambda N: s_one(6,N,YEL_BG,'SUNDAY EVENING',[[('Count ','s'),('down','h')],[('to ','s'),('Monday.','h')]],'One last round of numbers and tumbles before the new week.',('number_tower',520,560),'Number Stacking Tower')),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Plan your','h')],[('play','h')],[('weekend.','h')]],'Everything you need for a screen-free weekend.')),
],
}
render(SETS,REPO+'festive-posts/carousels/product-only/')
