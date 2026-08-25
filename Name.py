import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌 내려오기",
    page_icon="🧱",
    layout="centered"
)

html_code = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #10131c;
    font-family: Arial, sans-serif;
    color: white;
}

#gameBox {
    width: 100%;
    max-width: 760px;
    margin: auto;
    text-align: center;
}

#info {
    display: flex;
    justify-content: space-around;
    align-items: center;
    font-size: 17px;
    margin: 8px 0;
    font-weight: bold;
}

canvas {
    width: 100%;
    max-width: 720px;
    height: auto;
    background: #080b14;
    border: 2px solid #555;
    border-radius: 8px;
    touch-action: none;
}

button {
    margin-top: 10px;
    padding: 10px 25px;
    border: none;
    border-radius: 7px;
    background: #3478f6;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #2864d0;
}

#message {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 45%;
    font-size: 30px;
    font-weight: bold;
    text-shadow: 0 2px 5px black;
    pointer-events: none;
}

</style>
</head>

<body>

<div id="gameBox">

    <div id="info">
        <span>점수: <span id="score">0</span></span>
        <span>라운드: <span id="round">1</span></span>
        <span>❤️ <span id="lives">3</span></span>
        <span>⚾ <span id="ballCount">1</span></span>
    </div>

    <div style="position:relative;">

        <canvas id="game" width="720" height="600"></canvas>

        <div id="message"></div>

    </div>

    <button id="restart">다시 시작</button>

</div>


<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scoreText = document.getElementById("score");
const roundText = document.getElementById("round");
const livesText = document.getElementById("lives");
const ballCountText = document.getElementById("ballCount");
const restartButton = document.getElementById("restart");
const message = document.getElementById("message");


/* =========================
   게임 상태
========================= */

let score = 0;
let lives = 3;
let round = 1;

let gameRunning = true;

let bricks = [];
let balls = [];

let brickSpeed = 0.12;

let lastTime = performance.now();
let brickTimer = 0;


/* =========================
   패들
========================= */

const paddle = {

    x: 305,
    y: 555,

    width: 110,
    height: 14,

    normalWidth: 110,

    speed: 8

};


/* =========================
   키보드
========================= */

let leftPressed = false;
let rightPressed = false;


document.addEventListener("keydown", function(e) {

    if (
        e.key === "ArrowLeft" ||
        e.key.toLowerCase() === "a"
    ) {

        leftPressed = true;

    }


    if (
        e.key === "ArrowRight" ||
        e.key.toLowerCase() === "d"
    ) {

        rightPressed = true;

    }

});


document.addEventListener("keyup", function(e) {

    if (
        e.key === "ArrowLeft" ||
        e.key.toLowerCase() === "a"
    ) {

        leftPressed = false;

    }


    if (
        e.key === "ArrowRight" ||
        e.key.toLowerCase() === "d"
    ) {

        rightPressed = false;

    }

});


/* =========================
   마우스
========================= */

canvas.addEventListener(
    "mousemove",
    function(e) {

        const rect =
            canvas.getBoundingClientRect();

        const mouseX =
            (e.clientX - rect.left) *
            canvas.width /
            rect.width;

        paddle.x =
            mouseX -
            paddle.width / 2;

        keepPaddleInside();

    }
);


/* =========================
   모바일 터치
========================= */

canvas.addEventListener(
    "touchmove",
    function(e) {

        e.preventDefault();

        const rect =
            canvas.getBoundingClientRect();

        const touchX =
            (e.touches[0].clientX - rect.left) *
            canvas.width /
            rect.width;

        paddle.x =
            touchX -
            paddle.width / 2;

        keepPaddleInside();

    },
    { passive: false }
);


/* =========================
   패들 위치 제한
========================= */

function keepPaddleInside() {

    if (paddle.x < 0) {

        paddle.x = 0;

    }


    if (
        paddle.x +
        paddle.width >
        canvas.width
    ) {

        paddle.x =
            canvas.width -
            paddle.width;

    }

}


/* =========================
   벽돌 생성
========================= */

function createBrickRow() {

    const columns = 10;

    const width = 62;
    const height = 27;
    const gap = 8;

    const totalWidth =
        columns * width +
        (columns - 1) * gap;

    const startX =
        (canvas.width - totalWidth) / 2;


    for (
        let i = 0;
        i < columns;
        i++
    ) {

        /*
         * 라운드가 올라갈수록
         * 체력이 증가
         */

        let baseHP =
            1 +
            Math.floor((round - 1) / 2);


        /*
         * 높은 라운드에서는
         * 랜덤으로 더 튼튼한 벽돌 등장
         */

        let hp = baseHP;

        if (
            round >= 3 &&
            Math.random() < 0.25
        ) {

            hp += 1;

        }


        if (
            round >= 6 &&
            Math.random() < 0.20
        ) {

            hp += 1;

        }


        bricks.push({

            x:
                startX +
                i *
                (width + gap),

            y: -height,

            width: width,
            height: height,

            hp: hp,
            maxHp: hp,

            alive: true

        });

    }

}


/* =========================
   공 생성
========================= */

function createBall(
    x,
    y,
    dx,
    dy
) {

    balls.push({

        x: x,
        y: y,

        radius: 7,

        dx: dx,
        dy: dy,

        alive: true

    });

}


/* =========================
   처음 공
========================= */

function resetBalls() {

    balls = [];

    createBall(

        canvas.width / 2,

        paddle.y - 15,

        4,

        -4

    );

}


/* =========================
   공 개수 표시
========================= */

function updateBallCount() {

    ballCountText.textContent =
        balls.filter(
            b => b.alive
        ).length;

}


/* =========================
   아이템
========================= */

const items = [];


function createItem(x, y) {

    /*
     * 아이템이 나올 확률
     */

    if (Math.random() > 0.30) {

        return;

    }


    const types = [

        "BALL3",
        "MULTI",
        "PADDLE",
        "LIFE"

    ];


    const type =
        types[
            Math.floor(
                Math.random() *
                types.length
            )
        ];


    items.push({

        x: x,
        y: y,

        width: 32,
        height: 20,

        dy: 2,

        type: type

    });

}


/* =========================
   아이템 글자
========================= */

function itemText(type) {

    if (type === "BALL3") {

        return "+3";

    }

    if (type === "MULTI") {

        return "×3";

    }

    if (type === "PADDLE") {

        return "BIG";

    }

    if (type === "LIFE") {

        return "+1";

    }

    return "?";

}


/* =========================
   아이템 획득
========================= */

function collectItem(item) {

    if (item.type === "BALL3") {

        /*
         * 공 3개 추가
         */

        for (
            let i = 0;
            i < 3;
            i++
        ) {

            createBall(

                paddle.x +
                paddle.width / 2,

                paddle.y - 10,

                (Math.random() - 0.5) * 8,

                -5

            );

        }

    }


    else if (
        item.type === "MULTI"
    ) {

        /*
         * 현재 공 하나를
         * 여러 개로 복제
         */

        const current =
            balls.filter(
                b => b.alive
            );


        const copies = [];


        current.forEach(function(ball) {

            copies.push({

                x: ball.x,

                y: ball.y,

                radius: 7,

                dx: ball.dx + 2,

                dy: ball.dy,

                alive: true

            });


            copies.push({

                x: ball.x,

                y: ball.y,

                radius: 7,

                dx: ball.dx - 2,

                dy: ball.dy,

                alive: true

            });

        });


        balls =
            balls.concat(copies);

    }


    else if (
        item.type === "PADDLE"
    ) {

        paddle.width = 180;


        /*
         * 8초 뒤 원래 크기로
         */

        setTimeout(function() {

            paddle.width =
                paddle.normalWidth;

        }, 8000);

    }


    else if (
        item.type === "LIFE"
    ) {

        lives++;

        livesText.textContent =
            lives;

    }


    updateBallCount();

}


/* =========================
   벽돌 내려오기
========================= */

function moveBricks(delta) {

    /*
     * 시간이 지나면
     * 조금씩 아래로 이동
     */

    const speed =
        brickSpeed +
        round * 0.01;


    bricks.forEach(function(brick) {

        if (!brick.alive) return;

        brick.y +=
            speed * delta;


        /*
         * 바닥에 도착하면 게임 오버
         */

        if (
            brick.y +
            brick.height >=
            paddle.y
        ) {

            gameOver();

        }

    });

}


/* =========================
   공 이동
========================= */

function moveBalls() {

    balls.forEach(function(ball) {

        if (!ball.alive) return;


        ball.x += ball.dx;
        ball.y += ball.dy;


        /*
         * 좌우 벽
         */

        if (
            ball.x -
            ball.radius <= 0
        ) {

            ball.x =
                ball.radius;

            ball.dx =
                Math.abs(ball.dx);

        }


        if (
            ball.x +
            ball.radius >=
            canvas.width
        ) {

            ball.x =
                canvas.width -
                ball.radius;

            ball.dx =
                -Math.abs(ball.dx);

        }


        /*
         * 위쪽 벽
         */

        if (
            ball.y -
            ball.radius <= 0
        ) {

            ball.y =
                ball.radius;

            ball.dy =
                Math.abs(ball.dy);

        }


        /*
         * 패들 충돌
         */

        if (

            ball.dy > 0 &&

            ball.y +
            ball.radius >=
            paddle.y &&

            ball.y -
            ball.radius <=
            paddle.y +
            paddle.height &&

            ball.x >=
            paddle.x &&

            ball.x <=
            paddle.x +
            paddle.width

        ) {


            /*
             * 패들의 어디를 맞췄는지
             */

            const hit =
                (
                    ball.x -
                    paddle.x
                ) /
                paddle.width;


            /*
             * -5 ~ +5
             */

            ball.dx =
                (hit - 0.5) * 10;


            /*
             * 항상 위로
             */

            ball.dy =
                -Math.abs(ball.dy);


            /*
             * 패들에 박혀버리는 현상 방지
             */

            ball.y =
                paddle.y -
                ball.radius;

        }


        /*
         * 바닥으로 떨어짐
         */

        if (
            ball.y -
            ball.radius >
            canvas.height
        ) {

            ball.alive = false;

        }


        /*
         * 벽돌 충돌
         */

        bricks.forEach(function(brick) {

            if (!brick.alive) return;


            if (

                ball.x +
                ball.radius >
                brick.x &&

                ball.x -
                ball.radius <
                brick.x +
                brick.width &&

                ball.y +
                ball.radius >
                brick.y &&

                ball.y -
                ball.radius <
                brick.y +
                brick.height

            ) {


                /*
                 * 벽돌 체력 감소
                 */

                brick.hp--;


                /*
                 * 공 반사
                 */

                ball.dy *= -1;


                /*
                 * 체력이 0이면 파괴
                 */

                if (
                    brick.hp <= 0
                ) {

                    brick.alive = false;


                    score +=
                        brick.maxHp * 10;


                    scoreText.textContent =
                        score;


                    /*
                     * 아이템 생성
                     */

                    createItem(

                        brick.x +
                        brick.width / 2,

                        brick.y +
                        brick.height / 2

                    );

                }


            }

        });

    });


    /*
     * 죽은 공 제거
     */

    balls =
        balls.filter(
            b => b.alive
        );


    updateBallCount();


    /*
     * 공이 전부 사라지면
     * 목숨 감소
     */

    if (
        balls.length === 0 &&
        gameRunning
    ) {

        loseLife();

    }

}


/* =========================
   아이템 이동
========================= */

function moveItems() {

    items.forEach(function(item) {

        item.y += item.dy;


        /*
         * 패들과 충돌
         */

        if (

            item.y +
            item.height >=
            paddle.y &&

            item.y <=
            paddle.y +
            paddle.height &&

            item.x +
            item.width >=
            paddle.x &&

            item.x <=
            paddle.x +
            paddle.width

        ) {

            collectItem(item);

            item.collected = true;

        }


        /*
         * 화면 밖
         */

        if (
            item.y >
            canvas.height + 50
        ) {

            item.collected = true;

        }

    });


    /*
     * 획득한 아이템 제거
     */

    for (
        let i = items.length - 1;
        i >= 0;
        i--
    ) {

        if (
            items[i].collected
        ) {

            items.splice(i, 1);

        }

    }

}


/* =========================
   목숨 감소
========================= */

function loseLife() {

    lives--;

    livesText.textContent =
        lives;


    if (lives <= 0) {

        gameOver();

        return;

    }


    /*
     * 새로운 공
     */

    resetBalls();

}


/* =========================
   라운드 확인
========================= */

function checkRound() {

    const remaining =
        bricks.filter(
            b => b.alive
        ).length;


    if (
        remaining === 0
    ) {

        round++;

        roundText.textContent =
            round;


        /*
         * 다음 라운드
         */

        startRound();

    }

}


/* =========================
   라운드 시작
========================= */

function startRound() {

    bricks = [];

    items.length = 0;


    /*
     * 라운드 시작 시
     * 벽돌 여러 줄 생성
     */

    const rowCount =
        Math.min(
            4 +
            Math.floor(round / 2),
            9
        );


    for (
        let i = 0;
        i < rowCount;
        i++
    ) {

        setTimeout(
            function() {

                if (gameRunning) {

                    createBrickRow();

                }

            },
            i * 650
        );

    }


    /*
     * 라운드가 높을수록
     * 벽돌 생성 속도 증가
     */

    brickSpeed =
        0.10 +
        round * 0.015;

}


/* =========================
   게임 오버
========================= */

function gameOver() {

    if (!gameRunning) {
        return;
    }


    gameRunning = false;


    message.textContent =
        "GAME OVER";


}


/* =========================
   그림
========================= */

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /*
     * 배경 격자
     */

    ctx.strokeStyle =
        "rgba(255,255,255,0.04)";


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


    /*
     * 벽돌
     */

    bricks.forEach(function(brick) {

        if (!brick.alive) return;


        const colors = [

            "#ff5252",
            "#ff9800",
            "#ffeb3b",
            "#4caf50",
            "#2196f3",
            "#9c27b0"

        ];


        ctx.fillStyle =
            colors[
                Math.min(
                    brick.maxHp - 1,
                    colors.length - 1
                )
            ];


        ctx.fillRect(

            brick.x,
            brick.y,
            brick.width,
            brick.height

        );


        /*
         * 체력 숫자
         */

        ctx.fillStyle =
            "black";

        ctx.font =
            "bold 14px Arial";

        ctx.textAlign =
            "center";

        ctx.fillText(

            brick.hp,

            brick.x +
            brick.width / 2,

            brick.y +
            18

        );

    });


    /*
     * 패들
     */

    ctx.fillStyle =
        "#3478f6";


    ctx.fillRect(

        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height

    );


    /*
     * 공
     */

    balls.forEach(function(ball) {

        if (!ball.alive) return;


        ctx.beginPath();


        ctx.arc(

            ball.x,
            ball.y,
            ball.radius,
            0,
            Math.PI * 2

        );


        ctx.fillStyle =
            "#ffffff";

        ctx.fill();


        ctx.closePath();

    });


    /*
     * 아이템
     */

    items.forEach(function(item) {

        ctx.fillStyle =
            "#ffffff";


        ctx.fillRect(

            item.x,
            item.y,
            item.width,
            item.height

        );


        ctx.fillStyle =
            "#111";


        ctx.font =
            "bold 12px Arial";

        ctx.textAlign =
            "center";


        ctx.fillText(

            itemText(item.type),

            item.x +
            item.width / 2,

            item.y + 15

        );

    });

}


/* =========================
   다시 시작
========================= */

function restartGame() {

    score = 0;

    lives = 3;

    round = 1;

    gameRunning = true;


    scoreText.textContent =
        score;

    livesText.textContent =
        lives;

    roundText.textContent =
        round;


    paddle.width =
        paddle.normalWidth;


    paddle.x =
        canvas.width / 2 -
        paddle.width / 2;


    bricks = [];

    balls = [];

    items.length = 0;


    message.textContent = "";


    resetBalls();

    startRound();

}


/* =========================
   버튼
========================= */

restartButton.addEventListener(
    "click",
    function() {

        restartGame();

    }
);


/* =========================
   게임 루프
========================= */

function gameLoop(time) {

    const delta =
        Math.min(
            time - lastTime,
            50
        );


    lastTime = time;


    if (gameRunning) {

        /*
         * 패들
         */

        if (leftPressed) {

            paddle.x -=
                paddle.speed;

        }


        if (rightPressed) {

            paddle.x +=
                paddle.speed;

        }


        keepPaddleInside();


        /*
         * 공
         */

        moveBalls();


        /*
         * 벽돌
         */

        moveBricks(delta);


        /*
         * 아이템
         */

        moveItems();


        /*
         * 라운드
         */

        checkRound();

    }


    draw();


    requestAnimationFrame(
        gameLoop
    );

}


/* =========================
   최초 시작
========================= */

restartGame();

requestAnimationFrame(
    gameLoop
);

</script>

</body>
</html>
'''

components.html(
    html_code,
    height=700,
    scrolling=False
)
