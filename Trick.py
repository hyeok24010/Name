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
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #111;
    color: white;
    font-family: Arial, sans-serif;
    touch-action: none;
}

#wrap {
    position: relative;
    width: 100%;
    height: 100vh;
    min-height: 650px;
    background: #151515;
    overflow: hidden;
}

canvas {
    display: block;
    width: 100%;
    height: 100%;
    background: #182018;
}

#top {
    position: absolute;
    left: 12px;
    right: 12px;
    top: 10px;
    z-index: 5;
    pointer-events: none;
}

.row {
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
}

.bar {
    height: 18px;
    border: 2px solid #333;
    border-radius: 9px;
    background: #333;
    overflow: hidden;
    position: relative;
}

.bar i {
    display: block;
    height: 100%;
    width: 100%;
    transition: width .12s;
}

#hpBar {
    width: min(300px, 48vw);
}

#hpFill {
    background: #e74c3c;
}

#shieldBar {
    width: min(240px, 40vw);
    display: none;
}

#shieldFill {
    background: #3498db;
}

#xpBar {
    width: min(420px, 65vw);
    height: 14px;
}

#xpFill {
    background: #f1c40f;
}

#stats {
    font-size: 14px;
    text-shadow: 0 1px 2px #000;
}

#classInfo {
    font-size: 13px;
    margin-top: 4px;
    text-shadow: 0 1px 2px #000;
}

#message {
    position: absolute;
    top: 42%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    text-shadow: 0 3px 5px #000;
    pointer-events: none;
}

#select,
#levelup,
#gameover {
    position: absolute;
    inset: 0;
    z-index: 20;
    background: rgba(0,0,0,.78);
    display: flex;
    align-items: center;
    justify-content: center;
}

.panel {
    width: min(900px, 92vw);
    max-height: 90vh;
    overflow-y: auto;
    padding: 24px;
    border-radius: 18px;
    background: #20242a;
    border: 2px solid #555;
    text-align: center;
    box-shadow: 0 10px 40px #000;
}

.panel h1 {
    margin: 5px 0 10px;
    font-size: 32px;
}

.panel p {
    color: #bbb;
}

.choices {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 20px;
}

button {
    border: 0;
    border-radius: 14px;
    padding: 16px;
    color: #fff;
    background: #303840;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #46515b;
}

.weaponBtn {
    min-height: 150px;
}

.weaponBtn b {
    display: block;
    font-size: 30px;
    margin-bottom: 10px;
}

.weaponBtn small {
    display: block;
    color: #bbb;
    line-height: 1.5;
}

.upgradeGrid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 18px;
}

.upgrade {
    min-height: 100px;
    text-align: left;
}

.upgrade strong {
    font-size: 18px;
}

.upgrade span {
    display: block;
    color: #bbb;
    font-size: 13px;
    margin-top: 8px;
}

#controls {
    position: absolute;
    inset: 0;
    z-index: 6;
    pointer-events: none;
}

#joystick {
    position: absolute;
    left: 25px;
    bottom: 28px;
    width: 130px;
    height: 130px;
    border-radius: 50%;
    background: rgba(255,255,255,.12);
    border: 2px solid rgba(255,255,255,.2);
    pointer-events: auto;
}

#stick {
    position: absolute;
    left: 37px;
    top: 37px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: rgba(255,255,255,.35);
}

.action {
    position: absolute;
    right: 24px;
    bottom: 32px;
    width: 105px;
    height: 58px;
    padding: 8px;
    font-size: 14px;
    pointer-events: auto;
}

#skillBtn {
    bottom: 100px;
    background: #6941a5;
}

#formBtn {
    bottom: 32px;
    background: #2d607f;
}

.hidden {
    display: none !important;
}

@media(max-width:650px) {

    #wrap {
        min-height: 100vh;
    }

    #stats {
        font-size: 12px;
    }

    #classInfo {
        font-size: 11px;
    }

    .panel {
        padding: 18px;
    }

    .panel h1 {
        font-size: 25px;
    }

    .choices {
        grid-template-columns: 1fr;
    }

    .weaponBtn {
        min-height: 90px;
    }

    .upgradeGrid {
        grid-template-columns: 1fr;
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


<!-- 직업 선택 -->

<div id="select">

    <div class="panel">

        <h1>누루룽 서바이버</h1>

        <p>
            직업을 선택하세요
        </p>

        <div class="choices">

            <button class="weaponBtn"
                    onclick="startGame('gun')">

                <b>🔫 총</b>

                권총 / 저격 폼체인지

                <br>

                <small>
                    빠른 권총 · 강력한 저격 · 투사체 · 관통
                </small>

            </button>


            <button class="weaponBtn"
                    onclick="startGame('sword')">

                <b>⚔️ 검사</b>

                베기 / 검기

                <br>

                <small>
                    부채꼴 베기 · 전방 검기 · 방어막
                </small>

            </button>


            <button class="weaponBtn"
                    onclick="startGame('magic')">

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


<!-- 레벨업 -->

<div id="levelup" class="hidden">

    <div class="panel">

        <h1>LEVEL UP!</h1>

        <p>
            강화할 능력을 하나 선택하세요.
        </p>

        <div id="upgradeGrid" class="upgradeGrid"></div>

    </div>

</div>


<!-- 게임오버 -->

<div id="gameover" class="hidden">

    <div class="panel">

        <h1>게임 오버</h1>

        <p id="result"></p>

        <button onclick="location.reload()">
            다시 시작
        </button>

    </div>

</div>

</div>


<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let W = 0;
let H = 0;
let DPR = 1;

function resize() {

    DPR = Math.min(devicePixelRatio || 1, 2);

    W = canvas.clientWidth;
    H = canvas.clientHeight;

    canvas.width = W * DPR;
    canvas.height = H * DPR;

    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
}

addEventListener("resize", resize);

resize();


const TAU = Math.PI * 2;

function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
}

function rand(a, b) {
    return a + Math.random() * (b - a);
}

function dist(a, b) {
    return Math.hypot(a.x - b.x, a.y - b.y);
}


let state = "select";

let last = 0;

let elapsed = 0;

let nextEnemy = 0;

let nextBoss = 100;

let enemies = [];

let projectiles = [];

let slashes = [];

let lasers = [];

let particles = [];

let player = null;

let level = 1;

let xp = 0;

let xpNeed = 10;

let kills = 0;

let bossCount = 0;

let keys = {};

let joy = {
    x: 0,
    y: 0
};


const classNames = {

    gun: "총",

    sword: "검사",

    magic: "마법"

};


function makePlayer(cls) {

    return {

        cls: cls,

        x: W / 2,

        y: H / 2,

        r: 18,

        face: 0,

        hp: 100,

        maxHp: 100,

        speed: 185,

        damage: 15,

        attackSpeed: 2,

        range: 180,

        area: 1,

        projectileSpeed: 500,

        projectiles: 1,

        penetration: 0,

        shield: 0,

        maxShield: 0,

        damageReduction: 0,


        /* 검사 */

        swordDamage: 22,

        swordSpeed: 1.6,

        swordRange: 90,

        swordFan: 1.25,

        swordWaveDamage: 9,

        swordWaveSpeed: 0.55,

        swordWaveCount: 1,

        swordWaveSize: 12,


        /* 마법 */

        magicDamage: 14,

        magicSpeed: 1.5,

        laserDamage: 28,

        laserDuration: 0.8,

        laserCount: 1,

        enhancedEvery: 10,

        enhancedCounter: 0,


        /* 스킬 */

        skillReady: false,

        skillKills: 0,

        skillKillsOriginal: 12,

        skillDuration: 5,

        skillActive: false,

        skillTimer: 0,

        skillCooldown: 0,


        /* 총 폼 */

        gunForm: "pistol",

        formCooldown: 0,

        gunSkillTimer: 0,


        invuln: 0,

        attackTimer: 0,

        waveTimer: 0

    };

}


function startGame(cls) {

    player = makePlayer(cls);

    state = "playing";

    document.getElementById("select").classList.add("hidden");

    document.getElementById("formBtn").classList.toggle(
        "hidden",
        cls !== "gun"
    );

    updateUI();

    requestAnimationFrame(loop);

}


function nearestEnemy() {

    let best = null;

    let bd = Infinity;

    for (const e of enemies) {

        const d = dist(player, e);

        if (d < bd) {

            bd = d;

            best = e;

        }

    }

    return best;

}


function nearestAngle() {

    const e = nearestEnemy();

    if (!e) return player.face;

    return Math.atan2(
        e.y - player.y,
        e.x - player.x
    );

}


/* =========================================================
   총
========================================================= */

function shootGun() {

    const p = player;

    const target = nearestEnemy();

    if (!target) return;

    const base = nearestAngle();

    p.face = base;


    let count = p.projectiles;

    let dmg = p.damage;

    let speed = p.projectileSpeed;

    let penetration = p.penetration;

    let range = p.range;


    /* 권총 */

    if (p.gunForm === "pistol") {

        dmg *= 0.8;

        speed *= 1.2;

        range *= 0.9;

    }


    /* 저격 */

    else {

        dmg *= 1.9;

        speed *= 1.05;

        range *= 1.45;

        penetration += 2;

    }


    /* 총 스킬 중 */

    if (p.gunSkillTimer > 0) {

        dmg *= 1.35;

        speed *= 1.25;

    }


    for (let i = 0; i < count; i++) {

        const spread =
            (i - (count - 1) / 2) * 0.10;

        projectiles.push({

            x: p.x,

            y: p.y,

            a: base + spread,

            speed: speed,

            dmg: dmg,

            pen: penetration,

            range: range,

            travel: 0,

            r: 5,

            type: "gun"

        });

    }

}


/* =========================================================
   검사 - 베기
========================================================= */

function swordSlash() {

    const p = player;

    p.face = nearestAngle();

    slashes.push({

        x: p.x,

        y: p.y,

        a: p.face,

        life: 0.18,

        max: 0.18,

        range: p.swordRange * p.area,

        fan: p.swordFan,

        dmg: p.swordDamage

    });

}


/* =========================================================
   검사 - 검기
========================================================= */

function swordWave() {

    const p = player;

    const target = nearestEnemy();

    if (!target) return;

    const a = Math.atan2(
        target.y - p.y,
        target.x - p.x
    );

    p.face = a;


    for (let i = 0; i < p.swordWaveCount; i++) {

        const spread =
            (i - (p.swordWaveCount - 1) / 2) * 0.12;

        projectiles.push({

            x: p.x,

            y: p.y,

            a: a + spread,

            speed: 360,

            dmg: p.swordWaveDamage,

            /*
             * 999999 = 사실상 모든 적 관통
             */

            pen: 999999,

            range: p.range * 1.25,

            travel: 0,

            r: p.swordWaveSize * p.area,

            type: "wave"

        });

    }

}


/* =========================================================
   마법 기본공격 / 강화공격
========================================================= */

function magicBasic() {

    const p = player;

    const target = nearestEnemy();

    if (!target) return;

    const a = Math.atan2(
        target.y - p.y,
        target.x - p.x
    );

    p.face = a;


    /*
     * 각성 중이면 모든 평타가 강화공격
     */

    const enhanced =
        p.skillActive ||
        p.enhancedCounter >= p.enhancedEvery;


    if (enhanced) {

        p.enhancedCounter = 0;

        /*
         * 평상시 강화공격:
         * 가로 또는 세로 하나만
         */

        if (!p.skillActive) {

            const vertical =
                Math.random() < 0.5;

            makeLasers(vertical);

        }


        /*
         * 각성:
         * 가로 + 세로 모두
         */

        else {

            makeAwakeningLasers();

        }

    }


    else {

        p.enhancedCounter++;

        projectiles.push({

            x: p.x,

            y: p.y,

            a: a,

            speed: 430,

            dmg: p.magicDamage,

            pen: 0,

            range: p.range,

            travel: 0,

            r: 6,

            type: "magic"

        });

    }

}


/* =========================================================
   일반 강화공격 레이저
========================================================= */

function makeLasers(vertical) {

    const p = player;

    const angle =
        vertical
            ? Math.PI / 2
            : 0;


    for (let i = 0; i < p.laserCount; i++) {

        const offset =
            (i - (p.laserCount - 1) / 2)
            * 34
            * p.area;


        lasers.push({

            x: p.x,

            y: p.y,

            a: angle,

            offset: offset,

            life: p.laserDuration,

            max: p.laserDuration,

            dmg: p.laserDamage * p.area

        });

    }

}


/* =========================================================
   각성 레이저
========================================================= */

function makeAwakeningLasers() {

    const p = player;


    /*
     * 가로
     */

    makeLaserDirection(0);


    /*
     * 세로
     */

    makeLaserDirection(Math.PI / 2);

}


function makeLaserDirection(angle) {

    const p = player;

    for (let i = 0; i < p.laserCount; i++) {

        const offset =
            (i - (p.laserCount - 1) / 2)
            * 34
            * p.area;


        lasers.push({

            x: p.x,

            y: p.y,

            a: angle,

            offset: offset,

            life: p.laserDuration,

            max: p.laserDuration,

            dmg:
                p.laserDamage
                * p.area
                * 1.35

        });

    }

}


/* =========================================================
   스킬
========================================================= */

function useSkill() {

    const p = player;

    if (!p) return;


    /*
     * 마법 - 각성
     */

    if (p.cls === "magic") {

        if (p.skillActive) return;

        if (p.skillKills < p.skillKillsNeeded) return;

        p.skillKills = 0;

        p.skillActive = true;

        p.skillTimer = p.skillDuration;

        return;

    }


    /*
     * 검사 - 방어막
     */

    if (p.cls === "sword") {

        if (p.skillCooldown > 0) return;

        p.shield = p.maxShield =
            Math.max(
                50,
                p.maxHp * 0.75
            );

        p.skillCooldown = 8;

        return;

    }


    /*
     * 총 - 강화 사격
     */

    if (p.cls === "gun") {

        if (p.skillCooldown > 0) return;

        p.skillCooldown = 6;

        p.gunSkillTimer = 2.5;

    }

}


/* =========================================================
   폼체인지
========================================================= */

function formChange() {

    const p = player;

    if (!p) return;

    if (p.cls !== "gun") return;

    if (p.formCooldown > 0) return;

    p.gunForm =
        p.gunForm === "pistol"
            ? "sniper"
            : "pistol";

    p.formCooldown = 1.5;

}


/* =========================================================
   적 생성
========================================================= */

function spawnEnemy(boss = false) {

    const side =
        Math.floor(Math.random() * 4);

    const margin = 45;

    let x;
    let y;


    if (side === 0) {

        x = -margin;
        y = rand(0, H);

    }

    else if (side === 1) {

        x = W + margin;
        y = rand(0, H);

    }

    else if (side === 2) {

        x = rand(0, W);
        y = -margin;

    }

    else {

        x = rand(0, W);
        y = H + margin;

    }


    const t = elapsed;


    const hp =
        (
            10
            + t * 0.09
            + level * 0.7
        )
        * (boss ? 18 : 1);


    enemies.push({

        x: x,

        y: y,

        r: boss ? 28 : 13,

        hp: hp,

        maxHp: hp,

        speed:
            (boss ? 35 : 45)
            + Math.min(
                35,
                t * 0.035
            ),

        dmg:
            (boss ? 10 : 5)
            + t * 0.012
            + level * 0.1,

        boss: boss

    });

}


/* =========================================================
   경험치
========================================================= */

function gainXP(amount) {

    xp += amount;


    while (xp >= xpNeed) {

        xp -= xpNeed;

        level++;

        xpNeed =
            Math.floor(
                10 + level * 4
            );

        showLevelUp();

        /*
         * 한 번에 여러 레벨이 오르는 것을 방지
         */

        break;

    }

}


/* =========================================================
   적 처치
========================================================= */

function enemyKilled(enemy) {

    kills++;

    gainXP(
        enemy.boss ? 15 : 1
    );


    /*
     * 중요:
     *
     * 각성 중에는 스킬 게이지가
     * 절대로 증가하지 않는다.
     */

    if (!player.skillActive) {

        player.skillKills =
            Math.min(
                player.skillKillsNeeded,
                player.skillKills + 1
            );

    }


    for (let i = 0; i < 3; i++) {

        particles.push({

            x: enemy.x,

            y: enemy.y,

            vx: rand(-60, 60),

            vy: rand(-60, 60),

            life: 0.35

        });

    }

}


/* =========================================================
   적 피해
========================================================= */

function hitEnemy(enemy, damage) {

    enemy.hp -= damage;


    if (enemy.hp <= 0) {

        const index =
            enemies.indexOf(enemy);

        if (index >= 0) {

            enemies.splice(index, 1);

        }

        enemyKilled(enemy);

    }

}


/* =========================================================
   플레이어 피해
========================================================= */

function damagePlayer(damage) {

    const p = player;

    if (p.invuln > 0) return;


    let d =
        damage *
        (1 - p.damageReduction);


    /*
     * 검사 방어막
     */

    if (p.shield > 0) {

        const blocked =
            Math.min(
                p.shield,
                d
            );

        p.shield -= blocked;

        d -= blocked;

    }


    p.hp -= d;

    p.invuln = 0.25;


    if (p.hp <= 0) {

        gameOver();

    }

}


/* =========================================================
   레벨업 보상
========================================================= */

function showLevelUp() {

    state = "levelup";


    const grid =
        document.getElementById(
            "upgradeGrid"
        );


    grid.innerHTML = "";


    const options =
        makeUpgrades();


    options.forEach(option => {

        const button =
            document.createElement("button");


        button.className = "upgrade";


        button.innerHTML =
            "<strong>"
            + option.name
            + "</strong>"
            +
            "<span>"
            + option.desc
            + "</span>";


        button.onclick = () => {

            option.apply();

            document
                .getElementById("levelup")
                .classList.add("hidden");

            state = "playing";

            updateUI();

        };


        grid.appendChild(button);

    });


    document
        .getElementById("levelup")
        .classList.remove("hidden");

}


/* =========================================================
   레벨업 옵션
========================================================= */

function makeUpgrades() {

    const p = player;

    const options = [];


    function add(name, desc, apply) {

        options.push({

            name: name,

            desc: desc,

            apply: apply

        });

    }


    /* =====================================================
       총
    ===================================================== */

    if (p.cls === "gun") {

        add(
            "🔫 투사체 수 +1",
            "기본 공격과 스킬의 총알 수가 증가합니다.",
            () => {
                p.projectiles++;
            }
        );


        add(
            "🎯 관통 +1",
            "총알이 추가 적 1명을 관통합니다.",
            () => {
                p.penetration++;
            }
        );


        add(
            "💥 공격력 +15%",
            "권총과 저격 모두의 기본 공격력이 증가합니다.",
            () => {
                p.damage *= 1.15;
            }
        );


        add(
            "⚡ 공격속도 +15%",
            "총의 발사 속도가 증가합니다.",
            () => {
                p.attackSpeed *= 1.15;
            }
        );


        add(
            "📏 사거리 +15%",
            "총알의 최대 사거리가 증가합니다.",
            () => {
                p.range *= 1.15;
            }
        );


        add(
            "❤️ 최대 HP +20",
            "최대 체력이 증가합니다.",
            () => {
                p.maxHp += 20;
                p.hp += 20;
            }
        );

    }


    /* =====================================================
       검사
    ===================================================== */

    else if (p.cls === "sword") {

        add(
            "⚔️ 검기 개수 +1",
            "한 번에 발사하는 검기의 개수가 증가합니다.",
            () => {
                p.swordWaveCount++;
            }
        );


        add(
            "📐 공격 범위 +15%",
            "베기 범위와 검기 크기가 증가합니다.",
            () => {
                p.area *= 1.15;
            }
        );


        add(
            "🗡️ 베기 공격력 +15%",
            "근접 베기의 피해가 증가합니다.",
            () => {
                p.swordDamage *= 1.15;
            }
        );


        add(
            "⚡ 베기 공격속도 +15%",
            "베기 공격 속도가 증가합니다.",
            () => {
                p.swordSpeed *= 1.15;
            }
        );


        add(
            "💨 검기 공격력 +15%",
            "검기의 피해가 증가합니다.",
            () => {
                p.swordWaveDamage *= 1.15;
            }
        );


        add(
            "💨 검기 공격속도 +15%",
            "검기를 발사하는 속도가 증가합니다.",
            () => {
                p.swordWaveSpeed *= 1.15;
            }
        );


        add(
            "🛡️ 피해 감소 +5%",
            "받는 피해가 감소합니다.",
            () => {
                p.damageReduction =
                    Math.min(
                        0.65,
                        p.damageReduction + 0.05
                    );
            }
        );


        add(
            "❤️ 최대 HP +25",
            "최대 체력이 증가합니다.",
            () => {
                p.maxHp += 25;
                p.hp += 25;
            }
        );

    }


    /* =====================================================
       마법
    ===================================================== */

    else {

        add(
            "🔮 레이저 개수 +1",
            "강화공격과 각성의 레이저 개수가 증가합니다. 최대 5개.",
            () => {
                p.laserCount =
                    Math.min(
                        5,
                        p.laserCount + 1
                    );
            }
        );


        add(
            "✨ 강화공격 -1회",
            "강화공격까지 필요한 기본공격 횟수가 1 감소합니다. 최소 5회.",
            () => {
                p.enhancedEvery =
                    Math.max(
                        5,
                        p.enhancedEvery - 1
                    );
            }
        );


        add(
            "🔮 마법 공격력 +15%",
            "기본 마법탄의 공격력이 증가합니다.",
            () => {
                p.magicDamage *= 1.15;
            }
        );


        add(
            "⚡ 마법 공격속도 +15%",
            "기본 마법탄의 공격 속도가 증가합니다.",
            () => {
                p.magicSpeed *= 1.15;
            }
        );


        add(
            "🌈 레이저 공격력 +15%",
            "강화공격과 각성 레이저의 공격력이 증가합니다.",
            () => {
                p.laserDamage *= 1.15;
            }
        );


        add(
            "⏱️ 레이저 지속시간 +0.2초",
            "레이저가 유지되는 시간이 증가합니다. 최대 2초.",
            () => {
                p.laserDuration =
                    Math.min(
                        2,
                        p.laserDuration + 0.2
                    );
            }
        );


        add(
            "🔥 각성 지속시간 +0.5초",
            "각성 지속시간이 증가합니다. 최대 10초.",
            () => {
                p.skillDuration =
                    Math.min(
                        10,
                        p.skillDuration + 0.5
                    );
            }
        );


        add(
            "💀 각성 필요 처치 -1",
            "각성에 필요한 처치 수가 1 감소합니다. 최소 6마리.",
            () => {
                p.skillKillsNeeded =
                    Math.max(
                        6,
                        p.skillKillsNeeded - 1
                    );
            }
        );


        add(
            "❤️ 최대 HP +20",
            "최대 체력이 증가합니다.",
            () => {
                p.maxHp += 20;
                p.hp += 20;
            }
        );

    }


    /*
     * 매 레벨업마다 4개 선택지
     */

    options.sort(
        () => Math.random() - 0.5
    );


    return options.slice(0, 4);

}


/* =========================================================
   업데이트
========================================================= */

function update(dt) {

    const p = player;

    if (!p) return;


    elapsed += dt;


    p.invuln =
        Math.max(
            0,
            p.invuln - dt
        );


    p.formCooldown =
        Math.max(
            0,
            p.formCooldown - dt
        );


    p.skillCooldown =
        Math.max(
            0,
            p.skillCooldown - dt
        );


    p.gunSkillTimer =
        Math.max(
            0,
            p.gunSkillTimer - dt
        );


    /* 이동 */

    let mx = joy.x;

    let my = joy.y;


    if (keys["w"] || keys["ArrowUp"]) {
        my -= 1;
    }

    if (keys["s"] || keys["ArrowDown"]) {
        my += 1;
    }

    if (keys["a"] || keys["ArrowLeft"]) {
        mx -= 1;
    }

    if (keys["d"] || keys["ArrowRight"]) {
        mx += 1;
    }


    const length =
        Math.hypot(mx, my);


    if (length > 1) {

        mx /= length;
        my /= length;

    }


    if (length > 0.1) {

        p.x +=
            mx * p.speed * dt;

        p.y +=
            my * p.speed * dt;

        p.face =
            Math.atan2(my, mx);

    }


    p.x =
        clamp(
            p.x,
            20,
            W - 20
        );


    p.y =
        clamp(
            p.y,
            20,
            H - 20
        );


    /* =====================================================
       공격
    ===================================================== */


    if (p.cls === "gun") {

        p.attackTimer -= dt;


        if (p.attackTimer <= 0) {

            shootGun();

            p.attackTimer +=
                1 / p.attackSpeed;

        }

    }


    else if (p.cls === "sword") {

        /*
         * 베기
         */

        p.attackTimer -= dt;

        if (p.attackTimer <= 0) {

            swordSlash();

            p.attackTimer +=
                1 / p.swordSpeed;

        }


        /*
         * 검기
         */

        p.waveTimer -= dt;

        if (p.waveTimer <= 0) {

            swordWave();

            p.waveTimer +=
                1 / p.swordWaveSpeed;

        }

    }


    else if (p.cls === "magic") {

        p.attackTimer -= dt;


        let rate =
            p.magicSpeed;


        /*
         * 각성 중 공속 증가
         */

        if (p.skillActive) {

            rate *= 1.8;

        }


        if (p.attackTimer <= 0) {

            magicBasic();

            p.attackTimer +=
                1 / rate;

        }


        /*
         * 각성 시간
         */

        if (p.skillActive) {

            p.skillTimer -= dt;


            if (p.skillTimer <= 0) {

                p.skillActive = false;

            }

        }

    }


    /* =====================================================
       적 생성
    ===================================================== */

    if (elapsed >= nextEnemy) {

        nextEnemy =
            elapsed
            +
            (
                1.0
                -
                Math.min(
                    0.65,
                    elapsed / 500
                )
            );


        const amount =
            1
            +
            Math.floor(
                elapsed / 45
            );


        for (
            let i = 0;
            i < Math.min(5, amount);
            i++
        ) {

            spawnEnemy(false);

        }

    }


    /* 보스 */

    if (elapsed >= nextBoss) {

        nextBoss += 100;

        bossCount++;

        spawnEnemy(true);

    }


    /* =====================================================
       적 이동
    ===================================================== */

    for (const enemy of enemies) {

        const angle =
            Math.atan2(
                p.y - enemy.y,
                p.x - enemy.x
            );


        enemy.x +=
            Math.cos(angle)
            * enemy.speed
            * dt;


        enemy.y +=
            Math.sin(angle)
            * enemy.speed
            * dt;


        if (
            dist(enemy, p)
            <
            enemy.r + p.r
        ) {

            damagePlayer(
                enemy.dmg * dt * 8
            );

        }

    }


    updateProjectiles(dt);

    updateSlashes(dt);

    updateLasers(dt);

    updateParticles(dt);

    updateUI();

}


/* =========================================================
   투사체
========================================================= */

function updateProjectiles(dt) {

    for (
        let i = projectiles.length - 1;
        i >= 0;
        i--
    ) {

        const q =
            projectiles[i];


        q.x +=
            Math.cos(q.a)
            * q.speed
            * dt;


        q.y +=
            Math.sin(q.a)
            * q.speed
            * dt;


        q.travel +=
            q.speed * dt;


        let remove =
            q.travel > q.range
            ||
            q.x < -80
            ||
            q.x > W + 80
            ||
            q.y < -80
            ||
            q.y > H + 80;


        if (!remove) {

            for (
                const enemy
                of [...enemies]
            ) {

                if (
                    Math.hypot(
                        q.x - enemy.x,
                        q.y - enemy.y
                    )
                    <
                    q.r + enemy.r
                ) {

                    hitEnemy(
                        enemy,
                        q.dmg
                    );


                    /*
                     * 관통이 0이면 삭제
                     */

                    if (q.pen <= 0) {

                        remove = true;

                        break;

                    }


                    /*
                     * 관통 1이면
                     * 다음 적 하나까지 통과
                     */

                    q.pen--;

                }

            }

        }


        if (remove) {

            projectiles.splice(i, 1);

        }

    }

}


/* =========================================================
   베기
========================================================= */

function updateSlashes(dt) {

    for (
        let i = slashes.length - 1;
        i >= 0;
        i--
    ) {

        const slash =
            slashes[i];


        slash.life -= dt;


        for (
            const enemy
            of enemies
        ) {

            const dx =
                enemy.x - slash.x;

            const dy =
                enemy.y - slash.y;


            const d =
                Math.hypot(dx, dy);


            const angle =
                Math.atan2(dy, dx);


            let diff =
                Math.atan2(
                    Math.sin(
                        angle - slash.a
                    ),
                    Math.cos(
                        angle - slash.a
                    )
                );


            if (
                d
                <
                slash.range + enemy.r
                &&
                Math.abs(diff)
                <
                slash.fan / 2
            ) {

                if (
                    !enemy._slashHit
                    ||
                    enemy._slashHit
                    <
                    slash.life
                ) {

                    hitEnemy(
                        enemy,
                        slash.dmg
                    );

                    enemy._slashHit =
                        slash.life;

                }

            }

        }


        if (slash.life <= 0) {

            slashes.splice(i, 1);

        }

    }

}


/* =========================================================
   레이저
========================================================= */

function updateLasers(dt) {

    for (
        let i = lasers.length - 1;
        i >= 0;
        i--
    ) {

        const laser =
            lasers[i];


        laser.life -= dt;


        for (
            const enemy
            of [...enemies]
        ) {

            const x =
                enemy.x - laser.x;

            const y =
                enemy.y - laser.y;


            const c =
                Math.cos(-laser.a);

            const s =
                Math.sin(-laser.a);


            const rx =
                x * c - y * s;

            const ry =
                x * s + y * c;


            const laserWidth =
                9 *
                Math.max(
                    1,
                    player.area
                );


            if (
                Math.abs(
                    ry - laser.offset
                )
                <
                laserWidth
                + enemy.r
                &&
                Math.abs(rx)
                <
                Math.max(W, H)
            ) {

                hitEnemy(
                    enemy,
                    laser.dmg * dt * 3
                );

            }

        }


        if (laser.life <= 0) {

            lasers.splice(i, 1);

        }

    }

}


/* =========================================================
   파티클
========================================================= */

function updateParticles(dt) {

    for (
        let i = particles.length - 1;
        i >= 0;
        i--
    ) {

        const p =
            particles[i];


        p.x +=
            p.vx * dt;


        p.y +=
            p.vy * dt;


        p.life -= dt;


        if (p.life <= 0) {

            particles.splice(i, 1);

        }

    }

}


/* =========================================================
   그리기
========================================================= */

function draw() {

    ctx.clearRect(
        0,
        0,
        W,
        H
    );


    ctx.fillStyle = "#182018";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );


    /*
     * 배경 격자
     */

    ctx.strokeStyle =
        "rgba(255,255,255,.035)";

    ctx.lineWidth = 1;


    const grid = 50;

    const offset =
        -(elapsed * 8 % grid);


    for (
        let x = offset;
        x < W;
        x += grid
    ) {

        ctx.beginPath();

        ctx.moveTo(x, 0);

        ctx.lineTo(x, H);

        ctx.stroke();

    }


    for (
        let y = offset;
        y < H;
        y += grid
    ) {

        ctx.beginPath();

        ctx.moveTo(0, y);

        ctx.lineTo(W, y);

        ctx.stroke();

    }


    for (const laser of lasers) {

        drawLaser(laser);

    }


    for (const slash of slashes) {

        drawSlash(slash);

    }


    for (const projectile of projectiles) {

        drawProjectile(projectile);

    }


    for (const enemy of enemies) {

        drawEnemy(enemy);

    }


    if (player) {

        drawPlayer(player);

    }


    for (const particle of particles) {

        ctx.globalAlpha =
            Math.max(
                0,
                particle.life / 0.35
            );


        ctx.fillStyle = "#fff";

        ctx.beginPath();

        ctx.arc(
            particle.x,
            particle.y,
            3,
            0,
            TAU
        );

        ctx.fill();


        ctx.globalAlpha = 1;

    }

}


/* =========================================================
   플레이어
========================================================= */

function drawPlayer(p) {

    ctx.save();

    ctx.translate(
        p.x,
        p.y
    );


    if (p.cls === "gun") {

        ctx.fillStyle =
            p.gunForm === "pistol"
                ? "#e67e22"
                : "#9b59b6";


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


    else if (p.cls === "sword") {

        ctx.fillStyle =
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


        /*
         * 방어막
         */

        if (p.shield > 0) {

            ctx.strokeStyle =
                "#5dade2";

            ctx.lineWidth = 5;

            ctx.beginPath();

            ctx.arc(
                0,
                0,
                p.r + 7,
                0,
                TAU
            );

            ctx.stroke();

        }

    }


    else {

        ctx.fillStyle =
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


    /*
     * 바라보는 방향
     */

    ctx.rotate(p.face);

    ctx.fillStyle = "#eee";

    ctx.fillRect(
        8,
        -4,
        20,
        8
    );


    ctx.restore();

}


/* =========================================================
   적
========================================================= */

function drawEnemy(enemy) {

    ctx.fillStyle =
        enemy.boss
            ? "#c0392b"
            : "#75a85b";


    ctx.beginPath();

    ctx.arc(
        enemy.x,
        enemy.y,
        enemy.r,
        0,
        TAU
    );

    ctx.fill();


    /*
     * 눈
     */

    ctx.fillStyle = "#222";

    ctx.beginPath();

    ctx.arc(
        enemy.x - 4,
        enemy.y - 2,
        2,
        0,
        TAU
    );

    ctx.arc(
        enemy.x + 4,
        enemy.y - 2,
        2,
        0,
        TAU
    );

    ctx.fill();


    /*
     * HP바
     */

    ctx.fillStyle = "#333";

    ctx.fillRect(
        enemy.x - enemy.r,
        enemy.y - enemy.r - 7,
        enemy.r * 2,
        4
    );


    ctx.fillStyle = "#e74c3c";

    ctx.fillRect(
        enemy.x - enemy.r,
        enemy.y - enemy.r - 7,
        enemy.r * 2 *
        Math.max(
            0,
            enemy.hp / enemy.maxHp
        ),
        4
    );


    if (enemy.boss) {

        ctx.strokeStyle =
            "#f1c40f";

        ctx.lineWidth = 2;

        ctx.stroke();

    }

}


/* =========================================================
   투사체 그리기
========================================================= */

function drawProjectile(q) {

    if (q.type === "wave") {

        ctx.fillStyle =
            "#5dade2";

    }

    else if (q.type === "magic") {

        ctx.fillStyle =
            "#bb6bd9";

    }

    else {

        ctx.fillStyle =
            "#f5c542";

    }


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


/* =========================================================
   베기 그리기
========================================================= */

function drawSlash(s) {

    ctx.save();

    ctx.translate(
        s.x,
        s.y
    );

    ctx.rotate(s.a);

    ctx.globalAlpha =
        s.life / s.max;

    ctx.fillStyle =
        "#5dade2";


    ctx.beginPath();

    ctx.moveTo(0, 0);

    ctx.arc(
        0,
        0,
        s.range,
        -s.fan / 2,
        s.fan / 2
    );

    ctx.closePath();

    ctx.fill();


    ctx.globalAlpha = 1;

    ctx.restore();

}


/* =========================================================
   레이저 그리기
========================================================= */

function drawLaser(laser) {

    ctx.save();

    ctx.translate(
        laser.x,
        laser.y
    );

    ctx.rotate(laser.a);


    ctx.globalAlpha =
        0.8 *
        (laser.life / laser.max);


    ctx.fillStyle =
        "#e8b4ff";


    const width =
        9 *
        Math.max(
            1,
            player.area
        );


    ctx.fillRect(
        -Math.max(W, H),
        laser.offset - width,
        Math.max(W, H) * 2,
        width * 2
    );


    ctx.globalAlpha = 1;

    ctx.restore();

}


/* =========================================================
   UI
========================================================= */

function updateUI() {

    if (!player) return;


    document
        .getElementById("hpFill")
        .style.width =
        (
            100 *
            player.hp /
            player.maxHp
        )
        + "%";


    document
        .getElementById("shieldBar")
        .style.display =
        player.cls === "sword"
            ? "block"
            : "none";


    document
        .getElementById("shieldFill")
        .style.width =
        (
            player.maxShield
                ? 100 *
                  player.shield /
                  player.maxShield
                : 0
        )
        + "%";


    document
        .getElementById("xpFill")
        .style.width =
        (
            100 *
            xp /
            xpNeed
        )
        + "%";


    document
        .getElementById("stats")
        .textContent =
        `Lv.${level} | ${formatTime(elapsed)} | 처치 ${kills}`;


    let extra = "";


    if (player.cls === "gun") {

        extra =
            `${player.gunForm === "pistol" ? "권총" : "저격"}`
            +
            ` | 투사체 ${player.projectiles}`
            +
            ` | 관통 ${player.penetration}`;

    }


    if (player.cls === "sword") {

        extra =
            `베기 + 검기 ${player.swordWaveCount}개`
            +
            ` | 방어막 ${Math.ceil(player.shield)}`;

    }


    if (player.cls === "magic") {

        extra =
            `레이저 ${player.laserCount}개`
            +
            ` | 강화 ${player.enhancedCounter}/${player.enhancedEvery}`
            +
            ` | 각성 ${player.skillKills}/${player.skillKillsNeeded}`;

    }


    document
        .getElementById("classInfo")
        .textContent =
        classNames[player.cls]
        + " · "
        + extra;


    /*
     * 스킬 버튼
     */

    if (player.cls === "magic") {

        document
            .getElementById("skillBtn")
            .textContent =
            player.skillActive
                ? `각성 중 ${player.skillTimer.toFixed(1)}초`
                : `각성 ${player.skillKills}/${player.skillKillsNeeded}`;

    }

    else if (player.cls === "sword") {

        document
            .getElementById("skillBtn")
            .textContent =
            player.skillCooldown > 0
                ? `방어막 ${player.skillCooldown.toFixed(1)}`
                : "🛡️ 방어막";

    }

    else {

        document
            .getElementById("skillBtn")
            .textContent =
            player.skillCooldown > 0
                ? `강화 ${player.skillCooldown.toFixed(1)}`
                : "🔥 스킬";

    }


    /*
     * 폼체인지
     */

    if (player.cls === "gun") {

        document
            .getElementById("formBtn")
            .textContent =
            player.formCooldown > 0
                ? `대기 ${player.formCooldown.toFixed(1)}`
                : `🔄 ${player.gunForm === "pistol" ? "권총" : "저격"}`;

    }

}


/* =========================================================
   시간
========================================================= */

function formatTime(time) {

    const minutes =
        Math.floor(time / 60);

    const seconds =
        Math.floor(time % 60);


    return (
        minutes
        +
        ":"
        +
        String(seconds).padStart(2, "0")
    );

}


/* =========================================================
   게임오버
========================================================= */

function gameOver() {

    state = "gameover";


    document
        .getElementById("result")
        .textContent =
        `레벨 ${level} · `
        +
        `${formatTime(elapsed)} 생존 · `
        +
        `${kills}마리 처치`;


    document
        .getElementById("gameover")
        .classList.remove("hidden");

}


/* =========================================================
   메인 루프
========================================================= */

function loop(time) {

    if (!last) {

        last = time;

    }


    const dt =
        Math.min(
            0.033,
            (time - last) / 1000
        );


    last = time;


    if (state === "playing") {

        update(dt);

    }


    draw();


    requestAnimationFrame(loop);

}


requestAnimationFrame(loop);


/* =========================================================
   키보드
========================================================= */

addEventListener(
    "keydown",
    event => {

        keys[event.key] = true;


        if (event.key === " ") {

            event.preventDefault();

            useSkill();

        }


        if (
            event.key.toLowerCase()
            === "q"
        ) {

            formChange();

        }

    }
);


addEventListener(
    "keyup",
    event => {

        keys[event.key] = false;

    }
);


/* =========================================================
   모바일 버튼
========================================================= */

document
    .getElementById("skillBtn")
    .addEventListener(
        "pointerdown",
        event => {

            event.preventDefault();

            useSkill();

        }
    );


document
    .getElementById("formBtn")
    .addEventListener(
        "pointerdown",
        event => {

            event.preventDefault();

            formChange();

        }
    );


/* =========================================================
   모바일 조이스틱
========================================================= */

const joystick =
    document.getElementById(
        "joystick"
    );


const stick =
    document.getElementById(
        "stick"
    );


function moveJoystick(event) {

    const rect =
        joystick.getBoundingClientRect();


    const centerX =
        rect.left +
        rect.width / 2;


    const centerY =
        rect.top +
        rect.height / 2;


    let dx =
        event.clientX -
        centerX;


    let dy =
        event.clientY -
        centerY;


    const distance =
        Math.hypot(dx, dy);


    const max =
        47;


    if (distance > max) {

        dx =
            dx / distance * max;

        dy =
            dy / distance * max;

    }


    joy.x =
        dx / max;

    joy.y =
        dy / max;


    stick.style.transform =
        `translate(${dx}px, ${dy}px)`;

}


joystick.addEventListener(
    "pointerdown",
    event => {

        joystick.setPointerCapture(
            event.pointerId
        );

        moveJoystick(event);

    }
);


joystick.addEventListener(
    "pointermove",
    event => {

        if (event.buttons) {

            moveJoystick(event);

        }

    }
);


function resetJoystick() {

    joy.x = 0;

    joy.y = 0;

    stick.style.transform =
        "translate(0,0)";

}


joystick.addEventListener(
    "pointerup",
    resetJoystick
);


joystick.addEventListener(
    "pointercancel",
    resetJoystick
);

</script>

</body>
</html>
'''

components.html(
    html,
    height=820,
    scrolling=False
)
