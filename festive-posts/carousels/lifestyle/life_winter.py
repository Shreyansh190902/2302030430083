exec(open('/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/life.py').read())
PH=LROOT+'photos/winter-evenings/'
SETS={'winter-evenings':[
 ('01-cover',lambda N: v_slide(1,N,WHITE_BG,'WINTER EVENINGS',[[('Cosy evenings,','h')],[('sorted.','s')]],'One warm game for every cold night of the week',PH+'cover.jpg','Colorful Stacking Tower',True)),
 ('02-monday',lambda N: v_slide(2,N,YEL_BG,'MONDAY',[[('Draw ','h'),('the chill','s')],[('away.','h')]],'A snowman on the easel, hot chocolate on the side.',PH+'monday-easel.jpg','Tabletop Easel Board')),
 ('03-tuesday',lambda N: v_slide(3,N,WHITE_BG,'TUESDAY',[[('Quiet ','s'),('threads,','h')],[('warm ','s'),('hearts.','h')]],'Under the razai with Dadi, one butterfly at a time.',PH+'tuesday-joyboard.jpg','Joyboard')),
 ('04-wednesday',lambda N: v_slide(4,N,YEL_BG,'WEDNESDAY',[[('Count ','h'),('the blocks,','s')],[('not the ','s'),('cold.','h')]],'Roll the dice, find the number, pull it out!',PH+'wednesday-number.jpg','Number Stacking Tower')),
 ('05-thursday',lambda N: v_slide(5,N,WHITE_BG,'THURSDAY',[[('Blanket fort','h')],[('code ','s'),('breakers.','h')]],'Fairy lights, a secret code and one cheeky grin.',PH+'thursday-crackcode.jpg','Crack Code')),
 ('06-friday',lambda N: v_slide(6,N,YEL_BG,'FRIDAY NIGHT',[[('Gajak, chai','s')],[('and a ','s'),('face-off.','h')]],'Can anyone block Dadaji? The whole family is in.',PH+'friday-barrier.jpg','Barrier Minds')),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Make winter','h')],[('evenings','h')],[('warmer.','h')]],'Wooden games that bring the whole family under one blanket.')),
]}
render(SETS,LROOT)
