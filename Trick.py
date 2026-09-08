import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NURURUNG SURVIVOR",
    page_icon="👾",
    layout="centered"
)

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
html, body {
    margin: 0;
    padding: 0;
    background: #101018;
    overflow: hidden;
    touch-action: none;
    user-select: none;
    -webkit-user-select: none;
}

body {
    font-family: Arial, sans-serif;
}

#gameBox {
    width: 100%;
    max-width: 900px;
    margin: auto;
    text-align: center;
}

#info {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    color: white;
    font-size: 13px;
    margin: 6px 0;
    gap: 8px;
}

canvas {
    display: block;
    width: 100%;
    max-width: 850px;
    margin: auto;
    background: #151522;
    border: 2px solid #555;
    border-radius: 10px;
    touch-action: none;
}

#mobileControls {
    position: relative;
    height: 130px;
    width: 100%;
    max-width: 850px;
    margin: auto;
}

#joystick {
    position: absolute;
    left: 15px;
    bottom: 5px;
    width: 105px;
    height: 105px;
    border-radius: 50%;
    background: rgba(100,100,120,0.35);
    border: 2px solid rgba(255,255,255,0.3);
}

#stick {
    position: absolute;
    left: 27px;
    top: 27px;
    width: 51px;
    height: 51px;
    border-radius: 50%;
    background: rgba(220,220,220,0.65);
}

#skillButton {
    position: absolute;
    right: 20px;
    bottom: 15px;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: #673ab7;
    border: 3px solid #b388ff;
    color: white;
    font-size: 27px;
    font-weight: bold;
}

#skillButton:active {
    transform: scale(0.92);
}

#levelup {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    width: 90%;
    max-width: 650px;

    background: rgba(15,15,25,0.97);
    border: 2px solid #777;
    border-radius: 14px;

    padding: 18px;

    display: none;
    z-index: 50;

    color: white;
}

.upgrade {
    display: block;
    width: 100%;
    margin: 8px 0;
    padding: 14px;

    background: #29293b;
    color: white;

    border: 1px solid #666;
    border-radius: 8px;

    text-align: left;
    font-size: 15px;
}

.upgrade:active {
    background: #454560;
}

#gameOver {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    background: rgba(10,10,15,0.95);
    padding: 30px;
    border-radius: 15px;

    color: white;
    font-size: 30px;

    display: none;
    z-index: 60;
}

#gameOver button {
    margin-top: 20px;
    padding: 12px 25px;
    border: 0;
    border-radius: 8px;
    background: #4d7cff;
    color: white;
    font-weight: bold;
}

#characterSelect {
    color: white;
    margin: 5px;
}

.charButton {
    margin: 3px;
    padding: 7px 12px;
    border: 0;
    border-radius: 7px;
    background: #29293b;
    color: white;
}
</style>
</head>

<body>

<div id="gameBox">

<div id="characterSelect">
    <b>무기 선택</b><br>

    <button class="charButton"
        onclick="selectWeapon('gun')">
        🔫 총
    </button>

    <button class="charButton"
        onclick="selectWeapon('sword')">
        ⚔️ 칼
    </button>

    <button class="charButton"
        onclick="selectWeapon('magic')">
        🔮 마법
    </button>
</div>

<div id="info">
    <span>LV <b id="level">1</b></span>
    <span>❤️ <b id="hp">100/100</b></span>
    <span>🛡️ <b id="shield">0</b></span>
    <span>XP <b id="xp">0/10</b></span>
    <span>☠️ <b id="kills">0</b></span>
    <span>⏱️ <b id="time">0</b></span>
</div>

<canvas id="game"
        width="850"
        height="600">
</canvas>

<div id="mobileControls">

    <div id="joystick">
        <div id="stick"></div>
    </div>

    <button id="skillButton">⚡</button>

</div>

<div id="levelup">

    <h2>LEVEL UP!</h2>

    <p>원하는 능력을 하나 선택하세요.</p>

    <div id="upgradeList"></div>

</div>

<div id="gameOver">

    GAME OVER

    <br>

    <button onclick="restartGame()">
        다시 시작
    </button>

</div>

</div>


<script>

/* ==================================================
   기본
================================================== */

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let gameRunning = true;

let weapon = "gun";

let level = 1;
let xp = 0;
let xpNeed = 10;

let kills = 0;
let gameTime = 0;

let lastTime = performance.now();

let spawnTimer = 0;
let attackTimer = 0;


/* ==================================================
   플레이어
================================================== */

const player = {

    x: 425,
    y: 300,

    radius: 17,

    hp: 100,
    maxHp: 100,

    speed: 3.5,

    damage: 15,

    attackSpeed: 650,

    range: 260,

    area: 1,

    projectileSpeed: 8,

    damageReduction: 0,

    xpMultiplier: 1,

    shield: 0,

    skillCharge: 0,

    skillNeed: 15,

    skillActive: false,
    skillTimer: 0

};


/* ==================================================
   배열
================================================== */

let enemies = [];
let projectiles = [];
let gems = [];
let effects = [];


/* ==================================================
   키보드
================================================== */

const keys = {};

document.addEventListener("keydown", function(e) {

    keys[e.key.toLowerCase()] = true;

});

document.addEventListener("keyup", function(e) {

    keys[e.key.toLowerCase()] = false;

});


/* ==================================================
   모바일 조이스틱
================================================== */

const joystick =
    document.getElementById("joystick");

const stick =
    document.getElementById("stick");

let joystickActive = false;

let joyX = 0;
let joyY = 0;

const joystickRadius = 42;


function updateJoystick(clientX, clientY) {

    const rect =
        joystick.getBoundingClientRect();

    const centerX =
        rect.left + rect.width / 2;

    const centerY =
        rect.top + rect.height / 2;

    let dx =
        clientX - centerX;

    let dy =
        clientY - centerY;

    const distance =
        Math.sqrt(dx * dx + dy * dy);

    if (distance > joystickRadius) {

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

        const touch =
            e.touches[0];

        updateJoystick(
            touch.clientX,
            touch.clientY
        );

    },
    {passive:false}
);


joystick.addEventListener(
    "touchmove",
    function(e) {

        e.preventDefault();

        if (!joystickActive) {
            return;
        }

        const touch =
            e.touches[0];

        updateJoystick(
            touch.clientX,
            touch.clientY
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


/* ==================================================
   모바일 스킬 버튼
================================================== */

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


/* ==================================================
   무기 선택
================================================== */

function selectWeapon(type) {

    weapon = type;

    restartGame();

}


/* ==================================================
   플레이어 설정
================================================== */

function setupPlayer() {

    player.x = 425;
    player.y = 300;

    player.hp = 100;
    player.maxHp = 100;

    player.speed = 3.5;

    player.damage = 15;

    player.attackSpeed = 650;

    player.range = 260;

    player.area = 1;

    player.projectileSpeed = 8;

    player.damageReduction = 0;

    player.xpMultiplier = 1;

    player.shield = 0;

    player.skillCharge = 0;

    player.skillActive = false;
    player.skillTimer = 0;


    if (weapon === "gun") {

        player.maxHp = 90;
        player.hp = 90;

        player.speed = 3.8;

        player.damage = 13;

        player.attackSpeed = 480;

        player.range = 330;

        player.skillNeed = 18;

    }


    if (weapon === "sword") {

        player.maxHp = 140;
        player.hp = 140;

        player.speed = 3.0;

        player.damage = 24;

        player.attackSpeed = 750;

        player.range = 105;

        player.area = 1.2;

        player.damageReduction = 0.15;

        player.skillNeed = 12;

    }


    if (weapon === "magic") {

        player.maxHp = 100;
        player.hp = 100;

        player.speed = 3.2;

        player.damage = 18;

        player.attackSpeed = 800;

        player.range = 300;

        player.area = 1.4;

        player.skillNeed = 15;

    }

}


/* ==================================================
   적 생성
================================================== */

function spawnEnemy() {

    const side =
        Math.floor(Math.random() * 4);

    let x;
    let y;


    if (side === 0) {

        x =
            Math.random() *
            canvas.width;

        y = -30;

    }

    else if (side === 1) {

        x =
            canvas.width + 30;

        y =
            Math.random() *
            canvas.height;

    }

    else if (side === 2) {

        x =
            Math.random() *
            canvas.width;

        y =
            canvas.height + 30;

    }

    else {

        x = -30;

        y =
            Math.random() *
            canvas.height;

    }


    const hp =
        20 +
        gameTime * 1.7 +
        level * 5;


    enemies.push({

        x:x,
        y:y,

        radius:15,

        hp:hp,
        maxHp:hp,

        speed:
            0.65 +
            Math.random() * 0.35 +
            gameTime * 0.004,

        damage:
            5 +
            gameTime * 0.07,

        cooldown:0

    });

}


/* ==================================================
   플레이어 이동
================================================== */

function movePlayer() {

    let dx = 0;
    let dy = 0;


    if (keys["w"] || keys["arrowup"]) {
        dy -= 1;
    }

    if (keys["s"] || keys["arrowdown"]) {
        dy += 1;
    }

    if (keys["a"] || keys["arrowleft"]) {
        dx -= 1;
    }

    if (keys["d"] || keys["arrowright"]) {
        dx += 1;
    }


    /*
       모바일 조이스틱
    */

    if (joystickActive) {

        dx += joyX;
        dy += joyY;

    }


    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );


    if (length > 0) {

        dx /= length;
        dy /= length;

    }


    player.x +=
        dx *
        player.speed;

    player.y +=
        dy *
        player.speed;


    player.x =
        Math.max(
            player.radius,
            Math.min(
                canvas.width -
                player.radius,
                player.x
            )
        );


    player.y =
        Math.max(
            player.radius,
            Math.min(
                canvas.height -
                player.radius,
                player.y
            )
        );

}


/* ==================================================
   가장 가까운 적
================================================== */

function nearestEnemy() {

    let target = null;

    let bestDistance =
        player.range *
        player.range;


    for (const enemy of enemies) {

        const dx =
            enemy.x -
            player.x;

        const dy =
            enemy.y -
            player.y;

        const d =
            dx * dx +
            dy * dy;


        if (d < bestDistance) {

            bestDistance = d;
            target = enemy;

        }

    }


    return target;

}


/
