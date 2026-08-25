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

    x: 305
