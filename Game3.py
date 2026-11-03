
import streamlit as st
import requests
import re
import html
import time
import unicodedata
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="모바일 게임 랭킹",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

APPLE_RSS_URL = (
    "https://itunes.apple.com/kr/rss/"
    "topfreeapplications/limit=100/genre=6014/json"
)

APPLE_SEARCH_URL = "https://itunes.apple.com/search"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
}

# =========================================================
# 세션 상태
# =========================================================

if "icon_cache" not in st.session_state:
    st.session_state.icon_cache = {}

if "more_count" not in st.session_state:
    st.session_state.more_count = {
        "subculture": 30,
        "review": 30
    }

if "icon_cursor" not in st.session_state:
    st.session_state.icon_cursor = 0

if "icon_errors" not in st.session_state:
    st.session_state.icon_errors = []

# =========================================================
# 서브컬처 게임 기준 목록
# 실제 작품 중심으로 등록하고, 단순 검색어 일치로 분류하지 않음
# =========================================================

SUBCULTURE_GAMES = [
    {
        "name": "블루 아카이브",
        "aliases": ["Blue Archive", "ブルーアーカイブ"],
        "reason": "애니메이션풍 캐릭터 수집 및 육성 RPG"
    },
    {
        "name": "승리의 여신: 니케",
        "aliases": ["NIKKE", "GODDESS OF VICTORY: NIKKE"],
        "reason": "캐릭터 중심 수집형 슈팅 RPG"
    },
    {
        "name": "원신",
        "aliases": ["Genshin Impact"],
        "reason": "애니메이션풍 캐릭터 중심 오픈월드 RPG"
    },
    {
        "name": "붕괴: 스타레일",
        "aliases": ["Honkai: Star Rail"],
        "reason": "캐릭터 수집 및 스토리 중심 RPG"
    },
    {
        "name": "젠레스 존 제로",
        "aliases": ["Zenless Zone Zero", "ZZZ"],
        "reason": "애니메이션풍 캐릭터 중심 액션 RPG"
    },
    {
        "name": "명조: 워더링 웨이브",
        "aliases": ["Wuthering Waves"],
        "reason": "캐릭터 수집 및 스토리 중심 액션 RPG"
    },
    {
        "name": "명일방주",
        "aliases": ["Arknights"],
        "reason": "캐릭터 수집 및 스토리 중심 전략 RPG"
    },
    {
        "name": "림버스 컴퍼니",
        "aliases": ["Limbus Company"],
        "reason": "캐릭터와 서사를 중심으로 진행되는 RPG"
    },
    {
        "name": "트릭컬 리바이브",
        "aliases": ["Trickcal Re:VIVE", "Trickcal"],
        "reason": "캐릭터 수집 및 육성 중심 RPG"
    },
    {
        "name": "리버스: 1999",
        "aliases": ["Reverse: 1999"],
        "reason": "캐릭터와 스토리 중심 턴제 RPG"
    },
    {
        "name": "소녀전선 2: 망명",
        "aliases": ["Girls' Frontline 2: Exilium"],
        "reason": "캐릭터 수집 및 전략 전투 RPG"
    },
    {
        "name": "우마무스메 프리티 더비",
        "aliases": ["Uma Musume Pretty Derby"],
        "reason": "캐릭터 육성 및 스토리 중심 시뮬레이션"
    },
]

# 근거가 부족하거나 분류 판단이 더 필요한 게임은 이 목록에만 추가
REVIEW_GAMES = [
    # 예시:
    # {"name": "게임 이름", "reason": "서브컬처 요소가 있는지 추가 확인 필요"}
]

# =========================================================
# 이름 정리 / 비교
# =========================================================

def normalize_name(name):
    if not name:
        return ""

    name = unicodedata.normalize("NFKC", str(name))
    name = name.lower()
    name = re.sub(r"[^0-9a-z가-힣]", "", name)

    return name


def get_aliases(game):
    return [game["name"]] + game.get("aliases", [])


def is_same_game(name1, name2):
    a = normalize_name(name1)
    b = normalize_name(name2)

    if not a or not b:
        return False

    return a == b


def find_catalogue_game(name):
    target = normalize_name(name)

    for game in SUBCULTURE_GAMES:
        for alias in get_aliases(game):
            if target == normalize_name(alias):
                return game

    return None


# =========================================================
# HTTP 요청
# =========================================================

def request_json(url, params=None, timeout=12):
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
# 애플 앱스토어 순위
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_apple_games():
    data = request_json(APPLE_RSS_URL)

    if not data:
        return []

    entries = data.get("feed", {}).get("entry", [])
    games = []

    for rank, item in enumerate(entries, start=1):
        try:
            name = item.get("im:name", {}).get("label", "")
            artist = item.get("im:artist", {}).get("label", "")

            images = item.get("im:image", [])
            icon = ""

            if images:
                icon = images[-1].get("label", "")

            app_id = (
                item.get("id", {})
                .get("attributes", {})
                .get("im:id", "")
            )

            if not name:
                continue

            games.append({
                "name": name,
                "rank": rank,
                "store": "앱스토어",
                "icon": icon,
                "developer": artist,
                "app_id": str(app_id)
            })

        except Exception:
            continue

    return games


# =========================================================
# 구글 플레이 순위
# 설치된 스크래퍼 종류가 달라도 최대한 대응
# =========================================================

def get_google_games():
    games = []

    # 방식 1: google-play-scraper 패키지
    try:
        from google_play_scraper import (
            collection,
            Sort,
            Collection
        )

        results = collection(
            collection=Collection.TOP_FREE,
            category="GAME",
            country="kr",
            lang="ko",
            count=100
        )

        for rank, item in enumerate(results, start=1):
            name = item.get("title", "")

            if not name:
                continue

            games.append({
                "name": name,
                "rank": rank,
                "store": "구글 플레이",
                "icon": item.get("icon", ""),
                "developer": item.get("developer", ""),
                "app_id": item.get("appId", "")
            })

        if games:
            return games

    except Exception:
        pass

    # 방식 2: 기존 코드에서 사용하던 GPlayScraper
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

        for rank, item in enumerate(results, start=1):
            if not isinstance(item, dict):
                continue

            name = (
                item.get("title")
                or item.get("name")
                or ""
            )

            if not name:
                continue

            games.append({
                "name": name,
                "rank": rank,
                "store": "구글 플레이",
                "icon": item.get("icon", ""),
                "developer": item.get("developer", ""),
                "app_id": item.get("appId", "")
            })

        if games:
            return games

    except Exception:
        pass

    return games


# =========================================================
# 전체 게임 수집
# =========================================================

def collect_games():
    apple_games = get_apple_games()
    google_games = get_google_games()

    all_games = {}

    for game in apple_games + google_games:
        key = normalize_name(game["name"])

        if not key:
            continue

        if key not in all_games:
            all_games[key] = {
                "name": game["name"],
                "icon": game.get("icon", ""),
                "stores": {}
            }

        store = game["store"]

        all_games[key]["stores"][store] = game["rank"]

        if (
            not all_games[key]["icon"]
            and game.get("icon")
        ):
            all_games[key]["icon"] = game["icon"]

    return list(all_games.values()), apple_games, google_games


# =========================================================
# 아이콘 검색
# Apple Search API 이용
# =========================================================

@st.cache_data(ttl=604800, show_spinner=False)
def search_apple_icon(game_name):
    params = {
        "term": game_name,
        "entity": "software",
        "country": "kr",
        "limit": 10
    }

    data = request_json(
        APPLE_SEARCH_URL,
        params=params,
        timeout=15
    )

    if not data:
        return ""

    results = data.get("results", [])

    # 이름이 정확히 일치하는 결과 우선
    for item in results:
        result_name = item.get("trackName", "")

        if normalize_name(result_name) == normalize_name(game_name):
            return (
                item.get("artworkUrl512")
                or item.get("artworkUrl100")
                or ""
            )

    # 정확한 이름이 없으면 유사 결과 중 첫 번째 사용
    for item in results:
        icon = (
            item.get("artworkUrl512")
            or item.get("artworkUrl100")
            or ""
        )

        if icon:
            return icon

    return ""


# =========================================================
# 아이콘 캐시 적용
# =========================================================

def apply_icon_cache(games):
    for game in games:
        key = normalize_name(game["name"])

        saved_icon = st.session_state.icon_cache.get(key)

        if saved_icon:
            game["icon"] = saved_icon

    return games


# =========================================================
# 서브컬처 목록 만들기
# 순위와 무관하게 등록된 게임을 모두 표시
# =========================================================

def build_subculture_list(all_games):
    result = []

    for catalogue in SUBCULTURE_GAMES:
        found = None

        for game in all_games:
            if is_same_game(game["name"], catalogue["name"]):
                found = game
                break

            for alias in catalogue.get("aliases", []):
                if is_same_game(game["name"], alias):
                    found = game
                    break

            if found:
                break

        stores = found["stores"] if found else {}

        result.append({
            "name": catalogue["name"],
            "reason": catalogue["reason"],
            "icon": found.get("icon", "") if found else "",
            "stores": stores
        })

    return result


# =========================================================
# 화면 디자인
# =========================================================

st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    .game-card {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 13px;
        padding: 12px;
        margin-bottom: 10px;
        min-height: 100px;
    }

    .game-name {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 5px;
        word-break: keep-all;
    }

    .game-info {
        font-size: 12px;
        opacity: 0.75;
        line-height: 1.5;
    }

    .game-icon {
        width: 68px;
        height: 68px;
        border-radius: 13px;
        object-fit: cover;
    }

    .no-icon {
        width: 68px;
        height: 68px;
        border-radius: 13px;
        background: #77777722;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }

    @media (max-width: 600px) {
        .game-card {
            padding: 9px;
        }

        .game-name {
            font-size: 14px;
        }

        .game-icon, .no-icon {
            width: 58px;
            height: 58px;
        }
    }
</style>
""", unsafe_allow_html=True)


def show_game_card(name, icon, info, reason=""):
    col1, col2 = st.columns([1, 4])

    with col1:
        if icon:
            st.image(icon, width=68)
        else:
            st.markdown(
                '<div class="no-icon">🎮</div>',
                unsafe_allow_html=True
            )

    with col2:
        st.markdown(
            f"**{html.escape(name)}**"
        )

        st.caption(info)

        if reason:
            st.caption(reason)


# =========================================================
# 제목
# =========================================================

st.title("🎮 모바일 게임 랭킹")
st.caption("앱스토어와 구글 플레이의 게임 순위 및 서브컬처 게임 모음")

# =========================================================
# 데이터 불러오기
# =========================================================

with st.spinner("게임 정보를 불러오는 중입니다..."):
    all_games, apple_games, google_games = collect_games()

all_games = apply_icon_cache(all_games)

subculture_games = build_subculture_list(all_games)

# =========================================================
# 탭
# =========================================================

tab_all, tab_sub, tab_review = st.tabs([
    "전체 게임",
    "서브컬처 게임",
    "검토 목록"
])


# =========================================================
# 전체 게임
# =========================================================

with tab_all:
    st.subheader("전체 게임 순위")

    store_choice = st.radio(
        "스토어 선택",
        ["전체", "앱스토어", "구글 플레이"],
        horizontal=True,
        key="all_store_choice"
    )

    keyword = st.text_input(
        "게임 검색",
        placeholder="게임 이름을 입력하세요",
        key="all_search"
    )

    if store_choice == "앱스토어":
        display_games = apple_games

    elif store_choice == "구글 플레이":
        display_games = google_games

    else:
        display_games = []

        for game in all_games:
            stores = game["stores"]

            ranks = []

            for store, rank in stores.items():
                ranks.append(f"{store} {rank}위")

            display_games.append({
                "name": game["name"],
                "icon": game["icon"],
                "info": " · ".join(ranks)
            })

    if store_choice != "전체":
        display_games = [
            {
                "name": game["name"],
                "icon": game["icon"],
                "info": f'{game["store"]} {game["rank"]}위'
            }
            for game in display_games
        ]

    if keyword.strip():
        display_games = [
            game for game in display_games
            if keyword.strip().lower() in game["name"].lower()
        ]

    st.caption(f"검색 결과 {len(display_games)}개")

    if not display_games:
        st.info("표시할 게임이 없습니다.")

    else:
        for game in display_games:
            show_game_card(
                game["name"],
                game.get("icon", ""),
                game.get("info", "")
            )

    if not apple_games:
        st.warning("앱스토어 순위를 불러오지 못했습니다.")

    if not google_games:
        st.warning(
            "구글 플레이 순위를 불러오지 못했습니다. "
            "스크래퍼 패키지 또는 외부 서비스 상태를 확인해 주세요."
        )


# =========================================================
# 서브컬처 게임
# =========================================================

with tab_sub:
    st.subheader("서브컬처 게임")
    st.caption(
        "캐릭터와 세계관, 스토리, 수집·육성 요소를 중심으로 "
        "구성된 게임을 모았습니다."
    )

    sub_keyword = st.text_input(
        "서브컬처 게임 검색",
        placeholder="게임 이름 검색",
        key="sub_search"
    )

    filtered_sub = subculture_games

    if sub_keyword.strip():
        filtered_sub = [
            game for game in filtered_sub
            if sub_keyword.strip().lower() in game["name"].lower()
        ]

    visible_count = st.session_state.more_count["subculture"]
    visible_games = filtered_sub[:visible_count]

    st.caption(
        f"등록된 게임 {len(filtered_sub)}개 · "
        f"현재 {len(visible_games)}개 표시"
    )

    for game in visible_games:
        stores = game["stores"]

        if stores:
            rank_text = " · ".join(
                f"{store} {rank}위"
                for store, rank in stores.items()
            )
        else:
            rank_text = "순위 정보 없음"

        show_game_card(
            game["name"],
            game["icon"],
            rank_text,
            game["reason"]
        )

    if visible_count < len(filtered_sub):
        if st.button(
            "더보기",
            key="sub_more",
            use_container_width=True
        ):
            st.session_state.more_count["subculture"] += 30
            st.rerun()

    if not filtered_sub:
        st.info("검색 결과가 없습니다.")


# =========================================================
# 검토 목록
# =========================================================

with tab_review:
    st.subheader("분류 검토 목록")

    st.caption(
        "서브컬처 요소가 있는지 추가 확인이 필요한 게임입니다. "
        "확정 목록과는 별도로 관리합니다."
    )

    if not REVIEW_GAMES:
        st.info("현재 검토 중인 게임이 없습니다.")

    else:
        visible_review = REVIEW_GAMES[
            :st.session_state.more_count["review"]
        ]

        for game in visible_review:
            show_game_card(
                game["name"],
                "",
                "분류 검토 중",
                game.get("reason", "")
            )

        if len(visible_review) < len(REVIEW_GAMES):
            if st.button(
                "검토 목록 더보기",
                key="review_more",
                use_container_width=True
            ):
                st.session_state.more_count["review"] += 30
                st.rerun()


# =========================================================
# 아이콘 가져오기
# =========================================================

st.divider()
st.subheader("게임 아이콘 보완")

missing_icons = []

for game in subculture_games:
    key = normalize_name(game["name"])

    if not game["icon"] and not st.session_state.icon_cache.get(key):
        missing_icons.append(game)

st.caption(
    f"아이콘이 없는 서브컬처 게임: {len(missing_icons)}개"
)

if missing_icons:
    if st.button(
        "아이콘 5개 가져오기",
        use_container_width=True,
        key="get_icons"
    ):
        batch = missing_icons[:5]
        success = 0
        failed = []

        progress = st.progress(0)

        for index, game in enumerate(batch, start=1):
            try:
                icon_url = search_apple_icon(game["name"])

                if icon_url:
                    key = normalize_name(game["name"])

                    # 세션 상태에 저장해 재실행 후에도 유지
                    st.session_state.icon_cache[key] = icon_url
                    success += 1
                else:
                    failed.append(game["name"])

            except Exception:
                failed.append(game["name"])

            progress.progress(index / len(batch))
            time.sleep(0.2)

        st.session_state.icon_errors = failed

        if success:
            st.success(f"{success}개 아이콘을 가져왔습니다.")

        if failed:
            st.warning(
                "아이콘을 찾지 못한 게임: " + ", ".join(failed)
            )

        st.rerun()

else:
    st.success("서브컬처 게임의 아이콘을 모두 확인했습니다.")

if st.session_state.icon_errors:
    with st.expander("최근 아이콘 검색 실패 목록"):
        for name in st.session_state.icon_errors:
            st.write("•", name)


# =========================================================
# 새로고침
# =========================================================

st.divider()

if st.button("게임 순위 새로고침", use_container_width=True):
    get_apple_games.clear()
    st.rerun()

st.caption(
    "순위는 각 스토어에서 제공하는 무료 게임 목록을 기준으로 합니다. "
    "스토어의 데이터 제공 상태에 따라 일부 순위나 아이콘이 표시되지 않을 수 있습니다."
)
