exec(open('/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/life.py').read())
PW=LROOT+'photos/why-wooden-toys/'; PK=LROOT+'photos/play-that-builds-skills/'
SETS={
'why-wooden-toys':[
 ('01-cover',lambda N: v_slide(1,N,WHITE_BG,'WHY WOODEN TOYS?',[[('Real wood,','h')],[('real play.','s')]],'5 reasons parents are switching to wood',PW+'cover.jpg','Classic Tumbling Tower',True)),
 ('02-safe',lambda N: v_slide(2,N,YEL_BG,'01 · SAFE FOR LITTLE HANDS',[[('Natural ','h'),('wood,','s')],[('smooth ','s'),('edges.','h')]],'Smooth natural wood that little hands can grab, hold and trust.',PW+'safe.jpg','Step Bloom')),
 ('03-lasts',lambda N: v_slide(3,N,WHITE_BG,'02 · BUILT TO LAST',[[('Made for ','s'),('years,','h')],[('not ','s'),('weeks.','h')]],'Sturdy blocks that survive every tumble, and get passed down to little brother.',PW+'lasts.jpg','Number Stacking Tower')),
 ('04-imagination',lambda N: v_slide(4,N,YEL_BG,'03 · SPARKS IMAGINATION',[[('No ','s'),('batteries.','h')],[('Just ','s'),('ideas.','h')]],'Today she’s the teacher. Tomorrow? She decides.',PW+'imagination.jpg','Monkey Easel Board')),
 ('05-together',lambda N: v_slide(5,N,WHITE_BG,'04 · BRINGS FAMILIES TOGETHER',[[('Screens ','s'),('off,','h')],[('faces ','s'),('up.','h')]],'Three generations, one board, endless laughter.',PW+'together.jpg','Barrier Minds')),
 ('06-learning',lambda N: v_slide(6,N,YEL_BG,'05 · LEARNING HIDDEN IN PLAY',[[('Count, ','h'),('match,','s')],[('crack the ','s'),('code.','h')]],'Colours, patterns and logic, learning that feels like a game.',PW+'learning.jpg','Crack Code')),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Choose','h')],[('real wood.','h')]],'Safe, natural toys made to be loved for years.')),
],
'play-that-builds-skills':[
 ('01-cover',lambda N: v_slide(1,N,WHITE_BG,'PLAY THAT BUILDS SKILLS',[[('Every toy','h')],[('teaches something.','s')]],'Find the right toy for the skill you want to grow',PK+'cover.jpg','Joyboard',True)),
 ('02-motor',lambda N: v_slide(2,N,YEL_BG,'MOTOR SKILLS',[[('Steady ','h'),('steps,','s')],[('busy ','s'),('fingers.','h')]],'Every wobbly step gets stronger, with Didi cheering him on.',PK+'motor.jpg','Step Bloom')),
 ('03-creativity',lambda N: v_slide(3,N,WHITE_BG,'CREATIVITY',[[('Big ','s'),('ideas,','h')],[('blank ','s'),('boards.','h')]],'One chalk rocket, and Papa is already in space.',PK+'creativity.jpg','Monkey Easel Board')),
 ('04-focus',lambda N: v_slide(4,N,YEL_BG,'FOCUS & PATIENCE',[[('Steady ','s'),('hands,','h')],[('calm ','s'),('minds.','h')]],'Every careful pull builds concentration. Mumma can barely watch!',PK+'focus.jpg','Colorful Stacking Tower')),
 ('05-thinking',lambda N: v_slide(5,N,WHITE_BG,'LOGIC & STRATEGY',[[('Think ','h'),('ahead,','s')],[('play ','s'),('smart.','h')]],'Plan your move, block theirs, outsmart the family.',PK+'thinking.jpg','Barrier Minds')),
 ('06-culture',lambda N: v_slide(6,N,YEL_BG,'STORIES & CULTURE',[[('Learn the ','s'),('Ramayan.','h')]],'A question on every block. Nani asks, the kids race to answer.',PK+'ramayan.jpg','Ramayan Stacking Tower')),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Play that','h')],[('grows','h')],[('with them.','h')]],'Find the right wooden toy for every skill.')),
],
}
render(SETS,LROOT)
