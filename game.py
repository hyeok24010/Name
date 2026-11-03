
import streamlit as st
import requests
import re
import unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(
    page_title="오늘의 모바일 게임",
    page_icon="🎮",
    layout="wide"
)

# =====================================
# 디자인
# =====================================

st.markdown("""
<style>
.stApp {
    background: #101522;
    color: white;
}
.game-card {
    background: #1b2638;
    border-radius: 15px;
    padding: 15px;
}
[data-testid="stMetric"] {
    background: #1b2638;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 공통 설정
# =====================================

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LIMIT = 50
COUNTRY = "kr"

def normalize(name):
    name = unicodedata.normalize("NFKC", name.lower())
    return re.sub(r"[^a-z0-9가-힣]", "", name)


# =====================================
# 애플 앱스토어 데이터
# =====================================

@st.cache_data(ttl=3600)
def get_apple_games():

    url = (
        "https://itunes.apple.com/kr/rss/"
        "topfreeapplications/limit=50/genre=6014/json"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=25
    )
    response.raise_for_status()

    entries = response.json().get(
        "feed", {}
    ).get("entry", [])

    if isinstance(entries, dict):
        entries = [entries]

    games = []

    for rank, item in enumerate(entries, 1):

        app_id = item.get(
            "id", {}
        ).get("attributes", {}).get("im:id")

        if not app_id:
            continue

        games.append({
            "rank": rank,
            "id": str(app_id),
            "name": item.get(
                "im:name", {}
            ).get("label", "이름 없음"),
            "developer": item.get(
                "im:artist", {}
            ).get("label", "정보 없음"),
            "icon": item.get(
                "im:image", [{}]
            )[-1].get("label", ""),
            "url": "",
            "description": "",
            "rating": 0,
            "rating_count": 0,
            "genre": "게임",
            "store": "Apple App Store"
        })

    # 상세 정보 조회
    for start in range(0, len(games), 25):

        batch = games[start:start + 25]
        ids = ",".join(g["id"] for g in batch)

        try:
            detail_url = (
                "https://itunes.apple.com/lookup"
                f"?id={ids}&country=kr"
            )

            result = requests.get(
                detail_url,
                headers=HEADERS,
                timeout=20
            )
            result.raise_for_status()

            details = result.json().get("results", [])

            detail_map = {
                str(x["trackId"]): x
                for x in details
            }

            for game in batch:

                detail = detail_map.get(game["id"], {})

                game["icon"] = detail.get(
                    "artworkUrl512", game["icon"]
                )
                game["url"] = detail.get(
                    "trackViewUrl", ""
                )
                game["description"] = detail.get(
                    "description", "설명 없음"
                )
                game["rating"] = detail.get(
                    "averageUserRating", 0
                )
                game["rating_count"] = detail.get(
                    "userRatingCount", 0
                )
                game["genre"] = detail.get(
                    "primaryGenreName", "게임"
                )

        except requests.RequestException:
            continue

    return games


# =====================================
# 구글 플레이 데이터
# =====================================

@st.cache_data(ttl=3600)
def get_google_games():

    from urllib.parse import urlencode
    from xml.etree import ElementTree

    # Google Play 인기 무료 게임 차트
    url = (
        "https://play.google.com/store/apps"
        "/category/GAME/collection/topselling_free"
        "?hl=ko&gl=KR"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=25
    )
    response.raise_for_status()

    html = response.text

    # 게임 앱 ID 추출
    app_ids = list(dict.fromkeys(
        re.findall(
            r'/store/apps/details\?id=([a-zA-Z0-9._]+)',
            html
        )
    ))

    games = []

    for rank, app_id in enumerate(app_ids[:LIMIT], 1):

        # 검색 페이지에 노출되는 게임 정보를 사용
        games.append({
            "rank": rank,
            "id": app_id,
            "name": app_id,
            "developer": "Google Play",
            "icon": "",
            "url": (
                "https://play.google.com/store/apps/details?"
                + urlencode({
                    "id": app_id,
                    "hl": "ko",
                    "gl": "KR"
                })
            ),
            "description": "Google Play 게임",
            "rating": 0,
            "rating_count": 0,
            "genre": "게임",
            "store": "Google Play"
        })

    return games


# =====================================
# 통합 순위
# =====================================

def make_combined(apple, google):

    combined = {}

    for store, games in [
        ("Apple App Store", apple),
        ("Google Play", google)
    ]:

        total = len(games)

        if total == 0:
            continue

        for game in games:

            key = normalize(game["name"])

            if not key:
                continue

            score = (
                (total - game["rank"] + 1)
                / total * 100
            )

            if key not in combined:

                combined[key] = {
                    "name": game["name"],
                    "icon": game["icon"],
                    "developer": game["developer"],
                    "score_list": [],
                    "stores": [],
                    "ranks": [],
                    "links": []
                }

            item = combined[key]

            item["score_list"].append(score)
            item["stores"].append(store)
            item["ranks"].append(
                (store, game["rank"])
            )
            item["links"].append(
                (store, game["url"])
            )

            if not item["icon"] and game["icon"]:
                item["icon"] = game["icon"]

    result = []

    for item in combined.values():

        item["score"] = (
            sum(item["score_list"])
            / len(item["score_list"])
        )

        result.append(item)

    result.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return result


# =====================================
# 게임 카드 출력
# =====================================

def display_games(games):

    if not games:
        st.info("게임 정보가 없습니다.")
        return

    for game in games:

        with st.container(border=True):

            left, right = st.columns([1, 3])

            with left:

                if game.get("icon"):
                    st.image(
                        game["icon"],
                        use_container_width=True
                    )
                else:
                    st.markdown("🎮")

            with right:

                st.markdown(
                    f"### {game['rank']}위 · {game['name']}"
                )

                st.caption(
                    f"제작사: {game['developer']}"
                )

                st.caption(
                    f"스토어: {game['store']}"
                )

                if game.get("rating"):
                    st.write(
                        f"⭐ {game['rating']:.1f}"
                    )

                with st.expander("게임 정보"):
                    st.write(game.get(
                        "description", "정보 없음"
                    ))

                if game.get("url"):
                    st.link_button(
                        "게임 페이지 열기 ↗",
                        game["url"],
                        use_container_width=True
                    )


# =====================================
# 메인 화면
# =====================================

st.title("🎮 오늘의 모바일 게임")

st.caption(
    "APPLE APP STORE × GOOGLE PLAY"
)

today = datetime.now(
    ZoneInfo("Asia/Seoul")
).strftime("%Y년 %m월 %d일")

st.write("📅", today)

if st.button("🔄 데이터 새로고침"):

    get_apple_games.clear()
    get_google_games.clear()

    st.rerun()


# =====================================
# 데이터 수집
# =====================================

apple_games = []
google_games = []

errors = []

with st.spinner("게임 순위를 불러오는 중입니다..."):

    with ThreadPoolExecutor(max_workers=2) as executor:

        apple_future = executor.submit(get_apple_games)
        google_future = executor.submit(get_google_games)

        try:
            apple_games = apple_future.result()
        except Exception as e:
            errors.append(f"Apple: {e}")

        try:
            google_games = google_future.result()
        except Exception as e:
            errors.append(f"Google: {e}")


# =====================================
# 현황
# =====================================

col1, col2 = st.columns(2)

col1.metric(
    "Apple App Store",
    f"{len(apple_games)}개"
)

col2.metric(
    "Google Play",
    f"{len(google_games)}개"
)

for error in errors:
    st.warning(error)


# =====================================
# 메뉴
# =====================================

st.divider()

mode = st.radio(
    "스토어 선택",
    [
        "🌟 통합 순위",
        "🍎 Apple App Store",
        "▶ Google Play"
    ],
    horizontal=True
)

keyword = st.text_input(
    "🔍 게임 검색",
    placeholder="게임 이름 검색"
)


# =====================================
# 통합 순위
# =====================================

if mode == "🌟 통합 순위":

    st.subheader("🌟 모바일 게임 종합 순위")

    st.caption(
        "각 스토어 순위를 100점 기준으로 환산한 참고 점수입니다."
    )

    combined = make_combined(
        apple_games,
        google_games
    )

    filtered = [
        game for game in combined
        if keyword.lower() in game["name"].lower()
    ]

    for rank, game in enumerate(filtered, 1):

        with st.container(border=True):

            left, right = st.columns([1, 3])

            with left:
                if game["icon"]:
                    st.image(
                        game["icon"],
                        use_container_width=True
                    )
                else:
                    st.markdown("🎮")

            with right:

                st.markdown(
                    f"### 🏆 {rank}위 · {game['name']}"
                )

                st.metric(
                    "종합 점수",
                    f"{game['score']:.1f}점"
                )

                st.caption(
                    "참여 스토어: "
                    + ", ".join(game["stores"])
                )

                for store, rank_value in game["ranks"]:
                    st.write(
                        f"{store}: {rank_value}위"
                    )

                for store, link in game["links"]:
                    st.link_button(
                        f"{store}에서 보기",
                        link
                    )


# =====================================
# 애플 순위
# =====================================

elif mode == "🍎 Apple App Store":

    st.subheader("🍎 애플 인기 무료 게임")

    filtered = [
        game for game in apple_games
        if keyword.lower() in game["name"].lower()
    ]

    display_games(filtered)


# =====================================
# 구글 순위
# =====================================

else:

    st.subheader("▶ 구글 플레이 인기 무료 게임")

    filtered = [
        game for game in google_games
        if keyword.lower() in game["name"].lower()
    ]

    display_games(filtered)


# =====================================
# 출처
# =====================================

st.divider()

st.caption(
    "Apple: Apple App Store 공개 RSS 차트 및 Lookup API"
)

st.caption(
    "Google: Google Play 공개 웹 차트"
)

st.caption(
    "통합 점수는 자체 계산한 참고 지표이며 공식 순위가 아닙니다."
)

st.caption(
    "Google Play 웹페이지가 접근을 차단하면 해당 스토어 순위는 표시되지 않을 수 있습니다."
)
