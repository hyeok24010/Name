import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NURURUNG SURVIVOR",
    page_icon="🟣",
    layout="centered"
)

game = r'''
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

canvas {
    width: 100%;
    max-width: 850px;
    background: #151522;
    border: 2px solid #555;
    border-radius: 10px;
    touch-action: none;
}

#characterSelect {
    color: white;
    margin-bottom: 10px;
}

.charButton {
    margin: 3px;
    padding: 8px 14px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}

#info {
    display: flex;
    justify-content: space-around;
    color: white;
    font-size: 14px;
    margin: 7px;
}

button {
    padding: 9px 16px;
    border: none;
    border-radius: 6px;
    background: #4d7cff;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

#levelup {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    width: 90%;
    max-width: 650px;

    background: rgba(15,15,25,0.96);
    border: 2px solid #777;
    border-radius: 12px;

    padding: 20px;

    display: none;

    z-index: 10;
}

#levelup h2 {
    color: white;
}

.upgrade {
    display: block;

    width: 100%;

    margin: 8px 0;

    padding: 14px;

    background: #272738;

    color: white;

    border: 1px solid #555;

    border-radius: 8px;

    cursor: pointer;

    text-align: left;
}

.upgrade:hover {
    background: #383850;
}

#gameOver {
    position: absolute;

    left: 50%;
    top: 50%;

    transform: translate(-50%, -50%);

    color: white;

    font-size: 32px;

    display: none;

    z-index: 20;
}
</style>
</head>

<body>

<div id="gameBox">

<div id="characterSelect">

    <b>캐릭터 선택</b>

    <br>

    <button class="charButton"
        onclick="selectCharacter('butter')">
        🔫 버터
    </button>

    <button class="charButton"
        onclick="selectCharacter('bibi')">
        🛡️ 비비
    </button>

    <button class="charButton"
        onclick="selectCharacter('joan')">
        ⛓️ 조안
    </button>

</div>


<div id="info">

    <span>
        LV <b id="level">1</b>
    </span>

    <span>
        ❤️ <b id="hp">100 / 100</b>
    </span>

    <span>
        🛡️ <b id="shield">0</b>
    </span>

    <span>
        XP <b id="xp">0</b>
    </span>

    <span>
        ☠️ <b id="kills">0</b>
    </span>

    <span>
        ⏱️ <b id="time">0</b>
    </span>

</div>


<div style="position:relative;">

<canvas
    id="game"
    width="850"
    height="600">
</canvas>


<div id="levelup">

    <h2>LEVEL UP!</h2>

    <p style="color:#aaa;">
        강화할 능력을 하나 선택하세요.
    </p>

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

</div>


<script>

const canvas =
    document.getElementById("game");

const ctx =
    canvas.getContext("2d");


/* =====================================
   게임 상태
===================================== */

let gameRunning = true;

let level = 1;

let xp = 0;

let xpNeed = 10;

let kills = 0;

let gameTime = 0;

let lastTime = performance.now();

let spawnTimer = 0;

let attackTimer = 0;

let specialTimer = 0;

let levelUpOpen = false;


/* =====================================
   캐릭터
===================================== */

let characterType = "butter";


const character = {

    x: canvas.width / 2,

    y: canvas.height / 2,

    radius: 18,

    maxHp: 100,

    hp: 100,

    speed: 3.5,

    damage: 15,

    attackSpeed: 650,

    damageReduction: 0,

    xpMultiplier: 1,

    shield: 0,

    killsForSkill: 20,

    skillKills: 0,

    skillActive: false,

    skillTimer: 0

};


/* =====================================
   적
===================================== */

let enemies = [];

let projectiles = [];

let effects = [];

let gems = [];


/* =====================================
   키보드
===================================== */

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


/* =====================================
   캐릭터 선택
===================================== */

function selectCharacter(type) {

    characterType = type;

    restartGame();

}


/* =====================================
   캐릭터 초기 설정
===================================== */

function setupCharacter() {

    character.x =
        canvas.width / 2;

    character.y =
        canvas.height / 2;

    character.maxHp = 100;

    character.hp = 100;

    character.speed = 3.5;

    character.damage = 15;

    character.attackSpeed = 650;

    character.damageReduction = 0;

    character.xpMultiplier = 1;

    character.shield = 0;

    character.skillKills = 0;

    character.skillActive = false;

    character.skillTimer = 0;


    if (
        characterType === "butter"
    ) {

        character.maxHp = 90;

        character.hp = 90;

        character.speed = 3.8;

        character.damage = 14;

        character.attackSpeed = 550;

        character.killsForSkill = 20;

    }


    else if (
        characterType === "bibi"
    ) {

        character.maxHp = 130;

        character.hp = 130;

        character.speed = 2.8;

        character.damage = 18;

        character.attackSpeed = 800;

        character.damageReduction = 0.20;

        character.killsForSkill = 12;

    }


    else if (
        characterType === "joan"
    ) {

        character.maxHp = 100;

        character.hp = 100;

        character.speed = 3.2;

        character.damage = 16;

        character.attackSpeed = 750;

        character.killsForSkill = 15;

    }

}


/* =====================================
   적 생성
===================================== */

function spawnEnemy() {

    /*
     * 화면 바깥에서 등장
     */

    const side =
        Math.floor(
            Math.random() * 4
        );

    let x;
    let y;


    if (side === 0) {

        x = Math.random() *
            canvas.width;

        y = -30;

    }

    else if (side === 1) {

        x = canvas.width + 30;

        y = Math.random() *
            canvas.height;

    }

    else if (side === 2) {

        x = Math.random() *
            canvas.width;

        y = canvas.height + 30;

    }

    else {

        x = -30;

        y = Math.random() *
            canvas.height;

    }


    const hp =
        20 +
        gameTime * 1.5 +
        level * 4;


    enemies.push({

        x: x,

        y: y,

        radius: 15,

        hp: hp,

        maxHp: hp,

        speed:
            0.65 +
            Math.random() * 0.35 +
            gameTime * 0.005,

        damage:
            5 +
            gameTime * 0.08,

        attackCooldown: 0

    });

}


/* =====================================
   이동
===================================== */

function moveCharacter() {

    let dx = 0;
    let dy = 0;


    if (
        keys["w"] ||
        keys["arrowup"]
    ) {

        dy--;

    }


    if (
        keys["s"] ||
        keys["arrowdown"]
    ) {

        dy++;

    }


    if (
        keys["a"] ||
        keys["arrowleft"]
    ) {

        dx--;

    }


    if (
        keys["d"] ||
        keys["arrowright"]
    ) {

        dx++;

    }


    /*
     * 대각선 속도 보정
     */

    if (
        dx !== 0 ||
        dy !== 0
    ) {

        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        dx /= length;
        dy /= length;

    }


    character.x +=
        dx *
        character.speed;

    character.y +=
        dy *
        character.speed;


    /*
     * 화면 안에 유지
     */

    character.x =
        Math.max(
            character.radius,
            Math.min(
                canvas.width -
                character.radius,
                character.x
            )
        );


    character.y =
        Math.max(
            character.radius,
            Math.min(
                canvas.height -
                character.radius,
                character.y
            )
        );

}


/* =====================================
   가장 가까운 적
===================================== */

function nearestEnemy() {

    let target = null;

    let distance = Infinity;


    enemies.forEach(
        function(enemy) {

            const dx =
                enemy.x -
                character.x;

            const dy =
                enemy.y -
                character.y;

            const d =
                dx * dx +
                dy * dy;


            if (d < distance) {

                distance = d;

                target = enemy;

            }

        }
    );


    return target;

}


/* =====================================
   버터 공격
===================================== */

function butterAttack() {

    const target =
        nearestEnemy();


    if (!target) {
        return;
    }


    const dx =
        target.x -
        character.x;

    const dy =
        target.y -
        character.y;


    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );


    projectiles.push({

        x: character.x,

        y: character.y,

        dx: dx / length * 8,

        dy: dy / length * 8,

        damage:
            character.damage,

        radius: 5,

        type: "bullet"

    });

}


/* =====================================
   비비 공격
===================================== */

function bibiAttack() {

    /*
     * 주변 적 전체에 근접 피해
     */

    enemies.forEach(
        function(enemy) {

            const dx =
                enemy.x -
                character.x;

            const dy =
                enemy.y -
                character.y;

            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );


            if (
                distance < 90
            ) {

                enemy.hp -=
                    character.damage;

            }

        }
    );


    effects.push({

        type: "circle",

        x: character.x,

        y: character.y,

        radius: 90,

        life: 15

    });

}


/* =====================================
   조안 공격
===================================== */

function joanAttack() {

    /*
     * 가장 가까운 적 방향으로
     * 쇄사슬이 직선으로 뻗음
     */

    const target =
        nearestEnemy();


    if (!target) {
        return;
    }


    const dx =
        target.x -
        character.x;

    const dy =
        target.y -
        character.y;


    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );


    const nx =
        dx / length;

    const ny =
        dy / length;


    enemies.forEach(
        function(enemy) {

            const ex =
                enemy.x -
                character.x;

            const ey =
                enemy.y -
                character.y;


            /*
             * 쇄사슬 직선과 적의 거리
             */

            const cross =
                Math.abs(
                    ex * ny -
                    ey * nx
                );


            const forward =
                ex * nx +
                ey * ny;


            if (
                cross < 25 &&
                forward > 0 &&
                forward < 500
            ) {

                enemy.hp -=
                    character.damage *
                    1.5;

            }

        }
    );


    effects.push({

        type: "chain",

        x: character.x,

        y: character.y,

        nx: nx,

        ny: ny,

        life: 20

    });

}


/* =====================================
   일반 공격
===================================== */

function attack() {

    if (
        characterType === "butter"
    ) {

        butterAttack();

    }

    else if (
        characterType === "bibi"
    ) {

        bibiAttack();

    }

    else {

        joanAttack();

    }

}


/* =====================================
   캐릭터 스킬
===================================== */

function useSkill() {

    if (
        character.skillKills <
        character.killsForSkill
    ) {

        return;

    }


    character.skillKills = 0;


    /*
     * 버터
     */

    if (
        characterType === "butter"
    ) {

        character.skillActive = true;

        character.skillTimer = 7000;

    }


    /*
     * 비비
     */

    else if (
        characterType === "bibi"
    ) {

        /*
         * 은색 방어막 하나 추가
         */

        character.shield += 20;

    }


    /*
     * 조안
     */

    else if (
        characterType === "joan"
    ) {

        character.skillActive = true;

        character.skillTimer = 6000;

    }

}


/* =====================================
   스킬 업데이트
===================================== */

function updateSkill(delta) {

    if (
        character.skillActive
    ) {

        character.skillTimer -=
            delta;


        if (
            character.skillTimer <= 0
        ) {

            character.skillActive =
                false;

        }

    }


    /*
     * 비비 방어막은
     * 스킬 사용 즉시 발동
     */

    if (
        characterType === "bibi"
    ) {

        /*
         * 처치 수가 기준에 도달하면
         * 자동 사용
         */

        if (
            character.skillKills >=
            character.killsForSkill
        ) {

            useSkill();

        }

    }

    else {

        if (
            character.skillKills >=
            character.killsForSkill
        ) {

            useSkill();

        }

    }

}


/* =====================================
   공 업데이트
===================================== */

function updateProjectiles() {

    projectiles.forEach(
        function(p) {

            p.x += p.dx;

            p.y += p.dy;


            enemies.forEach(
                function(enemy) {

                    if (
                        enemy.hp <= 0
                    ) {
                        return;
                    }


                    const dx =
                        enemy.x -
                        p.x;

                    const dy =
                        enemy.y -
                        p.y;


                    const d =
                        Math.sqrt(
                            dx * dx +
                            dy * dy
                        );


                    if (
                        d <
                        enemy.radius +
                        p.radius
                    ) {

                        enemy.hp -=
                            p.damage;


                        p.dead = true;

                    }

                }
            );

        }
    );


    projectiles =
        projectiles.filter(
            p =>
                !p.dead &&
                p.x > -30 &&
                p.x <
                    canvas.width + 30 &&
                p.y > -30 &&
                p.y <
                    canvas.height + 30
        );

}


/* =====================================
   적 이동
===================================== */

function updateEnemies(delta) {

    enemies.forEach(
        function(enemy) {

            const dx =
                character.x -
                enemy.x;

            const dy =
                character.y -
                enemy.y;


            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );


            if (
                distance >
                character.radius +
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

                /*
                 * 캐릭터와 닿으면 공격
                 */

                enemy.attackCooldown -=
                    delta;


                if (
                    enemy.attackCooldown <= 0
                ) {

                    damageCharacter(
                        enemy.damage
                    );

                    enemy.attackCooldown =
                        700;

                }

            }

        }
    );

}


/* =====================================
   캐릭터 피해
===================================== */

function damageCharacter(amount) {

    let damage =
        amount *
        (1 -
        character.damageReduction);


    /*
     * 비비의 은색 방어막
     */

    if (
        character.shield > 0
    ) {

        const blocked =
            Math.min(
                character.shield,
                damage
            );


        character.shield -=
            blocked;

        damage -=
            blocked;

    }


    character.hp -=
        damage;


    if (
        character.hp <= 0
    ) {

        character.hp = 0;

        gameOver();

    }

}


/* =====================================
   적 처치
===================================== */

function processDeaths() {

    const alive = [];


    enemies.forEach(
        function(enemy) {

            if (
                enemy.hp <= 0
            ) {

                kills++;

                character.skillKills++;


                /*
                 * 경험치
                 */

                gems.push({

                    x: enemy.x,

                    y: enemy.y,

                    value: 1

                });

            }

            else {

                alive.push(enemy);

            }

        }
    );


    enemies = alive;

}


/* =====================================
   경험치 획득
===================================== */

function collectXP() {

    for (
        let i = gems.length - 1;
        i >= 0;
        i--
    ) {

        const gem =
            gems[i];


        const dx =
            character.x -
            gem.x;

        const dy =
            character.y -
            gem.y;


        const distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );


        /*
         * 가까이 가면 획득
         */

        if (
            distance < 60
        ) {

            xp +=
                gem.value *
                character.xpMultiplier;


            gems.splice(i, 1);

        }

    }


    /*
     * 레벨업
     */

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


/* =====================================
   레벨업 선택
===================================== */

function showLevelUp() {

    gameRunning = false;

    levelUpOpen = true;


    const list =
        document.getElementById(
            "upgradeList"
        );


    list.innerHTML = "";


    const upgrades = [

        {
            name: "⚔️ 공격력 +20%",
            effect: function() {

                character.damage *= 1.20;

            }
        },

        {
            name: "⚡ 공격속도 +20%",
            effect: function() {

                character.attackSpeed *= 0.80;

            }
        },

        {
            name: "🏃 이동속도 +15%",
            effect: function() {

                character.speed *= 1.15;

            }
        },

        {
            name: "❤️ 최대 체력 +25",
            effect: function() {

                character.maxHp += 25;

                character.hp += 25;

            }
        },

        {
            name: "🛡️ 피해 감소 +5%",
            effect: function() {

                character.damageReduction =
                    Math.min(
                        0.70,
                        character.damageReduction +
                        0.05
                    );

            }
        },

        {
            name: "✨ 경험치 획득 +20%",
            effect: function() {

                character.xpMultiplier *=
                    1.20;

            }
        }

    ];


    /*
     * 무작위 3개
     */

    upgrades.sort(
        () =>
            Math.random() -
            0.5
    );


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
                    upgrade.name;


                button.onclick =
                    function() {

                        upgrade.effect();

                        document
                            .getElementById(
                                "levelup"
                            )
                            .style.display =
                            "none";


                        levelUpOpen =
                            false;


                        gameRunning =
                            true;

                    };


                list.appendChild(
                    button
                );

            }
        );


    document
        .getElementById(
            "levelup"
        )
        .style.display =
        "block";

}


/* =====================================
   시간
===================================== */

function updateTime(delta) {

    gameTime +=
        delta / 1000;


    document.getElementById(
        "time"
    ).textContent =
        Math.floor(gameTime);

}


/* =====================================
   적 생성
===================================== */

function spawnEnemies(delta) {

    spawnTimer -=
        delta;


    /*
     * 시간이 지나면
     * 더 자주 생성
     */

    const interval =
        Math.max(
            850 -
            gameTime * 12,
            180
        );


    if (
        spawnTimer <= 0
    ) {

        /*
         * 시간이 지날수록
         * 한 번에 여러 마리
         */

        const amount =
            Math.min(
                1 +
                Math.floor(
                    gameTime / 30
                ),
                7
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


/* =====================================
   그리기
===================================== */

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /*
     * 배경
     */

    ctx.fillStyle =
        "#151522";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /*
     * 경험치
     */

    gems.forEach(
        function(gem) {

            ctx.beginPath();

            ctx.arc(
                gem.x,
                gem.y,
                5,
                0,
                Math.PI * 2
            );

            ctx.fillStyle =
                "#63e6ff";

            ctx.fill();

        }
    );


    /*
     * 적
     */

    enemies.forEach(
        function(enemy) {

            /*
             * 누루룽 임시 모습
             */

            ctx.beginPath();

            ctx.arc(
                enemy.x,
                enemy.y,
                enemy.radius,
                0,
                Math.PI * 2
            );

            ctx.fillStyle =
                "#8b72ff";

            ctx.fill();


            /*
             * 눈
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
             * HP
             */

            ctx.fillStyle =
                "#333";

            ctx.fillRect(
                enemy.x - 15,
                enemy.y - 23,
                30,
                4
            );


            ctx.fillStyle =
                "#ff4444";

            ctx.fillRect(
                enemy.x - 15,
                enemy.y - 23,
                30 *
                (enemy.hp /
                enemy.maxHp),
                4
            );

        }
    );


    /*
     * 투사체
     */

    projectiles.forEach(
        function(p) {

            ctx.beginPath();

            ctx.arc(
                p.x,
                p.y,
                p.radius,
                0,
                Math.PI * 2
            );

            ctx.fillStyle =
                "#ffd166";

            ctx.fill();

        }
    );


    /*
     * 캐릭터
     */

    ctx.beginPath();

    ctx.arc(
        character.x,
        character.y,
        character.radius,
        0,
        Math.PI * 2
    );


    if (
        characterType === "butter"
    ) {

        ctx.fillStyle =
            "#e5a15a";

    }

    else if (
        characterType === "bibi"
    ) {

        ctx.fillStyle =
            "#d6d6d6";

    }

    else {

        ctx.fillStyle =
            "#eeeeee";

    }


    ctx.fill();


    /*
     * 버터 빨간 눈
     */

    if (
        characterType === "butter"
    ) {

        ctx.fillStyle =
            "red";

    }

    else {

        ctx.fillStyle =
            "#333";

    }


    ctx.beginPath();

    ctx.arc(
        character.x - 6,
        character.y - 3,
        3,
        0,
        Math.PI * 2
    );

    ctx.arc(
        character.x + 6,
        character.y - 3,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    /*
     * 비비 방어막
     */

    if (
        characterType === "bibi" &&
        character.shield > 0
    ) {

        ctx.beginPath();

        ctx.arc(
            character.x,
            character.y,
            character.radius + 7,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle =
            "#d8d8d8";

        ctx.lineWidth = 5;

        ctx.stroke();

    }


    /*
     * 비비 근접 범위
     */

    if (
        characterType === "bibi"
    ) {

        ctx.beginPath();

        ctx.arc(
            character.x,
            character.y,
            90,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle =
            "rgba(255,255,255,0.12)";

        ctx.stroke();

    }


    /*
     * 조안 쇄사슬
     */

    effects.forEach(
        function(effect) {

            if (
                effect.type ===
                "chain"
            ) {

                ctx.beginPath();

                ctx.moveTo(
                    effect.x,
                    effect.y
                );

                ctx.lineTo(

                    effect.x +
                    effect.nx *
                    500,

                    effect.y +
                    effect.ny *
                    500

                );

                ctx.strokeStyle =
                    "#eeeeee";

                ctx.lineWidth = 10;

                ctx.stroke();


                ctx.strokeStyle =
                    "#777";

                ctx.lineWidth = 4;

                ctx.stroke();

            }


            if (
                effect.type ===
                "circle"
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
                    "#d0d0d0";

                ctx.lineWidth = 6;

                ctx.stroke();

            }

        }
    );


    /*
     * 체력바
     */

    const barWidth = 180;

    ctx.fillStyle =
        "#333";

    ctx.fillRect(
        character.x -
        barWidth / 2,
        character.y -
        34,
        barWidth,
        7
    );


    ctx.fillStyle =
        "#e53935";

    ctx.fillRect(

        character.x -
        barWidth / 2,

        character.y -
        34,

        barWidth *
        (
            character.hp /
            character.maxHp
        ),

        7

    );


    /*
     * 방어막 수치
     */

    if (
        character.shield > 0
    ) {

        ctx.fillStyle =
            "#ddd";

        ctx.font =
            "bold 12px Arial";

        ctx.textAlign =
            "center";

        ctx.fillText(

            "🛡 " +
            Math.floor(
                character.shield
            ),

            character.x,
            character.y -
            42

        );

    }


    /*
     * 스킬 게이지
     */

    const ratio =
        Math.min(
            character.skillKills /
            character.killsForSkill,
            1
        );


    ctx.fillStyle =
        "#333";

    ctx.fillRect(
        character.x - 30,
        character.y + 27,
        60,
        5
    );


    ctx.fillStyle =
        "#ffd43b";

    ctx.fillRect(
        character.x - 30,
        character.y + 27,
        60 * ratio,
        5
    );

}


/* =====================================
   효과 업데이트
===================================== */

function updateEffects() {

    effects.forEach(
        function(effect) {

            effect.life--;

        }
    );


    effects =
        effects.filter(
            e => e.life > 0
        );

}


/* =====================================
   UI
===================================== */

function updateUI() {

    document.getElementById(
        "level"
    ).textContent =
        level;


    document.getElementById(
        "hp"
    ).textContent =
        Math.ceil(
            character.hp
        ) +
        " / " +
        Math.ceil(
            character.maxHp
        );


    document.getElementById(
        "shield"
    ).textContent =
        Math.floor(
            character.shield
        );


    document.getElementById(
        "xp"
    ).textContent =
        Math.floor(xp) +
        " / " +
        xpNeed;


    document.getElementById(
        "kills"
    ).textContent =
        kills;

}


/* =====================================
   게임 오버
===================================== */

function gameOver() {

    gameRunning = false;

    document.getElementById(
        "gameOver"
    ).style.display =
        "block";

}


/* =====================================
   재시작
===================================== */

function restartGame() {

    score = 0;

    level = 1;

    xp = 0;

    xpNeed = 10;

    kills = 0;

    gameTime = 0;

    spawnTimer = 0;

    attackTimer = 0;

    characterType =
        characterType || "butter";


    enemies = [];

    projectiles = [];

    effects = [];

    gems = [];


    setupCharacter();


    gameRunning = true;

    levelUpOpen = false;


    document.getElementById(
        "levelup"
    ).style.display =
        "none";


    document.getElementById(
        "gameOver"
    ).style.display =
        "none";


    lastTime =
        performance.now();

}


/* =====================================
   메인 루프
===================================== */

function gameLoop(time) {

    const delta =
        Math.min(
            time - lastTime,
            40
        );


    lastTime = time;


    if (gameRunning) {

        updateTime(delta);

        moveCharacter();

        spawnEnemies(delta);

        updateEnemies(delta);

        updateProjectiles(delta);

        processDeaths();

        collectXP();

        updateSkill(delta);

        updateEffects();


        /*
         * 일반 공격
         */

        attackTimer -= delta;


        let currentAttackSpeed =
            character.attackSpeed;


        /*
         * 버터 스킬:
         * 연사 속도 크게 증가
         */

        if (
            characterType === "butter" &&
            character.skillActive
        ) {

            currentAttackSpeed *= 0.28;

        }


        if (
            attackTimer <= 0
        ) {

            attack();

            attackTimer =
                currentAttackSpeed;

        }


        /*
         * 조안 스킬:
         * 지속적으로 쇄사슬 공격
         */

        if (
            characterType === "joan" &&
            character.skillActive
        ) {

            specialTimer -= delta;


            if (
                specialTimer <= 0
            ) {

                joanAttack();

                specialTimer =
                    220;

            }

        }


        updateUI();

    }


    draw();


    requestAnimationFrame(
        gameLoop
    );

}


/* =====================================
   시작
===================================== */

setupCharacter();

restartGame();

requestAnimationFrame(
    gameLoop
);

</script>

</body>
</html>
'''

components.html(
    game,
    height=700,
    scrolling=False
)
