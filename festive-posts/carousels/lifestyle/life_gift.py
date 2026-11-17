exec(open('/tmp/claude-0/-home-user-2302030430083/3958de54-3eb1-593a-a0ed-b5b8eb22afdf/scratchpad/life.py').read())
PH=LROOT+'photos/gift-guide/'
SETS={'gift-guide':[
 ('01-cover',lambda N: v_slide(1,N,WHITE_BG,'GIFTS THAT LAST',[[('Gifts they','h')],[('unwrap again ','s'),('and again.','s')]],'Wooden toys for every little one on your list',PH+'cover-unwrap.jpg','Monkey Easel Board',True)),
 ('02-little-ones',lambda N: v_slide(2,N,YEL_BG,'FOR THE LITTLE ONES',[[('Little ','s'),('hands,','h')],[('big ','s'),('discoveries.','h')]],'Busy fingers threading a butterfly, with Mumma right there.',PH+'little-ones.jpg','Joyboard + Step Bloom')),
 ('03-little-artists',lambda N: v_slide(3,N,WHITE_BG,'FOR LITTLE ARTISTS',[[('Draw ','h'),('it, wipe it,','s')],[('draw ','s'),('again.','h')]],'"Look Dadaji, that’s you!" A gift that grows with them.',PH+'little-artist.jpg','Tabletop Easel Board')),
 ('04-stack-it-up',lambda N: v_slide(4,N,YEL_BG,'STACK IT UP',[[('Stack, ','h'),('wobble,','s')],[('laugh ','s'),('again.','h')]],'Endless rounds of who-pulls-next, and who knocks it down.',PH+'tower-tumble.jpg','Classic Tumbling Tower')),
 ('05-game-night',lambda N: v_slide(5,N,WHITE_BG,'FAMILY GAME NIGHT',[[('Game ','s'),('night,','h')],[('all ','s'),('together.','h')]],'She cracked the code. Papa is still in shock.',PH+'game-night.jpg','Crack Code')),
 ('06-favourite',lambda N: v_slide(6,N,YEL_BG,'THE CROWD FAVOURITE',[[('Bright, ','h'),('bold,','s')],[('built to ','s'),('last.','h')]],'Even Dadi can’t resist one more round.',PH+'dadi-tower.jpg','Colorful Stacking Tower')),
 ('07-shop',lambda N: s_end(N,WHITE_BG,[[('Wrap up','h')],[('real play.','h')]],'Wooden toys that are loved long after the wrapping paper is gone.')),
]}
render(SETS,LROOT)
