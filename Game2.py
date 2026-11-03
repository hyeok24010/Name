
import re
import time
import html
import requests
import xml.etree.ElementTree as ET
import streamlit as st

from urllib.parse import quote_plus


# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="모바일 게임 순위",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 모바일 게임 순위")
st.caption("한국 모바일 게임 순위 및 서브컬처 게임 탐색")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LIMIT = 100
DISCOVERY_LIMIT = 60

DISCOVERY_WORDS = [
    "서브컬처 게임",
    "서브컬처 RPG",
    "애니메이션 RPG"
]


# ==========================================
# 공통 함수
# ==========================================

def normalize(text):
    return re.sub(
        r"[^a-zA-Z0-9가-힣]",
        "",
        str(text)
    ).lower()


def add_game(database, store, item, rank=None, discovered=False):

    name = item.get("name", "").strip()

    if not name:
        return

    key = normalize(name)

    if not key:
        return

    if key not in database:
        database[key] = {
            "name": name,
            "developer": "",
            "icon": "",
            "description": "",
            "apple_rank": None,
            "google_rank": None,
            "apple_url": "",
            "google_url": "",
            "score": 0,
            "discovered": False,
            "evidence": []
        }

    game = database[key]

    if not game["developer"]:
        game["developer"] = item.get("developer", "")

    if not game["icon"]:
        game["icon"] = item.get("icon", "")

    if not game["description"]:
        game["description"] = item.get("description", "")

    if discovered:
        game["discovered"] = True

    if store == "Apple":
        game["apple_url"] = item.get("url", "")

        if rank is not None:
            game["apple_rank"] = rank
            game["score"] += 101 - rank

    elif store == "Google":
        game["google_url"] = item.get("url", "")

        if rank is not None:
            game["google_rank"] = rank
            game["score"] += 101 - rank


# ==========================================
# Apple 게임 순위
# ==========================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_apple_chart():

    url = (
        "https://itunes.apple.com/kr/rss/"
        "topfreeapplications/limit=100/genre=6014/json"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=25
    )

    response.raise_for_status()

    data = response.json()

    entries = data.get("feed", {}).get("entry", [])

    if isinstance(entries, dict):
        entries = [entries]

    games = []

    for rank, item in enumerate(entries, start=1):

        images = item.get("im:image", [])

        games.append({
            "name": item.get("im:name", {}).get("label", ""),
            "developer": item.get("im:artist", {}).get("label", ""),
            "icon": images[-1].get("label", "") if images else "",
            "url": item.get("id", {}).get("label", "")
        })

        games[-1]["rank"] = rank

    return games


# ==========================================
# Apple 검색
# ==========================================

@st.cache_data(ttl=86400, show_spinner=False)
def search_apple_games(keyword):

    url = "https://itunes.apple.com/search"

    params = {
        "term": keyword,
        "country": "kr",
        "entity": "software",
        "genreId": "6014",
        "limit": 20
    }

    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=25
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("results", []):

        results.append({
            "name": item.get("trackName", ""),
            "developer": item.get("sellerName", ""),
            "icon": item.get("artworkUrl512")
                    or item.get("artworkUrl100", ""),
            "url": item.get("trackViewUrl", ""),
            "description": item.get("description", "")
        })

    return results


# ==========================================
# Google Play
# ==========================================

@st.cache_resource
def get_google_scraper():

    from gplay_scraper import GPlayScraper

    return GPlayScraper()


@st.cache_data(ttl=1800, show_spinner=False)
def get_google_chart():

    scraper = get_google_scraper()

    result = scraper.list_analyze(
        "TOP_FREE",
        "GAME",
        count=100,
        lang="ko",
        country="kr"
    )

    games = []

    for rank, item in enumerate(result, start=1):

        games.append({
            "name": item.get("title", ""),
            "developer": item.get("developer", ""),
            "icon": item.get("icon", ""),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
            "rank": rank
        })

    return games


# ==========================================
# Google Play 검색
# ==========================================

@st.cache_data(ttl=86400, show_spinner=False)
def search_google_games(keyword):

    scraper = get_google_scraper()

    result = scraper.search_analyze(
        keyword,
        count=20,
        lang="ko",
        country="kr"
    )

    games = []

    for item in result:

        games.append({
            "name": item.get("title", ""),
            "developer": item.get("developer", ""),
            "icon": item.get("icon", ""),
            "url": item.get("url", ""),
            "description": item.get("description", "")
        })

    return games


# ==========================================
# 인터넷 기사로 서브컬처 여부 확인
# ==========================================

@st.cache_data(ttl=86400, show_spinner=False)
def search_subculture_evidence(game_name):

    query = f'"{game_name}" "서브컬처"'

    url = (
        "https://news.google.com/rss/search?q="
        + quote_plus(query)
        + "&hl=ko&gl=KR&ceid=KR:ko"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    evidence = []

    for item in root.findall(".//item"):

        title = item.findtext("title", "")
        description = item.findtext("description", "")
        link = item.findtext("link", "")

        text = normalize(
            html.unescape(title + " " + description)
        )

        # 기사 제목이나 설명에 실제 서브컬처 표현이 있는 경우만 인정
        if "서브컬처" not in text:
            continue

        evidence.append({
            "title": html.unescape(title),
            "description": html.unescape(
                re.sub("<[^>]+>", " ", description)
            ),
            "url": link
        })

        if len(evidence) >= 3:
            break

    return evidence


# ==========================================
# 전체 게임 데이터 수집
# ==========================================

def collect_games():

    database = {}
    errors = []

    # Apple 순위
    try:
        apple_chart = get_apple_chart()

        for game in apple_chart:
            rank = game.pop("rank")
            add_game(
                database,
                "Apple",
                game,
                rank=rank
            )

    except Exception as e:
        errors.append("Apple 순위: " + str(e))

    # Google 순위
    try:
        google_chart = get_google_chart()

        for game in google_chart:
            rank = game.pop("rank")
            add_game(
                database,
                "Google",
                game,
                rank=rank
            )

    except Exception as e:
        errors.append("Google 순위: " + str(e))

    # 인터넷 검색을 통한 신규 후보 수집
    for keyword in DISCOVERY_WORDS:

        try:
            apple_results = search_apple_games(keyword)

            for game in apple_results:
                add_game(
                    database,
                    "Apple",
                    game,
                    discovered=True
                )

        except Exception as e:
            errors.append(
                f"Apple 검색({keyword}): {str(e)}"
            )

        try:
            google_results = search_google_games(keyword)

            for game in google_results:
                add_game(
                    database,
                    "Google",
                    game,
                    discovered=True
                )

        except Exception as e:
            errors.append(
                f"Google 검색({keyword}): {str(e)}"
            )

    return list(database.values()), errors


# ==========================================
# 서브컬처 검증
# ==========================================

@st.cache_data(ttl=86400, show_spinner=False)
def verify_games(games):

    verified = []
    pending = []
    errors = []

    # 차트에 등장한 게임을 우선 확인
    games = sorted(
        games,
        key=lambda game: (
            0 if (
                game["apple_rank"] is not None
                or game["google_rank"] is not None
            ) else 1,
            -game["score"]
        )
    )

    # 한 번에 너무 많은 검색을 하지 않도록 제한
    for game in games[:DISCOVERY_LIMIT]:

        try:
            evidence = search_subculture_evidence(
                game["name"]
            )

            if evidence:
                game["evidence"] = evidence
                verified.append(game)
            else:
                pending.append(game)

            time.sleep(0.15)

        except Exception as e:
            pending.append(game)
            errors.append(
                f"{game['name']}: {str(e)}"
            )

    return verified, pending, errors


# ==========================================
# 순위 정렬
# ==========================================

def sort_games(games):

    return sorted(
        games,
        key=lambda game: (
            -game["score"],
            min(
                game["apple_rank"] or 999,
                game["google_rank"] or 999
            ),
            game["name"]
        )
    )


# ==========================================
# 게임 목록 출력
# ==========================================

def show_games(games, store_type):

    if not games:
        st.info("표시할 게임이 없습니다.")
        return

    games = sort_games(games)

    for index, game in enumerate(games, start=1):

        col1, col2 = st.columns([1, 5])

        with col1:

            if game["icon"]:
                st.image(game["icon"], width=75)
            else:
                st.write("🎮")

        with col2:

            st.markdown(
                f"**{index}위. {game['name']}**"
            )

            if store_type == "통합":

                apple = game["apple_rank"]
                google = game["google_rank"]

                a = (
                    f"Apple {apple}위"
                    if apple else "Apple 차트 외"
                )

                g = (
                    f"Google {google}위"
                    if google else "Google 차트 외"
                )

                st.caption(f"{a} · {g}")

                links = []

                if game["apple_url"]:
                    links.append(
                        f"[Apple App Store]({game['apple_url']})"
                    )

                if game["google_url"]:
                    links.append(
                        f"[Google Play]({game['google_url']})"
                    )

                if links:
                    st.markdown(" | ".join(links))

            elif store_type == "Apple":

                st.caption(game["developer"])

                if game["apple_url"]:
                    st.markdown(
                        f"[Apple App Store]({game['apple_url']})"
                    )

            else:

                st.caption(game["developer"])

                if game["google_url"]:
                    st.markdown(
                        f"[Google Play]({game['google_url']})"
                    )

            with st.expander("분류 근거 보기"):

                if game["description"]:
                    st.write(game["description"][:500])

                if game["evidence"]:

                    st.markdown("**인터넷 기사 근거**")

                    for article in game["evidence"]:

                        st.markdown(
                            f"- [{article['title']}]"
                            f"({article['url']})"
                        )

                        if article["description"]:
                            st.caption(
                                article["description"][:300]
                            )

                else:
                    st.caption("확인된 기사 근거가 없습니다.")

        st.divider()


# ==========================================
# 화면 설정
# ==========================================

st.sidebar.header("⚙️ 순위 설정")

store_choice = st.sidebar.selectbox(
    "스토어",
    [
        "통합 순위",
        "Google Play",
        "Apple App Store"
    ]
)

if st.sidebar.button("🔄 전체 데이터 새로고침"):

    st.cache_data.clear()
    st.rerun()


# ==========================================
# 데이터 불러오기
# ==========================================

with st.spinner("스토어 게임과 인터넷 자료를 수집하고 있습니다..."):

    all_games, collection_errors = collect_games()

    verified, pending, verification_errors = verify_games(
        all_games
    )


# ==========================================
# 오류 안내
# ==========================================

for error in collection_errors:
    st.warning(error)

for error in verification_errors:
    st.warning("서브컬처 확인 오류: " + error)


# ==========================================
# 스토어별 필터
# ==========================================

def filter_store(games, store):

    if store == "Apple App Store":
        return [
            game for game in games
            if game["apple_url"]
        ]

    if store == "Google Play":
        return [
            game for game in games
            if game["google_url"]
        ]

    return games


# ==========================================
# 메인 탭
# ==========================================

all_tab, sub_tab, pending_tab = st.tabs([
    "🌏 전체 게임",
    "✨ 서브컬처",
    "🔎 분류 검토"
])


# 전체 게임
with all_tab:

    st.subheader("전체 모바일 게임")

    selected = filter_store(
        all_games,
        store_choice
    )

    show_games(selected, store_choice.replace(" 순위", "").replace(" App Store", ""))


# 서브컬처 게임
with sub_tab:

    st.subheader("✨ 인터넷 자료로 확인된 서브컬처 게임")

    st.caption(
        "게임 이름과 서브컬처 표현이 함께 확인된 기사 자료를 기준으로 합니다."
    )

    selected = filter_store(
        verified,
        store_choice
    )

    st.metric(
        "확인된 서브컬처 게임",
        len(selected)
    )

    show_games(selected, store_choice.replace(" 순위", "").replace(" App Store", ""))


# 검토 대상
with pending_tab:

    st.subheader("🔎 분류 검토 대상")

    st.caption(
        "스토어 검색으로 발견했지만, 기사에서 서브컬처 표현을 확인하지 못한 게임입니다."
    )

    selected = filter_store(
        pending,
        store_choice
    )

    show_games(selected, store_choice.replace(" 순위", "").replace(" App Store", ""))


# ==========================================
# 하단 안내
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    f"수집한 게임: {len(all_games)}개"
)

st.sidebar.caption(
    f"서브컬처 확인: {len(verified)}개"
)

st.sidebar.caption(
    "인터넷 검색 결과는 약 24시간 캐시됩니다."
)

st.sidebar.caption(
    "서브컬처 분류는 기사 검색 결과를 이용한 참고 판정입니다."
)
