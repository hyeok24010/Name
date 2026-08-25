import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기")

game = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
    body {
        margin: 0;
        background: #111;
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }

    #gameWrapper {
        text-align: center;
        width: 100%;
    }

    canvas {
        background: #080b16;
        border: 2px solid #555;
        border-radius: 8px;
        max-width: 100%;
        height: auto;
        touch-action: none;
    }

    #info {
        color: white;
        margin: 8px 0;
        font-size: 17px;
    }

    button {
        padding: 9px 20px;
        border: none;
        border-radius: 6px;
        background: #4c8bf5;
        color: white;
        font-size: 15px;
        cursor: pointer;
    }

    button:hover {
        background: #3677df;
    }
</style>
</head>

<body>

<div id="gameWrapper">

    <div id="info">
        점수: <span id="score">0</span>
        &nbsp;&nbsp; 목숨: <span id="lives">3</span>
    </div>

    <canvas id="game" width="720" height="500"></canvas>

    <br>

    <button onclick="restartGame()">다시 시작</button>

</div>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scoreText = document.getElementById("score");
const livesText = document.getElementById("lives");

let score = 0;
let lives = 3;
let gameRunning = true;

const paddle = {
    width: 110,
    height: 14,
    x: canvas.width / 2 - 55,
    y: canvas.height - 35,
    speed: 8
};

const ball = {
    x: canvas.width / 2,
    y: canvas.height - 60,
    radius: 8,
    dx: 4,
    dy: -4
};

const brickRows = 6;
const brickColumns = 10;

const brickWidth = 62;
const brickHeight = 22;
const brickPadding = 8;

const bricks = [];

function createBricks() {

    bricks.length = 0;

    const totalWidth =
        brickColumns * brickWidth +
        (brickColumns - 1) * brickPadding;

    const startX = (canvas.width - totalWidth) / 2;

    for (let r = 0; r < brickRows; r++) {

        for (let c = 0; c < brickColumns; c++) {

            bricks.push({
                x: startX + c * (brickWidth + brickPadding),
                y: 45 + r * (brickHeight + brickPadding),
                width: brickWidth,
                height: brickHeight,
                alive: true
            });

        }

    }
}

createBricks();

let keys = {
    left: false,
    right: false
};

document.addEventListener("keydown", function(e) {

    if (e.key === "ArrowLeft" || e.key.toLowerCase() === "a") {
        keys.left = true;
    }

    if (e.key === "ArrowRight" || e.key.toLowerCase() === "d") {
        keys.right = true;
    }

});

document.addEventListener("keyup", function(e) {

    if (e.key === "ArrowLeft" || e.key.toLowerCase() === "a") {
        keys.left = false;
    }

    if (e.key === "ArrowRight" || e.key.toLowerCase() === "d") {
        keys.right = false;
    }

});


// 마우스 조작
canvas.addEventListener("mousemove", function(e) {

    const rect = canvas.getBoundingClientRect();

    const mouseX =
        (e.clientX - rect.left) *
        (canvas.width / rect.width);

    paddle.x = mouseX - paddle.width / 2;

    keepPaddleInside();

});


// 터치 조작
canvas.addEventListener("touchmove", function(e) {

    e.preventDefault();

    const rect = canvas.getBoundingClientRect();

    const touchX =
        (e.touches[0].clientX - rect.left) *
        (canvas.width / rect.width);

    paddle.x = touchX - paddle.width / 2;

    keepPaddleInside();

}, { passive: false });


function keepPaddleInside() {

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }

}


function drawPaddle() {

    ctx.fillStyle = "#4c8bf5";

    ctx.fillRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height
    );

}


function drawBall() {

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.closePath();

}


function drawBricks() {

    bricks.forEach(brick => {

        if (!brick.alive) return;

        const colors = [
            "#ff5252",
            "#ff9800",
            "#ffeb3b",
            "#4caf50",
            "#2196f3",
            "#9c27b0"
        ];

        ctx.fillStyle = colors[
            Math.floor(brick.y / 30) % colors.length
        ];

        ctx.fillRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height
        );

    });

}


function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();
    drawPaddle();
    drawBall();

}


function updatePaddle() {

    if (keys.left) {
        paddle.x -= paddle.speed;
    }

    if (keys.right) {
        paddle.x += paddle.speed;
    }

    keepPaddleInside();

}


function collisionDetection() {

    bricks.forEach(brick => {

        if (!brick.alive) return;

        if (
            ball.x + ball.radius > brick.x &&
            ball.x - ball.radius < brick.x + brick.width &&
            ball.y + ball.radius > brick.y &&
            ball.y - ball.radius < brick.y + brick.height
        ) {

            brick.alive = false;

            ball.dy *= -1;

            score += 10;

            scoreText.textContent = score;

            checkWin();

        }

    });

}


function checkWin() {

    const remaining = bricks.filter(
        brick => brick.alive
    ).length;

    if (remaining === 0) {

        gameRunning = false;

        setTimeout(() => {

            alert(
                "🎉 클리어!\n최종 점수: " + score
            );

        }, 100);

    }

}


function resetBall() {

    ball.x = canvas.width / 2;
    ball.y = canvas.height - 60;

    ball.dx =
        (Math.random() > 0.5 ? 1 : -1) * 4;

    ball.dy = -4;

}


function loseLife() {

    lives--;

    livesText.textContent = lives;

    if (lives <= 0) {

        gameRunning = false;

        setTimeout(() => {

            alert(
                "게임 오버!\n점수: " + score
            );

        }, 100);

        return;

    }

    resetBall();

}


function updateBall() {

    ball.x += ball.dx;
    ball.y += ball.dy;


    // 좌우 벽
    if (
        ball.x + ball.radius >= canvas.width ||
        ball.x - ball.radius <= 0
    ) {

        ball.dx *= -1;

    }


    // 위쪽 벽
    if (ball.y - ball.radius <= 0) {

        ball.dy *= -1;

    }


    // 패들 충돌
    if (
        ball.y + ball.radius >= paddle.y &&
        ball.y - ball.radius <= paddle.y + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width &&
        ball.dy > 0
    ) {

        // 패들 중앙에서 얼마나 떨어졌는지 계산
        const hitPosition =
            (ball.x - paddle.x) /
            paddle.width;

        // -1 ~ 1
        const normalized =
            hitPosition * 2 - 1;

        ball.dx = normalized * 6;

        ball.dy = -Math.abs(ball.dy);

    }


    // 바닥
    if (ball.y - ball.radius > canvas.height) {

        loseLife();

    }

}


function gameLoop() {

    if (gameRunning) {

        updatePaddle();
        updateBall();
        collisionDetection();

    }

    draw();

    requestAnimationFrame(gameLoop);

}


function restartGame() {

    score = 0;
    lives = 3;

    scoreText.textContent = score;
    livesText.textContent = lives;

    paddle.x =
        canvas.width / 2 -
        paddle.width / 2;

    resetBall();

    createBricks();

    gameRunning = true;

}


gameLoop();

</script>

</body>
</html>
"""

components.html(game, height=600, scrolling=False)
