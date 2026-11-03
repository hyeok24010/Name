import re
import requests
import streamlit as st

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

DISCOVERY_WORDS = [
    "서브컬처 게임",
    "서브컬처 RPG",
    "애니메이션 RPG"
]


# ==========================================
# 서브컬처 게임 등록 목록
#
# 게임 이름과 별칭을 비교하여 분류한다.
# 새로운 게임을 추가하려면 이 목록에 등록한다.
# ==========================================

SUBCULTURE_CATALOG = [
    {
        "name": "승리의 여신: 니케",
        "aliases": [
            "니케",
            "NIKKE",
            "Goddess of Victory NIKKE"
        ]
    },
    {
        "name": "명조: 워더링 웨이브",
        "aliases": [
            "명조",
            "Wuthering Waves"
        ]
    },
    {
        "name": "젠레스 존 제로",
        "aliases": [
            "젠레스",
            "ZZZ",
            "Zenless Zone Zero"
        ]
    },
    {
        "name": "붕괴: 스타레일",
        "aliases": [
            "붕괴 스타레일",
            "스타레일",
            "Honkai Star Rail"
        ]
    },
    {
        "name": "원신",
        "aliases": [
            "Genshin Impact"
        ]
    },
    {
        "name": "블루 아카이브",
        "aliases": [
            "블루아카이브",
            "Blue Archive"
        ]
    },
    {
        "name": "트릭컬 리바이브",
        "aliases": [
            "트릭컬",
            "Trickcal",
            "Trickcal Revive"
        ]
    },
    {
        "name": "림버스 컴퍼니",
        "aliases": [
            "림버스",
            "Limbus Company"
        ]
    },
    {
        "name": "소녀전선2: 망명",
        "aliases": [
            "소녀전선2",
            "Girls Frontline 2",
            "Girls Frontline 2 Exilium"
        ]
    },
    {
        "name": "명일방주",
        "aliases": [
            "Arknights"
        ]
    },
    {
        "name": "에픽세븐",
        "aliases": [
            "Epic Seven"
        ]
    },
    {
        "name": "우마무스메 프리티 더비",
        "aliases": [
            "우마무스메",
            "Uma Musume",
            "Uma Musume Pretty Derby"
        ]
    },
    {
        "name": "페이트/그랜드 오더",
        "aliases": [
            "페이트 그랜드 오더",
            "FGO",
            "Fate Grand Order"
        ]
    },
    {
        "name": "리버스: 1999",
        "aliases": [
            "리버스1999",
            "Reverse 1999"
        ]
    },
    {
        "name": "브라운더스트2",
        "aliases": [
            "Brown Dust 2",
            "BrownDust2"
        ]
    },
    {
        "name": "프로젝트 세카이",
        "aliases": [
            "프로세카",
            "Project Sekai",
            "Hatsune Miku Colorful Stage"
        ]
    },
    {
        "name": "앙상블 스타즈!!",
        "aliases": [
            "앙스타",
            "Ensemble Stars",
            "Ensemble Stars Music"
        ]
    },
    {
        "name": "카운터사이드",
        "aliases": [
            "CounterSide"
        ]
    },
    {
        "name": "벽람항로",
        "aliases": [
            "Azur Lane"
        ]
    },
    {
        "name": "뉴럴 클라우드",
        "aliases": [
            "Neural Cloud"
        ]
    },
    {
        "name": "붕괴3rd",
        "aliases": [
            "붕괴3",
            "Honkai Impact 3rd"
        ]
    },
    {
        "name": "무기미도",
        "aliases": [
            "Path to Nowhere"
        ]
    },
    {
        "name": "아우터플레인",
        "aliases": [
            "Outerplane"
        ]
    },
    {
        "name": "헤븐 번즈 레드",
        "aliases": [
            "헤번레",
            "Heaven Burns Red"
        ]
    },
    {
        "name": "카오스 제로 나이트메어",
        "aliases": [
            "카오스제로",
            "Chaos Zero Nightmare"
        ]
    },
    {
        "name": "명일방주: 엔드필드",
        "aliases": [
            "엔드필드",
            "Arknights Endfield"
        ]
    },
    {
        "name": "로스트 소드",
        "aliases": [
            "Lost Sword"
        ]
    }
]


# ==========================================
# 게임 이름 정리 및 분류
# ==========================================

def normalize(text):
    return re.sub(
        r"[^a-zA-Z0-9가-힣]",
        "",
        str(text)
    ).lower()


def find_subculture_game(game_name):

    normalized_name = normalize(game_name)

    for catalog_game in SUBCULTURE_CATALOG:

        names = [
            catalog_game["name"]
        ] + catalog_game["aliases"]

        for alias in names:

            if normalized_name == normalize(alias):
                return catalog_game["name"]

    return None


# ==========================================
# 게임 데이터 추가
# ==========================================

def add_game(
    database,
    store,
    item,
    rank=None,
    discovered=False
):

    name = item.get("name", "").strip()

    if not name:
        return

    subculture_name = find_subculture_game(name)

    # 등록된 서브컬처 게임은 정식 이름으로 통합
    key_name = subculture_name if subculture_name else name
    key = normalize(key_name)

    if not key:
        return

    if key not in database:

        database[key] = {
            "name": key_name,
            "developer": "",
            "icon": "",
            "description": "",

            "apple_rank": None,
            "google_rank": None,

            "apple_url": "",
            "google_url": "",

            "apple_discovered": False,
            "google_discovered": False,

            "score": 0,

            "subculture": subculture_name is not None
        }

    game = database[key]

    if not game["developer"]:
        game["developer"] = item.get("developer", "")

    if not game["icon"]:
        game["icon"] = item.get("icon", "")

    if not game["description"]:
        game["description"] = item.get("description", "")

    if store == "Apple":

        game["apple_url"] = (
            item.get("url", "")
            or game["apple_url"]
        )

        if rank is not None:
            game["apple_rank"] = rank

        if discovered:
            game["apple_discovered"] = True

    elif store == "Google":

        game["google_url"] = (
            item.get("url", "")
            or game["google_url"]
        )

        if rank is not None:
            game["google_rank"] = rank

        if discovered:
            game["google_discovered"] = True

    # 통합 순위 점수 계산
    game["score"] = 0

    if game["apple_rank"] is not None:
        game["score"] += 101 - game["apple_rank"]

    if game["google_rank"] is not None:
        game["score"] += 101 - game["google_rank"]


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
            "url": item.get("id", {}).get("label", ""),
            "rank": rank
        })

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
            "icon": (
                item.get("artworkUrl512")
                or item.get("artworkUrl100", "")
            ),
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
# 전체 게임 데이터 수집
# ==========================================

def collect_games():

    database = {}
    errors = []

    # Apple 순위
    try:

        apple_chart = get_apple_chart()

        for game in apple_chart:

            rank = game["rank"]

            add_game(
                database,
                "Apple",
                game,
                rank=rank
            )

    except Exception as e:

        errors.append(
            "Apple 순위: " + str(e)
        )

    # Google 순위
    try:

        google_chart = get_google_chart()

        for game in google_chart:

            rank = game["rank"]

            add_game(
                database,
                "Google",
                game,
                rank=rank
            )

    except Exception as e:

        errors.append(
            "Google 순위: " + str(e)
        )

    # 신규 게임 후보 검색
    # 검색 결과는 순위에 넣지 않고 분류 검토에만 사용
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
# 스토어별 필터
# ==========================================

def filter_store(
    games,
    store,
    include_candidates=False
):

    result = []

    for game in games:

        if store == "Apple App Store":

            has_game = (
                game["apple_rank"] is not None
                or (
                    include_candidates
                    and game["apple_discovered"]
                )
            )

        elif store == "Google Play":

            has_game = (
                game["google_rank"] is not None
                or (
                    include_candidates
                    and game["google_discovered"]
                )
            )

        else:

            has_game = (
                game["apple_rank"] is not None
                or game["google_rank"] is not None
                or (
                    include_candidates
                    and (
                        game["apple_discovered"]
                        or game["google_discovered"]
                    )
                )
            )

        if has_game:
            result.append(game)

    return result


# ==========================================
# 순위 정렬
# ==========================================

def sort_games(games, store):

    if store == "Apple App Store":

        return sorted(
            games,
            key=lambda game: (
                game["apple_rank"] or 999,
                game["name"]
            )
        )

    if store == "Google Play":

        return sorted(
            games,
            key=lambda game: (
                game["google_rank"] or 999,
                game["name"]
            )
        )

    # 통합 순위
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

def show_games(
    games,
    store,
    is_subculture=False
):

    if not games:

        st.info("표시할 게임이 없습니다.")
        return

    # 서브컬처 목록만 따로 정렬
    games = sort_games(games, store)

    for index, game in enumerate(games, start=1):

        col1, col2 = st.columns([1, 5])

        with col1:

            if game["icon"]:
                st.image(
                    game["icon"],
                    width=75
                )
            else:
                st.write("🎮")

        with col2:

            st.markdown(
                f"**{index}위. {game['name']}**"
            )

            if is_subculture:
                st.caption("✨ 서브컬처 등록 게임")

            if store == "통합 순위":

                apple = game["apple_rank"]
                google = game["google_rank"]

                a = (
                    f"Apple {apple}위"
                    if apple is not None
                    else "Apple 차트 외"
                )

                g = (
                    f"Google {google}위"
                    if google is not None
                    else "Google 차트 외"
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

            elif store == "Apple App Store":

                st.caption(game["developer"])

                if game["apple_url"]:

                    st.markdown(
                        f"[Apple App Store]({game['apple_url']})"
                    )

                if game["apple_rank"] is not None:

                    st.caption(
                        f"전체 앱스토어 순위: {game['apple_rank']}위"
                    )

            elif store == "Google Play":

                st.caption(game["developer"])

                if game["google_url"]:

                    st.markdown(
                        f"[Google Play]({game['google_url']})"
                    )

                if game["google_rank"] is not None:

                    st.caption(
                        f"전체 구글 플레이 순위: {game['google_rank']}위"
                    )

            with st.expander("게임 정보 및 분류"):

                if game["description"]:

                    st.write(
                        game["description"][:500]
                    )

                if game["subculture"]:

                    st.success(
                        "서브컬처 게임 등록 목록에 포함된 게임입니다."
                    )

                else:

                    st.caption(
                        "현재 서브컬처 등록 목록에 포함되어 있지 않습니다."
                    )

        st.divider()


# ==========================================
# 사이드바 설정
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
# 데이터 수집
# ==========================================

with st.spinner(
    "구글 플레이와 애플 앱스토어 순위를 수집하고 있습니다..."
):

    all_games, collection_errors = collect_games()


# ==========================================
# 오류 안내
# ==========================================

for error in collection_errors:

    st.warning(error)


# ==========================================
# 탭 구성
# ==========================================

all_tab, sub_tab, pending_tab = st.tabs([
    "🌏 전체 게임",
    "✨ 서브컬처",
    "🔎 분류 검토"
])


# ==========================================
# 전체 게임
# ==========================================

with all_tab:

    st.subheader("🌏 전체 모바일 게임")

    st.caption(
        "구글 플레이와 애플 앱스토어의 기존 전체 게임 순위입니다."
    )

    selected = filter_store(
        all_games,
        store_choice
    )

    st.metric(
        "전체 게임 수",
        len(selected)
    )

    show_games(
        selected,
        store_choice
    )


# ==========================================
# 서브컬처 게임
# ==========================================

with sub_tab:

    st.subheader("✨ 서브컬처 게임 순위")

    st.caption(
        "등록된 서브컬처 게임만 골라 각 스토어 순위에 따라 다시 정렬합니다."
    )

    verified = [
        game for game in all_games
        if game["subculture"]
    ]

    selected = filter_store(
        verified,
        store_choice
    )

    st.metric(
        "확인된 서브컬처 게임",
        len(selected)
    )

    show_games(
        selected,
        store_choice,
        is_subculture=True
    )


# ==========================================
# 분류 검토
# ==========================================

with pending_tab:

    st.subheader("🔎 서브컬처 분류 검토")

    st.caption(
        "스토어 순위 또는 검색에서 발견했지만, "
        "아직 서브컬처 목록에 등록되지 않은 게임입니다."
    )

    pending = [
        game for game in all_games
        if not game["subculture"]
    ]

    selected = filter_store(
        pending,
        store_choice,
        include_candidates=True
    )

    st.metric(
        "검토 대상 게임",
        len(selected)
    )

    show_games(
        selected,
        store_choice
    )


# ==========================================
# 하단 안내
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    f"수집한 게임: {len(all_games)}개"
)

st.sidebar.caption(
    f"서브컬처 등록 게임: "
    f"{sum(1 for game in all_games if game['subculture'])}개"
)

st.sidebar.caption(
    "스토어 순위 데이터는 약 30분간 캐시됩니다."
)

st.sidebar.caption(
    "서브컬처 분류는 등록 목록과 게임 이름을 대조합니다."
)
