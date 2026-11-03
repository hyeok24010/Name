
import streamlit as st
import requests
import re
import unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo

from google_play_scraper import collection as gp_collection
from google_play_scraper import Sort

st.set_page_config(
    page_title="모바일 게임 랭킹",
    page_icon="🎮",
    layout="wide"
)

# -------------------------
# 디자인
# -------------------------

st.markdown("""
<style>
.stApp {
    background: #101522;
    color: white;
}
h1, h2, h3 {
    color: white;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #1b2638;
    border-radius: 15px;
}
.game-title {
    font-size: 19px;
    font-weight: bold;
}
.small-text {
    color: #aab7ce;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 기본 설정
# -------------------------

COUNTRY = "kr"
LIMIT = 50

# -------------------------
# 게임 이름 정규화
# -------------------------

def normalize_name(name):
    name = unicodedata.normalize("NFKC", name.lower())
    name = re.sub(r"[^a-z0-9가-힣]", "", name)
    return name


# -------------------------
# Apple App Store
# -------------------------

@st.cache_data(ttl=3600)
def get_apple_games():

    url = (
        "https://itunes.apple.com/kr/rss/"
        "topfreeapplications/limit=50/genre=6014/json"
    )

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    entries = response.json().get(
        "feed", {}
    ).get("entry", [])

    games = []

    for rank, item in enumerate(entries, 1):

        app_id = item.get(
            "id", {}
        ).get("attributes", {}).get("im:id")

        if not app_id:
            continue

        games.append({
            "rank": rank,
            "id": app_id,
            "name": item.get(
                "im:name", {}
            ).get("label", "이름 없음"),
            "developer": item.get(
                "im:artist", {}
            ).get("label", "정보 없음"),
            "icon": item.get(
                "im:image", [{}]
            )[-1].get("label", ""),
            "url": item.get(
                "id", {}
            ).get("label", ""),
            "store": "Apple App Store"
        })

    # 상세 정보 일괄 조회
    for start in range(0, len(games), 25):

        batch = games[start:start + 25]
        ids = ",".join(g["id"] for g in batch)

        detail_url = (
            "https://itunes.apple.com/lookup"
            f"?id={ids}&country=kr"
        )

        try:
            detail_response = requests.get(
                detail_url, timeout=20
            )
            detail_response.raise_for_status()

            details = detail_response.json().get(
                "results", []
            )

            detail_map = {
                str(x["trackId"]): x
                for x in details
            }

            for game in batch:
                detail = detail_map.get(game["id"], {})

                game["icon"] = detail.get(
                    "artworkUrl512", game["icon"]
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
                game["url"] = detail.get(
                    "trackViewUrl", game["url"]
                )

        except requests.RequestException:
            pass

    return games


# -------------------------
# Google Play
# -------------------------

@st.cache_data(ttl=3600)
def get_google_games():

    result = gp_collection(
        collection=gp_collection.TOP_FREE,
        category="GAME",
        lang="ko",
        country="kr",
        sort=Sort.MOST_RELEVANT,
        results=LIMIT
    )

    games = []

    for rank, item in enumerate(result, 1):

        app_id = item.get("appId", "")

        if not app_id:
            continue

        games.append({
            "rank": rank,
            "id": app_id,
            "name": item.get("title", "이름 없음"),
            "developer": item.get(
                "developer", "정보 없음"
            ),
            "icon": item.get("icon", ""),
            "url": (
                "https://play.google.com/store/apps/details"
                f"?id={app_id}&hl=ko&gl=KR"
            ),
            "description": item.get(
                "summary", "설명 없음"
            ),
            "rating": item.get("score", 0) or 0,
            "rating_count": item.get(
                "ratings", 0
            ) or 0,
            "genre": item.get(
                "genre", "게임"
            ),
            "store": "Google Play"
        })

    return games


# -------------------------
# 통합 순위 계산
# -------------------------

def make_combined(apple, google):

    all_games = {}

    stores = [
        ("Apple App Store", apple),
        ("Google Play", google)
    ]

    for store_name, games in stores:

        total = len(games)

        for game in games:

            key = normalize_name(game["name"])

            if not key:
                continue

            # 순위가 높을수록 높은 점수
            score = (
                (total - game["rank"] + 1)
                / total * 100
            )

            if key not in all_games:

                all_games[key] = {
                    "name": game["name"],
                    "icon": game["icon"],
                    "developer": game["developer"],
                    "description": game.get(
                        "description", ""
                    ),
                    "stores": [],
                    "scores": [],
                    "ranks": [],
                    "links": []
                }

            data = all_games[key]

            data["stores"].append(store_name)
            data["scores"].append(score)
            data["ranks"].append(
                (store_name, game["rank"])
            )
            data["links"].append(
                (store_name, game["url"])
            )

    combined = []

    for data in all_games.values():

        data["score"] = sum(
            data["scores"]
        ) / len(data["scores"])

        combined.append(data)

    combined.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return combined


# -------------------------
# 게임 카드
# -------------------------

def show_games(games):

    if not games:
        st.info("게임 데이터가 없습니다.")
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

            with right:

                st.markdown(
                    f"**{game['rank']}위 · {game['name']}**"
                )

                st.caption(
                    f"제작사: {game['developer']}"
                )

                st.caption(
                    f"장르: {game.get('genre', '게임')}"
                )

                rating = game.get("rating", 0)

                if rating:
                    st.write(
                        f"⭐ {rating:.1f}"
                    )

                with st.expander("게임 설명"):
                    st.write(
                        game.get(
                            "description", "설명 없음"
                        )
                    )

                st.link_button(
                    "스토어에서 게임 보기 ↗",
                    game["url"],
                    use_container_width=True
                )


# -------------------------
# 메인 화면
# -------------------------

st.title("🎮 모바일 게임 랭킹")
st.caption("GOOGLE PLAY × APPLE APP STORE")

today = datetime.now(
    ZoneInfo("Asia/Seoul")
).strftime("%Y년 %m월 %d일")

st.write(f"📅 {today}")

if st.button("🔄 순위 새로고침", use_container_width=True):

    get_apple_games.clear()
    get_google_games.clear()

    st.rerun()

# -------------------------
# 데이터 수집
# -------------------------

with st.spinner("스토어별 게임 순위를 가져오는 중..."):

    apple_games = []
    google_games = []

    apple_error = None
    google_error = None

    try:
        apple_games = get_apple_games()
    except Exception as e:
        apple_error = str(e)

    try:
        google_games = get_google_games()
    except Exception as e:
        google_error = str(e)

# -------------------------
# 수집 결과
# -------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Apple App Store",
        f"{len(apple_games)}개"
    )

with col2:
    st.metric(
        "Google Play",
        f"{len(google_games)}개"
    )

if apple_error:
    st.warning(
        "애플 앱스토어 데이터를 가져오지 못했습니다."
    )
    st.caption(apple_error)

if google_error:
    st.warning(
        "구글 플레이 데이터를 가져오지 못했습니다."
    )
    st.caption(google_error)

# -------------------------
# 메뉴
# -------------------------

st.divider()

mode = st.radio(
    "순위 확인 방법",
    [
        "🌟 통합 순위",
        "🍎 Apple App Store",
        "▶ Google Play"
    ],
    horizontal=False
)

# -------------------------
# 검색
# -------------------------

keyword = st.text_input(
    "🔍 게임 검색",
    placeholder="게임 이름을 검색하세요."
)

# -------------------------
# 출력
# -------------------------

if mode == "🌟 통합 순위":

    st.subheader("🌟 모바일 게임 통합 순위")

    st.caption(
        "각 스토어의 무료 게임 순위를 100점 기준으로 "
        "환산한 뒤, 동일한 이름의 게임끼리 평균을 냅니다."
    )

    combined = make_combined(
        apple_games,
        google_games
    )

    filtered = [
        game for game in combined
        if keyword.lower() in game["name"].lower()
    ]

    if not filtered:
        st.info("검색 결과가 없습니다.")

    for rank, game in enumerate(filtered, 1):

        with st.container(border=True):

            left, right = st.columns([1, 3])

            with left:
                if game["icon"]:
                    st.image(
                        game["icon"],
                        use_container_width=True
                    )

            with right:

                st.markdown(
                    f"### 🏆 {rank}위 · {game['name']}"
                )

                st.write(
                    f"종합 점수: {game['score']:.1f}점"
                )

                st.caption(
                    "참여 스토어: "
                    + ", ".join(game["stores"])
                )

                for store, store_rank in game["ranks"]:
                    st.caption(
                        f"{store}: {store_rank}위"
                    )

                for store, link in game["links"]:
                    st.link_button(
                        f"{store}에서 보기",
                        link,
                        use_container_width=True
                    )

elif mode == "🍎 Apple App Store":

    st.subheader("🍎 애플 앱스토어 인기 무료 게임")

    filtered = [
        game for game in apple_games
        if keyword.lower() in game["name"].lower()
    ]

    show_games(filtered)

else:

    st.subheader("▶ 구글 플레이 인기 무료 게임")

    filtered = [
        game for game in google_games
        if keyword.lower() in game["name"].lower()
    ]

    show_games(filtered)


# -------------------------
# 출처 및 안내
# -------------------------

st.divider()

st.caption(
    "Apple: Apple App Store 공개 RSS 차트 및 Lookup API"
)

st.caption(
    "Google: Google Play 차트 비공식 수집 라이브러리"
)

st.caption(
    "무료 게임 차트 기준입니다. 유료 게임 및 매출 순위와 다릅니다."
)

st.caption(
    "통합 순위는 자체 계산한 참고 점수이며 공식 스토어 순위가 아닙니다."
)

st.caption(
    "동일 게임의 이름이 스토어마다 다르면 통합 과정에서 "
    "하나의 게임으로 인식하지 못할 수 있습니다."
)
