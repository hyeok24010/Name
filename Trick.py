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


/* ==================================================
   총 공격
================================================== */

function gunAttack() {

    const target =
        nearestEnemy();


    if (!target) {
        return;
    }


    const dx =
        target.x -
        player.x;

    const dy =
        target.y -
        player.y;


    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );


    projectiles.push({

        x:player.x,
        y:player.y,

        dx:
            dx / length *
            player.projectileSpeed,

        dy:
            dy / length *
            player.projectileSpeed,

        damage:player.damage,

        radius:5,

        type:"bullet"

    });

}


/* ==================================================
   칼 공격
================================================== */

function swordAttack() {

    effects.push({

        type:"slash",

        x:player.x,
        y:player.y,

        radius:
            player.range *
            player.area,

        life:15

    });


    for (const enemy of enemies) {

        const dx =
            enemy.x -
            player.x;

        const dy =
            enemy.y -
            player.y;

        const distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );


        if (
            distance <
            player.range *
            player.area
        ) {

            enemy.hp -=
                player.damage;

        }

    }

}


/* ==================================================
   마법 공격
================================================== */

function magicAttack() {

    const target =
        nearestEnemy();


    if (!target) {
        return;
    }


    const dx =
        target.x -
        player.x;

    const dy =
        target.y -
        player.y;


    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );


    projectiles.push({

        x:player.x,
        y:player.y,

        dx:
            dx / length *
            player.projectileSpeed,

        dy:
            dy / length *
            player.projectileSpeed,

        damage:
            player.damage,

        radius:
            12 *
            player.area,

        type:"magic"

    });

}


/* ==================================================
   일반 공격
================================================== */

function attack() {

    if (weapon === "gun") {
        gunAttack();
    }

    else if (weapon === "sword") {
        swordAttack();
    }

    else {
        magicAttack();
    }

}


/* ==================================================
   고유 스킬
================================================== */

function useSkill() {

    if (
        player.skillCharge <
        player.skillNeed
    ) {

        return;

    }


    player.skillCharge = 0;


    /*
       총:
       5초간 초고속 연사
    */

    if (weapon === "gun") {

        player.skillActive = true;

        player.skillTimer = 5000;

    }


    /*
       칼:
       주변을 크게 베면서
       잠시 피해 감소
    */

    else if (weapon === "sword") {

        player.skillActive = true;

        player.skillTimer = 3500;

        effects.push({

            type:"bigSlash",

            x:player.x,
            y:player.y,

            radius:150,

            life:35

        });


        for (const enemy of enemies) {

            const dx =
                enemy.x -
                player.x;

            const dy =
                enemy.y -
                player.y;

            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );


            if (distance < 150) {

                enemy.hp -=
                    player.damage *
                    5;

            }

        }

    }


    /*
       마법:
       화면 전체에 마법 폭발
    */

    else {

        player.skillActive = true;

        player.skillTimer = 5000;

        effects.push({

            type:"magicStorm",

            x:player.x,
            y:player.y,

            radius:250,

            life:60

        });


        for (const enemy of enemies) {

            enemy.hp -=
                player.damage *
                3;

        }

    }

}


/* ==================================================
   스킬 업데이트
================================================== */

function updateSkill(delta) {

    if (!player.skillActive) {
        return;
    }


    player.skillTimer -= delta;


    /*
       총 스킬
    */

    if (
        weapon === "gun"
    ) {

        if (Math.random() < 0.35) {

            gunAttack();

        }

    }


    /*
       칼 스킬
    */

    if (
        weapon === "sword"
    ) {

        player.damageReduction =
            0.55;

    }


    /*
       마법 스킬
    */

    if (
        weapon === "magic"
    ) {

        /*
           주변 적 지속 피해
        */

        for (const enemy of enemies) {

            const dx =
                enemy.x -
                player.x;

            const dy =
                enemy.y -
                player.y;

            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );


            if (distance < 250) {

                enemy.hp -=
                    player.damage *
                    0.12;

            }

        }

    }


    if (
        player.skillTimer <= 0
    ) {

        player.skillActive = false;

        /*
           칼 피해 감소 원상복구
        */

        if (weapon === "sword") {

            player.damageReduction =
                0.15;

        }

    }

}


/* ==================================================
   투사체
================================================== */

function updateProjectiles() {

    for (const p of projectiles) {

        p.x += p.dx;
        p.y += p.dy;


        for (const enemy of enemies) {

            if (enemy.hp <= 0) {
                continue;
            }


            const dx =
                enemy.x -
                p.x;

            const dy =
                enemy.y -
                p.y;


            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );


            if (
                distance <
                enemy.radius +
                p.radius
            ) {

                enemy.hp -=
                    p.damage;

                p.dead = true;

                break;

            }

        }

    }


    projectiles =
        projectiles.filter(
            p =>
                !p.dead &&
                p.x > -50 &&
                p.x < canvas.width + 50 &&
                p.y > -50 &&
                p.y < canvas.height + 50
        );

}


/* ==================================================
   적 이동
================================================== */

function updateEnemies(delta) {

    for (const enemy of enemies) {

        const dx =
            player.x -
            enemy.x;

        const dy =
            player.y -
            enemy.y;


        const distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );


        if (
            distance >
            player.radius +
            enemy.radius
        ) {

            enemy.x +=
                dx /
                distance *
                enemy.speed;

            enemy.y +=
                dy /
                distance *
                enemy.speed;

        }

        else {

            enemy.cooldown -= delta;


            if (
                enemy.cooldown <= 0
            ) {

                damagePlayer(
                    enemy.damage
                );

                enemy.cooldown = 650;

            }

        }

    }

}


/* ==================================================
   피해
================================================== */

function damagePlayer(amount) {

    let damage =
        amount *
        (1 -
        player.damageReduction);


    if (player.shield > 0) {

        const blocked =
            Math.min(
                player.shield,
                damage
            );

        player.shield -= blocked;

        damage -= blocked;

    }


    player.hp -= damage;


    if (player.hp <= 0) {

        player.hp = 0;

        gameOver();

    }

}


/* ==================================================
   적 처치
================================================== */

function processDeaths() {

    const alive = [];


    for (const enemy of enemies) {

        if (enemy.hp <= 0) {

            kills++;

            player.skillCharge++;


            gems.push({

                x:enemy.x,
                y:enemy.y,
                value:1

            });

        }

        else {

            alive.push(enemy);

        }

    }


    enemies = alive;

}


/* ==================================================
   경험치
================================================== */

function collectXP() {

    for (
        let i = gems.length - 1;
        i >= 0;
        i--
    ) {

        const gem = gems[i];


        const dx =
            player.x -
            gem.x;

        const dy =
            player.y -
            gem.y;


        const distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );


        /*
           경험치 획득 범위
        */

        if (
            distance <
            65 *
            player.area
        ) {

            xp +=
                gem.value *
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
                xpNeed * 1.35
            );


        showLevelUp();

    }

}


/* ==================================================
   레벨업
================================================== */

function showLevelUp() {

    gameRunning = false;


    const list =
        document.getElementById(
            "upgradeList"
        );


    list.innerHTML = "";


    const upgrades = [

        {
            text:"⚔️ 공격력 +20%",
            effect:function() {

                player.damage *= 1.20;

            }
        },

        {
            text:"⚡ 공격속도 +20%",
            effect:function() {

                player.attackSpeed *= 0.80;

            }
        },

        {
            text:"🎯 공격 범위 +25%",
            effect:function() {

                player.range *= 1.25;

            }
        },

        {
            text:"💥 공격 범위 크기 +20%",
            effect:function() {

                player.area *= 1.20;

            }
        },

        {
            text:"🏃 이동속도 +15%",
            effect:function() {

                player.speed *= 1.15;

            }
        },

        {
            text:"❤️ 최대 체력 +25",
            effect:function() {

                player.maxHp += 25;

                player.hp += 25;

            }
        },

        {
            text:"🛡️ 피해 감소 +5%",
            effect:function() {

                player.damageReduction =
                    Math.min(
                        0.70,
                        player.damageReduction + 0.05
                    );

            }
        },

        {
            text:"✨ 경험치 획득 +20%",
            effect:function() {

                player.xpMultiplier *= 1.20;

            }
        },

        {
            text:"💨 탄속 +25%",
            effect:function() {

                player.projectileSpeed *= 1.25;

            }
        },

        {
            text:"🧲 경험치 획득 범위 +30%",
            effect:function() {

                player.area *= 1.30;

            }
        }

    ];


    /*
       무작위로 섞기
    */

    upgrades.sort(
        () =>
            Math.random() - 0.5
    );


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


                    document
                    .getElementById(
                        "levelup"
                    )
                    .style.display =
                    "none";


                    gameRunning = true;

                };


            list.appendChild(button);

        }
    );


    document
    .getElementById(
        "levelup"
    )
    .style.display =
    "block";

}


/* ==================================================
   시간
================================================== */

function updateTime(delta) {

    gameTime +=
        delta / 1000;


    document.getElementById(
        "time"
    ).textContent =
        Math.floor(gameTime);

}


/* ==================================================
   적 생성 속도
================================================== */

function spawnEnemies(delta) {

    spawnTimer -= delta;


    /*
       시간이 지나면
       등장 간격 감소
    */

    const interval =
        Math.max(
            900 -
            gameTime * 15,
            130
        );


    if (
        spawnTimer <= 0
    ) {

        /*
           시간이 지날수록
           한 번에 많이 등장
        */

        const amount =
            Math.min(
                1 +
                Math.floor(
                    gameTime / 25
                ),
                10
            );


        for (
            let i = 0;
            i < amount;
            i++
        ) {

            spawnEnemy();

        }


        spawnTimer = interval;

    }

}


/* ==================================================
   효과
================================================== */

function updateEffects() {

    for (const effect of effects) {

        effect.life--;

    }


    effects =
        effects.filter(
            e => e.life > 0
        );

}


/* ==================================================
   그리기
================================================== */

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /*
       배경
    */

    ctx.fillStyle = "#151522";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /*
       격자
    */

    ctx.strokeStyle =
        "rgba(255,255,255,0.035)";

    for (
        let x = 0;
        x < canvas.width;
        x += 40
    ) {

        ctx.beginPath();

        ctx.moveTo(x,0);

        ctx.lineTo(
            x,
            canvas.height
        );

        ctx.stroke();

    }

    for (
        let y = 0;
        y < canvas.height;
        y += 40
    ) {

        ctx.beginPath();

        ctx.moveTo(0,y);

        ctx.lineTo(
            canvas.width,
            y
        );

        ctx.stroke();

    }


    /*
       경험치
    */

    for (const gem of gems) {

        ctx.beginPath();

        ctx.arc(
            gem.x,
            gem.y,
            5,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            "#65e6ff";

        ctx.fill();

    }


    /*
       적
    */

    for (const enemy of enemies) {

        ctx.beginPath();

        ctx.arc(
            enemy.x,
            enemy.y,
            enemy.radius,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            "#8c6cff";

        ctx.fill();


        /*
           누루룽 눈
        */

        ctx.fillStyle =
            "white";

        ctx.beginPath();

        ctx.arc(
            enemy.x - 5,
            enemy.y - 3,
            3,
            0,
            Math.PI * 2
        );

        ctx.arc(
            enemy.x + 5,
            enemy.y - 3,
            3,
            0,
            Math.PI * 2
        );

        ctx.fill();


        /*
           적 HP
        */

        ctx.fillStyle =
            "#333";

        ctx.fillRect(
            enemy.x - 16,
            enemy.y - 24,
            32,
            4
        );


        ctx.fillStyle =
            "#ff4040";

        ctx.fillRect(
            enemy.x - 16,
            enemy.y - 24,
            32 *
            Math.max(
                0,
                enemy.hp /
                enemy.maxHp
            ),
            4
        );

    }


    /*
       투사체
    */

    for (const p of projectiles) {

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            p.radius,
            0,
            Math.PI * 2
        );


        if (p.type === "bullet") {

            ctx.fillStyle =
                "#ffd166";

        }

        else {

            ctx.fillStyle =
                "#d56cff";

        }


        ctx.fill();

    }


    /*
       칼 범위
    */

    if (weapon === "sword") {

        ctx.beginPath();

        ctx.arc(
            player.x,
            player.y,
            player.range *
            player.area,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle =
            "rgba(255,255,255,0.08)";

        ctx.stroke();

    }


    /*
       스킬 효과
    */

    for (const effect of effects) {

        if (
            effect.type === "slash" ||
            effect.type === "bigSlash"
        ) {

            ctx.beginPath();

            ctx.arc(
                effect.x,
                effect.y,
                effect.radius,
                0,
                Math.PI * 2
            );

            ctx.strokeStyle =
                "#eeeeee";

            ctx.lineWidth =
                effect.type === "bigSlash"
                ? 15
                : 7;

            ctx.stroke();

        }


        if (
            effect.type === "magicStorm"
        ) {

            ctx.beginPath();

            ctx.arc(
                effect.x,
                effect.y,
                effect.radius,
                0,
                Math.PI * 2
            );

            ctx.strokeStyle =
                "#b45cff";

            ctx.lineWidth = 12;

            ctx.stroke();

        }

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
        Math.PI * 2
    );


    if (weapon === "gun") {

        ctx.fillStyle =
            "#e8a45c";

    }

    else if (weapon === "sword") {

        ctx.fillStyle =
            "#d7e7ff";

    }

    else {

        ctx.fillStyle =
            "#b86cff";

    }


    ctx.fill();


    /*
       플레이어 방향 표시
    */

    ctx.fillStyle =
        "#222";

    ctx.beginPath();

    ctx.arc(
        player.x - 5,
        player.y - 3,
        3,
        0,
        Math.PI * 2
    );

    ctx.arc(
        player.x + 5,
        player.y - 3,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    /*
       방어막
    */

    if (player.shield > 0) {

        ctx.beginPath();

        ctx.arc(
            player.x,
            player.y,
            player.radius + 8,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle =
            "#dddddd";

        ctx.lineWidth = 5;

        ctx.stroke();

    }


    /*
       체력바
    */

    ctx.fillStyle =
        "#333";

    ctx.fillRect(
        player.x - 35,
        player.y - 34,
        70,
        6
    );


    ctx.fillStyle =
        "#ef4444";

    ctx.fillRect(
        player.x - 35,
        player.y - 34,
        70 *
        Math.max(
            0,
            player.hp /
            player.maxHp
        ),
        6
    );


    /*
       스킬 게이지
    */

    const skillRatio =
        Math.min(
            player.skillCharge /
            player.skillNeed,
            1
        );


    ctx.fillStyle =
        "#333";

    ctx.fillRect(
        player.x - 30,
        player.y + 27,
        60,
        5
    );


    ctx.fillStyle =
        "#b56cff";

    ctx.fillRect(
        player.x - 30,
        player.y + 27,
        60 *
        skillRatio,
        5
    );


    /*
       스킬 준비
    */

    if (
        player.skillCharge >=
        player.skillNeed
    ) {

        ctx.fillStyle =
            "#ffffff";

        ctx.font =
            "bold 11px Arial";

        ctx.textAlign =
            "center";

        ctx.fillText(
            "SKILL!",
            player.x,
            player.y + 45
        );

    }

}


/* ==================================================
   UI
================================================== */

function updateUI() {

    document.getElementById(
        "level"
    ).textContent = level;


    document.getElementById(
        "hp"
    ).textContent =
        Math.ceil(player.hp) +
        "/" +
        Math.ceil(player.maxHp);


    document.getElementById(
        "shield"
    ).textContent =
        Math.floor(player.shield);


    document.getElementById(
        "xp"
    ).textContent =
        Math.floor(xp) +
        "/" +
        xpNeed;


    document.getElementById(
        "kills"
    ).textContent =
        kills;

}


/* ==================================================
   게임 오버
================================================== */

function gameOver() {

    gameRunning = false;

    document.getElementById(
        "gameOver"
    ).style.display =
        "block";

}


/* ==================================================
   재시작
================================================== */

function restartGame() {

    level = 1;

    xp = 0;

    xpNeed = 10;

    kills = 0;

    gameTime = 0;

    spawnTimer = 0;

    attackTimer = 0;


    enemies = [];
    projectiles = [];
    gems = [];
    effects = [];


    setupPlayer();


    gameRunning = true;


    document.getElementById(
        "gameOver"
    ).style.display =
        "none";


    document.getElementById(
        "levelup"
    ).style.display =
        "none";


    resetJoystick();


    lastTime =
        performance.now();

}


/* ==================================================
   메인 루프
================================================== */

function gameLoop(time) {

    const delta =
        Math.min(
            time - lastTime,
            40
        );


    lastTime = time;


    if (gameRunning) {

        updateTime(delta);

        movePlayer();

        spawnEnemies(delta);

        updateEnemies(delta);

        updateProjectiles();

        processDeaths();

        collectXP();

        updateSkill(delta);

        updateEffects();


        /*
           자동 공격
        */

        attackTimer -= delta;


        let currentAttackSpeed =
            player.attackSpeed;


        /*
           총 스킬 동안
           엄청 빠른 연사
        */

        if (
            weapon === "gun" &&
            player.skillActive
        ) {

            currentAttackSpeed *= 0.25;

        }


        if (
            attackTimer <= 0
        ) {

            attack();

            attackTimer =
                currentAttackSpeed;

        }


        updateUI();

    }


    draw();


    requestAnimationFrame(
        gameLoop
    );

}


/* ==================================================
   시작
================================================== */

setupPlayer();

restartGame();

requestAnimationFrame(
    gameLoop
);

</script>

</body>
</html>
"""

components.html(
    game,
    height=850,
    scrolling=False
)
