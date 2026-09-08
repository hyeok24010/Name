import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="누루룽 서바이버",
    page_icon="🎮",
    layout="wide"
)

html = r'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">

<style>
*{
    box-sizing:border-box
}

html,body{
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#111;
}

body{
    touch-action:none;
    font-family:Arial,sans-serif;
    color:white;
}

#gamebox{
    position:relative;
    width:100%;
    height:560px;
    max-height:100%;
    overflow:hidden;
    background:#172017;
}

canvas{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    display:block;
}

#hud{
    position:absolute;
    left:7px;
    right:7px;
    top:6px;
    z-index:5;
    text-shadow:0 1px 2px #000;
    font-size:11px;
}

.line{
    display:flex;
    align-items:center;
    gap:5px;
}

.bar{
    height:13px;
    border:1px solid #222;
    border-radius:8px;
    background:#333;
    overflow:hidden;
}

.bar i{
    display:block;
    height:100%;
    width:100%;
}

#hp{
    width:min(190px,43vw);
}

#hp i{
    background:#e53935;
}

#shield{
    width:min(120px,30vw);
    display:none;
}

#shield i{
    background:#42a5f5;
}

#xp{
    height:8px;
    width:min(380px,70vw);
    margin-top:3px;
}

#xp i{
    background:#f5c518;
}

#info{
    margin-top:2px;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

.overlay{
    position:absolute;
    inset:0;
    z-index:20;
    background:rgba(0,0,0,.78);
    display:flex;
    align-items:center;
    justify-content:center;
    padding:10px;
}

.hidden{
    display:none!important;
}

.panel{
    width:min(850px,94%);
    max-height:94%;
    overflow:auto;
    background:#20242a;
    border:1px solid #555;
    border-radius:15px;
    padding:16px;
    text-align:center;
    box-shadow:0 8px 30px #000;
}

.panel h1{
    font-size:25px;
    margin:2px 0 8px;
}

.panel p{
    color:#bbb;
    margin:5px 0 12px;
}

.classes{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:9px;
}

.upgrades{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:8px;
}

button{
    border:0;
    border-radius:11px;
    background:#303840;
    color:#fff;
    padding:12px;
    font-size:14px;
    font-weight:bold;
    cursor:pointer;
}

.classbtn{
    min-height:105px;
}

.classbtn b{
    font-size:23px;
    display:block;
    margin-bottom:5px;
}

.classbtn small,
.up small{
    color:#bbb;
    line-height:1.3;
}

.up{
    text-align:left;
    min-height:75px;
}

.up strong{
    font-size:14px;
}

.up small{
    display:block;
    margin-top:5px;
}

.action{
    position:absolute;
    right:12px;
    width:86px;
    height:47px;
    padding:4px;
    font-size:12px;
    z-index:8;
}

.action:active{
    transform:scale(.96);
}

#skill{
    bottom:70px;
    background:#7047a8;
}

#form{
    bottom:13px;
    background:#28627d;
}

#joy{
    position:absolute;
    left:12px;
    bottom:12px;
    width:104px;
    height:104px;
    border-radius:50%;
    background:rgba(255,255,255,.1);
    border:1px solid rgba(255,255,255,.22);
    z-index:8;
    pointer-events:auto;
}

#stick{
    position:absolute;
    width:42px;
    height:42px;
    left:30px;
    top:30px;
    border-radius:50%;
    background:rgba(255,255,255,.35);
}

#msg{
    position:absolute;
    top:46%;
    left:50%;
    transform:translate(-50%,-50%);
    z-index:9;
    font-size:22px;
    font-weight:bold;
    text-shadow:0 2px 4px #000;
    pointer-events:none;
    text-align:center;
}

@media(max-width:650px){

    #gamebox{
        height:500px;
    }

    .panel{
        padding:11px;
        border-radius:12px;
    }

    .panel h1{
        font-size:21px;
    }

    .panel p{
        font-size:11px;
    }

    .classes{
        grid-template-columns:1fr;
        gap:6px;
    }

    .classbtn{
        min-height:65px;
        padding:8px;
    }

    .classbtn b{
        font-size:19px;
        margin-bottom:2px;
    }

    .classbtn small{
        font-size:10px;
    }

    .upgrades{
        gap:6px;
    }

    .up{
        min-height:67px;
        padding:8px;
    }

    .up strong{
        font-size:12px;
    }

    .up small{
        font-size:9px;
    }

    .action{
        width:82px;
        height:44px;
        right:10px;
    }

    .bar{
        height:12px;
    }

    #hp{
        width:42vw;
    }

    #shield{
        width:28vw;
    }

    #xp{
        width:72vw;
    }

    #info{
        font-size:10px;
    }

    #msg{
        font-size:18px;
    }
}

@media(min-width:651px){

    #gamebox{
        height:680px;
    }

    .action{
        right:20px;
        width:105px;
        height:55px;
        font-size:14px;
    }

    #skill{
        bottom:88px;
    }

    #form{
        bottom:22px;
    }

    #joy{
        left:20px;
        bottom:20px;
        width:130px;
        height:130px;
    }

    #stick{
        left:37px;
        top:37px;
        width:54px;
        height:54px;
    }
}
</style>
</head>

<body>

<div id="gamebox">

<canvas id="c"></canvas>

<div id="hud">

    <div class="line">

        <div class="bar" id="hp">
            <i></i>
        </div>

        <div class="bar" id="shield">
            <i></i>
        </div>

        <span id="stats">
            Lv.1 | 0:00 | 처치 0
        </span>

    </div>

    <div class="bar" id="xp">
        <i></i>
    </div>

    <div id="info">
        직업을 선택하세요
    </div>

</div>


<div id="msg"></div>


<div id="joy">
    <div id="stick"></div>
</div>


<button id="skill" class="action">
    스킬
</button>

<button id="form" class="action hidden">
    폼체인지
</button>


<!-- 직업 선택 -->

<div id="select" class="overlay">

    <div class="panel">

        <h1>
            🎮 누루룽 서바이버
        </h1>

        <p>
            직업을 선택하세요
        </p>

        <div class="classes">

            <button
                class="classbtn"
                onclick="start('gun')"
            >
                <b>🔫 총</b>

                <small>
                    권총 / 저격<br>
                    빠른 사격 / 강한 관통
                </small>
            </button>


            <button
                class="classbtn"
                onclick="start('sword')"
            >
                <b>⚔️ 검사</b>

                <small>
                    베기 / 검기<br>
                    근접 공격 + 전방 검기
                </small>
            </button>


            <button
                class="classbtn"
                onclick="start('magic')"
            >
                <b>🔮 마법</b>

                <small>
                    마법탄 / 강화공격 / 각성<br>
                    레이저 공격
                </small>
            </button>

        </div>

    </div>

</div>


<!-- 레벨업 -->

<div id="level" class="overlay hidden">

    <div class="panel">

        <h1>
            LEVEL UP!
        </h1>

        <p>
            강화할 능력을 하나 선택하세요.
        </p>

        <div
            id="ups"
            class="upgrades"
        ></div>

    </div>

</div>


<!-- 게임오버 -->

<div id="over" class="overlay hidden">

    <div class="panel">

        <h1>
            게임 오버
        </h1>

        <p id="result"></p>

        <button onclick="location.reload()">
            다시 시작
        </button>

    </div>

</div>


</div>


<script>

const cv =
    document.getElementById("c");

const ctx =
    cv.getContext("2d");


let W = 0;
let H = 0;
let dpr = 1;


function resize(){

    dpr =
        Math.min(
            devicePixelRatio || 1,
            2
        );

    W = cv.clientWidth;
    H = cv.clientHeight;

    cv.width =
        W * dpr;

    cv.height =
        H * dpr;

    ctx.setTransform(
        dpr,
        0,
        0,
        dpr,
        0,
        0
    );
}


addEventListener(
    "resize",
    resize
);

resize();


const TAU =
    Math.PI * 2;


const clamp =
    (v,a,b) =>
        Math.max(
            a,
            Math.min(b,v)
        );


const D =
    (a,b) =>
        Math.hypot(
            a.x-b.x,
            a.y-b.y
        );


let state = "select";

let last = 0;

let time = 0;

let level = 1;

let xp = 0;

let need = 10;

let kills = 0;

let nextSpawn = 0;

let nextBoss = 100;


let enemies = [];

let shots = [];

let slashes = [];

let lasers = [];

let parts = [];


let p = null;


let keys = {};

let joy = {
    x:0,
    y:0
};


/* =========================
   플레이어
========================= */

function start(cls){

    p = {

        cls,

        x:W/2,
        y:H/2,

        r:17,

        hp:100,
        maxHp:100,

        speed:180,

        damage:15,

        atk:2,

        range:190,

        area:1,

        projectiles:1,

        penetration:0,

        projSpeed:500,


        shield:0,
        maxShield:0,

        reduction:0,


        face:0,


        /* 총 */

        gunForm:"pistol",

        gunSkill:0,

        formCd:0,


        /* 검사 */

        swordDamage:22,

        swordAtk:1.5,

        waveDamage:9,

        waveAtk:.55,

        waveCount:1,

        waveSize:11,


        /* 마법 */

        magicDamage:14,

        magicAtk:1.5,

        laserDamage:28,

        laserDuration:.8,

        laserCount:1,

        enhancedEvery:10,

        enhancedCount:0,


        /* 스킬 */

        skillCd:0,

        skillProgress:0,

        skillNeed:12,

        skillDuration:5,

        skillActive:false,

        skillTimer:0,


        inv:0,

        _a:0,

        _w:0

    };


    state = "play";


    document
        .getElementById("select")
        .classList
        .add("hidden");


    document
        .getElementById("form")
        .classList
        .toggle(
            "hidden",
            cls !== "gun"
        );


    updateUI();


    requestAnimationFrame(
        loop
    );
}


/* =========================
   가장 가까운 적
========================= */

function nearest(){

    let b = null;

    let bd = Infinity;


    for(
        const e of enemies
    ){

        let d =
            D(p,e);

        if(d < bd){

            bd = d;

            b = e;

        }

    }


    return b;
}


function aim(){

    let e =
        nearest();

    if(!e)
        return p.face;


    return Math.atan2(
        e.y-p.y,
        e.x-p.x
    );
}


/* =========================
   총
========================= */

function shootGun(){

    let e =
        nearest();

    if(!e)
        return;


    let a =
        aim();


    let d =
        p.damage;


    let s =
        p.projSpeed;


    let r =
        p.range;


    let pen =
        p.penetration;


    /* 권총 */

    if(
        p.gunForm === "pistol"
    ){

        d *= .8;

        s *= 1.15;

        r *= .9;

    }


    /* 저격 */

    else{

        d *= 1.9;

        r *= 1.45;

        pen += 2;

    }


    /*
       총 스킬

       현재 투사체 수와
       관통력을 그대로 사용
    */

    if(
        p.gunSkill > 0
    ){

        d *= 1.7;

        s *= 1.35;

    }


    /*
       투사체 수

       일반 공격과 스킬 모두
       p.projectiles 사용
    */

    for(
        let i=0;
        i<p.projectiles;
        i++
    ){

        let spread =
            (
                i -
                (p.projectiles-1)/2
            ) * .1;


        shots.push({

            x:p.x,
            y:p.y,

            a:a+spread,

            speed:s,

            dmg:d,

            pen,

            range:r,

            t:0,

            r:5,

            type:"gun"

        });

    }


    p.face = a;
}


/* =========================
   검사 - 베기
========================= */

function slash(){

    p.face =
        aim();


    slashes.push({

        x:p.x,
        y:p.y,

        a:p.face,

        life:.18,

        max:.18,

        range:
            90*p.area,

        fan:1.25,

        dmg:
            p.swordDamage

    });

}


/* =========================
   검사 - 검기
========================= */

function wave(){

    let e =
        nearest();

    if(!e)
        return;


    let a =
        Math.atan2(
            e.y-p.y,
            e.x-p.x
        );


    p.face = a;


    for(
        let i=0;
        i<p.waveCount;
        i++
    ){

        let spread =
            (
                i -
                (p.waveCount-1)/2
            ) * .12;


        shots.push({

            x:p.x,
            y:p.y,

            a:a+spread,

            speed:360,

            dmg:p.waveDamage,

            /*
                검기는 모든 적 관통
            */

            pen:999999,

            range:p.range*1.25,

            t:0,

            r:p.waveSize*p.area,

            type:"wave"

        });

    }

}


/* =========================
   마법
========================= */

function magic(){

    let e =
        nearest();

    if(!e)
        return;


    let a =
        Math.atan2(
            e.y-p.y,
            e.x-p.x
        );


    /*
       각성 중이면
       모든 평타가 강화공격
    */

    let enhanced =
        p.skillActive ||
        p.enhancedCount >=
        p.enhancedEvery;


    p.face = a;


    if(enhanced){

        p.enhancedCount = 0;

        makeLasers(
            p.skillActive
        );

    }

    else{

        p.enhancedCount++;


        shots.push({

            x:p.x,
            y:p.y,

            a,

            speed:430,

            dmg:p.magicDamage,

            pen:0,

            range:p.range,

            t:0,

            r:6,

            type:"magic"

        });

    }

}


/* =========================
   레이저
========================= */

function makeLasers(
    awake
){

    /*
       일반 강화공격:
       가로 또는 세로

       각성:
       가로 + 세로
    */

    let dirs =
        awake
            ? [0,Math.PI/2]
            : [
                Math.random()<.5
                    ? 0
                    : Math.PI/2
              ];


    for(
        const a of dirs
    ){

        for(
            let i=0;
            i<p.laserCount;
            i++
        ){

            lasers.push({

                x:p.x,
                y:p.y,

                a,

                off:
                    (
                        i -
                        (p.laserCount-1)/2
                    ) *
                    34 *
                    p.area,

                life:
                    p.laserDuration,

                max:
                    p.laserDuration,

                dmg:
                    p.laserDamage *
                    p.area *
                    (
                        awake
                            ? 1.35
                            : 1
                    )

            });

        }

    }

}


/* =========================
   스킬
========================= */

function useSkill(){

    if(!p)
        return;


    if(
        p.skillCd > 0 ||
        p.skillActive ||
        p.skillProgress < p.skillNeed
    )
        return;


    /*
       게이지 소비
    */

    p.skillProgress = 0;


    /* 마법 */

    if(
        p.cls === "magic"
    ){

        p.skillActive = true;

        p.skillTimer =
            p.skillDuration;

    }


    /* 검사 */

    else if(
        p.cls === "sword"
    ){

        p.shield =
            p.maxShield =
            Math.max(
                50,
                p.maxHp*.75
            );

        p.skillCd = 8;

    }


    /* 총 */

    else{

        p.gunSkill = 2.5;

        p.skillCd = 6;

    }

}


/* =========================
   총 폼체인지
========================= */

function formChange(){

    if(
        p &&
        p.cls === "gun" &&
        p.formCd <= 0
    ){

        p.gunForm =
            p.gunForm === "pistol"
                ? "sniper"
                : "pistol";


        p.formCd = 1;

    }

}


/* =========================
   적 생성
========================= */

function spawn(
    boss=false
){

    let side =
        Math.floor(
            Math.random()*4
        );


    let margin = 40;


    let x;
    let y;


    if(side===0){

        x=-margin;

        y=Math.random()*H;

    }

    else if(side===1){

        x=W+margin;

        y=Math.random()*H;

    }

    else if(side===2){

        x=Math.random()*W;

        y=-margin;

    }

    else{

        x=Math.random()*W;

        y=H+margin;

    }


    let hp =
        (
            10 +
            time*.09 +
            level*.7
        ) *
        (
            boss
                ? 18
                : 1
        );


    enemies.push({

        x,
        y,

        r:
            boss
                ? 28
                : 13,

        hp,

        maxHp:hp,

        speed:
            (
                boss
                    ? 34
                    : 44
            ) +
            Math.min(
                35,
                time*.035
            ),

        dmg:
            (
                boss
                    ? 10
                    : 5
            ) +
            time*.012 +
            level*.1,

        boss

    });

}


/* =========================
   경험치
========================= */

function gain(n){

    xp += n;


    while(
        xp >= need
    ){

        xp -= need;

        level++;


        need =
            Math.floor(
                10 +
                level*4
            );


        showLevel();

    }

}


/* =========================
   적 처치
========================= */

function killed(e){

    kills++;


    gain(
        e.boss
            ? 15
            : 1
    );


    /*
       마법 각성 중에는
       처치해도 게이지 증가 X
    */

    if(
        !p.skillActive
    ){

        p.skillProgress =
            Math.min(
                p.skillNeed,
                p.skillProgress+1
            );

    }


    for(
        let i=0;
        i<3;
        i++
    ){

        parts.push({

            x:e.x,
            y:e.y,

            vx:
                (Math.random()-.5)*100,

            vy:
                (Math.random()-.5)*100,

            life:.35

        });

    }

}


function hit(
    e,
    d
){

    e.hp -= d;


    if(
        e.hp <= 0
    ){

        let i =
            enemies.indexOf(e);


        if(i >= 0){

            enemies.splice(
                i,
                1
            );

        }


        killed(e);

    }

}


/* =========================
   플레이어 피해
========================= */

function hurt(d){

    if(
        p.inv > 0
    )
        return;


    d *=
        1-p.reduction;


    if(
        p.shield > 0
    ){

        let s =
            Math.min(
                p.shield,
                d
            );


        p.shield -= s;

        d -= s;

    }


    p.hp -= d;

    p.inv = .25;


    if(
        p.hp <= 0
    ){

        gameOver();

    }

}


/* =========================
   레벨업
========================= */

function showLevel(){

    state = "level";


    let box =
        document.getElementById(
            "ups"
        );


    box.innerHTML = "";


    let a = [];


    function add(
        name,
        desc,
        fn
    ){

        a.push({
            name,
            desc,
            fn
        });

    }


    /* 총 */

    if(
        p.cls === "gun"
    ){

        add(
            "투사체 수 +1",
            "총알 수 증가. 스킬에도 적용",
            ()=>{
                p.projectiles++;
            }
        );


        add(
            "관통 +1",
            "총알 관통 증가",
            ()=>{
                p.penetration++;
            }
        );


        add(
            "공격력 +15%",
            "총 피해 증가",
            ()=>{
                p.damage *= 1.15;
            }
        );


        add(
            "공격속도 +15%",
            "총 발사 속도 증가",
            ()=>{
                p.atk *= 1.15;
            }
        );


        add(
            "사거리 +15%",
            "총 사거리 증가",
            ()=>{
                p.range *= 1.15;
            }
        );


        add(
            "최대 HP +20",
            "체력 증가",
            ()=>{
                p.maxHp += 20;
                p.hp += 20;
            }
        );

    }


    /* 검사 */

    else if(
        p.cls === "sword"
    ){

        add(
            "검기 개수 +1",
            "한 번에 발사하는 검기 증가",
            ()=>{
                p.waveCount++;
            }
        );


        add(
            "공격 범위 +15%",
            "베기 범위와 검기 크기 증가",
            ()=>{
                p.area *= 1.15;
            }
        );


        add(
            "베기 공격력 +15%",
            "베기 피해 증가",
            ()=>{
                p.swordDamage *= 1.15;
            }
        );


        add(
            "베기 공격속도 +15%",
            "베기 속도 증가",
            ()=>{
                p.swordAtk *= 1.15;
            }
        );


        add(
            "검기 공격력 +15%",
            "검기 피해 증가",
            ()=>{
                p.waveDamage *= 1.15;
            }
        );


        add(
            "검기 공격속도 +15%",
            "검기 발사 속도 증가",
            ()=>{
                p.waveAtk *= 1.15;
            }
        );


        add(
            "피해 감소 +5%",
            "받는 피해 감소",
            ()=>{
                p.reduction =
                    Math.min(
                        .65,
                        p.reduction+.05
                    );
            }
        );


        add(
            "최대 HP +25",
            "체력 증가",
            ()=>{
                p.maxHp += 25;
                p.hp += 25;
            }
        );

    }


    /* 마법 */

    else{

        add(
            "레이저 개수 +1",
            "최대 5개",
            ()=>{
                p.laserCount =
                    Math.min(
                        5,
                        p.laserCount+1
                    );
            }
        );


        add(
            "강화공격 -1회",
            "강화공격 필요 횟수 감소. 최소 5회",
            ()=>{
                p.enhancedEvery =
                    Math.max(
                        5,
                        p.enhancedEvery-1
                    );
            }
        );


        add(
            "마법 공격력 +15%",
            "기본 마법탄 피해 증가",
            ()=>{
                p.magicDamage *= 1.15;
            }
        );


        add(
            "마법 공격속도 +15%",
            "기본 공격 속도 증가",
            ()=>{
                p.magicAtk *= 1.15;
            }
        );


        add(
            "레이저 공격력 +15%",
            "레이저 피해 증가",
            ()=>{
                p.laserDamage *= 1.15;
            }
        );


        add(
            "레이저 지속시간 +0.2초",
            "최대 2초",
            ()=>{
                p.laserDuration =
                    Math.min(
                        2,
                        p.laserDuration+.2
                    );
            }
        );


        add(
            "각성 지속시간 +0.5초",
            "최대 10초",
            ()=>{
                p.skillDuration =
                    Math.min(
                        10,
                        p.skillDuration+.5
                    );
            }
        );


        add(
            "각성 필요 처치 -1",
            "최소 6마리",
            ()=>{
                p.skillNeed =
                    Math.max(
                        6,
                        p.skillNeed-1
                    );
            }
        );


        add(
            "최대 HP +20",
            "체력 증가",
            ()=>{
                p.maxHp += 20;
                p.hp += 20;
            }
        );

    }


    /*
       랜덤 4개
    */

    a.sort(
        ()=>Math.random()-.5
    );


    a
    .slice(0,4)
    .forEach(
        o=>{

            let b =
                document.createElement(
                    "button"
                );


            b.className =
                "up";


            b.innerHTML =
                "<strong>"+
                o.name+
                "</strong>"+
                "<small>"+
                o.desc+
                "</small>";


            b.onclick =
                ()=>{

                    o.fn();


                    document
                        .getElementById(
                            "level"
                        )
                        .classList
                        .add("hidden");


                    state = "play";


                    updateUI();

                };


            box.appendChild(b);

        }
    );


    document
        .getElementById("level")
        .classList
        .remove("hidden");

}


/* =========================
   게임 업데이트
========================= */

function update(dt){

    time += dt;


    p.inv =
        Math.max(
            0,
            p.inv-dt
        );


    p.skillCd =
        Math.max(
            0,
            p.skillCd-dt
        );


    p.gunSkill =
        Math.max(
            0,
            p.gunSkill-dt
        );


    p.formCd =
        Math.max(
            0,
            p.formCd-dt
        );


    /* 이동 */

    let mx =
        joy.x;

    let my =
        joy.y;


    if(
        keys.w ||
        keys.ArrowUp
    )
        my--;


    if(
        keys.s ||
        keys.ArrowDown
    )
        my++;


    if(
        keys.a ||
        keys.ArrowLeft
    )
        mx--;


    if(
        keys.d ||
        keys.ArrowRight
    )
        mx++;


    let len =
        Math.hypot(
            mx,
            my
        );


    if(len > 1){

        mx /= len;
        my /= len;

    }


    if(
        len > .1
    ){

        p.x +=
            mx*p.speed*dt;

        p.y +=
            my*p.speed*dt;


        p.face =
            Math.atan2(
                my,
                mx
            );

    }


    p.x =
        clamp(
            p.x,
            18,
            W-18
        );


    p.y =
        clamp(
            p.y,
            18,
            H-18
        );


    /* 총 */

    if(
        p.cls === "gun"
    ){

        p._a -= dt;


        if(
            p._a <= 0
        ){

            shootGun();

            p._a +=
                1/p.atk;

        }

    }


    /* 검사 */

    else if(
        p.cls === "sword"
    ){

        p._a -= dt;


        if(
            p._a <= 0
        ){

            slash();

            p._a +=
                1/p.swordAtk;

        }


        p._w -= dt;


        if(
            p._w <= 0
        ){

            wave();

            p._w +=
                1/p.waveAtk;

        }

    }


    /* 마법 */

    else{

        p._a -= dt;


        if(
            p._a <= 0
        ){

            magic();


            let rate =
                p.magicAtk *
                (
                    p.skillActive
                        ? 1.8
                        : 1
                );


            p._a +=
                1/rate;

        }


        if(
            p.skillActive
        ){

            p.skillTimer -= dt;


            if(
                p.skillTimer <= 0
            ){

                p.skillActive =
                    false;

            }

        }

    }


    /* 적 생성 */

    if(
        time >= nextSpawn
    ){

        nextSpawn =
            time +
            Math.max(
                .35,
                1-time/500
            );


        let n =
            Math.min(
                5,
                1+
                Math.floor(
                    time/45
                )
            );


        for(
            let i=0;
            i<n;
            i++
        ){

            spawn(false);

        }

    }


    /* 보스 */

    if(
        time >= nextBoss
    ){

        nextBoss += 100;

        spawn(true);

    }


    /* 적 이동 */

    for(
        const e of enemies
    ){

        let a =
            Math.atan2(
                p.y-e.y,
                p.x-e.x
            );


        e.x +=
            Math.cos(a) *
            e.speed *
            dt;


        e.y +=
            Math.sin(a) *
            e.speed *
            dt;


        if(
            D(e,p) <
            e.r+p.r
        ){

            hurt(
                e.dmg*dt*8
            );

        }

    }


    updateShots(dt);

    updateSlashes(dt);

    updateLasers(dt);

    updateParts(dt);

    updateUI();

}


/* =========================
   투사체
========================= */

function updateShots(dt){

    for(
        let i=shots.length-1;
        i>=0;
        i--
    ){

        let q =
            shots[i];


        q.x +=
            Math.cos(q.a) *
            q.speed *
            dt;


        q.y +=
            Math.sin(q.a) *
            q.speed *
            dt;


        q.t +=
            q.speed*dt;


        let remove =
            q.t > q.range ||
            q.x < -70 ||
            q.x > W+70 ||
            q.y < -70 ||
            q.y > H+70;


        if(!remove){

            for(
                const e of [...enemies]
            ){

                if(
                    D(q,e) <
                    q.r+e.r
                ){

                    hit(
                        e,
                        q.dmg
                    );


                    if(
                        q.pen <= 0
                    ){

                        remove = true;

                        break;

                    }


                    q.pen--;

                }

            }

        }


        if(remove){

            shots.splice(
                i,
                1
            );

        }

    }

}


/* =========================
   베기
========================= */

function updateSlashes(dt){

    for(
        let i=slashes.length-1;
        i>=0;
        i--
    ){

        let s =
            slashes[i];


        s.life -= dt;


        for(
            const e of enemies
        ){

            let dx =
                e.x-s.x;

            let dy =
                e.y-s.y;

            let d =
                Math.hypot(
                    dx,
                    dy
                );


            let a =
                Math.atan2(
                    dy,
                    dx
                );


            let da =
                Math.atan2(
                    Math.sin(
                        a-s.a
                    ),
                    Math.cos(
                        a-s.a
                    )
                );


            if(
                d <
                s.range+e.r &&
                Math.abs(da) <
                s.fan/2 &&
                !e._sh
            ){

                hit(
                    e,
                    s.dmg
                );


                e._sh = .18;

            }

        }


        if(
            s.life <= 0
        ){

            slashes.splice(
                i,
                1
            );

        }

    }


    for(
        const e of enemies
    ){

        e._sh =
            Math.max(
                0,
                (e._sh||0)-dt
            );

    }

}


/* =========================
   레이저
========================= */

function updateLasers(dt){

    for(
        let i=lasers.length-1;
        i>=0;
        i--
    ){

        let l =
            lasers[i];


        l.life -= dt;


        let c =
            Math.cos(-l.a);


        let s =
            Math.sin(-l.a);


        for(
            const e of enemies
        ){

            let x =
                e.x-l.x;

            let y =
                e.y-l.y;


            let rx =
                x*c-y*s;

            let ry =
                x*s+y*c;


            if(
                Math.abs(
                    ry-l.off
                ) <
                9*
                Math.max(
                    1,
                    p.area
                )+
                e.r &&
                Math.abs(rx) <
                Math.max(W,H)
            ){

                hit(
                    e,
                    l.dmg*dt*3
                );

            }

        }


        if(
            l.life <= 0
        ){

            lasers.splice(
                i,
                1
            );

        }

    }

}


/* =========================
   파티클
========================= */

function updateParts(dt){

    for(
        let i=parts.length-1;
        i>=0;
        i--
    ){

        let q =
            parts[i];


        q.x +=
            q.vx*dt;

        q.y +=
            q.vy*dt;

        q.life -= dt;


        if(
            q.life <= 0
        ){

            parts.splice(
                i,
                1
            );

        }

    }

}


/* =========================
   그리기
========================= */

function draw(){

    ctx.clearRect(
        0,
        0,
        W,
        H
    );


    ctx.fillStyle =
        "#172017";


    ctx.fillRect(
        0,
        0,
        W,
        H
    );


    /*
       배경 격자
    */

    ctx.strokeStyle =
        "rgba(255,255,255,.035)";


    let grid = 50;

    let off =
        -(time*8%grid);


    for(
        let x=off;
        x<W;
        x+=grid
    ){

        ctx.beginPath();

        ctx.moveTo(
            x,
            0
        );

        ctx.lineTo(
            x,
            H
        );

        ctx.stroke();

    }


    for(
        let y=off;
        y<H;
        y+=grid
    ){

        ctx.beginPath();

        ctx.moveTo(
            0,
            y
        );

        ctx.lineTo(
            W,
            y
        );

        ctx.stroke();

    }


    /*
       레이저
    */

    for(
        const l of lasers
    ){

        ctx.save();

        ctx.translate(
            l.x,
            l.y
        );

        ctx.rotate(
            l.a
        );


        ctx.globalAlpha =
            .75 *
            l.life /
            l.max;


        ctx.fillStyle =
            "#e8b4ff";


        ctx.fillRect(
            -Math.max(W,H),
            l.off -
                8*p.area,
            Math.max(W,H)*2,
            16*p.area
        );


        ctx.restore();

    }


    /*
       베기
    */

    for(
        const s of slashes
    ){

        ctx.save();

        ctx.translate(
            s.x,
            s.y
        );

        ctx.rotate(
            s.a
        );


        ctx.globalAlpha =
            s.life/s.max;


        ctx.fillStyle =
            "#5dade2";


        ctx.beginPath();

        ctx.moveTo(
            0,
            0
        );


        ctx.arc(
            0,
            0,
            s.range,
            -s.fan/2,
            s.fan/2
        );


        ctx.closePath();

        ctx.fill();


        ctx.restore();

    }


    /*
       투사체
    */

    for(
        const q of shots
    ){

        ctx.fillStyle =
            q.type === "wave"
                ? "#5dade2"
                : q.type === "magic"
                    ? "#c56cf0"
                    : "#ffd04a";


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


    /*
       적
    */

    for(
        const e of enemies
    ){

        ctx.fillStyle =
            e.boss
                ? "#c0392b"
                : "#75ad5d";


        ctx.beginPath();

        ctx.arc(
            e.x,
            e.y,
            e.r,
            0,
            TAU
        );


        ctx.fill();


        /*
           눈
        */

        ctx.fillStyle =
            "#222";


        ctx.beginPath();

        ctx.arc(
            e.x-4,
            e.y-2,
            2,
            0,
            TAU
        );


        ctx.arc(
            e.x+4,
            e.y-2,
            2,
            0,
            TAU
        );


        ctx.fill();


        /*
           HP
        */

        ctx.fillStyle =
            "#333";


        ctx.fillRect(
            e.x-e.r,
            e.y-e.r-7,
            e.r*2,
            4
        );


        ctx.fillStyle =
            "#e74c3c";


        ctx.fillRect(
            e.x-e.r,
            e.y-e.r-7,
            e.r*2 *
            Math.max(
                0,
                e.hp/e.maxHp
            ),
            4
        );

    }


    /*
       플레이어
    */

    if(p){

        ctx.save();


        ctx.translate(
            p.x,
            p.y
        );


        ctx.rotate(
            p.face
        );


        if(
            p.cls === "gun"
        ){

            ctx.fillStyle =
                p.gunForm === "pistol"
                    ? "#e67e22"
                    : "#9b59b6";

        }

        else if(
            p.cls === "sword"
        ){

            ctx.fillStyle =
                "#3498db";

        }

        else{

            ctx.fillStyle =
                "#8e44ad";

        }


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
           무기 방향
        */

        ctx.fillStyle =
            "#eee";


        ctx.fillRect(
            8,
            -4,
            20,
            8
        );


        /*
           방어막
        */

        if(
            p.shield > 0
        ){

            ctx.strokeStyle =
                "#5dade2";

            ctx.lineWidth = 4;


            ctx.beginPath();

            ctx.arc(
                0,
                0,
                p.r+7,
                0,
                TAU
            );


            ctx.stroke();

        }


        ctx.restore();

    }


    /*
       파티클
    */

    for(
        const q of parts
    ){

        ctx.globalAlpha =
            q.life/.35;


        ctx.fillStyle =
            "#fff";


        ctx.beginPath();

        ctx.arc(
            q.x,
            q.y,
            3,
            0,
            TAU
        );


        ctx.fill();


        ctx.globalAlpha = 1;

    }

}


/* =========================
   UI
========================= */

function updateUI(){

    if(!p)
        return;


    document
        .querySelector("#hp i")
        .style
        .width =
        (
            100 *
            p.hp /
            p.maxHp
        ) + "%";


    document
        .querySelector("#xp i")
        .style
        .width =
        (
            100 *
            xp /
            need
        ) + "%";


    document
        .getElementById("shield")
        .style
        .display =
            p.cls === "sword"
                ? "block"
                : "none";


    document
        .querySelector("#shield i")
        .style
        .width =
        (
            p.maxShield
                ? 100*p.shield/p.maxShield
                : 0
        ) + "%";


    document
        .getElementById("stats")
        .textContent =
        `Lv.${level} | `+
        `${Math.floor(time/60)}:`+
        `${String(
            Math.floor(time%60)
        ).padStart(2,"0")} | `+
        `처치 ${kills}`;


    let info = "";


    if(
        p.cls === "gun"
    ){

        info =
            `총 · `+
            `${
                p.gunForm === "pistol"
                    ? "권총"
                    : "저격"
            } · `+
            `투사체 ${p.projectiles} · `+
            `관통 ${p.penetration}`;

    }


    else if(
        p.cls === "sword"
    ){

        info =
            `검사 · 베기 + `+
            `검기 ${p.waveCount}개 · `+
            `방어막 ${Math.ceil(
                p.shield
            )}`;

    }


    else{

        info =
            `마법 · 레이저 ${p.laserCount}개 · `+
            `강화 ${p.enhancedCount}/${p.enhancedEvery} · `+
            `각성 ${p.skillProgress}/${p.skillNeed}`;

    }


    document
        .getElementById("info")
        .textContent =
            info;


    /*
       스킬 버튼
    */

    document
        .getElementById("skill")
        .textContent =
        p.cls === "magic"

            ? (
                p.skillActive
                    ? "각성 중!"
                    : `각성 ${p.skillProgress}/${p.skillNeed}`
              )

            : (
                p.skillCd > 0
                    ? `스킬 ${p.skillCd.toFixed(1)}s`
                    : "스킬"
              );


    /*
       폼체인지
    */

    if(
        p.cls === "gun"
    ){

        document
            .getElementById("form")
            .textContent =
            `🔄 ${
                p.gunForm === "pistol"
                    ? "권총"
                    : "저격"
            }`;

    }

}


/* =========================
   게임 오버
========================= */

function gameOver(){

    state = "over";


    document
        .getElementById("result")
        .textContent =
        `레벨 ${level} · `+
        `${Math.floor(time/60)}분 `+
        `${Math.floor(time%60)}초 생존 · `+
        `${kills}마리 처치`;


    document
        .getElementById("over")
        .classList
        .remove("hidden");

}


/* =========================
   게임 루프
========================= */

function loop(t){

    if(!last)
        last = t;


    let dt =
        Math.min(
            .033,
            (t-last)/1000
        );


    last = t;


    if(
        state === "play"
    ){

        update(dt);

    }


    draw();


    requestAnimationFrame(
        loop
    );

}


requestAnimationFrame(
    loop
);


/* =========================
   키보드
========================= */

addEventListener(
    "keydown",
    e=>{

        keys[e.key] = true;


        if(
            e.key === " "
        ){

            e.preventDefault();

            useSkill();

        }


        if(
            e.key.toLowerCase() === "q"
        ){

            formChange();

        }

    }
);


addEventListener(
    "keyup",
    e=>{

        keys[e.key] = false;

    }
);


/* =========================
   버튼
========================= */

document
    .getElementById("skill")
    .addEventListener(
        "pointerdown",
        e=>{

            e.preventDefault();

            useSkill();

        }
    );


document
    .getElementById("form")
    .addEventListener(
        "pointerdown",
        e=>{

            e.preventDefault();

            formChange();

        }
    );


/* =========================
   모바일 조이스틱
========================= */

const je =
    document.getElementById(
        "joy"
    );


const stick =
    document.getElementById(
        "stick"
    );


function jm(e){

    let r =
        je.getBoundingClientRect();


    let dx =
        e.clientX -
        (
            r.left +
            r.width/2
        );


    let dy =
        e.clientY -
        (
            r.top +
            r.height/2
        );


    let max =
        r.width*.45;


    let d =
        Math.hypot(
            dx,
            dy
        );


    if(
        d > max
    ){

        dx =
            dx/d*max;

        dy =
            dy/d*max;

    }


    joy.x =
        dx/max;


    joy.y =
        dy/max;


    stick.style.transform =
        `translate(
            ${dx}px,
            ${dy}px
        )`;

}


function jr(){

    joy.x = 0;

    joy.y = 0;

    stick.style.transform =
        "translate(0,0)";

}


je.addEventListener(
    "pointerdown",
    e=>{

        je.setPointerCapture(
            e.pointerId
        );

        jm(e);

    }
);


je.addEventListener(
    "pointermove",
    e=>{

        if(e.buttons)
            jm(e);

    }
);


je.addEventListener(
    "pointerup",
    jr
);


je.addEventListener(
    "pointercancel",
    jr
);

</script>

</body>
</html>'''


components.html(
    html,
    height=520,
    scrolling=False
)
