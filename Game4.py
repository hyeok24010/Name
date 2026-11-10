
import streamlit as st
import requests
import re
import unicodedata
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================================================
# 기본 설정
# ==================================================

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

# ==================================================
# 세션 상태
# ==================================================

if "more_sub" not in st.session_state:
    st.session_state.more_sub = 30

if "icon_cache" not in st.session_state:
    st.session_state.icon_cache = {}

# ==================================================
# 게임 이름 정리
# ==================================================

def normalize(text):
    text = unicodedata.normalize("NFKC", str(text or ""))
    text = text.lower()
    return re.sub(r"[^0-9a-z가-힣]", "", text)


def same_name(a, b):
    return normalize(a) == normalize(b)


# ==================================================
# 서브컬처 게임 목록
# 이름과 별칭을 이용해 순위 및 아이콘 검색
# ==================================================

SUBCULTURE = [
    {
        "name": "블루 아카이브",
        "aliases": ["Blue Archive"],
        "reason": "캐릭터 수집 및 육성 RPG"
    },
    {
        "name": "승리의 여신: 니케",
        "aliases": ["GODDESS OF VICTORY: NIKKE", "NIKKE"],
        "reason": "캐릭터 중심 수집형 슈팅 RPG"
    },
    {
        "name": "원신",
        "aliases": ["Genshin Impact"],
        "reason": "캐릭터 중심 오픈월드 RPG"
    },
    {
        "name": "붕괴: 스타레일",
        "aliases": ["Honkai: Star Rail"],
        "reason": "캐릭터 수집 및 스토리 RPG"
    },
    {
        "name": "젠레스 존 제로",
        "aliases": ["Zenless Zone Zero"],
        "reason": "캐릭터 중심 액션 RPG"
    },
    {
        "name": "명조: 워더링 웨이브",
        "aliases": ["Wuthering Waves"],
        "reason": "캐릭터 수집형 액션 RPG"
    },
    {
        "name": "명일방주",
        "aliases": ["Arknights"],
        "reason": "캐릭터 수집형 전략 RPG"
    },
    {
        "name": "림버스 컴퍼니",
        "aliases": ["Limbus Company"],
        "reason": "캐릭터와 스토리 중심 RPG"
    },
    {
        "name": "트릭컬 리바이브",
        "aliases": ["Trickcal Re:VIVE", "Trickcal"],
        "reason": "캐릭터 수집 및 육성 RPG"
    },
    {
        "name": "리버스: 1999",
        "aliases": ["Reverse: 1999"],
        "reason": "캐릭터와 스토리 중심 RPG"
    },
    {
        "name": "소녀전선 2: 망명",
        "aliases": ["Girls' Frontline 2: Exilium"],
        "reason": "캐릭터 수집형 전략 RPG"
    },
    {
        "name": "우마무스메 프리티 더비",
        "aliases": ["Uma Musume Pretty Derby"],
        "reason": "캐릭터 육성 시뮬레이션"
    },
    {
        "name": "페이트/그랜드 오더",
        "aliases": ["Fate/Grand Order", "FGO"],
        "reason": "캐릭터 수집 및 스토리 RPG"
    },
    {
        "name": "에픽세븐",
        "aliases": ["Epic Seven"],
        "reason": "애니메이션풍 캐릭터 수집 RPG"
    },
    {
        "name": "쿠키런: 킹덤",
        "aliases": ["CookieRun: Kingdom"],
        "reason": "캐릭터 수집 및 스토리 RPG"
    },
    {
        "name": "앙상블스타즈!!",
        "aliases": ["Ensemble Stars!!", "あんさんぶるスターズ"],
        "reason": "아이돌 캐릭터 육성 및 리듬 게임"
    },
    {
        "name": "아이돌마스터 신데렐라 걸즈 스타라이트 스테이지",
        "aliases": ["THE IDOLM@STER Cinderella Girls Starlight Stage"],
        "reason": "아이돌 캐릭터 중심 리듬 게임"
    },
    {
        "name": "프로젝트 세카이",
        "aliases": ["Project SEKAI", "Hatsune Miku: Colorful Stage"],
        "reason": "캐릭터와 음악 중심 리듬 게임"
    },
    {
        "name": "뱅드림! 걸즈 밴드 파티!",
        "aliases": ["BanG Dream! Girls Band Party!"],
        "reason": "캐릭터와 밴드 중심 리듬 게임"
    },
    {
        "name": "D4DJ",
        "aliases": ["D4DJ Groovy Mix"],
        "reason": "캐릭터 중심 리듬 게임"
    },
    {
        "name": "헤븐 번즈 레드",
        "aliases": ["Heaven Burns Red"],
        "reason": "캐릭터와 스토리 중심 RPG"
    },
    {
        "name": "아우터플레인",
        "aliases": ["OUTERPLANE"],
        "reason": "애니메이션풍 캐릭터 수집 RPG"
    },
    {
        "name": "카운터사이드",
        "aliases": ["CounterSide"],
        "reason": "캐릭터 수집 및 스토리 RPG"
    },
    {
        "name": "브라운더스트2",
        "aliases": ["BrownDust2"],
        "reason": "캐릭터 수집형 RPG"
    },
    {
        "name": "이터널 리턴",
        "aliases": ["Eternal Return"],
        "reason": "캐릭터 중심 생존 액션 게임"
    },
    {
        "name": "벽람항로",
        "aliases": ["Azur Lane"],
        "reason": "캐릭터 수집형 슈팅 RPG"
    },
    {
        "name": "백야극광",
        "aliases": ["Alchemy Stars"],
        "reason": "캐릭터 수집형 전략 RPG"
    },
    {
        "name": "천년의 소녀",
        "aliases": ["Girl's"],
        "reason": "분류 및 서비스 여부 추가 확인 필요"
    },
    {
        "name": "마스터 오브 가든",
        "aliases": ["Master of Garden"],
        "reason": "캐릭터 중심 RPG"
    },
    {
        "name": "소녀전선",
        "aliases": ["Girls' Frontline"],
        "reason": "캐릭터 수집형 전략 게임"
    },
]

# ==================================================
# HTTP 요청
# ==================================================

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


# ==================================================
# 앱스토어 아이콘 검색
# 정확한 이름 또는 별칭이 일치하는 결과만 사용
# ==================================================

@st.cache_data(ttl=604800, show_spinner=False)
def search_icon(game_name, aliases):
    search_names = [game_name] + list(aliases)

    for search_name in search_names:
        params = {
            "term": search_name,
            "entity": "software",
            "country": "kr",
            "limit": 20
        }

        data = get_json(
            APPLE_SEARCH,
            params=params
        )

        if not data:
            continue

        for item in data.get("results", []):
            result_name = item.get("trackName", "")

            possible_names = [game_name] + list(aliases)

            if any(
                same_name(result_name, candidate)
                for candidate in possible_names
            ):
                icon = (
                    item.get("artworkUrl512")
                    or item.get("artworkUrl100")
                    or ""
                )

                if icon:
                    return icon

    return ""


# ==================================================
# 전체 서브컬처 아이콘 자동 수집
# 처음 화면을 열 때 전체 게임을 동시에 검색
# ==================================================

@st.cache_data(ttl=604800, show_spinner=False)
def load_all_subculture_icons():
    result = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(
                search_icon,
                game["name"],
                tuple(game["aliases"])
            ): game["name"]
            for game in SUBCULTURE
        }

        for future in as_completed(futures):
            name = futures[future]

            try:
                result[normalize(name)] = future.result()
            except Exception:
                result[normalize(name)] = ""

    return result


# ==================================================
# 앱스토어 인기 게임
# ==================================================

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
                "icon": icon
            })
        except Exception:
            continue

    return games


# ==================================================
# 구글 플레이 인기 게임
# ==================================================

def get_google_ranking():
    try:
        from google_play_scraper import collection, Collection

        results = collection(
            collection=Collection.TOP_FREE,
            category="GAME",
            country="kr",
            lang="ko",
            count=100
        )

        games = []

        for rank, item in enumerate(results, start=1):
            games.append({
                "name": item.get("title", ""),
                "rank": rank,
                "icon": item.get("icon", "")
            })

        return [g for g in games if g["name"]]

    except Exception:
        pass

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
            name = item.get("title") or item.get("name")

            if name:
                games.append({
                    "name": name,
                    "rank": rank,
                    "icon": item.get("icon", "")
                })

        return games

    except Exception:
        return []


# ==================================================
# 서브컬처 게임에 순위 연결
# ==================================================

def get_game_rank(game, apple, google):
    names = [game["name"]] + game["aliases"]
    found = []

    for store_name, store_games in [
        ("앱스토어", apple),
        ("구글 플레이", google)
    ]:
        for item in store_games:
            if any(
                same_name(item["name"], alias)
                for alias in names
            ):
                found.append(
                    f'{store_name} {item["rank"]}위'
                )
                break

    return " · ".join(found) if found else "순위 정보 없음"


# ==================================================
# 게임 카드
# ==================================================

def show_card(name, icon, info, reason=""):
    left, right = st.columns([1, 4])

    with left:
        if icon:
            st.image(icon, width=72)
        else:
            st.markdown(
                """
                <div style="
                    width:72px;
                    height:72px;
                    border-radius:14px;
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
        st.markdown(f"**{name}**")
        st.caption(info)

        if reason:
            st.caption(reason)


# ==================================================
# 화면
# ==================================================

st.title("🎮 모바일 게임 랭킹")
st.caption("앱스토어 · 구글 플레이 · 서브컬처 게임")

# ==================================================
# 서브컬처 아이콘 먼저 불러오기
# ==================================================

with st.spinner("서브컬처 게임 아이콘을 모두 불러오는 중입니다..."):
    icons = load_all_subculture_icons()

# ==================================================
# 순위 데이터
# ==================================================

with st.spinner("게임 순위를 불러오는 중입니다..."):
    apple_games = get_apple_ranking()
    google_games = get_google_ranking()

# ==================================================
# 탭
# ==================================================

tab_all, tab_sub = st.tabs([
    "전체 게임",
    "서브컬처"
])

# ==================================================
# 전체 게임
# ==================================================

with tab_all:
    st.subheader("전체 게임 순위")

    store = st.radio(
        "스토어",
        ["전체", "앱스토어", "구글 플레이"],
        horizontal=True
    )

    keyword = st.text_input(
        "게임 검색",
        placeholder="게임 이름 입력"
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

        for store_name, games in [
            ("앱스토어", apple_games),
            ("구글 플레이", google_games)
        ]:
            for game in games:
                key = normalize(game["name"])

                if key not in combined:
                    combined[key] = {
                        "name": game["name"],
                        "icon": game["icon"],
                        "ranks": []
                    }

                combined[key]["ranks"].append(
                    f'{store_name} {game["rank"]}위'
                )

        display = [
            {
                "name": g["name"],
                "icon": g["icon"],
                "info": " · ".join(g["ranks"])
            }
            for g in combined.values()
        ]

    if keyword:
        display = [
            g for g in display
            if keyword.lower() in g["name"].lower()
        ]

    st.caption(f"게임 {len(display)}개")

    for game in display:
        show_card(
            game["name"],
            game["icon"],
            game["info"]
        )

    if not apple_games:
        st.warning("앱스토어 순위를 불러오지 못했습니다.")

    if not google_games:
        st.warning("구글 플레이 순위를 불러오지 못했습니다.")

# ==================================================
# 서브컬처
# ==================================================

with tab_sub:
    st.subheader("서브컬처 게임")

    st.caption(
        "캐릭터 수집, 육성, 스토리, 애니메이션풍 작품 등을 중심으로 분류했습니다."
    )

    keyword = st.text_input(
        "서브컬처 게임 검색",
        placeholder="게임 이름 입력",
        key="sub_search"
    )

    filtered = SUBCULTURE

    if keyword:
        filtered = [
            game for game in SUBCULTURE
            if keyword.lower() in game["name"].lower()
        ]

    visible = filtered[:st.session_state.more_sub]

    st.caption(
        f"등록 {len(filtered)}개 · 표시 {len(visible)}개"
    )

    for game in visible:
        icon = icons.get(normalize(game["name"]), "")

        rank = get_game_rank(
            game,
            apple_games,
            google_games
        )

        show_card(
            game["name"],
            icon,
            rank,
            game["reason"]
        )

    if len(filtered) > len(visible):
        if st.button(
            "더보기",
            use_container_width=True
        ):
            st.session_state.more_sub += 30
            st.rerun()

    if not filtered:
        st.info("검색 결과가 없습니다.")

# ==================================================
# 새로고침
# ==================================================

st.divider()

if st.button("순위 새로고침", use_container_width=True):
    get_apple_ranking.clear()
    st.rerun()

st.caption(
    "아이콘은 앱스토어 검색 결과에서 정확한 게임 이름이 확인된 경우에 표시합니다. "
    "일부 게임은 한국 앱스토어에 등록되어 있지 않아 아이콘이 없을 수 있습니다."
)
