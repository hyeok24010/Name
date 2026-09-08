import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Nururung Survivor",
    page_icon="🔮",
    layout="centered"
)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    background: #101018;
    overflow: hidden;
    touch-action: none;
    user-select: none;
    font-family: Arial, sans-serif;
}

#weaponSelect {
    color: white;
    text-align: center;
    padding: 20px 10px;
}

#weaponSelect h1 {
    font-size: 27px;
}

.weaponButton {
    display: block;
    width: 94%;
    max-width: 500px;
    margin: 12px auto;
    padding: 16px;
    border-radius: 13px;
    border: 1px solid #555;
    background: #252536;
    color: white;
    font-size: 19px;
    font-weight: bold;
}

.weaponButton:active {
    background: #4a4a65;
}

.weaponDescription {
    display: block;
    margin-top: 5px;
    color: #aaa;
    font-size: 12px;
    font-weight: normal;
}

#gameArea {
    display: none;
}

#info {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 5px;
    padding: 6px;
    color: white;
    font-size: 13px;
}

canvas {
    display: block;
    width: 100%;
    max-width: 850px;
    height: auto;
    margin: auto;
    background: #151522;
    border: 2px solid #444;
    border-radius: 10px;
    touch-action: none;
}

#controls {
    position: relative;
    width: 100%;
    height: 120px;
}

#joystick {
    position: absolute;
    left: 12px;
    bottom: 7px;
    width: 105px;
    height: 105px;
    border-radius: 50%;
    background: rgba(130,130,150,0.30);
    border: 2px solid rgba(255,255,255,0.22);
}

#stick {
    position: absolute;
    left: 27px;
    top: 27px;
    width: 51px;
    height: 51px;
    border-radius: 50%;
    background: rgba(220,220,220,0.75);
}

#skillButton {
    position: absolute;
    right: 18px;
    bottom: 12px;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    border: 3px solid #9d6cff;
    background: #402575;
    color: white;
    font-size: 25px;
    font-weight: bold;
}

#skillButton.ready {
    background: #9b5cff;
    box-shadow: 0 0 20px #9b5cff;
}

#levelUp,
#gameOver {
    position: fixed;
    z-index: 100;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 560px;
    padding: 20px;
    border-radius: 15px;
    background: rgba(12,12,20,0.98);
    border: 2px solid #555;
    color: white;
    text-align: center;
}

#levelUp {
    display: none;
}

.upgrade {
    display: block;
    width: 100%;
    padding: 14px;
    margin: 9px 0;
    border-radius: 9px;
    border: 1px solid #555;
    background: #28283a;
    color: white;
    text-align: left;
    font-size: 14px;
}

.upgrade:active {
    background: #4a4a62;
}

#gameOver {
    display: none;
    font-size: 28px;
}

#gameOver button {
    margin-top: 20px;
    padding: 12px 25px;
    border: 0;
    border-radius: 8px;
    background: #4d7cff;
    color: white;
    font-size: 16px;
}
</style>
</head>

<body>

<div id="weaponSelect">

<h1>🔮 NURURUNG SURVIVOR</h1>

<p>무기를 선택하세요.</p>

<button class="weaponButton" onclick="startGame('gun')">
🔫 총
<span class="weaponDescription">
빠른 연사와 여러 발의 탄환
</span>
</button>

<button class="weaponButton" onclick="startGame('sword')">
⚔️ 검
<span class="weaponDescription">
바라보는 방향 부채꼴 공격 · 높은 방어력 · 방어막
</span>
</button>

<button class="weaponButton" onclick="startGame('magic')">
🔮 마법
<span class="weaponDescription">
10회마다 강화 레이저 · 처치로 충전되는 각성
</span>
</button>

</div>


<div id="gameArea">

<div id="info">
<span>LV <b id="level">1</b></span>
<span>❤️ <b id="hp">100/100</b></span>
<span>🔵 <b id="shield">0</b></span>
<span>XP <b id="xp">0/10</b></span>
<span>☠️ <b id="kills">0</b></span>
<span>⏱️ <b id="time">0</b></span>
</div>

<canvas id="game" width="850" height="600"></canvas>

<div id="controls">

<div id="joystick">
<div id="stick"></div>
</div>

<button id="skillButton">⚡</button>

</div>

</div>


<div id="levelUp">

<h2>LEVEL UP!</h2>
<p>하나를 선택하세요.</p>

<div id="upgradeList"></div>

</div>


<div id="gameOver">

GAME OVER

<br>

<button onclick="returnToSelect()">
다시 시작
</button>

</div>


<script>

const canvas =
document.getElementById("game");

const ctx =
canvas.getContext("2d");

let weapon = "gun";

let gameRunning = false;

let level = 1;

let xp = 0;

let xpNeed = 10;

let kills = 0;

let gameTime = 0;

let spawnTimer = 0;

let attackTimer = 0;

let nextBossTime = 100;

let lastTime = performance.now();

let enemies = [];

let projectiles = [];

let gems = [];

let effects = [];


/* ==========================================
   플레이어
========================================== */

const player = {

x: 425,
y: 300,

radius: 17,

hp: 100,
maxHp: 100,

shield: 0,

speed: 3.4,

damage: 17,

attackSpeed: 720,

range: 300,

area: 1,

projectileSpeed: 7,

projectileCount: 1,

damageReduction: 0,

xpMultiplier: 1,

/*
   스킬 처치 게이지
*/
skillCharge: 0,

skillNeed: 12,

/*
   각성 상태
*/
skillActive: false,

skillTimer: 0,

skillDuration: 7000,

maxSkillDuration: 10000,

/*
   강화 공격
   기본값 10회마다
*/
magicAttackCount: 0,

enhancedAttackNeed: 10,

/*
   강화 공격 최소 5회
*/
minEnhancedAttackNeed: 5,

/*
   레이저
*/
laserDuration: 900,

maxLaserDuration: 2000,

laserDamage: 55,

facingX: 1,
facingY: 0

};


/* ==========================================
   시작
========================================== */

function startGame(type) {

weapon = type;

document.getElementById(
"weaponSelect"
).style.display = "none";

document.getElementById(
"gameArea"
).style.display = "block";

resetGame();

gameRunning = true;

}


/* ==========================================
   초기화
========================================== */

function resetGame() {

level = 1;

xp = 0;

xpNeed = 10;

kills = 0;

gameTime = 0;

spawnTimer = 0;

attackTimer = 0;

nextBossTime = 100;

enemies = [];

projectiles = [];

gems = [];

effects = [];


player.x = 425;
player.y = 300;

player.shield = 0;

player.skillCharge = 0;

player.skillActive = false;

player.magicAttackCount = 0;

player.projectileCount = 1;

player.area = 1;

player.damageReduction = 0;

player.xpMultiplier = 1;

player.enhancedAttackNeed = 10;

player.laserDuration = 900;

player.skillDuration = 7000;


if (weapon === "gun") {

player.maxHp = 90;
player.hp = 90;

player.speed = 3.8;

player.damage = 20;

player.attackSpeed = 1200;

player.range = 330;

player.skillNeed = 12;

}


if (weapon === "sword") {

player.maxHp = 140;
player.hp = 140;

player.speed = 3.1;

player.damage = 24;

player.attackSpeed = 720;

player.range = 220;

player.damageReduction = 0.2;

player.skillNeed = 10;

}


if (weapon === "magic") {

player.maxHp = 100;
player.hp = 100;

player.speed = 3.3;

player.damage = 17;

player.attackSpeed = 720;

player.range = 300;

player.area = 1.2;

player.projectileSpeed = 7;

player.skillNeed = 12;

}

}


/* ==========================================
   키보드
========================================== */

const keys = {};

document.addEventListener(
"keydown",
function(e) {

keys[e.key.toLowerCase()] = true;

});

document.addEventListener(
"keyup",
function(e) {

keys[e.key.toLowerCase()] = false;

});


/* ==========================================
   모바일 조이스틱
========================================== */

const joystick =
document.getElementById("joystick");

const stick =
document.getElementById("stick");

let joystickActive = false;

let joyX = 0;

let joyY = 0;

const joystickRadius = 42;


function updateJoystick(x,y) {

const rect =
joystick.getBoundingClientRect();

const centerX =
rect.left + rect.width / 2;

const centerY =
rect.top + rect.height / 2;

let dx = x - centerX;

let dy = y - centerY;

const distance =
Math.sqrt(dx*dx + dy*dy);

if (
distance > joystickRadius
) {

dx =
dx / distance *
joystickRadius;

dy =
dy / distance *
joystickRadius;

}

joyX =
dx / joystickRadius;

joyY =
dy / joystickRadius;

stick.style.left =
(27 + dx) + "px";

stick.style.top =
(27 + dy) + "px";


if (
Math.abs(joyX) +
Math.abs(joyY) > 0.15
) {

player.facingX = joyX;

player.facingY = joyY;

}

}


function resetJoystick() {

joystickActive = false;

joyX = 0;

joyY = 0;

stick.style.left = "27px";

stick.style.top = "27px";

}


joystick.addEventListener(
"touchstart",
function(e) {

e.preventDefault();

joystickActive = true;

const t = e.touches[0];

updateJoystick(
t.clientX,
t.clientY
);

},
{passive:false}
);


joystick.addEventListener(
"touchmove",
function(e) {

e.preventDefault();

if (!joystickActive) return;

const t = e.touches[0];

updateJoystick(
t.clientX,
t.clientY
);

},
{passive:false}
);


joystick.addEventListener(
"touchend",
function(e) {

e.preventDefault();

resetJoystick();

},
{passive:false}
);


/* ==========================================
   이동
========================================== */

function movePlayer() {

let dx = 0;
let dy = 0;


if (
keys["w"] ||
keys["arrowup"]
) dy -= 1;

if (
keys["s"] ||
keys["arrowdown"]
) dy += 1;

if (
keys["a"] ||
keys["arrowleft"]
) dx -= 1;

if (
keys["d"] ||
keys["arrowright"]
) dx += 1;


if (joystickActive) {

dx += joyX;
dy += joyY;

}


const len =
Math.sqrt(dx*dx + dy*dy);


if (len > 0) {

dx /= len;
dy /= len;

player.facingX = dx;
player.facingY = dy;

player.x +=
dx * player.speed;

player.y +=
dy * player.speed;

}


player.x =
Math.max(
player.radius,
Math.min(
canvas.width-player.radius,
player.x
)
);

player.y =
Math.max(
player.radius,
Math.min(
canvas.height-player.radius,
player.y
)
);

}


/* ==========================================
   가까운 적
========================================== */

function nearestEnemy() {

let target = null;

let best =
player.range * player.range;


for (
const enemy of enemies
) {

const dx =
enemy.x-player.x;

const dy =
enemy.y-player.y;

const d =
dx*dx + dy*dy;


if (
d < best
) {

best = d;

target = enemy;

}

}


return target;

}


/* ==========================================
   총 공격
========================================== */

function gunAttack() {

const target =
nearestEnemy();

if (!target) return;


const angle =
Math.atan2(
target.y-player.y,
target.x-player.x
);


for (
let i=0;
i<player.projectileCount;
i++
) {

let a = angle;


if (
player.projectileCount > 1
) {

a +=
(
i -
(player.projectileCount-1)/2
) * 0.10;

}


projectiles.push({

x: player.x,
y: player.y,

dx:
Math.cos(a) *
player.projectileSpeed,

dy:
Math.sin(a) *
player.projectileSpeed,

damage:
player.damage,

radius: 5,

type:"bullet"

});

}

}


/* ==========================================
   검
========================================== */

function swordAttack() {

const angle =
Math.atan2(
player.facingY,
player.facingX
);

const range =
player.range *
player.area;

const fan =
Math.PI * 0.56;


effects.push({

type:"swordFan",

x:player.x,
y:player.y,

angle:angle,

range:range,

fan:fan,

life:120

});


for (
const enemy of enemies
) {

const dx =
enemy.x-player.x;

const dy =
enemy.y-player.y;

const distance =
Math.sqrt(dx*dx+dy*dy);


if (
distance >
range+enemy.radius
) continue;


const enemyAngle =
Math.atan2(dy,dx);

let diff =
enemyAngle-angle;


while(diff > Math.PI)
diff -= Math.PI*2;

while(diff < -Math.PI)
diff += Math.PI*2;


if (
Math.abs(diff) <= fan/2
) {

dealDamage(
enemy,
player.damage
);

}

}

}


/* ==========================================
   🔮 법사 기본 공격
========================================== */

function magicAttack() {

const target =
nearestEnemy();

if (!target) return;


/*
   기본 공격 횟수 +1
*/

player.magicAttackCount++;


/*
   현재 공격이
   강화 공격인지 결정

   중요:
   각성 중에는 모든 평타가 강화공격
*/

let enhanced = false;


if (
player.skillActive
) {

enhanced = true;

}
else if (
player.magicAttackCount >=
player.enhancedAttackNeed
) {

enhanced = true;

player.magicAttackCount = 0;

}


/*
   각성 중:
   공속和 공격力 강화
*/

let damage =
player.damage;

if (
player.skillActive
) {

damage *= 1.45;

}


/*
   기본 마법탄
*/

const angle =
Math.atan2(
target.y-player.y,
target.x-player.x
);


for (
let i=0;
i<player.projectileCount;
i++
) {

let a = angle;

if (
player.projectileCount > 1
) {

a +=
(
i -
(player.projectileCount-1)/2
) * 0.12;

}


projectiles.push({

x:player.x,
y:player.y,

dx:
Math.cos(a) *
player.projectileSpeed,

dy:
Math.sin(a) *
player.projectileSpeed,

damage:damage,

radius:
8*player.area,

type:"magic"

});

}


/*
   강화 공격
*/

if (enhanced) {

enhancedMagicAttack();

}

}


/* ==========================================
   🔥 강화 공격
========================================== */

function enhancedMagicAttack() {

/*
   일반 상태에서는
   가로 OR 세로 중 하나
*/

if (!player.skillActive) {

if (
Math.random() < 0.5
) {

createVerticalLaser();

}
else {

createHorizontalLaser();

}

return;

}


/*
   ⭐ 각성 상태에서는
   가로 + 세로 둘 다
*/

createVerticalLaser();

createHorizontalLaser();

}


/* ==========================================
   세로 레이저
========================================== */

function createVerticalLaser() {

const target =
nearestEnemy();

if (!target) return;


effects.push({

type:"laserVertical",

x:target.x,

life:player.laserDuration,

maxLife:player.laserDuration,

width:
25*player.area,

damage:
player.laserDamage

});

}


/* ==========================================
   가로 레이저
========================================== */

function createHorizontalLaser() {

const target =
nearestEnemy();

if (!target) return;


effects.push({

type:"laserHorizontal",

y:target.y,

life:player.laserDuration,

maxLife:player.laserDuration,

height:
25*player.area,

damage:
player.laserDamage

});

}


/* ==========================================
   투사체
========================================== */

function updateProjectiles() {

for (
const p of projectiles
) {

p.x += p.dx;
p.y += p.dy;


for (
const enemy of enemies
) {

if (
enemy.hp <= 0
) continue;


const dx =
enemy.x-p.x;

const dy =
enemy.y-p.y;

const d =
Math.sqrt(dx*dx+dy*dy);


if (
d <
enemy.radius+p.radius
) {

dealDamage(
enemy,
p.damage
);

p.dead = true;

break;

}

}

}


projectiles =
projectiles.filter(
p =>
!p.dead &&
p.x > -100 &&
p.x < canvas.width+100 &&
p.y > -100 &&
p.y < canvas.height+100
);

}


/* ==========================================
   레이저 피해
========================================== */

function updateLasers(delta) {

for (
const effect of effects
) {

if (
effect.type !== "laserVertical" &&
effect.type !== "laserHorizontal"
) continue;


for (
const enemy of enemies
) {

if (
enemy.hp <= 0
) continue;


let hit = false;


if (
effect.type === "laserVertical"
) {

if (
Math.abs(enemy.x-effect.x)
<
effect.width/2+
enemy.radius
) {

hit = true;

}

}


if (
effect.type === "laserHorizontal"
) {

if (
Math.abs(enemy.y-effect.y)
<
effect.height/2+
enemy.radius
) {

hit = true;

}

}


if (hit) {

dealDamage(
enemy,
effect.damage *
(delta/1000)
);

}

}

}

}


/* ==========================================
   공격
========================================== */

function attack() {

if (
weapon === "gun"
) {

gunAttack();

}

else if (
weapon === "sword"
) {

swordAttack();

}

else {

magicAttack();

}

}


/* ==========================================
   피해
========================================== */

function dealDamage(enemy,damage) {

if (enemy.boss) {

damage *=
1-enemy.armor;

}

enemy.hp -= damage;

}


/* ==========================================
   ⭐ 스킬 사용
========================================== */

function useSkill() {

if (
player.skillActive
) return;


if (
player.skillCharge <
player.skillNeed
) return;


/*
   스킬 게이지 소비
*/

player.skillCharge = 0;


/*
   총
*/

if (
weapon === "gun"
) {

player.skillActive = true;

player.skillTimer = 5000;

}


/*
   검
*/

else if (
weapon === "sword"
) {

player.shield +=
65+level*20;

player.skillActive = true;

player.skillTimer = 6000;

}


/*
   🔮 법사 각성
*/

else {

player.skillActive = true;

player.skillTimer =
player.skillDuration;

player.magicAttackCount = 0;

effects.push({

type:"awakening",

life:player.skillDuration

});

}

}


/* ==========================================
   스킬 업데이트
========================================== */

function updateSkill(delta) {

if (!player.skillActive)
return;


player.skillTimer -= delta;


if (
player.skillTimer <= 0
) {

player.skillTimer = 0;

player.skillActive = false;

}

}


/* ==========================================
   적 생성
========================================== */

function spawnEnemy() {

const side =
Math.floor(
Math.random()*4
);

let x,y;


if(side===0) {

x=Math.random()*canvas.width;
y=-30;

}
else if(side===1) {

x=canvas.width+30;
y=Math.random()*canvas.height;

}
else if(side===2) {

x=Math.random()*canvas.width;
y=canvas.height+30;

}
else {

x=-30;
y=Math.random()*canvas.height;

}


const scale =
1+gameTime*0.012;


const hp =
(22+level*4)*scale;


enemies.push({

x:x,
y:y,

radius:15,

hp:hp,
maxHp:hp,

speed:
(0.65+Math.random()*0.3) *
(1+gameTime*0.0015),

damage:
(5+level*0.25) *
(1+gameTime*0.006),

cooldown:0,

boss:false,

armor:0

});

}


/* ==========================================
   보스
========================================== */

function spawnBoss() {

const side =
Math.floor(
Math.random()*4
);

let x,y;


if(side===0) {

x=Math.random()*canvas.width;
y=-70;

}
else if(side===1) {

x=canvas.width+70;
y=Math.random()*canvas.height;

}
else if(side===2) {

x=Math.random()*canvas.width;
y=canvas.height+70;

}
else {

x=-70;
y=Math.random()*canvas.height;

}


const scale =
1+gameTime*0.015;


const hp =
(600+level*120)*scale;


const armor =
Math.min(
0.75,
0.15+
level*0.012+
gameTime*0.0003
);


enemies.push({

x:x,
y:y,

radius:34,

hp:hp,
maxHp:hp,

speed:
0.43+gameTime*0.001,

damage:
(15+level*0.7)*scale,

cooldown:0,

boss:true,

armor:armor

});

}


/* ==========================================
   적 이동
========================================== */

function updateEnemies(delta) {

for (
const enemy of enemies
) {

const dx =
player.x-enemy.x;

const dy =
player.y-enemy.y;

const d =
Math.sqrt(dx*dx+dy*dy);


if (
d >
player.radius+enemy.radius
) {

enemy.x +=
dx/d*enemy.speed;

enemy.y +=
dy/d*enemy.speed;

}
else {

enemy.cooldown -= delta;


if (
enemy.cooldown <= 0
) {

damagePlayer(
enemy.damage
);

enemy.cooldown = 700;

}

}

}

}


/* ==========================================
   플레이어 피해
========================================== */

function damagePlayer(amount) {

let damage =
amount*
(1-player.damageReduction);


/*
   방어막 먼저
*/

if (
player.shield > 0
) {

const blocked =
Math.min(
player.shield,
damage
);

player.shield -= blocked;

damage -= blocked;

}


if(damage>0) {

player.hp -= damage;

}


if (
player.hp <= 0
) {

player.hp = 0;

gameOver();

}

}


/* ==========================================
   적 사망
========================================== */

function processDeaths() {

const alive = [];


for (
const enemy of enemies
) {

if (
enemy.hp <= 0
) {

kills++;


/*
   ⭐ 핵심
   각성 중에는 스킬 게이지 증가 X
*/

if (
!player.skillActive
) {

player.skillCharge++;

}


gems.push({

x:enemy.x,

y:enemy.y,

value:
enemy.boss ? 20 : 1

});

}
else {

alive.push(enemy);

}

}


enemies = alive;

}


/* ==========================================
   경험치
========================================== */

function collectXP() {

for (
let i=gems.length-1;
i>=0;
i--
) {

const gem =
gems[i];

const dx =
player.x-gem.x;

const dy =
player.y-gem.y;

const d =
Math.sqrt(dx*dx+dy*dy);


if (
d <
70*player.area
) {

xp +=
gem.value*
player.xpMultiplier;

gems.splice(i,1);

}

}


if (
xp >= xpNeed
) {

xp -= xpNeed;

level++;

xpNeed =
Math.floor(
xpNeed*1.16+3
);

showLevelUp();

}

}


/* ==========================================
   총 업그레이드
========================================== */

function gunUpgrades() {

return [

{
text:"🔫 공격력 +8%",
effect:() =>
player.damage*=1.08
},

{
text:"⚡ 공격속도 +7%",
effect:() =>
player.attackSpeed*=0.93
},

{
text:"🔫 발사체 +1",
effect:() =>
player.projectileCount++
},

{
text:"🎯 사거리 +10%",
effect:() =>
player.range*=1.10
},

{
text:"💨 탄속 +10%",
effect:() =>
player.projectileSpeed*=1.10
},

{
text:"❤️ 최대 체력 +10",
effect:() => {

player.maxHp+=10;
player.hp+=10;

}
}

];

}


/* ==========================================
   검 업그레이드
========================================== */

function swordUpgrades() {

return [

{
text:"⚔️ 공격력 +8%",
effect:() =>
player.damage*=1.08
},

{
text:"🛡️ 피해 감소 +4%",
effect:() => {

player.damageReduction =
Math.min(
0.65,
player.damageReduction+0.04
);

}
},

{
text:"❤️ 최대 체력 +15",
effect:() => {

player.maxHp+=15;
player.hp+=15;

}
},

{
text:"⚔️ 공격 범위 +10%",
effect:() =>
player.range*=1.10
},

{
text:"💥 부채꼴 범위 +8%",
effect:() =>
player.area*=1.08
},

{
text:"🏃 이동속도 +7%",
effect:() =>
player.speed*=1.07
},

{
text:"🔵 스킬 필요 처치 -1",
effect:() => {

player.skillNeed =
Math.max(
6,
player.skillNeed-1
);

}
}

];

}


/* ==========================================
   🔮 마법 업그레이드
========================================== */

function magicUpgrades() {

return [

{
text:"🔮 마법 공격력 +8%",
effect:() =>
player.damage*=1.08
},

{
text:"⚡ 기본 공격속도 +7%",
effect:() =>
player.attackSpeed*=0.93
},

{
text:"🔮 발사체 +1",
effect:() =>
player.projectileCount++
},

{
text:"💥 마법 범위 +10%",
effect:() =>
player.area*=1.10
},

/*
   ⭐ 강화 공격 주기
   10 → 9 → 8 ...
   최소 5
*/

{
text:
"✨ 강화 공격 필요 횟수 -1",
effect:() => {

player.enhancedAttackNeed =
Math.max(
player.minEnhancedAttackNeed,
player.enhancedAttackNeed-1
);

}
},

/*
   ⭐ 각성 지속시간
   최대 10초
*/

{
text:
"🌟 각성 지속시간 +0.5초",
effect:() => {

player.skillDuration =
Math.min(
player.maxSkillDuration,
player.skillDuration+500
);

}
},

/*
   ⭐ 스킬 필요 처치
   최대 절반까지만 감소
*/

{
text:
"⚡ 스킬 필요 처치 -1",
effect:() => {

const originalNeed = 12;

const minimum =
Math.ceil(
originalNeed/2
);

player.skillNeed =
Math.max(
minimum,
player.skillNeed-1
);

}
},

/*
   레이저 지속시간
*/

{
text:
"⚡ 레이저 지속시간 +0.2초",
effect:() => {

player.laserDuration =
Math.min(
player.maxLaserDuration,
player.laserDuration+200
);

}
},

{
text:
"💥 레이저 공격력 +12%",
effect:() =>
player.laserDamage*=1.12
},

{
text:
"❤️ 최대 체력 +10",
effect:() => {

player.maxHp+=10;
player.hp+=10;

}
}

];

}


/* ==========================================
   레벨업
========================================== */

function showLevelUp() {

gameRunning = false;


let upgrades;


if (
weapon==="gun"
) {

upgrades =
gunUpgrades();

}
else if (
weapon==="sword"
) {

upgrades =
swordUpgrades();

}
else {

upgrades =
magicUpgrades();

}


upgrades.sort(
() =>
Math.random()-0.5
);


const list =
document.getElementById(
"upgradeList"
);

list.innerHTML = "";


upgrades
.slice(0,3)
.forEach(
function(upgrade) {

const button =
document.createElement(
"button"
);

button.className =
"upgrade";

button.textContent =
upgrade.text;

button.onclick =
function() {

upgrade.effect();

document.getElementById(
"levelUp"
).style.display =
"none";

gameRunning = true;

};

list.appendChild(button);

}
);


document.getElementById(
"levelUp"
).style.display =
"block";

}


/* ==========================================
   적 스폰
========================================== */

function updateSpawning(delta) {

spawnTimer -= delta;


const interval =
Math.max(
900-gameTime*9,
170
);


if (
spawnTimer<=0
) {

const amount =
Math.min(
1+
Math.floor(gameTime/18),
12
);


for (
let i=0;
i<amount;
i++
) {

spawnEnemy();

}


spawnTimer =
interval;

}

}


/* ==========================================
   시간
========================================== */

function updateTime(delta) {

gameTime +=
delta/1000;


if (
gameTime>=nextBossTime
) {

spawnBoss();

nextBossTime+=100;

}


document.getElementById(
"time"
).textContent =
Math.floor(gameTime);

}


/* ==========================================
   효과
========================================== */

function updateEffects(delta) {

for (
const effect of effects
) {

effect.life-=delta;

}


updateLasers(delta);


effects =
effects.filter(
e=>e.life>0
);

}


/* ==========================================
   그리기
========================================== */

function draw() {

ctx.clearRect(
0,
0,
canvas.width,
canvas.height
);


ctx.fillStyle="#151522";

ctx.fillRect(
0,
0,
canvas.width,
canvas.height
);


/*
   배경
*/

ctx.strokeStyle =
"rgba(255,255,255,0.035)";


for (
let x=0;
x<canvas.width;
x+=40
) {

ctx.beginPath();

ctx.moveTo(x,0);

ctx.lineTo(x,canvas.height);

ctx.stroke();

}


for (
let y=0;
y<canvas.height;
y+=40
) {

ctx.beginPath();

ctx.moveTo(0,y);

ctx.lineTo(canvas.width,y);

ctx.stroke();

}


/*
   경험치
*/

for (
const gem of gems
) {

ctx.beginPath();

ctx.arc(
gem.x,
gem.y,
gem.value>5?8:5,
0,
Math.PI*2
);

ctx.fillStyle =
gem.value>5
?"#ffd166"
:"#55dfff";

ctx.fill();

}


/*
   레이저
*/

for (
const effect of effects
) {

if (
effect.type==="laserVertical"
) {

const alpha =
Math.max(
0.18,
effect.life/effect.maxLife
);

ctx.fillStyle =
"rgba(185,80,255,"+
alpha+
")";

ctx.fillRect(
effect.x-effect.width/2,
0,
effect.width,
canvas.height
);

ctx.strokeStyle="white";

ctx.lineWidth=3;

ctx.beginPath();

ctx.moveTo(
effect.x,
0
);

ctx.lineTo(
effect.x,
canvas.height
);

ctx.stroke();

}


if (
effect.type==="laserHorizontal"
) {

const alpha =
Math.max(
0.18,
effect.life/effect.maxLife
);

ctx.fillStyle =
"rgba(185,80,255,"+
alpha+
")";

ctx.fillRect(
0,
effect.y-effect.height/2,
canvas.width,
effect.height
);

ctx.strokeStyle="white";

ctx.lineWidth=3;

ctx.beginPath();

ctx.moveTo(
0,
effect.y
);

ctx.lineTo(
canvas.width,
effect.y
);

ctx.stroke();

}

}


/*
   검 부채꼴
*/

for (
const effect of effects
) {

if (
effect.type==="swordFan"
) {

ctx.beginPath();

ctx.moveTo(
effect.x,
effect.y
);

ctx.arc(
effect.x,
effect.y,
effect.range,
effect.angle-effect.fan/2,
effect.angle+effect.fan/2
);

ctx.closePath();

ctx.fillStyle =
"rgba(220,235,255,0.30)";

ctx.fill();

ctx.strokeStyle =
"rgba(235,245,255,0.85)";

ctx.lineWidth=4;

ctx.stroke();

}

}


/*
   적
*/

for (
const enemy of enemies
) {

ctx.beginPath();

ctx.arc(
enemy.x,
enemy.y,
enemy.radius,
0,
Math.PI*2
);

ctx.fillStyle =
enemy.boss
?"#a83255"
:"#7661ca";

ctx.fill();


if(enemy.boss) {

ctx.strokeStyle="#ffd166";

ctx.lineWidth=4;

ctx.stroke();

}


ctx.fillStyle="white";

ctx.beginPath();

ctx.arc(
enemy.x-5,
enemy.y-3,
3,
0,
Math.PI*2
);

ctx.arc(
enemy.x+5,
enemy.y-3,
3,
0,
Math.PI*2
);

ctx.fill();


const barWidth =
enemy.boss?75:32;


ctx.fillStyle="#333";

ctx.fillRect(
enemy.x-barWidth/2,
enemy.y-enemy.radius-10,
barWidth,
5
);

ctx.fillStyle =
enemy.boss
?"#ff405c"
:"#55dd70";

ctx.fillRect(
enemy.x-barWidth/2,
enemy.y-enemy.radius-10,
barWidth*
Math.max(
0,
enemy.hp/enemy.maxHp
),
5
);

}


/*
   투사체
*/

for (
const p of projectiles
) {

ctx.beginPath();

ctx.arc(
p.x,
p.y,
p.radius,
0,
Math.PI*2
);

ctx.fillStyle =
p.type==="bullet"
?"#ffd166"
:"#d878ff";

ctx.fill();

}


/*
   플레이어
*/

ctx.beginPath();

ctx.arc(
player.x,
player.y,
player.radius,
0,
Math.PI*2
);


if(weapon==="gun")
ctx.fillStyle="#e7a35e";

else if(weapon==="sword")
ctx.fillStyle="#dcecff";

else
ctx.fillStyle="#b76cff";

ctx.fill();


/*
   방향
*/

ctx.strokeStyle="white";

ctx.lineWidth=3;

ctx.beginPath();

ctx.moveTo(
player.x,
player.y
);

ctx.lineTo(
player.x+player.facingX*25,
player.y+player.facingY*25
);

ctx.stroke();


/*
   🔵 방어막
*/

if(player.shield>0) {

ctx.beginPath();

ctx.arc(
player.x,
player.y,
player.radius+9,
0,
Math.PI*2
);

ctx.strokeStyle="#299cff";

ctx.lineWidth=6;

ctx.stroke();

}


/*
   🔮 법사 각성
*/

if (
weapon==="magic" &&
player.skillActive
) {

ctx.beginPath();

ctx.arc(
player.x,
player.y,
player.radius+12,
0,
Math.PI*2
);

ctx.strokeStyle="#c16cff";

ctx.lineWidth=4;

ctx.stroke();

}


/*
   HP
*/

ctx.fillStyle="#333";

ctx.fillRect(
player.x-35,
player.y-34,
70,
6
);

ctx.fillStyle="#ef4444";

ctx.fillRect(
player.x-35,
player.y-34,
70*
Math.max(
0,
player.hp/player.maxHp
),
6
);


/*
   스킬 게이지
*/

const ratio =
Math.min(
player.skillCharge/player.skillNeed,
1
);

ctx.fillStyle="#333";

ctx.fillRect(
player.x-30,
player.y+27,
60,
5
);

ctx.fillStyle =
ratio>=1
?"#b276ff"
:"#7042a8";

ctx.fillRect(
player.x-30,
player.y+27,
60*ratio,
5
);

}


/* ==========================================
   UI
========================================== */

function updateUI() {

document.getElementById(
"level"
).textContent=level;

document.getElementById(
"hp"
).textContent=
Math.ceil(player.hp)+
"/"+
Math.ceil(player.maxHp);

document.getElementById(
"shield"
).textContent=
Math.floor(player.shield);

document.getElementById(
"xp"
).textContent=
Math.floor(xp)+
"/"+
xpNeed;

document.getElementById(
"kills"
).textContent=kills;


const skillButton =
document.getElementById(
"skillButton"
);


if (
player.skillCharge>=
player.skillNeed &&
!player.skillActive
) {

skillButton.classList.add(
"ready"
);

}
else {

skillButton.classList.remove(
"ready"
);

}


/*
   법사 각성 중에는
   버튼을 각성 표시
*/

if (
weapon==="magic" &&
player.skillActive
) {

skillButton.textContent="✨";

}
else {

skillButton.textContent="⚡";

}

}


/* ==========================================
   게임오버
========================================== */

function gameOver() {

gameRunning=false;

document.getElementById(
"gameOver"
).style.display="block";

}


/* ==========================================
   선택 화면
========================================== */

function returnToSelect() {

gameRunning=false;

document.getElementById(
"gameOver"
).style.display="none";

document.getElementById(
"gameArea"
).style.display="none";

document.getElementById(
"weaponSelect"
).style.display="block";

}


/* ==========================================
   스킬 버튼
========================================== */

document
.getElementById("skillButton")
.addEventListener(
"touchstart",
function(e) {

e.preventDefault();

useSkill();

},
{passive:false}
);


document
.getElementById("skillButton")
.addEventListener(
"click",
function() {

useSkill();

}
);


/* ==========================================
   게임 루프
========================================== */

function gameLoop(time) {

const delta =
Math.min(
time-lastTime,
40
);

lastTime=time;


if(gameRunning) {

updateTime(delta);

movePlayer();

updateSpawning(delta);

updateEnemies(delta);

updateProjectiles();

processDeaths();

collectXP();

updateSkill(delta);

updateEffects(delta);


attackTimer-=delta;


/*
   총 각성
*/

let currentSpeed =
player.attackSpeed;


if (
weapon==="gun" &&
player.skillActive
) {

currentSpeed*=0.25;

}


/*
   🔮 법사 각성
   공속 증가
*/

if (
weapon==="magic" &&
player.skillActive
) {

currentSpeed*=0.65;

}


if (
attackTimer<=0
) {

attack();

attackTimer=currentSpeed;

}


updateUI();

}


draw();

requestAnimationFrame(
gameLoop
);

}


requestAnimationFrame(
gameLoop
);

</script>

</body>
</html>
"""


components.html(
    html,
    height=850,
    scrolling=False
)
