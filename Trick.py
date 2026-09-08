import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="누루룽 서바이버",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

html = r'''
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>누루룽 서바이버</title>

<style>
*{box-sizing:border-box}

html,body{
 margin:0;
 width:100%;
 height:100%;
 overflow:hidden;
 background:#111;
 color:#fff;
 font-family:Arial,sans-serif;
 touch-action:none
}

#wrap{
 position:relative;
 width:100%;
 height:100%;
 min-height:0;
 background:#151515;
 overflow:hidden
}

canvas{
 display:block;
 width:100%;
 height:100%;
 background:#182018
}

#top{
 position:absolute;
 left:12px;
 right:12px;
 top:10px;
 z-index:5;
 pointer-events:none
}

.row{
 display:flex;
 gap:8px;
 align-items:center;
 flex-wrap:wrap
}

.bar{
 height:18px;
 border:2px solid #333;
 border-radius:9px;
 background:#333;
 overflow:hidden;
 position:relative
}

.bar i{
 display:block;
 height:100%;
 width:100%;
 transition:width .12s
}

#hpBar{width:min(300px,48vw)}
#hpFill{background:#e74c3c}

#shieldBar{
 width:min(240px,40vw);
 display:none
}

#shieldFill{background:#3498db}

#xpBar{
 width:min(420px,65vw);
 height:14px
}

#xpFill{background:#f1c40f}

#stats{
 font-size:14px;
 text-shadow:0 1px 2px #000
}

#message{
 position:absolute;
 top:42%;
 left:50%;
 transform:translate(-50%,-50%);
 z-index:10;
 text-align:center;
 font-size:28px;
 font-weight:bold;
 text-shadow:0 3px 5px #000;
 pointer-events:none
}

#select,#levelup,#gameover{
 position:absolute;
 inset:0;
 z-index:20;
 background:rgba(0,0,0,.78);
 display:flex;
 align-items:center;
 justify-content:center
}

.panel{
 width:min(900px,92vw);
 padding:24px;
 border-radius:18px;
 background:#20242a;
 border:2px solid #555;
 text-align:center;
 box-shadow:0 10px 40px #000
}

.panel h1{
 margin:5px 0 10px;
 font-size:32px
}

.panel p{
 color:#bbb
}

.choices{
 display:grid;
 grid-template-columns:repeat(3,1fr);
 gap:14px;
 margin-top:20px
}

button{
 border:0;
 border-radius:14px;
 padding:16px;
 color:#fff;
 background:#303840;
 font-size:17px;
 font-weight:bold;
 cursor:pointer
}

button:hover{
 background:#46515b
}

.weaponBtn{
 min-height:150px
}

.weaponBtn b{
 display:block;
 font-size:30px;
 margin-bottom:10px
}

.weaponBtn small{
 display:block;
 color:#bbb;
 line-height:1.5
}

.upgradeGrid{
 display:grid;
 grid-template-columns:repeat(2,1fr);
 gap:12px;
 margin-top:18px
}

.upgrade{
 min-height:100px;
 text-align:left
}

.upgrade strong{
 font-size:18px
}

.upgrade span{
 display:block;
 color:#bbb;
 font-size:13px;
 margin-top:8px
}

#controls{
 position:absolute;
 inset:0;
 z-index:6;
 pointer-events:none
}

#joystick{
 position:absolute;
 left:25px;
 bottom:28px;
 width:130px;
 height:130px;
 border-radius:50%;
 background:rgba(255,255,255,.12);
 border:2px solid rgba(255,255,255,.2);
 pointer-events:auto
}

#stick{
 position:absolute;
 left:37px;
 top:37px;
 width:56px;
 height:56px;
 border-radius:50%;
 background:rgba(255,255,255,.35)
}

.action{
 position:absolute;
 right:24px;
 bottom:32px;
 width:105px;
 height:58px;
 padding:8px;
 font-size:14px;
 pointer-events:auto
}

#skillBtn{
 bottom:100px;
 background:#6941a5
}

#formBtn{
 bottom:32px;
 background:#2d607f
}

#keyboardHint{
 position:absolute;
 right:18px;
 bottom:12px;
 color:#aaa;
 font-size:12px
}

.hidden{
 display:none!important
}


/* 모바일 */
@media(max-width:650px){

 #wrap{
  height:100%;
  min-height:0
 }

 #top{
  left:7px;
  right:7px;
  top:6px
 }

 .row{
  gap:5px
 }

 .bar{
  height:13px;
  border-width:1px;
  border-radius:7px
 }

 #hpBar{
  width:42vw;
  max-width:190px
 }

 #shieldBar{
  width:34vw;
  max-width:150px
 }

 #xpBar{
  width:72vw;
  height:10px;
  margin-top:2px
 }

 #stats{
  font-size:10px;
  white-space:nowrap
 }

 #classInfo{
  font-size:10px;
  max-width:100%;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  text-shadow:0 1px 2px #000
 }

 #message{
  font-size:20px
 }

 .panel{
  width:94vw;
  max-height:94%;
  overflow:auto;
  padding:12px;
  border-radius:13px
 }

 .panel h1{
  font-size:22px;
  margin:2px 0 6px
 }

 .panel p{
  font-size:12px;
  margin:5px 0
 }

 .choices{
  grid-template-columns:1fr;
  gap:7px;
  margin-top:10px
 }

 button{
  border-radius:10px;
  padding:10px;
  font-size:14px
 }

 .weaponBtn{
  min-height:68px
 }

 .weaponBtn b{
  font-size:22px;
  margin-bottom:3px
 }

 .weaponBtn small{
  font-size:10px;
  line-height:1.25
 }

 .upgradeGrid{
  grid-template-columns:1fr 1fr;
  gap:7px;
  margin-top:10px
 }

 .upgrade{
  min-height:72px;
  padding:9px;
  text-align:left
 }

 .upgrade strong{
  font-size:13px
 }

 .upgrade span{
  font-size:10px;
  margin-top:4px;
  line-height:1.2
 }

 #joystick{
  left:14px;
  bottom:14px;
  width:100px;
  height:100px
 }

 #stick{
  left:29px;
  top:29px;
  width:42px;
  height:42px
 }

 .action{
  right:14px;
  width:88px;
  height:48px;
  padding:5px;
  font-size:12px;
  border-radius:12px
 }

 #skillBtn{
  bottom:76px
 }

 #formBtn{
  bottom:14px
 }

 #keyboardHint{
  display:none
 }
}
</style>
</head>

<body>

<div id="wrap">

<canvas id="game"></canvas>

<div id="top">

 <div class="row">

  <div class="bar" id="hpBar">
   <i id="hpFill"></i>
  </div>

  <div class="bar" id="shieldBar">
   <i id="shieldFill"></i>
  </div>

  <div id="stats">
   Lv.1 | 0:00
  </div>

 </div>

 <div class="bar" id="xpBar">
  <i id="xpFill"></i>
 </div>

 <div id="classInfo"></div>

</div>


<div id="message"></div>


<div id="controls">

 <div id="joystick">
  <div id="stick"></div>
 </div>

 <button id="skillBtn" class="action">
  스킬
 </button>

 <button id="formBtn" class="action">
  폼체인지
 </button>

</div>


<div id="select">

 <div class="panel">

  <h1>
   누루룽 서바이버
  </h1>

  <p>
   직업을 선택하세요
  </p>

  <div class="choices">

   <button class="weaponBtn" onclick="startGame('gun')">

    <b>🔫 총</b>

    권총 / 저격 폼체인지

    <br>

    <small>
     자동 사격 · 투사체 수 · 관통
    </small>

   </button>


   <button class="weaponBtn" onclick="startGame('sword')">

    <b>⚔️ 검사</b>

    베기 / 검기

    <br>

    <small>
     근접 부채꼴 공격 · 전방 검기 · 방어막
    </small>

   </button>


   <button class="weaponBtn" onclick="startGame('magic')">

    <b>🔮 마법</b>

    기본공격 / 강화공격 / 각성

    <br>

    <small>
     레이저 · 각성 · 레이저 개수
    </small>

   </button>

  </div>

 </div>

</div>


<div id="levelup" class="hidden">

 <div class="panel">

  <h1>
   LEVEL UP!
  </h1>

  <p>
   강화할 능력을 하나 선택하세요.
  </p>

  <div id="upgradeGrid" class="upgradeGrid"></div>

 </div>

</div>


<div id="gameover" class="hidden">

 <div class="panel">

  <h1>
   게임 오버
  </h1>

  <p id="result"></p>

  <button onclick="location.reload()">
   다시 시작
  </button>

 </div>

</div>

</div>


<script>

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");

let W=0,H=0,DPR=1;

function resize(){

 DPR=Math.min(devicePixelRatio||1,2);

 W=canvas.clientWidth;
 H=canvas.clientHeight;

 canvas.width=W*DPR;
 canvas.height=H*DPR;

 ctx.setTransform(DPR,0,0,DPR,0,0);
}

addEventListener("resize",resize);

resize();


const TAU=Math.PI*2;

const clamp=(v,a,b)=>
 Math.max(a,Math.min(b,v));

const rand=(a,b)=>
 a+Math.random()*(b-a);

const dist=(a,b)=>
 Math.hypot(a.x-b.x,a.y-b.y);


let state="select";

let last=0;
let elapsed=0;

let nextEnemy=0;
let nextBoss=100;

let enemies=[];
let projectiles=[];
let slashes=[];
let lasers=[];
let texts=[];
let particles=[];

let player=null;

let level=1;
let xp=0;
let xpNeed=10;
let kills=0;
let bossCount=0;

let keys={};

let joy={
 x:0,
 y:0
};

let mouse={
 x:0,
 y:0,
 active:false
};


const classNames={
 gun:"총",
 sword:"검사",
 magic:"마법"
};


function makePlayer(cls){

 return {

  cls,

  x:W/2,
  y:H/2,

  r:18,

  face:0,

  hp:100,
  maxHp:100,

  speed:185,

  damage:15,
  attackSpeed:2,

  range:180,
  area:1,

  projectiles:1,
  penetration:0,

  projectileSpeed:500,


  shield:0,
  maxShield:0,

  damageReduction:0,


  swordDamage:22,
  swordSpeed:1.6,
  swordRange:90,
  swordFan:1.25,

  swordWaveDamage:9,
  swordWaveSpeed:.55,
  swordWaveCount:1,
  swordWaveSize:12,


  magicDamage:14,
  magicSpeed:1.5,

  laserDamage:28,
  laserDuration:.8,
  laserCount:1,

  enhancedEvery:10,
  enhancedCounter:0,


  skillReady:false,

  skillKills:12,
  skillKillProgress:0,

  skillDuration:5,

  skillActive:false,

  skillTimer:0,
  skillCooldown:0,

  gunSkillTimer:0,


  gunForm:"pistol",
  formCooldown:0,

  invuln:0
 };
}


function startGame(cls){

 player=makePlayer(cls);

 state="playing";

 document
  .getElementById("select")
  .classList
  .add("hidden");

 document
  .getElementById("formBtn")
  .classList
  .toggle("hidden",cls!=="gun");

 updateUI();

 requestAnimationFrame(loop);
}


function nearestEnemy(){

 let best=null;
 let bd=Infinity;

 for(const e of enemies){

  let d=dist(player,e);

  if(d<bd){
   bd=d;
   best=e;
  }

 }

 return best;
}


function nearestAngle(){

 const e=nearestEnemy();

 return e
  ? Math.atan2(
      e.y-player.y,
      e.x-player.x
    )
  : player.face;
}


/* =========================
   총
========================= */

function shootGun(){

 const p=player;

 const target=nearestEnemy();

 if(!target)return;

 const base=nearestAngle();

 p.face=base;

 let count=p.projectiles;

 let dmg=p.damage;
 let speed=p.projectileSpeed;
 let pen=p.penetration;
 let range=p.range;


 /* 총 스킬 */

 if(p.gunSkillTimer>0){

  dmg*=1.7;
  speed*=1.35;

 }


 /* 권총 */

 if(p.gunForm==="pistol"){

  dmg*=.8;
  speed*=1.15;
  range*=.9;

 }


 /* 저격 */

 else{

  dmg*=1.9;
  speed*=1.05;
  range*=1.45;

  pen+=2;

 }


 /* 투사체 수는
    일반 공격과 스킬 모두 동일하게 적용 */

 for(let i=0;i<count;i++){

  const spread=
   (i-(count-1)/2)*.10;

  projectiles.push({

   x:p.x,
   y:p.y,

   a:base+spread,

   speed,

   dmg,

   pen,

   range,

   travel:0,

   r:5,

   type:"gun"

  });

 }

}


/* =========================
   검사
========================= */

function swordSlash(){

 const p=player;

 p.face=nearestAngle();

 slashes.push({

  x:p.x,
  y:p.y,

  a:p.face,

  life:.18,
  max:.18,

  range:p.swordRange*p.area,

  fan:p.swordFan,

  dmg:p.swordDamage

 });

}


function swordWave(){

 const p=player;

 const e=nearestEnemy();

 if(!e)return;

 const a=
  Math.atan2(
   e.y-p.y,
   e.x-p.x
  );

 p.face=a;


 for(
  let i=0;
  i<p.swordWaveCount;
  i++
 ){

  const spread=
   (i-(p.swordWaveCount-1)/2)*.12;

  projectiles.push({

   x:p.x,
   y:p.y,

   a:a+spread,

   speed:360,

   dmg:p.swordWaveDamage,

   /* 검기는 모든 적 관통 */

   pen:999999,

   range:p.range*1.25,

   travel:0,

   r:p.swordWaveSize*p.area,

   type:"wave"

  });

 }

}


/* =========================
   마법
========================= */

function magicBasic(){

 const p=player;

 const e=nearestEnemy();

 if(!e)return;

 const a=
  Math.atan2(
   e.y-p.y,
   e.x-p.x
  );

 p.face=a;


 /*
   일반:
   일정 횟수마다 강화공격

   각성 중:
   모든 평타가 강화공격
 */

 let enhanced=
  p.skillActive ||
  p.enhancedCounter>=p.enhancedEvery;


 if(enhanced){

  p.enhancedCounter=0;

  const vertical=
   Math.random()<.5;

  makeLasers(vertical);

 }

 else{

  p.enhancedCounter++;

  projectiles.push({

   x:p.x,
   y:p.y,

   a,

   speed:430,

   dmg:p.magicDamage,

   pen:0,

   range:p.range,

   travel:0,

   r:6,

   type:"magic"

  });

 }

}


function makeLasers(both){

 const p=player;

 /*
   일반 강화공격:
   가로 OR 세로

   각성:
   가로 AND 세로
 */

 const dirs=
  both
   ? [0,Math.PI/2]
   : [
      Math.random()<.5
       ? 0
       : Math.PI/2
     ];


 for(const a of dirs){

  for(
   let i=0;
   i<p.laserCount;
   i++
  ){

   const offset=
    (i-(p.laserCount-1)/2)
    *34*p.area;

   lasers.push({

    x:p.x,
    y:p.y,

    a,

    offset,

    life:p.laserDuration,

    max:p.laserDuration,

    dmg:p.laserDamage*p.area

   });

  }

 }

}


/* =========================
   스킬
========================= */

function useSkill(){

 const p=player;

 if(!p)return;

 if(p.skillActive)return;

 if(p.skillCooldown>0)return;

 if(p.skillKillProgress<p.skillKills)return;


 /*
   스킬 게이지 사용
 */

 p.skillKillProgress=0;


 /* 마법 각성 */

 if(p.cls==="magic"){

  p.skillActive=true;

  p.skillTimer=p.skillDuration;

 }


 /* 검사 방어막 */

 else if(p.cls==="sword"){

  p.shield=
   p.maxShield=
   Math.max(
    50,
    p.maxHp*.75
   );

  p.skillCooldown=8;

 }


 /* 총 강화사격 */

 else if(p.cls==="gun"){

  p.skillCooldown=6;

  /*
    2.5초 동안 강화사격.

    shootGun()에서
    현재 투사체 수와 관통을
    그대로 사용한다.
  */

  p.gunSkillTimer=2.5;

 }

}


/* =========================
   총 폼체인지
========================= */

function formChange(){

 const p=player;

 if(
  p.cls!=="gun" ||
  p.formCooldown>0
 )return;

 p.gunForm=
  p.gunForm==="pistol"
   ?"sniper"
   :"pistol";

 p.formCooldown=1.5;

}


/* =========================
   적 생성
========================= */

function spawnEnemy(boss=false){

 const side=
  Math.floor(Math.random()*4);

 const margin=45;

 let x,y;


 if(side===0){

  x=-margin;
  y=rand(0,H);

 }

 else if(side===1){

  x=W+margin;
  y=rand(0,H);

 }

 else if(side===2){

  x=rand(0,W);
  y=-margin;

 }

 else{

  x=rand(0,W);
  y=H+margin;

 }


 const t=elapsed;


 const hp=
  (
   10+
   t*.09+
   level*.7
  )*
  (boss?18:1);


 enemies.push({

  x,
  y,

  r:boss?28:13,

  hp,
  maxHp:hp,

  speed:
   (boss?35:45)+
   Math.min(35,t*.035),

  dmg:
   (boss?10:5)+
   t*.012+
   level*.1,

  boss

 });

}


/* =========================
   경험치
========================= */

function gainXP(n){

 xp+=n;

 while(xp>=xpNeed){

  xp-=xpNeed;

  level++;

  xpNeed=
   Math.floor(
    10+level*4
   );

  showLevelUp();

 }

}


/* =========================
   적 처치
========================= */

function enemyKilled(e){

 kills++;

 gainXP(
  e.boss
   ? 15
   : 1
 );


 /*
   마법 각성 중에는
   처치해도 게이지 증가 X
 */

 if(!player.skillActive){

  player.skillKillProgress=
   Math.min(
    player.skillKills,
    player.skillKillProgress+1
   );

 }


 for(let i=0;i<3;i++){

  particles.push({

   x:e.x,
   y:e.y,

   vx:rand(-60,60),
   vy:rand(-60,60),

   life:.35

  });

 }

}


function hitEnemy(e,dmg){

 e.hp-=dmg;

 if(e.hp<=0){

  const idx=
   enemies.indexOf(e);

  if(idx>=0){

   enemies.splice(
    idx,
    1
   );

  }

  enemyKilled(e);

 }

}


/* =========================
   플레이어 피해
========================= */

function damagePlayer(dmg){

 const p=player;

 if(p.invuln>0)return;

 let d=
  dmg*
  (1-p.damageReduction);


 if(p.shield>0){

  const s=
   Math.min(
    p.shield,
    d
   );

  p.shield-=s;

  d-=s;

 }


 p.hp-=d;

 p.invuln=.25;


 if(p.hp<=0){

  gameOver();

 }

}


/* =========================
   레벨업
========================= */

function showLevelUp(){

 state="levelup";

 const grid=
  document.getElementById(
   "upgradeGrid"
  );

 grid.innerHTML="";

 const options=
  makeUpgrades();


 options.forEach(o=>{

  const b=
   document.createElement(
    "button"
   );

  b.className="upgrade";

  b.innerHTML=
   "<strong>"+
   o.name+
   "</strong>"+
   "<span>"+
   o.desc+
   "</span>";


  b.onclick=()=>{

   o.apply();

   document
    .getElementById("levelup")
    .classList
    .add("hidden");

   state="playing";

   updateUI();

  };


  grid.appendChild(b);

 });


 document
  .getElementById("levelup")
  .classList
  .remove("hidden");

}


/* =========================
   강화 목록
========================= */

function makeUpgrades(){

 const p=player;

 const arr=[];


 const add=
  (name,desc,fn)=>
   arr.push({
    name,
    desc,
    apply:fn
   });


 /* 총 */

 if(p.cls==="gun"){

  add(
   "투사체 수 +1",
   "기본 공격과 스킬의 총알 수 증가",
   ()=>p.projectiles++
  );


  add(
   "관통 +1",
   "총알이 추가 적 1명을 관통",
   ()=>p.penetration++
  );


  add(
   "공격력 +15%",
   "총의 기본 공격력 증가",
   ()=>p.damage*=1.15
  );


  add(
   "공격속도 +15%",
   "총의 발사 속도 증가",
   ()=>p.attackSpeed*=1.15
  );


  add(
   "사거리 +15%",
   "총알의 최대 사거리 증가",
   ()=>p.range*=1.15
  );


  add(
   "최대 HP +20",
   "생존력 증가",
   ()=>{
    p.maxHp+=20;
    p.hp+=20;
   }
  );

 }


 /* 검사 */

 else if(p.cls==="sword"){

  add(
   "검기 개수 +1",
   "한 번에 발사하는 검기 증가",
   ()=>p.swordWaveCount++
  );


  add(
   "공격 범위 +15%",
   "베기 범위와 검기 크기 증가",
   ()=>p.area*=1.15
  );


  add(
   "베기 공격력 +15%",
   "근접 베기 피해 증가",
   ()=>p.swordDamage*=1.15
  );


  add(
   "베기 공격속도 +15%",
   "베기 속도 증가",
   ()=>p.swordSpeed*=1.15
  );


  add(
   "검기 공격력 +15%",
   "검기 피해 증가",
   ()=>p.swordWaveDamage*=1.15
  );


  add(
   "검기 공격속도 +15%",
   "검기 발사 속도 증가",
   ()=>p.swordWaveSpeed*=1.15
  );


  add(
   "피해 감소 +5%",
   "받는 피해 감소",
   ()=>p.damageReduction=
    Math.min(
     .65,
     p.damageReduction+.05
    )
  );


  add(
   "최대 HP +25",
   "최대 체력 증가",
   ()=>{
    p.maxHp+=25;
    p.hp+=25;
   }
  );

 }


 /* 마법 */

 else{

  add(
   "레이저 개수 +1",
   "강화공격의 가로/세로 레이저 수 증가",
   ()=>p.laserCount=
    Math.min(
     5,
     p.laserCount+1
    )
  );


  add(
   "강화공격 -1회",
   "강화공격까지 필요한 평타 감소 (최소 5회)",
   ()=>p.enhancedEvery=
    Math.max(
     5,
     p.enhancedEvery-1
    )
  );


  add(
   "마법 공격력 +15%",
   "기본 마법탄 피해 증가",
   ()=>p.magicDamage*=1.15
  );


  add(
   "마법 공격속도 +15%",
   "기본 공격 속도 증가",
   ()=>p.magicSpeed*=1.15
  );


  add(
   "레이저 공격력 +15%",
   "강화공격 레이저 피해 증가",
   ()=>p.laserDamage*=1.15
  );


  add(
   "레이저 지속시간 +0.2초",
   "최대 2초",
   ()=>p.laserDuration=
    Math.min(
     2,
     p.laserDuration+.2
    )
  );


  add(
   "각성 지속시간 +0.5초",
   "최대 10초",
   ()=>p.skillDuration=
    Math.min(
     10,
     p.skillDuration+.5
    )
  );


  add(
   "각성 필요 처치 -1",
   "각성 게이지 필요 처치 수 감소",
   ()=>{
    const min=6;

    p.skillKills=
     Math.max(
      min,
      p.skillKills-1
     );
   }
  );


  add(
   "최대 HP +20",
   "최대 체력 증가",
   ()=>{
    p.maxHp+=20;
    p.hp+=20;
   }
  );

 }


 /*
   항상 4개 선택지
 */

 const shuffled=
  arr.sort(
   ()=>Math.random()-.5
  );

 return shuffled.slice(0,4);

}


/* =========================
   게임 업데이트
========================= */

function update(dt){

 const p=player;

 if(!p)return;

 elapsed+=dt;


 p.invuln=
  Math.max(
   0,
   p.invuln-dt
  );

 p.formCooldown=
  Math.max(
   0,
   p.formCooldown-dt
  );

 p.skillCooldown=
  Math.max(
   0,
   p.skillCooldown-dt
  );

 p.gunSkillTimer=
  Math.max(
   0,
   p.gunSkillTimer-dt
  );


 /* 이동 */

 let mx=joy.x;
 let my=joy.y;


 if(
  keys["w"] ||
  keys["ArrowUp"]
 )
  my-=1;


 if(
  keys["s"] ||
  keys["ArrowDown"]
 )
  my+=1;


 if(
  keys["a"] ||
  keys["ArrowLeft"]
 )
  mx-=1;


 if(
  keys["d"] ||
  keys["ArrowRight"]
 )
  mx+=1;


 const len=
  Math.hypot(mx,my);


 if(len>1){

  mx/=len;
  my/=len;

 }


 if(len>.1){

  p.x+=
   mx*p.speed*dt;

  p.y+=
   my*p.speed*dt;

  p.face=
   Math.atan2(
    my,
    mx
   );

 }


 p.x=
  clamp(
   p.x,
   20,
   W-20
  );

 p.y=
  clamp(
   p.y,
   20,
   H-20
  );


 /* 공격 */

 if(p.cls==="gun"){

  const interval=
   1/p.attackSpeed;

  p._atk=
   (p._atk||0)-dt;

  if(p._atk<=0){

   shootGun();

   p._atk+=interval;

  }

 }


 else if(p.cls==="sword"){

  p._atk=
   (p._atk||0)-dt;

  if(p._atk<=0){

   swordSlash();

   p._atk+=
    1/p.swordSpeed;

  }


  p._wave=
   (p._wave||0)-dt;

  if(p._wave<=0){

   swordWave();

   p._wave+=
    1/p.swordWaveSpeed;

  }

 }


 else{

  p._atk=
   (p._atk||0)-dt;


  let rate=
   p.magicSpeed*
   (p.skillActive?1.8:1);


  if(p._atk<=0){

   magicBasic();

   p._atk+=
    1/rate;

  }


  if(p.skillActive){

   p.skillTimer-=dt;

   if(p.skillTimer<=0){

    p.skillActive=false;

   }

  }

 }


 /* 적 생성 */

 if(elapsed>=nextEnemy){

  nextEnemy=
   elapsed+
   (
    1.0-
    Math.min(
     .65,
     elapsed/500
    )
   );


  let amount=
   1+
   Math.floor(
    elapsed/45
   );


  for(
   let i=0;
   i<Math.min(5,amount);
   i++
  ){

   spawnEnemy(false);

  }

 }


 /* 보스 */

 if(elapsed>=nextBoss){

  nextBoss+=100;

  bossCount++;

  spawnEnemy(true);

 }


 /* 적 이동 */

 for(const e of enemies){

  const a=
   Math.atan2(
    p.y-e.y,
    p.x-e.x
   );


  e.x+=
   Math.cos(a)*
   e.speed*
   dt;


  e.y+=
   Math.sin(a)*
   e.speed*
   dt;


  if(
   dist(e,p)<
   e.r+p.r
  ){

   damagePlayer(
    e.dmg*dt*8
   );

  }

 }


 updateProjectiles(dt);
 updateSlashes(dt);
 updateLasers(dt);
 updateParticles(dt);

 updateUI();

}


/* =========================
   투사체 업데이트
========================= */

function updateProjectiles(dt){

 for(
  let i=projectiles.length-1;
  i>=0;
  i--
 ){

  const q=
   projectiles[i];


  q.x+=
   Math.cos(q.a)*
   q.speed*
   dt;


  q.y+=
   Math.sin(q.a)*
   q.speed*
   dt;


  q.travel+=
   q.speed*dt;


  let remove=
   q.travel>q.range ||
   q.x<-80 ||
   q.x>W+80 ||
   q.y<-80 ||
   q.y>H+80;


  if(!remove){

   for(
    const e of [...enemies]
   ){

    if(
     Math.hypot(
      q.x-e.x,
      q.y-e.y
     )<
     q.r+e.r
    ){

     hitEnemy(
      e,
      q.dmg
     );


     if(q.pen<=0){

      remove=true;

      break;

     }


     q.pen--;

    }

   }

  }


  if(remove){

   projectiles.splice(
    i,
    1
   );

  }

 }

}


/* =========================
   검 베기
========================= */

function updateSlashes(dt){

 for(
  let i=slashes.length-1;
  i>=0;
  i--
 ){

  const s=
   slashes[i];

  s.life-=dt;


  for(
   const e of enemies
  ){

   const dx=
    e.x-s.x;

   const dy=
    e.y-s.y;

   const d=
    Math.hypot(dx,dy);


   const a=
    Math.atan2(
     dy,
     dx
    );


   let da=
    Math.atan2(
     Math.sin(a-s.a),
     Math.cos(a-s.a)
    );


   if(
    d<s.range+e.r &&
    Math.abs(da)<s.fan/2
   ){

    if(
     !e._slashHit ||
     e._slashHit<s.life
    ){

     hitEnemy(
      e,
      s.dmg
     );

     e._slashHit=
      s.life;

    }

   }

  }


  if(s.life<=0){

   slashes.splice(
    i,
    1
   );

  }

 }

}


/* =========================
   레이저
========================= */

function updateLasers(dt){

 for(
  let i=lasers.length-1;
  i>=0;
  i--
 ){

  const l=
   lasers[i];

  l.life-=dt;


  for(
   const e of enemies
  ){

   let x=
    e.x-l.x;

   let y=
    e.y-l.y;


   let c=
    Math.cos(-l.a);

   let s=
    Math.sin(-l.a);


   let rx=
    x*c-y*s;

   let ry=
    x*s+y*c;


   if(
    Math.abs(
     ry-l.offset
    )<
    9*Math.max(
     1,
     player.area
    )+
    e.r
    &&
    Math.abs(rx)<
    Math.max(W,H)
   ){

    hitEnemy(
     e,
     l.dmg*dt*3
    );

   }

  }


  if(l.life<=0){

   lasers.splice(
    i,
    1
   );

  }

 }

}


/* =========================
   파티클
========================= */

function updateParticles(dt){

 for(
  let i=particles.length-1;
  i>=0;
  i--
 ){

  const q=
   particles[i];

  q.x+=
   q.vx*dt;

  q.y+=
   q.vy*dt;

  q.life-=dt;


  if(q.life<=0){

   particles.splice(
    i,
    1
   );

  }

 }

}


/* =========================
   그리기
========================= */

function draw(){

 ctx.clearRect(
  0,
  0,
  W,
  H
 );


 ctx.fillStyle=
  "#182018";

 ctx.fillRect(
  0,
  0,
  W,
  H
 );


 ctx.strokeStyle=
  "rgba(255,255,255,.035)";

 ctx.lineWidth=1;


 const grid=50;

 const off=
  -(elapsed*8%grid);


 for(
  let x=off;
  x<W;
  x+=grid
 ){

  ctx.beginPath();

  ctx.moveTo(
   x,
   0
  );

  ctx.lineTo(
   x,
   H
  );

  ctx.stroke();

 }


 for(
  let y=off;
  y<H;
  y+=grid
 ){

  ctx.beginPath();

  ctx.moveTo(
   0,
   y
  );

  ctx.lineTo(
   W,
   y
  );

  ctx.stroke();

 }


 for(
  const l of lasers
 )
  drawLaser(l);


 for(
  const s of slashes
 )
  drawSlash(s);


 for(
  const q of projectiles
 )
  drawProjectile(q);


 for(
  const e of enemies
 )
  drawEnemy(e);


 if(player)
  drawPlayer(player);


 for(
  const q of particles
 ){

  ctx.globalAlpha=
   Math.max(
    0,
    q.life/.35
   );

  ctx.fillStyle="#fff";

  ctx.beginPath();

  ctx.arc(
   q.x,
   q.y,
   3,
   0,
   TAU
  );

  ctx.fill();

  ctx.globalAlpha=1;

 }

}


/* =========================
   플레이어
========================= */

function drawPlayer(p){

 ctx.save();

 ctx.translate(
  p.x,
  p.y
 );


 if(p.cls==="gun"){

  ctx.fillStyle=
   p.gunForm==="pistol"
    ?" #e67e22"
    :"#9b59b6";

  ctx.beginPath();

  ctx.arc(
   0,
   0,
   p.r,
   0,
   TAU
  );

  ctx.fill();

 }


 else if(p.cls==="sword"){

  ctx.fillStyle=
   "#3498db";

  ctx.beginPath();

  ctx.arc(
   0,
   0,
   p.r,
   0,
   TAU
  );

  ctx.fill();


  if(p.shield>0){

   ctx.strokeStyle=
    "#5dade2";

   ctx.lineWidth=5;

   ctx.beginPath();

   ctx.arc(
    0,
    0,
    p.r+7,
    0,
    TAU
   );

   ctx.stroke();

  }

 }


 else{

  ctx.fillStyle=
   "#8e44ad";

  ctx.beginPath();

  ctx.arc(
   0,
   0,
   p.r,
   0,
   TAU
  );

  ctx.fill();

 }


 ctx.rotate(
  p.face
 );

 ctx.fillStyle="#eee";

 ctx.fillRect(
  8,
  -4,
  20,
  8
 );


 ctx.restore();

}


/* =========================
   적
========================= */

function drawEnemy(e){

 ctx.fillStyle=
  e.boss
   ?" #c0392b"
   :"#75a85b";

 ctx.beginPath();

 ctx.arc(
  e.x,
  e.y,
  e.r,
  0,
  TAU
 );

 ctx.fill();


 ctx.fillStyle="#222";

 ctx.beginPath();

 ctx.arc(
  e.x-4,
  e.y-2,
  2,
  0,
  TAU
 );

 ctx.arc(
  e.x+4,
  e.y-2,
  2,
  0,
  TAU
 );

 ctx.fill();


 ctx.fillStyle="#333";

 ctx.fillRect(
  e.x-e.r,
  e.y-e.r-7,
  e.r*2,
  4
 );


 ctx.fillStyle=
  "#e74c3c";

 ctx.fillRect(
  e.x-e.r,
  e.y-e.r-7,
  e.r*2*
  Math.max(
   0,
   e.hp/e.maxHp
  ),
  4
 );


 if(e.boss){

  ctx.strokeStyle=
   "#f1c40f";

  ctx.lineWidth=2;

  ctx.stroke();

 }

}


/* =========================
   투사체 그리기
========================= */

function drawProjectile(q){

 ctx.fillStyle=
  q.type==="wave"
   ?" #5dade2"
   :q.type==="magic"
    ?" #bb6bd9"
    :"#f5c542";

 ctx.beginPath();

 ctx.arc(
  q.x,
  q.y,
  q.r,
  0,
  TAU
 );

 ctx.fill();

}


/* =========================
   베기 그리기
========================= */

function drawSlash(s){

 ctx.save();

 ctx.translate(
  s.x,
  s.y
 );

 ctx.rotate(
  s.a
 );

 ctx.globalAlpha=
  s.life/s.max;

 ctx.fillStyle=
  "#5dade2";


 ctx.beginPath();

 ctx.moveTo(
  0,
  0
 );

 ctx.arc(
  0,
  0,
  s.range,
  -s.fan/2,
  s.fan/2
 );

 ctx.closePath();

 ctx.fill();


 ctx.globalAlpha=1;

 ctx.restore();

}


/* =========================
   레이저 그리기
========================= */

function drawLaser(l){

 ctx.save();

 ctx.translate(
  l.x,
  l.y
 );

 ctx.rotate(
  l.a
 );

 ctx.globalAlpha=
  .8*
  (l.life/l.max);

 ctx.fillStyle=
  "#e8b4ff";


 const width=
  9*player.area;


 ctx.fillRect(
  -Math.max(W,H),
  l.offset-width,
  Math.max(W,H)*2,
  width*2
 );


 ctx.globalAlpha=1;

 ctx.restore();

}


/* =========================
   UI
========================= */

function updateUI(){

 if(!player)return;


 document
  .getElementById("hpFill")
  .style
  .width=
  (
   100*
   player.hp/
   player.maxHp
  )+"%";


 document
  .getElementById("shieldBar")
  .style
  .display=
  player.cls==="sword"
   ?"block"
   :"none";


 document
  .getElementById("shieldFill")
  .style
  .width=
  (
   player.maxShield
    ?100*
     player.shield/
     player.maxShield
    :0
  )+"%";


 document
  .getElementById("xpFill")
  .style
  .width=
  (
   100*xp/xpNeed
  )+"%";


 document
  .getElementById("stats")
  .textContent=
  `Lv.${level} | ${fmtTime(elapsed)} | 처치 ${kills}`;


 let extra="";


 if(player.cls==="gun"){

  extra=
   `${
    player.gunForm==="pistol"
     ?"권총"
     :"저격"
   } | 투사체 ${
    player.projectiles
   } | 관통 ${
    player.penetration
   }`;

 }


 if(player.cls==="sword"){

  extra=
   `베기 + 검기 ${
    player.swordWaveCount
   }개 | 방어막 ${
    Math.ceil(
     player.shield
    )
   }`;

 }


 if(player.cls==="magic"){

  extra=
   `레이저 ${
    player.laserCount
   }개 | 강화공격 ${
    player.enhancedCounter
   }/${
    player.enhancedEvery
   } | 각성 ${
    player.skillKillProgress
   }/${
    player.skillKills
   }`;

 }


 document
  .getElementById("classInfo")
  .textContent=
  classNames[player.cls]+
  " · "+
  extra;


 document
  .getElementById("skillBtn")
  .textContent=
  player.cls==="magic"

   ?(
     player.skillActive
      ?"각성 중!"
      :`각성 (${
        player.skillKillProgress
       }/${
        player.skillKills
       })`
    )

   :(
     player.skillCooldown>0
      ?`스킬 ${
        player.skillCooldown.toFixed(1)
       }s`
      :"스킬"
    );


 document
  .getElementById("formBtn")
  .textContent=
  player.cls==="gun"
   ?`🔄 ${
      player.gunForm==="pistol"
       ?"권총"
       :"저격"
     }`
   :"폼체인지";

}


function fmtTime(t){

 let m=
  Math.floor(
   t/60
  );

 let s=
  Math.floor(
   t%60
  );

 return `${
  m
 }:${String(s).padStart(2,"0")}`;

}


function gameOver(){

 state="gameover";

 document
  .getElementById("result")
  .textContent=
  `레벨 ${level} · ${
   fmtTime(elapsed)
  } 생존 · ${
   kills
  }마리 처치`;


 document
  .getElementById("gameover")
  .classList
  .remove("hidden");

}


/* =========================
   메인 루프
========================= */

function loop(t){

 if(!last)
  last=t;


 let dt=
  Math.min(
   .033,
   (t-last)/1000
  );


 last=t;


 if(state==="playing")
  update(dt);


 draw();


 requestAnimationFrame(loop);

}


requestAnimationFrame(loop);


/* =========================
   키보드
========================= */

addEventListener(
 "keydown",
 e=>{

  keys[e.key]=true;


  if(e.key===" "){

   e.preventDefault();

   useSkill();

  }


  if(
   e.key.toLowerCase()==="q"
  ){

   formChange();

  }

 }
);


addEventListener(
 "keyup",
 e=>{
  keys[e.key]=false;
 }
);


/* =========================
   버튼
========================= */

document
 .getElementById("skillBtn")
 .addEventListener(
  "pointerdown",
  e=>{
   e.preventDefault();
   useSkill();
  }
 );


document
 .getElementById("formBtn")
 .addEventListener(
  "pointerdown",
  e=>{
   e.preventDefault();
   formChange();
  }
 );


/* =========================
   모바일 조이스틱
========================= */

const joyEl=
 document.getElementById(
  "joystick"
 );

const stick=
 document.getElementById(
  "stick"
 );


function joyMove(e){

 const r=
  joyEl.getBoundingClientRect();


 const cx=
  r.left+
  r.width/2;


 const cy=
  r.top+
  r.height/2;


 let dx=
  e.clientX-cx;


 let dy=
  e.clientY-cy;


 let d=
  Math.hypot(
   dx,
   dy
  );


 /*
   실제 조이스틱 크기에 맞춰
   최대 이동거리 계산
 */

 let max=
  r.width*.47;


 if(d>max){

  dx=
   dx/d*max;

  dy=
   dy/d*max;

 }


 joy.x=
  dx/max;

 joy.y=
  dy/max;


 stick.style.transform=
  `translate(${
   dx
  }px,${
   dy
  }px)`;

}


joyEl.addEventListener(
 "pointerdown",
 e=>{

  joyEl.setPointerCapture(
   e.pointerId
  );

  joyMove(e);

 }
);


joyEl.addEventListener(
 "pointermove",
 e=>{

  if(e.buttons)
   joyMove(e);

 }
);


joyEl.addEventListener(
 "pointerup",
 ()=>{

  joy.x=0;
  joy.y=0;

  stick.style.transform=
   "translate(0,0)";

 }
);


joyEl.addEventListener(
 "pointercancel",
 ()=>{

  joy.x=0;
  joy.y=0;

  stick.style.transform=
   "translate(0,0)";

 }
);

</script>

</body>
</html>
'''

components.html(
    html,
    height=650,
    scrolling=False
)
