
import streamlit as st
import requests
import re
import unicodedata
import html
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="모바일 게임 랭킹",
    page_icon="🎮",
    layout="wide"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

APPLE_RSS = (
    "https://itunes.apple.com/kr/rss/"
    "topfreeapplications/limit=100/genre=6014/json"
)

APPLE_SEARCH = "https://itunes.apple.com/search"

# =========================================================
# 2. 세션 상태
# =========================================================

defaults = {
    "page": "게임 랭킹",
    "last_page": "게임 랭킹",
    "ranking_search": "",
    "sub_search": "",
    "recommendation_result": False,
    "recommendation_answers": {},
    "recommendation_feedback": {}
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 3. 게임 데이터
# =========================================================

# tags:
# genre = 장르
# story = 스토리
# growth = 성장 및 육성
# art = 그림체

SUBCULTURE = [
    {
        "name": "블루 아카이브",
        "aliases": ["Blue Archive"],
        "reason": "캐릭터 수집 및 육성 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "승리의 여신: 니케",
        "aliases": ["GODDESS OF VICTORY: NIKKE", "NIKKE"],
        "reason": "캐릭터 중심 수집형 슈팅 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "원신",
        "aliases": ["Genshin Impact"],
        "reason": "캐릭터 중심 오픈월드 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "붕괴: 스타레일",
        "aliases": ["Honkai: Star Rail"],
        "reason": "캐릭터 수집 및 스토리 중심 턴제 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "젠레스 존 제로",
        "aliases": ["Zenless Zone Zero"],
        "reason": "캐릭터 중심 액션 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "명조: 워더링 웨이브",
        "aliases": ["Wuthering Waves"],
        "reason": "캐릭터 수집형 액션 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "명일방주",
        "aliases": ["Arknights"],
        "reason": "캐릭터 수집형 전략 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "림버스 컴퍼니",
        "aliases": ["Limbus Company"],
        "reason": "캐릭터와 서사 중심 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "개성 있는 그림체"]
    },
    {
        "name": "트릭컬 리바이브",
        "aliases": ["Trickcal Re:VIVE", "Trickcal"],
        "reason": "캐릭터 수집 및 육성 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "리버스: 1999",
        "aliases": ["Reverse: 1999"],
        "reason": "캐릭터와 스토리 중심 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "개성 있는 그림체"]
    },
    {
        "name": "소녀전선 2: 망명",
        "aliases": ["Girls' Frontline 2: Exilium"],
        "reason": "캐릭터 수집형 전략 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "우마무스메 프리티 더비",
        "aliases": ["Uma Musume Pretty Derby"],
        "reason": "캐릭터 육성 시뮬레이션",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "페이트/그랜드 오더",
        "aliases": ["Fate/Grand Order", "FGO"],
        "reason": "캐릭터 수집 및 스토리 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "에픽세븐",
        "aliases": ["Epic Seven"],
        "reason": "애니메이션풍 캐릭터 수집 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "앙상블스타즈!!",
        "aliases": ["Ensemble Stars!!", "あんさんぶるスターズ"],
        "reason": "아이돌 캐릭터 육성 및 리듬 게임",
        "tags": ["리듬 게임", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "프로젝트 세카이",
        "aliases": ["Project SEKAI", "Hatsune Miku: Colorful Stage"],
        "reason": "캐릭터와 음악 중심 리듬 게임",
        "tags": ["리듬 게임", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "뱅드림! 걸즈 밴드 파티!",
        "aliases": ["BanG Dream! Girls Band Party!"],
        "reason": "캐릭터와 밴드 중심 리듬 게임",
        "tags": ["리듬 게임", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "헤븐 번즈 레드",
        "aliases": ["Heaven Burns Red"],
        "reason": "캐릭터와 스토리 중심 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "아우터플레인",
        "aliases": ["OUTERPLANE"],
        "reason": "애니메이션풍 캐릭터 수집 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "카운터사이드",
        "aliases": ["CounterSide"],
        "reason": "캐릭터 수집 및 스토리 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "브라운더스트2",
        "aliases": ["BrownDust2"],
        "reason": "캐릭터 수집형 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "벽람항로",
        "aliases": ["Azur Lane"],
        "reason": "캐릭터 수집형 슈팅 RPG",
        "tags": ["수집형 RPG", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "백야극광",
        "aliases": ["Alchemy Stars"],
        "reason": "캐릭터 수집형 전략 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "소녀전선",
        "aliases": ["Girls' Frontline"],
        "reason": "캐릭터 수집형 전략 게임",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "에버소울",
        "aliases": ["Eversoul"],
        "reason": "캐릭터 수집 및 육성 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "퍼니싱: 그레이 레이븐",
        "aliases": ["Punishing: Gray Raven"],
        "reason": "캐릭터 수집형 액션 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "에테르 게이저",
        "aliases": ["Aether Gazer"],
        "reason": "캐릭터 중심 액션 RPG",
        "tags": ["수집형 RPG", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "뉴럴 클라우드",
        "aliases": ["Neural Cloud"],
        "reason": "캐릭터 수집형 전략 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "마스터 오브 가든",
        "aliases": ["The Eminence in Shadow: Master of Garden"],
        "reason": "애니메이션 IP 기반 캐릭터 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "D4DJ Groovy Mix",
        "aliases": ["D4DJ"],
        "reason": "캐릭터 중심 리듬 게임",
        "tags": ["리듬 게임", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "아이돌마스터 신데렐라 걸즈 스타라이트 스테이지",
        "aliases": ["THE IDOLM@STER Cinderella Girls Starlight Stage"],
        "reason": "아이돌 캐릭터 중심 리듬 게임",
        "tags": ["리듬 게임", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
    {
        "name": "월드 플리퍼",
        "aliases": ["World Flipper"],
        "reason": "캐릭터 수집형 액션 RPG",
        "tags": ["수집형 RPG", "스토리 중심", "캐릭터 육성", "애니메이션풍"]
    },
]

# =========================================================
# 4. 이름 비교
# =========================================================

def normalize(text):
    text = unicodedata.normalize("NFKC", str(text or ""))
    text = text.lower()
    return re.sub(r"[^0-9a-z가-힣]", "", text)


def matches_game(name, game):
    candidates = [game["name"]] + game.get("aliases", [])
    target = normalize(name)

    return any(
        target == normalize(candidate)
        for candidate in candidates
    )


# =========================================================
# 5. HTTP 요청
# =========================================================

def get_json(url, params=None, timeout=15):
    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


# =========================================================
# 6. 앱스토어 인기 순위
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_apple_ranking():
    data = get_json(APPLE_RSS)

    if not data:
        return []

    entries = data.get("feed", {}).get("entry", [])
    games = []

    for rank, item in enumerate(entries, start=1):
        try:
            name = item["im:name"]["label"]
            images = item.get("im:image", [])

            icon = (
                images[-1].get("label", "")
                if images else ""
            )

            games.append({
                "name": name,
                "rank": rank,
                "icon": icon,
                "store": "앱스토어"
            })
        except Exception:
            continue

    return games


# =========================================================
# 7. 구글 플레이 인기 순위
# =========================================================

def get_google_ranking():
    # 먼저 google-play-scraper 방식 시도
    try:
        from google_play_scraper import collection, Collection

        results = collection(
            collection=Collection.TOP_FREE,
            category="GAME",
            country="kr",
            lang="ko",
            count=100
        )

        return [
            {
                "name": item.get("title", ""),
                "rank": rank,
                "icon": item.get("icon", ""),
                "store": "구글 플레이"
            }
            for rank, item in enumerate(results, start=1)
            if item.get("title")
        ]

    except Exception:
        pass

    # 기존 GPlayScraper 방식도 지원
    try:
        from gplay_scraper import GPlayScraper

        scraper = GPlayScraper()

        results = scraper.list_analyze(
            "TOP_FREE",
            "GAME",
            count=100,
            lang="ko",
            country="kr"
        )

        games = []

        for rank, item in enumerate(results, start=1):
            if not isinstance(item, dict):
                continue

            name = item.get("title") or item.get("name")

            if name:
                games.append({
                    "name": name,
                    "rank": rank,
                    "icon": item.get("icon", ""),
                    "store": "구글 플레이"
                })

        return games

    except Exception:
        return []


# =========================================================
# 8. 서브컬처 아이콘 검색
# 정확한 이름이나 별칭이 일치할 때만 사용
# =========================================================

@st.cache_data(ttl=604800, show_spinner=False)
def search_apple_icon(game_name, aliases):
    search_names = [game_name] + list(aliases)

    for search_name in search_names:
        data = get_json(
            "https://itunes.apple.com/search",
            params={
                "term": search_name,
                "entity": "software",
                "country": "kr",
                "limit": 20
            }
        )

        if not data:
            continue

        for item in data.get("results", []):
            result_name = item.get("trackName", "")

            if any(
                normalize(result_name) == normalize(candidate)
                for candidate in search_names
            ):
                return (
                    item.get("artworkUrl512")
                    or item.get("artworkUrl100")
                    or ""
                )

    return ""


@st.cache_data(ttl=604800, show_spinner=False)
def load_subculture_icons():
    icons = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(
                search_apple_icon,
                game["name"],
                tuple(game["aliases"])
            ): game["name"]
            for game in SUBCULTURE
        }

        for future in as_completed(futures):
            name = futures[future]

            try:
                icons[normalize(name)] = future.result()
            except Exception:
                icons[normalize(name)] = ""

    return icons


# =========================================================
# 9. 게임 순위 연결
# =========================================================

def get_game_rank(game, apple_games, google_games):
    results = []

    for store_name, games in [
        ("앱스토어", apple_games),
        ("구글 플레이", google_games)
    ]:
        for item in games:
            if matches_game(item["name"], game):
                results.append(
                    f'{store_name} {item["rank"]}위'
                )
                break

    return " · ".join(results) if results else "순위 정보 없음"


# =========================================================
# 10. 화면 디자인
# =========================================================

st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

div[data-testid="stRadio"] > div {
    gap: 8px;
}

.game-title {
    font-weight: 700;
    font-size: 16px;
}

div[data-testid="stImage"] img {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


def show_game_card(name, icon, info, reason=""):
    left, right = st.columns([1, 4])

    with left:
        if icon:
            st.image(icon, width=72)
        else:
            st.markdown(
                """
                <div style="
                    width:72px;height:72px;
                    border-radius:13px;
                    background:rgba(128,128,128,0.15);
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:30px;">
                    🎮
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:
        st.markdown(f"**{html.escape(name)}**")
        st.caption(info)

        if reason:
            st.caption(reason)


# =========================================================
# 11. 메뉴 전환 및 검색어 초기화
# =========================================================

def change_page():
    previous = st.session_state.last_page
    current = st.session_state.page

    if previous != current:
        if previous == "게임 랭킹":
            st.session_state.ranking_search = ""

        elif previous == "서브컬처":
            st.session_state.sub_search = ""

        st.session_state.last_page = current


# =========================================================
# 12. 제목과 메뉴
# =========================================================

st.title("🎮 모바일 게임 랭킹")

st.radio(
    "메뉴",
    ["게임 랭킹", "서브컬처", "게임 추천"],
    horizontal=True,
    key="page",
    on_change=change_page,
    label_visibility="collapsed"
)

# =========================================================
# 13. 데이터 수집
# =========================================================

with st.spinner("게임 정보를 불러오는 중입니다..."):
    apple_games = get_apple_ranking()
    google_games = get_google_ranking()

# 아이콘 검색은 서브컬처 메뉴에 들어갔을 때만 실행
icons = {}

if st.session_state.page == "서브컬처":
    with st.spinner("서브컬처 게임 아이콘을 불러오는 중입니다..."):
        icons = load_subculture_icons()


# =========================================================
# 14. 게임 랭킹 메뉴
# =========================================================

if st.session_state.page == "게임 랭킹":

    st.subheader("전체 게임 순위")

    store = st.radio(
        "스토어 선택",
        ["전체", "앱스토어", "구글 플레이"],
        horizontal=True,
        key="ranking_store"
    )

    keyword = st.text_input(
        "게임 검색",
        placeholder="게임 이름을 입력하세요",
        key="ranking_search"
    )

    if store == "앱스토어":
        display = [
            {
                "name": g["name"],
                "icon": g["icon"],
                "info": f'앱스토어 {g["rank"]}위'
            }
            for g in apple_games
        ]

    elif store == "구글 플레이":
        display = [
            {
                "name": g["name"],
                "icon": g["icon"],
                "info": f'구글 플레이 {g["rank"]}위'
            }
            for g in google_games
        ]

    else:
        combined = {}

        for games in [apple_games, google_games]:
            for game in games:
                key = normalize(game["name"])

                if key not in combined:
                    combined[key] = {
                        "name": game["name"],
                        "icon": game["icon"],
                        "ranks": []
                    }

                combined[key]["ranks"].append(
                    f'{game["store"]} {game["rank"]}위'
                )

        display = [
            {
                "name": game["name"],
                "icon": game["icon"],
                "info": " · ".join(game["ranks"])
            }
            for game in combined.values()
        ]

    if keyword.strip():
        display = [
            game for game in display
            if keyword.strip().lower() in game["name"].lower()
        ]

    st.caption(f"검색 결과 {len(display)}개")

    if not display:
        st.info("검색 결과가 없습니다.")

    for game in display:
        show_game_card(
            game["name"],
            game["icon"],
            game["info"]
        )

    if not apple_games:
        st.warning("앱스토어 순위를 불러오지 못했습니다.")

    if not google_games:
        st.warning("구글 플레이 순위를 불러오지 못했습니다.")


# =========================================================
# 15. 서브컬처 메뉴
# =========================================================

elif st.session_state.page == "서브컬처":

    st.subheader("서브컬처 게임")

    st.caption(
        "캐릭터 수집, 육성, 스토리, 애니메이션풍 작품 등을 중심으로 분류했습니다."
    )

    keyword = st.text_input(
        "게임 검색",
        placeholder="게임 이름을 입력하세요",
        key="sub_search"
    )

    filtered = SUBCULTURE

    if keyword.strip():
        filtered = [
            game for game in SUBCULTURE
            if keyword.strip().lower() in game["name"].lower()
            or any(
                keyword.strip().lower() in alias.lower()
                for alias in game["aliases"]
            )
        ]

    if "sub_count" not in st.session_state:
        st.session_state.sub_count = 30

    visible = filtered[:st.session_state.sub_count]

    st.caption(
        f"등록된 게임 {len(filtered)}개 · 표시 중 {len(visible)}개"
    )

    for game in visible:
        icon = icons.get(normalize(game["name"]), "")

        rank = get_game_rank(
            game,
            apple_games,
            google_games
        )

        show_game_card(
            game["name"],
            icon,
            rank,
            game["reason"]
        )

    if len(filtered) > len(visible):
        if st.button("더보기", use_container_width=True):
            st.session_state.sub_count += 30
            st.rerun()

    if not filtered:
        st.info("검색 결과가 없습니다.")


# =========================================================
# 16. 게임 추천 점수
# =========================================================

def calculate_score(game, answers):
    tags = game["tags"]
    score = 0
    maximum = 0

    weights = {
        "genre": 30,
        "story": 25,
        "growth": 20,
        "art": 15
    }

    choices = {
        "genre": {
            "캐릭터 수집형 RPG": "수집형 RPG",
            "리듬 게임": "리듬 게임",
            "액션 RPG": "수집형 RPG",
            "상관없음": None
        },
        "story": {
            "스토리 중심": "스토리 중심",
            "게임성 중심": None,
            "상관없음": None
        },
        "growth": {
            "성장과 육성": "캐릭터 육성",
            "캐릭터 수집": "수집형 RPG",
            "전략과 전투": "전략과 전투",
            "상관없음": None
        },
        "art": {
            "애니메이션풍": "애니메이션풍",
            "픽셀 및 도트": "픽셀 및 도트",
            "개성 있는 그림체": "개성 있는 그림체",
            "상관없음": None
        }
    }

    for category, weight in weights.items():
        answer = answers.get(category, "상관없음")
        target = choices[category].get(answer)

        if answer == "상관없음":
            continue

        maximum += weight

        if target is None or target in tags:
            score += weight

    if maximum == 0:
        return 0

    return round(score / maximum * 100)


def recommendation_reasons(game, answers):
    tags = game["tags"]
    reasons = []

    if answers.get("genre") == "캐릭터 수집형 RPG":
        if "수집형 RPG" in tags:
            reasons.append("캐릭터 수집")

    if answers.get("story") == "스토리 중심":
        if "스토리 중심" in tags:
            reasons.append("스토리")

    if answers.get("growth") == "성장과 육성":
        if "캐릭터 육성" in tags:
            reasons.append("성장 및 육성")

    if answers.get("art") == "애니메이션풍":
        if "애니메이션풍" in tags:
            reasons.append("애니메이션풍 그림체")

    return reasons


# =========================================================
# 17. 게임 추천 메뉴
# =========================================================

elif st.session_state.page == "게임 추천":

    st.subheader("✨ 나에게 맞는 게임 찾기")

    st.write(
        "몇 가지 질문에 답하면 취향에 맞는 게임을 추천해 드립니다."
    )

    with st.form("game_recommendation_form"):

        st.markdown("### 1. 어떤 장르를 좋아하나요?")

        genre = st.radio(
            "선호 장르",
            [
                "캐릭터 수집형 RPG",
                "리듬 게임",
                "액션 RPG",
                "상관없음"
            ],
            key="question_genre"
        )

        st.divider()

        st.markdown("### 2. 스토리는 얼마나 중요한가요?")

        story = st.radio(
            "스토리 선호도",
            [
                "스토리 중심",
                "게임성 중심",
                "상관없음"
            ],
            key="question_story"
        )

        st.divider()

        st.markdown("### 3. 가장 중요하게 생각하는 요소는?")

        growth = st.radio(
            "중요 요소",
            [
                "성장과 육성",
                "캐릭터 수집",
                "전략과 전투",
                "상관없음"
            ],
            key="question_growth"
        )

        st.divider()

        st.markdown("### 4. 선호하는 그림체는?")

        art = st.radio(
            "그림체",
            [
                "애니메이션풍",
                "픽셀 및 도트",
                "개성 있는 그림체",
                "상관없음"
            ],
            key="question_art"
        )

        st.divider()

        st.markdown("### 5. 어떤 플랫폼에서 플레이하나요?")

        platform = st.radio(
            "플랫폼",
            [
                "모바일",
                "PC",
                "둘 다"
            ],
            key="question_platform"
        )

        submitted = st.form_submit_button(
            "내 취향으로 게임 추천받기",
            use_container_width=True
        )

    if submitted:
        st.session_state.recommendation_answers = {
            "genre": genre,
            "story": story,
            "growth": growth,
            "art": art,
            "platform": platform
        }

        st.session_state.recommendation_result = True

    # 추천 결과
    if st.session_state.recommendation_result:

        answers = st.session_state.recommendation_answers

        st.divider()
        st.markdown("## 🎯 추천 결과")

        st.caption(
            "선택한 취향과 등록된 게임의 특징을 비교한 결과입니다."
        )

        if answers.get("platform") == "PC":
            st.info(
                "현재 등록된 게임 목록은 모바일 게임 중심입니다. "
                "PC 게임 데이터가 추가되기 전까지 추천 결과가 제한됩니다."
            )

        results = []

        for game in SUBCULTURE:
            score = calculate_score(game, answers)

            results.append({
                "game": game,
                "score": score,
                "reasons": recommendation_reasons(game, answers)
            })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # 같은 점수의 게임은 등록 순서 유지
        shown = results[:15]

        for index, item in enumerate(shown, start=1):

            game = item["game"]
            score = item["score"]
            reasons = item["reasons"]

            icon = icons.get(normalize(game["name"]), "")

            left, right = st.columns([1, 4])

            with left:
                if icon:
                    st.image(icon, width=72)
                else:
                    st.markdown("🎮")

            with right:
                st.markdown(
                    f"**{index}. {game['name']}**"
                )

                st.progress(score / 100)

                st.caption(
                    f"취향 일치도 {score}%"
                )

                if reasons:
                    st.caption(
                        "추천 이유: " + ", ".join(reasons)
                    )

                st.caption(game["reason"])

        st.caption(
            "일치도는 게임의 실제 품질이나 재미를 평가한 점수가 아니라, "
            "선택한 취향과 등록된 게임 특징의 일치 정도입니다."
        )

        if st.button(
            "질문 다시 하기",
            use_container_width=True
        ):
            st.session_state.recommendation_result = False
            st.rerun()


# =========================================================
# 18. 하단 새로고침
# =========================================================

st.divider()

if st.button("게임 순위 새로고침", use_container_width=True):
    get_apple_ranking.clear()
    st.rerun()

st.caption(
    "게임 순위와 아이콘은 각 스토어의 데이터 제공 상태에 따라 "
    "일부 표시되지 않을 수 있습니다."
)
