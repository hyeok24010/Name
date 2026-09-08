import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Nururung Survivor",
    page_icon="⚔️",
    layout="centered"
)

html = """
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
    -webkit-user-select: none;
    font-family: Arial, sans-serif;
}

#gameWrap {
    width: 100%;
    max-width: 900px;
    margin: auto;
}

#weaponSelect {
    color: white;
    text-align: center;
    padding: 20px 10px;
}

#weaponSelect h1 {
    font-size: 27px;
    margin-bottom: 8px;
}

#weaponSelect p {
    color: #aaa;
    font-size: 14px;
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
    font-size: 26px;
    font-weight: bold;
}

#skillButton.ready {
    background: #8655df;
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

<div id="gameWrap">

    <div id="weaponSelect">

        <h1>⚔️ NURURUNG SURVIVOR</h1>

        <p>무기를 선택하고 살아남으세요.</p>

        <button class="weaponButton" onclick="startGame('gun')">
            🔫 총
            <span class="weaponDescription">
                빠른 연사 · 발사체 증가 · 공격력 강화
            </span>
        </button>

        <button class="weaponButton" onclick="startGame('sword')">
            ⚔️ 검
            <span class="weaponDescription">
                높은 방어력 · 바라보는 방향의 부채꼴 공격 · 방어막
            </span>
        </button>

        <button class="weaponButton" onclick="startGame('magic')">
            🔮 마법
            <span class="weaponDescription">
                광역 공격 · 강화 사슬 · 강화 공격 주기 감소
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

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

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


/* ======================================
   플레이어
====================================== */

const player = {

    x: 425,
    y: 300,

    radius: 17,

    hp: 100,
    maxHp: 100,

    shield: 0,

    speed: 3.4,

    damage: 15,

    attackSpeed: 650,

    range: 300,

    area: 1,

    projectileSpeed: 8,

    projectileCount: 1,

    damageReduction: 0,

    xpMultiplier: 1,

    skillCharge: 0,

    skillNeed: 15,

    skillActive: false,

    skillTimer: 0,

    magicCount: 0,

    magicEnhancedNeed: 10,

    facingX: 1,
    facingY: 0

};


/* ======================================
   게임 시작
====================================== */

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


/* ======================================
   게임 초기화
====================================== */

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

    player.magicCount = 0;

    player.magicEnhancedNeed = 10;

    player.projectileCount = 1;

    player.area = 1;

    player.projectileSpeed = 8;

    player.damageReduction = 0;

    player.xpMultiplier = 1;

    player.facingX = 1;
    player.facingY = 0;


    if (weapon === "gun") {

        player.maxHp = 90;
        player.hp = 90;

        player.speed = 3.8;

        player.damage = 13;

        player.attackSpeed = 500;

        player.range = 330;

        player.skillNeed = 15;

    }


    if (weapon === "sword") {

        player.maxHp = 140;
        player.hp = 140;

        player.speed = 3.1;

        player.damage = 24;

        player.attackSpeed = 720;

        player.range = 120;

        player.area = 1;

        player.damageReduction = 0.12;

        player.skillNeed = 12;

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


/* ======================================
   키보드
====================================== */

const keys = {};

document.addEventListener(
    "keydown",
    function(e) {

        keys[e.key.toLowerCase()] = true;

    }
);

document.addEventListener(
    "keyup",
    function(e) {

        keys[e.key.toLowerCase()] = false;

    }
);


/* ======================================
   모바일 조이스틱
====================================== */

const joystick =
    document.getElementById("joystick");

const stick =
    document.getElementById("stick");

let joystickActive = false;

let joyX = 0;
let joyY = 0;

const joystickRadius = 42;


function updateJoystick(x, y) {

    const rect =
        joystick.getBoundingClientRect();

    const centerX =
        rect.left +
        rect.width / 2;

    const centerY =
        rect.top +
        rect.height / 2;

    let dx =
        x - centerX;

    let dy =
        y - centerY;

    const distance =
        Math.sqrt(
            dx * dx +
            dy * dy
        );


    if (
        distance >
        joystickRadius
    ) {

        dx =
            dx / distance *
            joystickRadius;

        dy =
            dy / distance *
            joystickRadius;

    }


    joyX =
        dx /
        joystickRadius;

    joyY =
        dy /
        joystickRadius;


    stick.style.left =
        (27 + dx) + "px";

    stick.style.top =
        (27 + dy) + "px";


    /*
       조이스틱 방향 = 바라보는 방향
    */

    if (
        Math.abs(joyX) +
        Math.abs(joyY) >
        0.15
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

        const t =
            e.touches[0];

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

        const t =
            e.touches[0];

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


/* ======================================
   플레이어 이동
====================================== */

function movePlayer() {

    let dx = 0;
    let dy = 0;


    if (
        keys["w"] ||
        keys["arrowup"]
    ) {
        dy -= 1;
    }

    if (
        keys["s"] ||
        keys["arrowdown"]
    ) {
        dy += 1;
    }

    if (
        keys["a"] ||
        keys["arrowleft"]
    ) {
        dx -= 1;
    }

    if (
        keys["d"] ||
        keys["arrowright"]
    ) {
        dx += 1;
    }


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

        /*
           마지막 이동 방향을
           바라보는 방향으로 저장
        */

        player.facingX = dx;
        player.facingY = dy;

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


/* ======================================
   가까운 적
====================================== */

function nearestEnemy() {

    let target = null;

    let best =
        player.range *
        player.range;


    for (
        const enemy of enemies
    ) {

        const dx =
            enemy.x -
            player.x;

        const dy =
            enemy.y -
            player.y;

        const d =
            dx * dx +
            dy * dy;


        if (d < best) {

            best = d;
            target = enemy;

        }

    }


    return target;

}


/* ======================================
   총 공격
====================================== */

function gunAttack() {

    const target =
        nearestEnemy();

    if (!target) return;


    const dx =
        target.x -
        player.x;

    const dy =
        target.y -
        player.y;


    const angle =
        Math.atan2(dy, dx);


    const count =
        player.projectileCount;


    for (
        let i = 0;
        i < count;
        i++
    ) {

        let a = angle;


        if (count > 1) {

            a +=
                (
                    i -
                    (count - 1) / 2
                )
                * 0.10;

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

            type: "bullet"

        });

    }

}


/* ======================================
   검 부채꼴 공격
====================================== */

function swordAttack() {

    /*
       검이 향하는 중심 각도
    */

    const centerAngle =
        Math.atan2(
            player.facingY,
            player.facingX
        );


    /*
       부채꼴 각도
       기본 100도
    */

    const fanAngle =
        Math.PI *
        0.56 *
        player.area;


    const attackRange =
        player.range *
        player.area;


    effects.push({

        type: "swordFan",

        x: player.x,
        y: player.y,

        angle: centerAngle,

        range: attackRange,

        fan: fanAngle,

        life: 13

    });


    for (
        const enemy of enemies
    ) {

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
            distance >
            attackRange +
            enemy.radius
        ) {

            continue;

        }


        const enemyAngle =
            Math.atan2(dy, dx);


        let difference =
            enemyAngle -
            centerAngle;


        while (
            difference > Math.PI
        ) {
            difference -=
                Math.PI * 2;
        }


        while (
            difference < -Math.PI
        ) {
            difference +=
                Math.PI * 2;
        }


        /*
           부채꼴 안에 있는 적만 공격
        */

        if (
            Math.abs(difference)
            <=
            fanAngle / 2
        ) {

            dealDamage(
                enemy,
                player.damage
            );

        }

    }

}


/* ======================================
   마법 공격
====================================== */

function magicAttack() {

    const target =
        nearestEnemy();

    if (!target) return;


    player.magicCount++;


    /*
       강화 공격
    */

    if (
        player.magicCount >=
        player.magicEnhancedNeed
    ) {

        player.magicCount = 0;

        magicChainAttack();

    }


    /*
       기본 마법탄
    */

    const angle =
        Math.atan2(
            target.y -
            player.y,

            target.x -
            player.x
        );


    for (
        let i = 0;
        i <
        player.projectileCount;
        i++
    ) {

        let a =
            angle;


        if (
            player.projectileCount > 1
        ) {

            a +=
                (
                    i -
                    (player.projectileCount - 1) / 2
                )
                * 0.12;

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

            radius:
                8 *
                player.area,

            type: "magic"

        });

    }

}


/* ======================================
   마법 강화 사슬
====================================== */

function magicChainAttack() {

    const target =
        nearestEnemy();

    if (!target) return;


    const x =
        target.x;


    const width =
        45 *
        player.area;


    effects.push({

        type: "chain",

        x: x,

        width: width,

        life: 35

    });


    /*
       세로 일자 공격
    */

    for (
        const enemy of enemies
    ) {

        if (
            Math.abs(
                enemy.x -
                x
            )
            <=
            width / 2
        ) {

            dealDamage(
                enemy,
                player.damage * 3.5
            );

        }

    }

}


/* ======================================
   일반 공격
====================================== */

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


/* ======================================
   피해
====================================== */

function dealDamage(
    enemy,
    damage
) {

    if (enemy.boss) {

        damage *=
            1 -
            enemy.armor;

    }


    enemy.hp -= damage;

}


/* ======================================
   스킬
====================================== */

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
       공격속도 크게 증가
       발사체 +2
    */

    if (
        weapon === "gun"
    ) {

        player.skillActive = true;

        player.skillTimer = 5000;

        effects.push({

            type: "gunSkill",

            life: 30

        });

    }


    /*
       검:
       공격하지 않고
       파란 방어막 생성
    */

    else if (
        weapon === "sword"
    ) {

        player.shield +=
            65 +
            level * 12;

        player.skillActive = true;

        player.skillTimer = 6000;

        effects.push({

            type: "shield",

            x: player.x,

            y: player.y,

            radius: 43,

            life: 70

        });

    }


    /*
       마법:
       즉시 강화 사슬
    */

    else {

        player.skillActive = true;

        player.skillTimer = 1200;

        magicChainAttack();

    }

}


/* ======================================
   스킬 업데이트
====================================== */

function updateSkill(delta) {

    if (
        !player.skillActive
    ) {

        return;

    }


    player.skillTimer -=
        delta;


    if (
        player.skillTimer <= 0
    ) {

        player.skillActive = false;

    }

}


/* ======================================
   투사체
====================================== */

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
            ) {
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
                p.x <
                canvas.width + 100 &&
                p.y > -100 &&
                p.y <
                canvas.height + 100
        );

}


/* ======================================
   적 생성
====================================== */

function spawnEnemy() {

    const side =
        Math.floor(
            Math.random() * 4
        );


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
        22 +
        gameTime * 1.6 +
        level * 4;


    enemies.push({

        x: x,
        y: y,

        radius: 15,

        hp: hp,
        maxHp: hp,

        speed:
            0.65 +
            Math.random() * 0.3 +
            gameTime * 0.0025,

        damage:
            5 +
            gameTime * 0.045,

        cooldown: 0,

        boss: false,

        armor: 0

    });

}


/* ======================================
   보스
====================================== */

function spawnBoss() {

    const side =
        Math.floor(
            Math.random() * 4
        );


    let x;
    let y;


    if (side === 0) {

        x =
            Math.random() *
            canvas.width;

        y = -70;

    }

    else if (side === 1) {

        x =
            canvas.width + 70;

        y =
            Math.random() *
            canvas.height;

    }

    else if (side === 2) {

        x =
            Math.random() *
            canvas.width;

        y =
            canvas.height + 70;

    }

    else {

        x = -70;

        y =
            Math.random() *
            canvas.height;

    }


    const hp =
        600 +
        level * 120 +
        gameTime * 8;


    const armor =
        Math.min(
            0.72,
            0.15 +
            level * 0.012
        );


    enemies.push({

        x: x,
        y: y,

        radius: 34,

        hp: hp,
        maxHp: hp,

        speed: 0.43,

        damage:
            15 +
            level * 0.7,

        cooldown: 0,

        boss: true,

        armor: armor

    });

}


/* ======================================
   적 이동
====================================== */

function updateEnemies(delta) {

    for (
        const enemy of enemies
    ) {

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

            enemy.cooldown -=
                delta;


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


/* ======================================
   플레이어 피해
====================================== */

function damagePlayer(
    amount
) {

    let damage =
        amount *
        (
            1 -
            player.damageReduction
        );


    /*
       파란 방어막 먼저
    */

    if (
        player.shield > 0
    ) {

        const blocked =
            Math.min(
                player.shield,
                damage
            );


        player.shield -=
            blocked;

        damage -=
            blocked;

    }


    if (
        damage > 0
    ) {

        player.hp -=
            damage;

    }


    if (
        player.hp <= 0
    ) {

        player.hp = 0;

        gameOver();

    }

}


/* ======================================
   처치
====================================== */

function processDeaths() {

    const alive = [];


    for (
        const enemy of enemies
    ) {

        if (
            enemy.hp <= 0
        ) {

            kills++;

            player.skillCharge++;


            const value =
                enemy.boss
                ? 20
                : 1;


            gems.push({

                x: enemy.x,
                y: enemy.y,

                value: value

            });

        }

        else {

            alive.push(enemy);

        }

    }


    enemies = alive;

}


/* ======================================
   경험치
====================================== */

function collectXP() {

    for (
        let i = gems.length - 1;
        i >= 0;
        i--
    ) {

        const gem =
            gems[i];


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


        if (
            distance <
            70 *
            player.area
        ) {

            xp +=
                gem.value *
                player.xpMultiplier;


            gems.splice(
                i,
                1
            );

        }

    }


    while (
        xp >= xpNeed
    ) {

        xp -=
            xpNeed;

        level++;


        /*
           레벨업 필요 경험치가
           너무 급격하게 증가하지 않도록
        */

        xpNeed =
            Math.floor(
                xpNeed * 1.16 + 3
            );


        showLevelUp();

        break;

    }

}


/* ======================================
   총 업그레이드
====================================== */

function gunUpgrades() {

    return [

        {
            text:
                "🔫 공격력 +8%",
            effect:
                () =>
                    player.damage *= 1.08
        },

        {
            text:
                "⚡ 공격속도 +7%",
            effect:
                () =>
                    player.attackSpeed *= 0.93
        },

        {
            text:
                "🔫 발사체 +1",
            effect:
                () =>
                    player.projectileCount++
        },

        {
            text:
                "🎯 사거리 +10%",
            effect:
                () =>
                    player.range *= 1.10
        },

        {
            text:
                "💨 탄속 +10%",
            effect:
                () =>
                    player.projectileSpeed *= 1.10
        },

        {
            text:
                "❤️ 최대 체력 +10",
            effect:
                () => {
                    player.maxHp += 10;
                    player.hp += 10;
                }
        }

    ];

}


/* ======================================
   검 업그레이드
====================================== */

function swordUpgrades() {

    return [

        {
            text:
                "⚔️ 공격력 +8%",
            effect:
                () =>
                    player.damage *= 1.08
        },

        {
            text:
                "🛡️ 피해 감소 +4%",
            effect:
                () => {
                    player.damageReduction =
                        Math.min(
                            0.65,
                            player.damageReduction +
                            0.04
                        );
                }
        },

        {
            text:
                "❤️ 최대 체력 +15",
            effect:
                () => {
                    player.maxHp += 15;
                    player.hp += 15;
                }
        },

        {
            text:
                "⚔️ 검 범위 +10%",
            effect:
                () =>
                    player.range *= 1.10
        },

        {
            text:
                "💥 부채꼴 범위 +8%",
            effect:
                () =>
                    player.area *= 1.08
        },

        {
            text:
                "🏃 이동속도 +7%",
            effect:
                () =>
                    player.speed *= 1.07
        },

        {
            text:
                "🔵 방어막 충전 필요 처치 -1",
            effect:
                () =>
                    player.skillNeed =
                        Math.max(
                            6,
                            player.skillNeed - 1
                        )
        }

    ];

}


/* ======================================
   마법 업그레이드
====================================== */

function magicUpgrades() {

    return [

        {
            text:
                "🔮 마법 공격력 +8%",
            effect:
                () =>
                    player.damage *= 1.08
        },

        {
            text:
                "⚡ 마법 공격속도 +7%",
            effect:
                () =>
                    player.attackSpeed *= 0.93
        },

        {
            text:
                "💥 광역 범위 +10%",
            effect:
                () =>
                    player.area *= 1.10
        },

        {
            text:
                "🔮 마법탄 +1",
            effect:
                () =>
                    player.projectileCount++
        },

        {
            text:
                "⛓️ 강화 공격 주기 -1회",
            effect:
                () =>
                    player.magicEnhancedNeed =
                        Math.max(
                            3,
                            player.magicEnhancedNeed - 1
                        )
        },

        {
            text:
                "⛓️ 강화 사슬 공격력 +12%",
            effect:
                () =>
                    player.damage *= 1.12
        },

        {
            text:
                "❤️ 최대 체력 +10",
            effect:
                () => {
                    player.maxHp += 10;
                    player.hp += 10;
                }
        }

    ];

}


/* ======================================
   레벨업 화면
====================================== */

function showLevelUp() {

    gameRunning = false;


    let upgrades;


    if (
        weapon === "gun"
    ) {

        upgrades =
            gunUpgrades();

    }

    else if (
        weapon === "sword"
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
            Math.random() -
            0.5
    );


    const list =
        document.getElementById(
            "upgradeList"
        );


    list.innerHTML = "";


    upgrades
        .slice(0, 3)
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


                list.appendChild(
                    button
                );

            }
        );


    document.getElementById(
        "levelUp"
    ).style.display =
    "block";

}


/* ======================================
   적 생성 속도
====================================== */

function updateSpawning(delta) {

    spawnTimer -=
        delta;


    /*
       시간이 지날수록
       생성 간격 감소
    */

    const interval =
        Math.max(
            900 -
            gameTime * 9,
            170
        );


    if (
        spawnTimer <= 0
    ) {

        const amount =
            Math.min(
                1 +
                Math.floor(
                    gameTime / 18
                ),
                12
            );


        for (
            let i = 0;
            i < amount;
            i++
        ) {

            spawnEnemy();

        }


        spawnTimer =
            interval;

    }

}


/* ======================================
   시간 + 보스
====================================== */

function updateTime(delta) {

    gameTime +=
        delta / 1000;


    if (
        gameTime >=
        nextBossTime
    ) {

        spawnBoss();

        nextBossTime +=
            100;

    }


    document.getElementById(
        "time"
    ).textContent =
        Math.floor(
            gameTime
        );

}


/* ======================================
   효과
====================================== */

function updateEffects() {

    for (
        const effect of effects
    ) {

        effect.life--;

    }


    effects =
        effects.filter(
            e =>
                e.life > 0
        );

}


/* ======================================
   그리기
====================================== */

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    ctx.fillStyle =
        "#151522";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /*
       배경 격자
    */

    ctx.strokeStyle =
        "rgba(255,255,255,0.035)";


    for (
        let x = 0;
        x < canvas.width;
        x += 40
    ) {

        ctx.beginPath();

        ctx.moveTo(
            x,
            0
        );

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

        ctx.moveTo(
            0,
            y
        );

        ctx.lineTo(
            canvas.width,
            y
        );

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
            gem.value > 5
                ? 8
                : 5,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            gem.value > 5
                ? "#ffd166"
                : "#55dfff";

        ctx.fill();

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
            Math.PI * 2
        );


        ctx.fillStyle =
            enemy.boss
                ? "#a83255"
                : "#7661ca";

        ctx.fill();


        if (
            enemy.boss
        ) {

            ctx.strokeStyle =
                "#ffd166";

            ctx.lineWidth = 4;

            ctx.stroke();

        }


        /*
           눈
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
           HP
        */

        const barWidth =
            enemy.boss
                ? 75
                : 32;


        ctx.fillStyle =
            "#333";

        ctx.fillRect(
            enemy.x -
            barWidth / 2,
            enemy.y -
            enemy.radius -
            10,
            barWidth,
            5
        );


        ctx.fillStyle =
            enemy.boss
                ? "#ff405c"
                : "#55dd70";


        ctx.fillRect(
            enemy.x -
            barWidth / 2,
            enemy.y -
            enemy.radius -
            10,
            barWidth *
            Math.max(
                0,
                enemy.hp /
                enemy.maxHp
            ),
            5
        );


        if (
            enemy.boss
        ) {

            ctx.fillStyle =
                "#ffd166";

            ctx.font =
                "bold 12px Arial";

            ctx.textAlign =
                "center";

            ctx.fillText(
                "BOSS",
                enemy.x,
                enemy.y -
                enemy.radius -
                17
            );

        }

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
            Math.PI * 2
        );


        ctx.fillStyle =
            p.type === "bullet"
                ? "#ffd166"
                : "#d878ff";

        ctx.fill();

    }


    /*
       검 부채꼴
    */

    for (
        const effect of effects
    ) {

        if (
            effect.type ===
            "swordFan"
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
                effect.angle -
                effect.fan / 2,
                effect.angle +
                effect.fan / 2
            );


            ctx.closePath();


            ctx.fillStyle =
                "rgba(220,235,255,0.30)";

            ctx.fill();


            ctx.strokeStyle =
                "rgba(235,245,255,0.85)";

            ctx.lineWidth = 4;

            ctx.stroke();

        }


        /*
           마법 사슬
        */

        if (
            effect.type ===
            "chain"
        ) {

            ctx.fillStyle =
                "rgba(175,90,255,0.60)";

            ctx.fillRect(
                effect.x -
                effect.width / 2,
                0,
                effect.width,
                canvas.height
            );


            ctx.strokeStyle =
                "white";

            ctx.lineWidth = 5;

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


        /*
           검 방어막
        */

        if (
            effect.type ===
            "shield"
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
                "#36a9ff";

            ctx.lineWidth = 7;

            ctx.stroke();

        }


        /*
           총 스킬 효과
        */

        if (
            effect.type ===
            "gunSkill"
        ) {

            ctx.beginPath();

            ctx.arc(
                player.x,
                player.y,
                30,
                0,
                Math.PI * 2
            );


            ctx.strokeStyle =
                "#ffd166";

            ctx.lineWidth = 4;

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


    if (
        weapon === "gun"
    ) {

        ctx.fillStyle =
            "#e7a35e";

    }

    else if (
        weapon === "sword"
    ) {

        ctx.fillStyle =
            "#dcecff";

    }

    else {

        ctx.fillStyle =
            "#b76cff";

    }


    ctx.fill();


    /*
       플레이어 바라보는 방향 표시
    */

    ctx.strokeStyle =
        "rgba(255,255,255,0.8)";

    ctx.lineWidth = 3;

    ctx.beginPath();

    ctx.moveTo(
        player.x,
        player.y
    );

    ctx.lineTo(
        player.x +
        player.facingX *
        25,

        player.y +
        player.facingY *
        25
    );

    ctx.stroke();


    /*
       방어막
    */

    if (
        player.shield > 0
    ) {

        ctx.beginPath();

        ctx.arc(
            player.x,
            player.y,
            player.radius + 9,
            0,
            Math.PI * 2
        );


        ctx.strokeStyle =
            "#299cff";

        ctx.lineWidth = 6;

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
       방어막 표시
    */

    if (
        player.shield > 0
    ) {

        ctx.fillStyle =
            "#4db5ff";

        ctx.font =
            "bold 11px Arial";

        ctx.textAlign =
            "center";

        ctx.fillText(
            "SHIELD " +
            Math.floor(
                player.shield
            ),
            player.x,
            player.y + 48
        );

    }


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
        skillRatio >= 1
            ? "#b276ff"
            : "#7042a8";


    ctx.fillRect(
        player.x - 30,
        player.y + 27,
        60 *
        skillRatio,
        5
    );

}


/* ======================================
   UI
====================================== */

function updateUI() {

    document.getElementById(
        "level"
    ).textContent =
        level;


    document.getElementById(
        "hp"
    ).textContent =
        Math.ceil(player.hp) +
        "/" +
        Math.ceil(player.maxHp);


    document.getElementById(
        "shield"
    ).textContent =
        Math.floor(
            player.shield
        );


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


    const skillButton =
        document.getElementById(
            "skillButton"
        );


    if (
        player.skillCharge >=
        player.skillNeed
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

}


/* ======================================
   게임오버
====================================== */

function gameOver() {

    gameRunning = false;

    document.getElementById(
        "gameOver"
    ).style.display =
    "block";

}


/* ======================================
   무기 선택으로 돌아가기
====================================== */

function returnToSelect() {

    gameRunning = false;

    document.getElementById(
        "gameOver"
    ).style.display =
    "none";

    document.getElementById(
        "gameArea"
    ).style.display =
    "none";

    document.getElementById(
        "weaponSelect"
    ).style.display =
    "block";

}


/* ======================================
   스킬 버튼
====================================== */

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


/* ======================================
   메인 루프
====================================== */

function gameLoop(time) {

    const delta =
        Math.min(
            time -
            lastTime,
            40
        );


    lastTime =
        time;


    if (gameRunning) {

        updateTime(delta);

        movePlayer();

        updateSpawning(delta);

        updateEnemies(delta);

        updateProjectiles();

        processDeaths();

        collectXP();

        updateSkill(delta);

        updateEffects();


        /*
           자동 공격
        */

        attackTimer -=
            delta;


        let currentSpeed =
            player.attackSpeed;


        /*
           총 스킬 동안
           공격속도 4배
        */

        if (
            weapon === "gun" &&
            player.skillActive
        ) {

            currentSpeed *=
                0.25;

        }


        if (
            attackTimer <= 0
        ) {

            attack();

            attackTimer =
                currentSpeed;

        }


        updateUI();

    }


    draw();


    requestAnimationFrame(
        gameLoop
    );

}


/* ======================================
   시작
====================================== */

document.getElementById(
    "gameArea"
).style.display =
"none";

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
