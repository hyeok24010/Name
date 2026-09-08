import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NURURUNG SURVIVOR",
    page_icon="👾",
    layout="centered"
)

html = r'''
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

#gameBox {
    width: 100%;
    max-width: 900px;
    margin: auto;
}

#info {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    color: white;
    font-size: 13px;
    margin: 5px;
    gap: 8px;
}

canvas {
    display: block;
    width: 100%;
    max-width: 850px;
    height: auto;
    margin: auto;
    background: #151522;
    border: 2px solid #555;
    border-radius: 10px;
    touch-action: none;
}

#mobileControls {
    position: relative;
    width: 100%;
    max-width: 850px;
    height: 125px;
    margin: auto;
}

#joystick {
    position: absolute;
    left: 12px;
    bottom: 5px;
    width: 105px;
    height: 105px;
    border-radius: 50%;
    background: rgba(120,120,140,0.35);
    border: 2px solid rgba(255,255,255,0.25);
}

#stick {
    position: absolute;
    left: 27px;
    top: 27px;
    width: 51px;
    height: 51px;
    border-radius: 50%;
    background: rgba(220,220,220,0.7);
}

#skillButton {
    position: absolute;
    right: 18px;
    bottom: 12px;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    border: 3px solid #a77bff;
    background: #57329b;
    color: white;
    font-size: 28px;
    font-weight: bold;
}

#skillButton.ready {
    background: #8655e8;
}

#levelup {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 600px;
    background: rgba(15,15,25,0.98);
    border: 2px solid #777;
    border-radius: 15px;
    padding: 18px;
    display: none;
    z-index: 50;
    color: white;
}

.upgrade {
    display: block;
    width: 100%;
    margin: 9px 0;
    padding: 14px;
    background: #29293b;
    color: white;
    border: 1px solid #666;
    border-radius: 9px;
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
    background: rgba(10,10,15,0.97);
    padding: 30px;
    border-radius: 15px;
    color: white;
    font-size: 30px;
    text-align: center;
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
</style>
</head>

<body>

<div id="gameBox">

<div id="info">
    <span>LV <b id="level">1</b></span>
    <span>❤️ <b id="hp">100/100</b></span>
    <span>🛡️ <b id="shield">0</b></span>
    <span>XP <b id="xp">0/10</b></span>
    <span>☠️ <b id="kills">0</b></span>
    <span>⏱️ <b id="time">0</b></span>
</div>

<canvas id="game" width="850" height="600"></canvas>

<div id="mobileControls">

    <div id="joystick">
        <div id="stick"></div>
    </div>

    <button id="skillButton">⚡</button>

</div>

<div id="levelup">

    <h2 id="upgradeTitle">LEVEL UP!</h2>

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

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let gameRunning = true;

let weapon = "gun";

let level = 1;
let xp = 0;
let xpNeed = 10;

let kills = 0;
let gameTime = 0;

let spawnTimer = 0;
let attackTimer = 0;
let bossTimer = 100;

let lastTime = performance.now();

let enemies = [];
let projectiles = [];
let gems = [];
let effects = [];


/* =========================================
   플레이어
========================================= */

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

    range: 260,

    area: 1,

    projectileSpeed: 8,

    projectileCount: 1,

    damageReduction: 0,

    xpMultiplier: 1,

    skillCharge: 0,

    skillNeed: 15,

    skillActive: false,

    skillTimer: 0,

    magicAttackCount: 0,

    magicEnhancedNeed: 10

};


/* =========================================
   키보드
========================================= */

const keys = {};

document.addEventListener("keydown", function(e) {
    keys[e.key.toLowerCase()] = true;
});

document.addEventListener("keyup", function(e) {
    keys[e.key.toLowerCase()] = false;
});


/* =========================================
   모바일 조이스틱
========================================= */

const joystick = document.getElementById("joystick");
const stick = document.getElementById("stick");

let joystickActive = false;
let joyX = 0;
let joyY = 0;

const joystickRadius = 42;

function updateJoystick(x, y) {

    const rect = joystick.getBoundingClientRect();

    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    let dx = x - centerX;
    let dy = y - centerY;

    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance > joystickRadius) {

        dx = dx / distance * joystickRadius;
        dy = dy / distance * joystickRadius;

    }

    joyX = dx / joystickRadius;
    joyY = dy / joystickRadius;

    stick.style.left = (27 + dx) + "px";
    stick.style.top = (27 + dy) + "px";
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


/* =========================================
   무기 설정
========================================= */

function setupPlayer() {

    player.x = 425;
    player.y = 300;

    player.shield = 0;

    player.damageReduction = 0;

    player.projectileCount = 1;

    player.area = 1;

    player.projectileSpeed = 8;

    player.xpMultiplier = 1;

    player.skillCharge = 0;

    player.magicAttackCount = 0;

    player.magicEnhancedNeed = 10;


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

        player.damage = 23;

        player.attackSpeed = 750;

        player.range = 105;

        player.area = 1.15;

        player.damageReduction = 0.10;

        player.skillNeed = 12;

    }


    if (weapon === "magic") {

        player.maxHp = 100;
        player.hp = 100;

        player.speed = 3.3;

        player.damage = 17;

        player.attackSpeed = 720;

        player.range = 300;

        player.area = 1.25;

        player.projectileSpeed = 7;

        player.skillNeed = 12;

    }

}


/* =========================================
   적 생성
========================================= */

function spawnEnemy() {

    const side = Math.floor(Math.random() * 4);

    let x;
    let y;

    if (side === 0) {

        x = Math.random() * canvas.width;
        y = -30;

    }

    else if (side === 1) {

        x = canvas.width + 30;
        y = Math.random() * canvas.height;

    }

    else if (side === 2) {

        x = Math.random() * canvas.width;
        y = canvas.height + 30;

    }

    else {

        x = -30;
        y = Math.random() * canvas.height;

    }


    const hp =
        22 +
        gameTime * 1.8 +
        level * 5;


    enemies.push({

        x: x,
        y: y,

        radius: 15,

        hp: hp,
        maxHp: hp,

        speed:
            0.65 +
            Math.random() * 0.3 +
            gameTime * 0.003,

        damage:
            5 +
            gameTime * 0.05,

        cooldown: 0,

        boss: false,

        armor: 0

    });

}


/* =========================================
   보스 생성
========================================= */

function spawnBoss() {

    const side = Math.floor(Math.random() * 4);

    let x;
    let y;

    if (side === 0) {

        x = canvas.width / 2;
        y = -70;

    }

    else if (side === 1) {

        x = canvas.width + 70;
        y = canvas.height / 2;

    }

    else if (side === 2) {

        x = canvas.width / 2;
        y = canvas.height + 70;

    }

    else {

        x = -70;
        y = canvas.height / 2;

    }


    /*
       보스 HP는 현재 레벨과
       생존 시간에 따라 증가
    */

    const bossHp =
        600 +
        level * 120 +
        gameTime * 8;


    const armor =
        Math.min(
            0.70,
            0.15 +
            level * 0.012
        );


    enemies.push({

        x: x,
        y: y,

        radius: 32,

        hp: bossHp,
        maxHp: bossHp,

        speed: 0.42,

        damage:
            15 +
            level * 0.7,

        cooldown: 0,

        boss: true,

        armor: armor

    });

}


/* =========================================
   이동
========================================= */

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


    if (joystickActive) {

        dx += joyX;
        dy += joyY;

    }


    const length = Math.sqrt(dx * dx + dy * dy);

    if (length > 0) {

        dx /= length;
        dy /= length;

    }


    player.x += dx * player.speed;
    player.y += dy * player.speed;


    player.x = Math.max(
        player.radius,
        Math.min(
            canvas.width - player.radius,
            player.x
        )
    );


    player.y = Math.max(
        player.radius,
        Math.min(
            canvas.height - player.radius,
            player.y
        )
    );

}


/* =========================================
   가까운 적
========================================= */

function nearestEnemy() {

    let target = null;

    let best =
        player.range *
        player.range;


    for (const enemy of enemies) {

        const dx = enemy.x - player.x;
        const dy = enemy.y - player.y;

        const d = dx * dx + dy * dy;

        if (d < best) {

            best = d;
            target = enemy;

        }

    }

    return target;

}


/* =========================================
   총
========================================= */

function gunAttack() {

    const target = nearestEnemy();

    if (!target) return;


    const dx = target.x - player.x;
    const dy = target.y - player.y;

    const distance =
        Math.sqrt(dx * dx + dy * dy);


    const count = player.projectileCount;


    for (let i = 0; i < count; i++) {

        let angle =
            Math.atan2(dy, dx);


        /*
           여러 발이면 약간 퍼짐
        */

        if (count > 1) {

            angle +=
                (i - (count - 1) / 2)
                * 0.10;

        }


        projectiles.push({

            x: player.x,
            y: player.y,

            dx:
                Math.cos(angle) *
                player.projectileSpeed,

            dy:
                Math.sin(angle) *
                player.projectileSpeed,

            damage: player.damage,

            radius: 5,

            type: "bullet"

        });

    }

}


/* =========================================
   검
========================================= */

function swordAttack() {

    const radius =
        player.range *
        player.area;


    effects.push({

        type: "slash",

        x: player.x,
        y: player.y,

        radius: radius,

        life: 12

    });


    for (const enemy of enemies) {

        const dx = enemy.x - player.x;
        const dy = enemy.y - player.y;

        const distance =
            Math.sqrt(dx * dx + dy * dy);


        if (distance < radius) {

            dealDamage(
                enemy,
                player.damage
            );

        }

    }

}


/* =========================================
   마법 기본 공격
========================================= */

function magicAttack() {

    const target = nearestEnemy();

    if (!target) return;


    player.magicAttackCount++;


    /*
       일정 횟수마다 강화 공격
    */

    if (
        player.magicAttackCount >=
        player.magicEnhancedNeed
    ) {

        player.magicAttackCount = 0;

        magicEnhancedAttack();

    }


    /*
       기본 광역 마법탄
    */

    const count =
        player.projectileCount;


    for (let i = 0; i < count; i++) {

        const angle =
            Math.atan2(
                target.y - player.y,
                target.x - player.x
            )
            +
            (i - (count - 1) / 2)
            * 0.12;


        projectiles.push({

            x: player.x,
            y: player.y,

            dx:
                Math.cos(angle) *
                player.projectileSpeed,

            dy:
                Math.sin(angle) *
                player.projectileSpeed,

            damage: player.damage,

            radius:
                9 *
                player.area,

            type: "magic"

        });

    }

}


/* =========================================
   마법 강화 공격
   하늘에서 일직선 사슬
========================================= */

function magicEnhancedAttack() {

    /*
       가장 가까운 적을 기준으로
       수직으로 강력한 사슬 공격
    */

    const target = nearestEnemy();

    if (!target) return;


    const x = target.x;


    effects.push({

        type: "chain",

        x: x,

        y: target.y,

        width:
            45 *
            player.area,

        life: 35

    });


    /*
       해당 세로선에 있는 적들 공격
    */

    for (const enemy of enemies) {

        if (
            Math.abs(enemy.x - x)
            <
            25 *
            player.area
        ) {

            dealDamage(
                enemy,
                player.damage * 3.5
            );

        }

    }

}


/* =========================================
   공격
========================================= */

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


/* =========================================
   피해 계산
========================================= */

function dealDamage(enemy, damage) {

    /*
       보스 방어력
    */

    if (enemy.boss) {

        damage *=
            (1 - enemy.armor);

    }


    enemy.hp -= damage;

}


/* =========================================
   스킬
========================================= */

function useSkill() {

    if (
        player.skillCharge <
        player.skillNeed
    ) {

        return;

    }


    player.skillCharge = 0;


    /*
       총 스킬
       5초간 공격속도 크게 증가
       + 발사체 증가
    */

    if (weapon === "gun") {

        player.skillActive = true;

        player.skillTimer = 5000;

    }


    /*
       검 스킬
       공격하지 않고 방어막 생성
    */

    else if (weapon === "sword") {

        player.skillActive = true;

        player.skillTimer = 6000;

        const shieldAmount =
            60 +
            level * 12;


        player.shield += shieldAmount;


        effects.push({

            type: "shield",

            x: player.x,
            y: player.y,

            radius: 42,

            life: 70

        });

    }


    /*
       마법 스킬
       즉시 강화 사슬 공격
    */

    else {

        player.skillActive = true;

        player.skillTimer = 1500;

        magicEnhancedAttack();

    }

}


/* =========================================
   스킬 업데이트
========================================= */

function updateSkill(delta) {

    if (!player.skillActive) return;


    player.skillTimer -= delta;


    /*
       총 스킬
    */

    if (weapon === "gun") {

        /*
           스킬 중 공격속도와 발사체 수 증가
        */

        if (Math.random() < 0.45) {

            const oldCount =
                player.projectileCount;

            player.projectileCount =
                oldCount + 2;

            gunAttack();

            player.projectileCount =
                oldCount;

        }

    }


    /*
       마법 스킬 종료
    */

    if (
        player.skillTimer <= 0
    ) {

        player.skillActive = false;

    }

}


/* =========================================
   투사체 업데이트
========================================= */

function updateProjectiles() {

    for (const p of projectiles) {

        p.x += p.dx;
        p.y += p.dy;


        for (const enemy of enemies) {

            if (enemy.hp <= 0) continue;


            const dx =
                enemy.x - p.x;

            const dy =
                enemy.y - p.y;


            const distance =
                Math.sqrt(dx * dx + dy * dy);


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
                p.x > -80 &&
                p.x < canvas.width + 80 &&
                p.y > -80 &&
                p.y < canvas.height + 80
        );

}


/* =========================================
   적 업데이트
========================================= */

function updateEnemies(delta) {

    for (const enemy of enemies) {

        const dx =
            player.x -
            enemy.x;

        const dy =
            player.y -
            enemy.y;


        const distance =
            Math.sqrt(dx * dx + dy * dy);


        if (
            distance >
            player.radius +
            enemy.radius
        ) {

            enemy.x +=
                dx / distance *
                enemy.speed;

            enemy.y +=
                dy / distance *
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

                enemy.cooldown = 700;

            }

        }

    }

}


/* =========================================
   플레이어 피해
========================================= */

function damagePlayer(amount) {

    let damage =
        amount *
        (1 - player.damageReduction);


    /*
       방어막이 먼저 피해를 받음
    */

    if (player.shield > 0) {

        const blocked =
            Math.min(
                player.shield,
                damage
            );

        player.shield -= blocked;

        damage -= blocked;

    }


    if (damage > 0) {

        player.hp -= damage;

    }


    if (player.hp <= 0) {

        player.hp = 0;

        gameOver();

    }

}


/* =========================================
   처치 처리
========================================= */

function processDeaths() {

    const alive = [];


    for (const enemy of enemies) {

        if (enemy.hp <= 0) {

            kills++;

            player.skillCharge++;


            /*
               보스는 경험치를 많이 줌
            */

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


/* =========================================
   경험치
========================================= */

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
            Math.sqrt(dx * dx + dy * dy);


        if (
            distance <
            65 *
            player.area
        ) {

            xp +=
                gem.value *
                player.xpMultiplier;

            gems.splice(i, 1);

        }

    }


    if (xp >= xpNeed) {

        xp -= xpNeed;

        level++;


        /*
           레벨업 요구 경험치는
           조금씩 증가
        */

        xpNeed =
            Math.floor(
                xpNeed * 1.18 + 3
            );


        showLevelUp();

    }

}


/* =========================================
   총 전용 업그레이드
========================================= */

function gunUpgrades() {

    return [

        {
            text: "🔫 공격력 +8%",
            effect: function() {
                player.damage *= 1.08;
            }
        },

        {
            text: "⚡ 공격속도 +7%",
            effect: function() {
                player.attackSpeed *= 0.93;
            }
        },

        {
            text: "🔫 발사체 +1",
            effect: function() {
                player.projectileCount += 1;
            }
        },

        {
            text: "🎯 사거리 +10%",
            effect: function() {
                player.range *= 1.10;
            }
        },

        {
            text: "💨 탄속 +10%",
            effect: function() {
                player.projectileSpeed *= 1.10;
            }
        },

        {
            text: "❤️ 최대 체력 +10",
            effect: function() {
                player.maxHp += 10;
                player.hp += 10;
            }
        }

    ];

}


/* =========================================
   검 전용 업그레이드
========================================= */

function swordUpgrades() {

    return [

        {
            text: "⚔️ 공격력 +8%",
            effect: function() {
                player.damage *= 1.08;
            }
        },

        {
            text: "🛡️ 피해 감소 +4%",
            effect: function() {
                player.damageReduction =
                    Math.min(
                        0.65,
                        player.damageReduction + 0.04
                    );
            }
        },

        {
            text: "❤️ 최대 체력 +15",
            effect: function() {
                player.maxHp += 15;
                player.hp += 15;
            }
        },

        {
            text: "⚔️ 공격 범위 +10%",
            effect: function() {
                player.range *= 1.10;
            }
        },

        {
            text: "💥 범위 크기 +8%",
            effect: function() {
                player.area *= 1.08;
            }
        },

        {
            text: "🏃 이동속도 +7%",
            effect: function() {
                player.speed *= 1.07;
            }
        },

        {
            text: "🛡️ 방어막 효과 +10%",
            effect: function() {
                player.skillNeed =
                    Math.max(
                        6,
                        player.skillNeed - 1
                    );
            }
        }

    ];

}


/* =========================================
   마법 전용 업그레이드
========================================= */

function magicUpgrades() {

    return [

        {
            text: "🔮 마법 공격력 +8%",
            effect: function() {
                player.damage *= 1.08;
            }
        },

        {
            text: "⚡ 마법 공격속도 +7%",
            effect: function() {
                player.attackSpeed *= 0.93;
            }
        },

        {
            text: "💥 광역 범위 +10%",
            effect: function() {
                player.area *= 1.10;
            }
        },

        {
            text: "🔮 마법탄 +1",
            effect: function() {
                player.projectileCount += 1;
            }
        },

        {
            text: "⛓️ 강화 공격 발동 횟수 -1",
            effect: function() {

                player.magicEnhancedNeed =
                    Math.max(
                        3,
                        player.magicEnhancedNeed - 1
                    );

            }
        },

        {
            text: "❤️ 최대 체력 +10",
            effect: function() {
                player.maxHp += 10;
                player.hp += 10;
            }
        },

        {
            text: "🧲 경험치 획득 범위 +10%",
            effect: function() {
                player.area *= 1.10;
            }
        }

    ];

}


/* =========================================
   레벨업
========================================= */

function showLevelUp() {

    gameRunning = false;


    let upgrades;


    if (weapon === "gun") {

        upgrades = gunUpgrades();

    }

    else if (weapon === "sword") {

        upgrades = swordUpgrades();

    }

    else {

        upgrades = magicUpgrades();

    }


    /*
       무작위로 섞기
    */

    upgrades.sort(
        () =>
            Math.random() - 0.5
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


/* =========================================
   적 생성
========================================= */

function updateSpawning(delta) {

    spawnTimer -= delta;


    /*
       시간이 지나면 생성 간격 감소
    */

    const interval =
        Math.max(
            900 -
            gameTime * 10,
            180
        );


    if (spawnTimer <= 0) {

        /*
           시간이 지날수록
           한 번에 더 많은 적
        */

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


        spawnTimer = interval;

    }

}


/* =========================================
   시간
========================================= */

function updateTime(delta) {

    gameTime += delta / 1000;


    /*
       100초마다 보스
    */

    if (
        gameTime >= bossTimer
    ) {

        spawnBoss();

        bossTimer += 100;

    }


    document.getElementById(
        "time"
    ).textContent =
        Math.floor(gameTime);

}


/* =========================================
   효과
========================================= */

function updateEffects() {

    for (const effect of effects) {

        effect.life--;

    }


    effects =
        effects.filter(
            e => e.life > 0
        );

}


/* =========================================
   그림
========================================= */

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

        ctx.moveTo(x, 0);

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

        ctx.moveTo(0, y);

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
            gem.value > 5 ? 8 : 5,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            gem.value > 5
            ? "#ffd166"
            : "#65e6ff";

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


        if (enemy.boss) {

            ctx.fillStyle =
                "#a83255";

        }

        else {

            ctx.fillStyle =
                "#8064d8";

        }


        ctx.fill();


        /*
           보스 테두리
        */

        if (enemy.boss) {

            ctx.strokeStyle =
                "#ffcc55";

            ctx.lineWidth = 4;

            ctx.stroke();

        }


        /*
           눈
        */

        ctx.fillStyle = "white";

        ctx.beginPath();

        ctx.arc(
            enemy.x - 5,
            enemy.y - 3,
            enemy.boss ? 4 : 3,
            0,
            Math.PI * 2
        );

        ctx.arc(
            enemy.x + 5,
            enemy.y - 3,
            enemy.boss ? 4 : 3,
            0,
            Math.PI * 2
        );

        ctx.fill();


        /*
           HP 바
        */

        const barWidth =
            enemy.boss ? 70 : 32;


        ctx.fillStyle = "#333";

        ctx.fillRect(
            enemy.x - barWidth / 2,
            enemy.y - enemy.radius - 10,
            barWidth,
            5
        );


        ctx.fillStyle =
            enemy.boss
            ? "#ff455f"
            : "#55e070";


        ctx.fillRect(
            enemy.x - barWidth / 2,
            enemy.y - enemy.radius - 10,
            barWidth *
            Math.max(
                0,
                enemy.hp / enemy.maxHp
            ),
            5
        );


        if (enemy.boss) {

            ctx.fillStyle =
                "#ffd166";

            ctx.font =
                "bold 12px Arial";

            ctx.textAlign =
                "center";

            ctx.fillText(
                "BOSS",
                enemy.x,
                enemy.y - enemy.radius - 17
            );

        }

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
                "#d879ff";

        }


        ctx.fill();

    }


    /*
       효과
    */

    for (const effect of effects) {


        if (
            effect.type === "slash"
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
                "#e9f4ff";

            ctx.lineWidth = 8;

            ctx.stroke();

        }


        /*
           마법 사슬
        */

        if (
            effect.type === "chain"
        ) {

            ctx.fillStyle =
                "rgba(180,100,255,0.65)";

            ctx.fillRect(
                effect.x -
                effect.width / 2,
                0,
                effect.width,
                canvas.height
            );


            ctx.strokeStyle =
                "#ffffff";

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
            effect.type === "shield"
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
                "rgba(80,170,255,0.9)";

            ctx.lineWidth = 7;

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
            "#dcecff";

    }

    else {

        ctx.fillStyle =
            "#b96cff";

    }


    ctx.fill();


    /*
       플레이어 눈
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
       파란 방어막
    */

    if (player.shield > 0) {

        ctx.beginPath();

        ctx.arc(
            player.x,
            player.y,
            player.radius + 9,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle =
            "#3fa9ff";

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
       방어막 숫자
    */

    if (player.shield > 0) {

        ctx.fillStyle =
            "#55baff";

        ctx.font =
            "bold 11px Arial";

        ctx.textAlign =
            "center";

        ctx.fillText(
            "SHIELD " +
            Math.floor(player.shield),
            player.x,
            player.y + 48
        );

    }


    /*
       스킬 게이지
    */

    const ratio =
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
        ratio >= 1
        ? "#b477ff"
        : "#7042a8";


    ctx.fillRect(
        player.x - 30,
        player.y + 27,
        60 * ratio,
        5
    );

}


/* =========================================
   UI
========================================= */

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


/* =========================================
   게임오버
========================================= */

function gameOver() {

    gameRunning = false;

    document.getElementById(
        "gameOver"
    ).style.display =
    "block";

}


/* =========================================
   재시작
========================================= */

function restartGame() {

    level = 1;

    xp = 0;

    xpNeed = 10;

    kills = 0;

    gameTime = 0;

    bossTimer = 100;

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


/* =========================================
   스킬 버튼
========================================= */

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


/*
   PC에서도 스킬 사용 가능
*/

document
.getElementById("skillButton")
.addEventListener(
    "click",
    function() {

        useSkill();

    }
);


/* =========================================
   메인 루프
========================================= */

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

        attackTimer -= delta;


        let currentSpeed =
            player.attackSpeed;


        /*
           총 스킬:
           공격속도 4배
        */

        if (
            weapon === "gun" &&
            player.skillActive
        ) {

            currentSpeed *= 0.25;

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


/* =========================================
   시작
========================================= */

setupPlayer();

requestAnimationFrame(
    gameLoop
);

</script>

</body>
</html>
'''

components.html(
    html,
    height=800,
    scrolling=False
)
