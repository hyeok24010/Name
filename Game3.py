
import re
import time
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

HEADERS = {"User-Agent": "Mozilla/5.0"}

PAGE_SIZE = 30

# ==========================================
# 서브컬처 게임 데이터베이스
# 대표작 및 넓은 기준의 후보
# ==========================================

SUBCULTURE_CATALOG = {
    "승리의 여신: 니케": ["니케", "NIKKE", "Goddess of Victory NIKKE"],
    "블루 아카이브": ["블루아카이브", "Blue Archive"],
    "원신": ["Genshin Impact"],
    "붕괴: 스타레일": ["붕괴 스타레일", "스타레일", "Honkai Star Rail"],
    "붕괴3rd": ["붕괴3", "Honkai Impact 3rd"],
    "젠레스 존 제로": ["젠레스", "ZZZ", "Zenless Zone Zero"],
    "명조: 워더링 웨이브": ["명조", "Wuthering Waves"],
    "소녀전선": ["Girls Frontline"],
    "소녀전선2: 망명": ["소녀전선2", "Girls Frontline 2"],
    "명일방주": ["Arknights"],
    "명일방주: 엔드필드": ["엔드필드", "Arknights Endfield"],
    "림버스 컴퍼니": ["림버스", "Limbus Company"],
    "트릭컬 리바이브": ["트릭컬", "Trickcal", "Trickcal Revive"],
    "브라운더스트2": ["Brown Dust 2", "BrownDust2"],
    "에픽세븐": ["Epic Seven"],
    "우마무스메 프리티 더비": ["우마무스메", "Uma Musume"],
    "페이트/그랜드 오더": ["FGO", "Fate Grand Order"],
    "리버스: 1999": ["리버스1999", "Reverse 1999"],
    "프로젝트 세카이": ["프로세카", "Project Sekai"],
    "앙상블 스타즈!!": ["앙스타", "Ensemble Stars"],
    "벽람항로": ["Azur Lane"],
    "뉴럴 클라우드": ["Neural Cloud"],
    "무기미도": ["Path to Nowhere"],
    "헤븐 번즈 레드": ["헤번레", "Heaven Burns Red"],
    "카오스 제로 나이트메어": ["카오스제로", "Chaos Zero Nightmare"],
    "로스트 소드": ["Lost Sword"],
    "아우터플레인": ["Outerplane"],
    "카운터사이드": ["CounterSide"],
    "프린세스 커넥트! Re:Dive": ["프리코네", "Princess Connect"],
    "뱅드림! 걸즈 밴드 파티!": ["뱅드림", "BanG Dream"],
    "D4DJ Groovy Mix": ["D4DJ"],
    "아이돌마스터 샤이니 컬러즈": ["Shiny Colors"],
    "아이돌마스터 밀리언 라이브": ["Million Live"],
    "아이돌마스터 신데렐라 걸즈": ["Cinderella Girls"],
    "아이돌마스터 학원": ["Gakuen Idolmaster"],
    "러브라이브!": ["Love Live"],
    "마기아 레코드": ["Magia Record"],
    "월드 플리퍼": ["World Flipper"],
    "어나더 에덴": ["Another Eden"],
    "섀도우버스": ["Shadowverse"],
    "유희왕 마스터 듀얼": ["Yu-Gi-Oh Master Duel"],
    "퍼즐앤드래곤": ["Puzzle and Dragons", "Puzzle Dragons"],
    "드래곤 트래블러": ["Dragon Traveler"],
    "ONE PIECE TREASURE CRUISE": ["원피스 트레저 크루즈"],
    "소울타이드": ["Soul Tide"],
    "에테르 게이저": ["Aether Gazer"],
    "퍼니싱: 그레이 레이븐": ["Punishing Gray Raven"],
    "백야극광": ["Alchemy Stars"],
    "천년전쟁 아이기스": ["Aigis"],
    "이터널 리턴": ["Eternal Return"],
    "이터널 트리": ["Eternal Tree"],
    "아르케랜드": ["Archeland"],
    "브라운더스트": ["Brown Dust"],
    "라스트 오리진": ["Last Origin"],
    "소울워커": ["SoulWorker"],
    "클로저스": ["Closers"],
    "테일즈 오브 크레스토리아": ["Tales of Crestoria"],
    "테일즈 오브 더 레이즈": ["Tales of the Rays"],
    "코노스바": ["KonoSuba"],
    "데이트 어 라이브": ["Date A Live"],
    "마술사 오펜": ["Sorcerous Stabber Orphen"],
    "전생했더니 슬라임이었던 건에 대하여": ["That Time I Got Reincarnated as a Slime"],
    "일곱 개의 대죄: 그랜드 크로스": ["Seven Deadly Sins"],
    "소드 아트 온라인": ["Sword Art Online"],
    "도쿄 구울": ["Tokyo Ghoul"],
    "나루토 모바일": ["Naruto Mobile"],
    "드래곤볼 레전즈": ["Dragon Ball Legends"],
    "블리치 브레이브 소울즈": ["Bleach Brave Souls"],
    "페르소나5: 더 팬텀 X": ["Persona 5 The Phantom X"],
    "메멘토 모리": ["Memento Mori"],
    "이터널 리턴": ["Eternal Return"],
    "아스트라: 나이츠 오브 베더": ["Astra Knights of Veda"],
    "리틀 위치 노베타": ["Little Witch Nobeta"],
    "마스터 오브 나이츠": ["Master of Knights"],
    "메카아라시": ["Mecha BREAK"],
    "아카디아": ["Arcadia"]
}

# ==========================================
# 신규 게임 발견용 검색어
# 넓은 분류를 위해 여러 유형을 검색
# ==========================================

DISCOVERY_WORDS = [
    "서브컬처 게임",
    "애니메이션 RPG",
    "애니풍 RPG",
    "미소녀 RPG",
    "미소년 RPG",
    "캐릭터 수집 RPG",
    "수집형 RPG",
    "일본 애니메이션 게임",
    "애니메이션 모바일 게임",
    "아이돌 육성 게임",
    "아이돌 리듬 게임",
    "애니메이션 리듬 게임",
    "비주얼 노벨 게임",
    "캐릭터 육성 게임",
    "미소녀 수집 게임",
    "미소년 수집 게임",
    "애니메이션 전략 게임",
    "2D 캐릭터 RPG",
    "애니메이션 IP 게임",
    "일본식 RPG",
    "학원 RPG",
    "캐릭터 스토리 RPG"
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


def catalog_match(name):
    key = normalize(name)

    for official_name, aliases in SUBCULTURE_CATALOG.items():
        candidates = [official_name] + aliases

        for candidate in candidates:
            if key == normalize(candidate):
                return official_name

    return None


def add_game(database, store, item, rank=None,
             discovered=False, query=""):

    name = str(item.get("name", "")).strip()

    if not name:
        return

    official_name = catalog_match(name)

    # 등록된 게임은 정식 이름으로 통일
    display_name = official_name or name
    key = normalize(display_name)

    if not key:
        return

    if key not in database:
        database[key] = {
            "name": display_name,
            "developer": "",
            "icon": "",
            "description": "",
            "apple_rank": None,
            "google_rank": None,
            "apple_url": "",
            "google_url": "",
            "subculture": official_name is not None,
            "discovered": False,
            "queries": [],
            "order": len(database)
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
        game["subculture"] = True

    if query and query not in game["queries"]:
        game["queries"].append(query)

    if store == "Apple":
        if item.get("url"):
            game["apple_url"] = item["url"]
        if rank is not None:
            game["apple_rank"] = rank

    elif store == "Google":
        if item.get("url"):
            game["google_url"] = item["url"]
        if rank is not None:
            game["google_rank"] = rank


# ==========================================
# Apple 전체 게임 순위
# ==========================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_apple_chart():

    url = (
        "https://itunes.apple.com/kr/rss/"
        "topfreeapplications/limit=100/genre=6014/json"
    )

    response = requests.get(
        url, headers=HEADERS, timeout=25
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
        "limit": 50
    }

    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=25
    )
    response.raise_for_status()

    results = []

    for item in response.json().get("results", []):

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
# 기존 사용 라이브러리 유지
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
        count=50,
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
        for item in get_apple_chart():
            add_game(
                database,
                "Apple",
                item,
                rank=item["rank"]
            )
    except Exception as e:
        errors.append("Apple 순위: " + str(e))

    # Google 순위
    try:
        for item in get_google_chart():
            add_game(
                database,
                "Google",
                item,
                rank=item["rank"]
            )
    except Exception as e:
        errors.append("Google 순위: " + str(e))

    # 서브컬처 데이터베이스의 등록 게임 검색
    # 대표 게임도 현재 스토어 순위와 별도로 검색
    catalog_searches = list(SUBCULTURE_CATALOG.keys())

    # 신규 게임 검색
    all_searches = DISCOVERY_WORDS + catalog_searches

    progress = st.progress(0)
    status = st.empty()

    total = len(all_searches) * 2
    completed = 0

    for keyword in all_searches:

        # Apple 검색
        try:
            apple_results = search_apple_games(keyword)

            for item in apple_results:
                add_game(
                    database,
                    "Apple",
                    item,
                    discovered=True,
                    query=keyword
                )

        except Exception as e:
            errors.append(
                f"Apple 검색({keyword}): {str(e)}"
            )

        completed += 1
        progress.progress(min(completed / total, 1.0))
        status.caption(
            f"게임 검색 중... {completed}/{total}"
        )

        # Google 검색
        try:
            google_results = search_google_games(keyword)

            for item in google_results:
                add_game(
                    database,
                    "Google",
                    item,
                    discovered=True,
                    query=keyword
                )

        except Exception as e:
            errors.append(
                f"Google 검색({keyword}): {str(e)}"
            )

        completed += 1
        progress.progress(min(completed / total, 1.0))
        status.caption(
            f"게임 검색 중... {completed}/{total}"
        )

        time.sleep(0.05)

    progress.empty()
    status.empty()

    # 검색으로 확인된 게임 중복 제거
    return list(database.values()), errors


# ==========================================
# 스토어별 필터
# ==========================================

def filter_store(games, store):

    if store == "Apple App Store":
        return [
            game for game in games
            if game["apple_url"]
            or game["apple_rank"] is not None
        ]

    if store == "Google Play":
        return [
            game for game in games
            if game["google_url"]
            or game["google_rank"] is not None
        ]

    return games


# ==========================================
# 순위 정렬
# ==========================================

def sort_games(games, store):

    if store == "Apple App Store":
        return sorted(
            games,
            key=lambda g: (
                g["apple_rank"] is None,
                g["apple_rank"] or 9999,
                g["order"]
            )
        )

    if store == "Google Play":
        return sorted(
            games,
            key=lambda g: (
                g["google_rank"] is None,
                g["google_rank"] or 9999,
                g["order"]
            )
        )

    return sorted(
        games,
        key=lambda g: (
            g["apple_rank"] is None
            and g["google_rank"] is None,
            min(
                g["apple_rank"] or 9999,
                g["google_rank"] or 9999
            ),
            g["order"]
        )
    )


# ==========================================
# 게임 출력
# ==========================================

def show_games(games, store, is_subculture=False):

    if not games:
        st.info("표시할 게임이 없습니다.")
        return

    games = sort_games(games, store)

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

            if is_subculture:
                if game["apple_rank"] is None and game["google_rank"] is None:
                    st.caption("✨ 서브컬처 · 스토어 순위 정보 없음")
                else:
                    st.caption("✨ 서브컬처 게임")

            if store == "통합 순위":

                apple = game["apple_rank"]
                google = game["google_rank"]

                a = f"Apple {apple}위" if apple else "Apple 순위 없음"
                g = f"Google {google}위" if google else "Google 순위 없음"

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

                if game["apple_rank"] is not None:
                    st.caption(
                        f"전체 애플 무료 게임 순위: {game['apple_rank']}위"
                    )

                if game["apple_url"]:
                    st.markdown(
                        f"[Apple App Store]({game['apple_url']})"
                    )

            else:

                st.caption(game["developer"])

                if game["google_rank"] is not None:
                    st.caption(
                        f"전체 구글 무료 게임 순위: {game['google_rank']}위"
                    )

                if game["google_url"]:
                    st.markdown(
                        f"[Google Play]({game['google_url']})"
                    )

            with st.expander("게임 정보"):

                if game["developer"]:
                    st.write("개발사:", game["developer"])

                if game["description"]:
                    st.write(game["description"][:500])

                if game["queries"]:
                    st.caption(
                        "발견 검색어: " + ", ".join(game["queries"][:5])
                    )

        st.divider()


# ==========================================
# 사이드바
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
    st.session_state["subculture_count"] = PAGE_SIZE
    st.rerun()


# ==========================================
# 데이터 수집
# ==========================================

with st.spinner(
    "전체 게임과 서브컬처 게임을 검색하고 있습니다..."
):

    all_games, collection_errors = collect_games()


# ==========================================
# 오류 표시
# ==========================================

for error in collection_errors:
    st.warning(error)


# ==========================================
# 탭 구성
# ==========================================

all_tab, sub_tab, pending_tab = st.tabs([
    "🌏 전체 게임",
    "✨ 서브컬처",
    "🔎 분류 정보"
])


# ==========================================
# 전체 게임 탭
# ==========================================

with all_tab:

    st.subheader("🌏 전체 모바일 게임")

    st.caption(
        "기존 구글 플레이와 애플 앱스토어 무료 게임 순위입니다."
    )

    selected = filter_store(
        [
            g for g in all_games
            if g["apple_rank"] is not None
            or g["google_rank"] is not None
        ],
        store_choice
    )

    st.metric("전체 게임 수", len(selected))

    show_games(selected, store_choice)


# ==========================================
# 서브컬처 탭
# ==========================================

with sub_tab:

    st.subheader("✨ 서브컬처 게임")

    st.caption(
        "대표적인 서브컬처 게임과 넓은 기준으로 검색된 게임을 함께 표시합니다."
    )

    subculture_games = [
        g for g in all_games
        if g["subculture"]
    ]

    selected = filter_store(
        subculture_games,
        store_choice
    )

    st.metric(
        "수집된 서브컬처 게임",
        len(selected)
    )

    if "subculture_count" not in st.session_state:
        st.session_state["subculture_count"] = PAGE_SIZE

    visible_count = st.session_state["subculture_count"]

    visible_games = selected[:visible_count]

    show_games(
        visible_games,
        store_choice,
        is_subculture=True
    )

    if visible_count < len(selected):

        st.caption(
            f"{len(visible_games)} / {len(selected)}개 표시 중"
        )

        if st.button(
            "더보기 +30개",
            use_container_width=True
        ):
            st.session_state["subculture_count"] += PAGE_SIZE
            st.rerun()

    else:

        if selected:
            st.success("수집된 게임을 모두 표시했습니다.")


# ==========================================
# 분류 정보 탭
# ==========================================

with pending_tab:

    st.subheader("🔎 분류 및 검색 정보")

    st.write(
        "이 탭은 넓은 검색 기준으로 발견된 게임을 확인하는 곳입니다."
    )

    st.write(
        f"등록된 대표 게임: {len(SUBCULTURE_CATALOG)}개"
    )

    st.write(
        f"검색에 사용한 검색어: {len(DISCOVERY_WORDS)}개"
    )

    st.write(
        f"수집한 전체 게임: {len(all_games)}개"
    )

    st.write(
        f"서브컬처로 분류된 게임: "
        f"{sum(1 for g in all_games if g['subculture'])}개"
    )

    st.info(
        "검색어를 통해 발견된 게임은 넓은 서브컬처 후보로 분류됩니다. "
        "따라서 일부 일반 게임이 포함될 수 있습니다."
    )


# ==========================================
# 하단 안내
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    f"전체 수집 게임: {len(all_games)}개"
)

st.sidebar.caption(
    f"서브컬처 후보: "
    f"{sum(1 for g in all_games if g['subculture'])}개"
)

st.sidebar.caption(
    "순위 데이터: 약 30분 캐시"
)

st.sidebar.caption(
    "검색 데이터: 약 24시간 캐시"
)

st.sidebar.caption(
    "서브컬처 분류는 넓은 검색 기준을 사용합니다."
)
