import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기",
    page_icon="🧱",
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
    background: #111;
    overflow: hidden;
}

#container {
    width: 100%;
    text-align: center;
    font-family: Arial, sans-serif;
}

#info {
    color: white;
    font-size: 18px;
    margin: 8px;
}

canvas {
    background: #080b16;
    border: 2px solid #555;
    border-radius: 8px;
    max-width: 100%;
    touch-action: none;
}

button {
    margin-top: 10px;
    padding: 10px 25px;
    font-size: 16px;
    border: 0;
    border-radius: 7px;
    background: #4c8bf5;
    color: white;
    cursor: pointer;
}

button:active {
    transform: scale(0.97);
}
</style>
</head>

<body>

<div id="container">

    <div id="info">
        점수: <span id="score">0</span>
        &nbsp;&nbsp;
        목숨: <span id="lives">3</span>
    </div>

    <canvas id="game" width="720" height="500"></canvas>

    <br>

    <button id="restart">다시 시작</button>

</div>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scoreText = document.getElementById("score");
const livesText = document.getElementById("lives");
const restartButton = document.getElementById("restart");


/* =========================
   게임 변수
========================= */

let score = 0;
let lives = 3;
let gameRunning = true;

const paddle = {
    width: 110,
    height: 14,
    x: 305,
    y: 455,
    speed: 8
};

const ball = {
    x: 360,
    y: 430,
    radius: 8,
    dx: 4,
    dy: -4
};


/* =========================
   벽돌
========================= */

const rows = 6;
const columns = 10;

const brickWidth = 62;
const brickHeight = 22;
const padding = 8;

let bricks = [];

function makeBricks() {

    bricks = [];

    const totalWidth =
        columns * brickWidth +
        (columns - 1) * padding;

    const startX =
        (canvas.width - totalWidth) / 2;

    for (let row = 0; row < rows; row++) {

        for (let col = 0; col < columns; col++) {

            bricks.push({
                x: startX + col * (brickWidth + padding),
                y: 45 + row * (brickHeight + padding),
                width: brickWidth,
                height: brickHeight,
                alive: true
            });

        }
    }
}


/* =========================
   키보드
========================= */

let leftPressed = false;
let rightPressed = false;

document.addEventListener("keydown", function(e) {

    if (e.key === "ArrowLeft" || e.key.toLowerCase() === "a") {
        leftPressed = true;
    }

    if (e.key === "ArrowRight" || e.key.toLowerCase() === "d") {
        rightPressed = true;
    }

});

document.addEventListener("keyup", function(e) {

    if (e.key === "ArrowLeft" || e.key.toLowerCase() === "a") {
        leftPressed = false;
    }

    if (e.key === "ArrowRight" || e.key.toLowerCase() === "d") {
        rightPressed = false;
    }

});


/* =========================
   패들
========================= */

function movePaddle() {

    if (leftPressed) {
        paddle.x -= paddle.speed;
    }

    if (rightPressed) {
        paddle.x += paddle.speed;
    }

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }

}


/* =========================
   마우스
========================= */

canvas.addEventListener("mousemove", function(e) {

    const rect = canvas.getBoundingClientRect();

    const mouseX =
        (e.clientX - rect.left) *
        canvas.width / rect.width;

    paddle.x = mouseX - paddle.width / 2;

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }

});


/* =========================
   터치
========================= */

canvas.addEventListener("touchmove", function(e) {

    e.preventDefault();

    const rect = canvas.getBoundingClientRect();

    const touchX =
        (e.touches[0].clientX - rect.left) *
        canvas.width / rect.width;

    paddle.x = touchX - paddle.width / 2;

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }

}, { passive: false });


/* =========================
   그리기
========================= */

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // 벽돌
    bricks.forEach(function(brick, index) {

        if (!brick.alive) return;

        const colors = [
            "#ff5252",
            "#ff9800",
            "#ffeb3b",
            "#4caf50",
            "#2196f3",
            "#9c27b0"
        ];

        ctx.fillStyle = colors[index % colors.length];

        ctx.fillRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height
        );

    });


    // 패들
    ctx.fillStyle = "#4c8bf5";

    ctx.fillRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height
    );


    // 공
    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI
