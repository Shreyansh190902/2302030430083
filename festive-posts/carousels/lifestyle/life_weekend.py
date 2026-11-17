exec(open('/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/life.py').read())
PH=LROOT+'photos/screen-free-weekend/'
SETS={'screen-free-weekend':[
 ('01-cover',lambda N: v_slide(1,N,WHITE_BG,'YOUR WEEKEND PLAN',[[('A screen-free','h')],[('weekend, ','s'),('sorted.','s')]],'Simple play ideas from morning to night',PH+'cover.jpg','',True)),
 ('02-morning',lambda N: v_slide(2,N,YEL_BG,'SATURDAY MORNING',[[('Start ','s'),('with ','s'),('art.','h')]],'Draw the weekend plan together on the easel.',PH+'morning-art.jpg','Monkey Easel Board')),
 ('03-afternoon',lambda N: v_slide(3,N,WHITE_BG,'SATURDAY AFTERNOON',[[('Tower ','h'),('challenge!','s')]],'Who can pull the most blocks before it tumbles?',PH+'tower-challenge.jpg','Colorful Stacking Tower')),
 ('04-evening',lambda N: v_slide(4,N,YEL_BG,'SATURDAY NIGHT',[[('Family ','s'),('game ','h'),('night.','h')]],'Phones in a basket, games on the table.',PH+'game-night.jpg','Barrier Minds')),
 ('05-sunday',lambda N: v_slide(5,N,WHITE_BG,'SUNDAY MORNING',[[('Slow ','h'),('play for little ','s'),('ones.','h')]],'Wobbly first steps and a lot of cheering.',PH+'first-steps.jpg','Step Bloom')),
 ('06-sunday-evening',lambda N: v_slide(6,N,YEL_BG,'SUNDAY EVENING',[[('Count ','s'),('down ','h'),('to ','s'),('Monday.','h')]],'One last round of numbers and tumbles with Dadi.',PH+'number-tower.jpg','Number Stacking Tower')),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Plan your','h')],[('playful','h')],[('weekend.','h')]],'Everything you need for a screen-free weekend.')),
]}
render(SETS,LROOT)
