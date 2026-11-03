
import re
import time
import requests
import streamlit as st

st.set_page_config(
    page_title="모바일 게임 순위",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 모바일 게임 순위")
st.caption("한국 모바일 게임 순위 및 서브컬처 게임 비교")

PAGE_SIZE = 30
ICON_BATCH_SIZE = 5
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ==========================================
# 서브컬처 게임 데이터베이스
# ==========================================

SUBCULTURE_CATALOG = [
    ("승리의 여신: 니케", ["니케", "NIKKE"], "core"),
    ("블루 아카이브", ["Blue Archive"], "core"),
    ("원신", ["Genshin Impact"], "core"),
    ("붕괴: 스타레일", ["Honkai Star Rail"], "core"),
    ("붕괴3rd", ["Honkai Impact 3rd"], "core"),
    ("젠레스 존 제로", ["Zenless Zone Zero", "ZZZ"], "core"),
    ("명조: 워더링 웨이브", ["Wuthering Waves"], "core"),
    ("소녀전선", ["Girls Frontline"], "core"),
    ("소녀전선2: 망명", ["Girls Frontline 2"], "core"),
    ("명일방주", ["Arknights"], "core"),
    ("명일방주: 엔드필드", ["Arknights Endfield"], "core"),
    ("림버스 컴퍼니", ["Limbus Company"], "core"),
    ("트릭컬 리바이브", ["Trickcal", "Trickcal Revive"], "core"),
    ("브라운더스트2", ["Brown Dust 2"], "core"),
    ("에픽세븐", ["Epic Seven"], "core"),
    ("우마무스메 프리티 더비", ["Uma Musume"], "core"),
    ("페이트/그랜드 오더", ["Fate Grand Order", "FGO"], "core"),
    ("리버스: 1999", ["Reverse 1999"], "core"),
    ("벽람항로", ["Azur Lane"], "core"),
    ("뉴럴 클라우드", ["Neural Cloud"], "core"),
    ("무기미도", ["Path to Nowhere"], "core"),
    ("헤븐 번즈 레드", ["Heaven Burns Red"], "core"),
    ("카오스 제로 나이트메어", ["Chaos Zero Nightmare"], "core"),
    ("아우터플레인", ["Outerplane"], "core"),
    ("카운터사이드", ["CounterSide"], "core"),
    ("에버소울", ["Eversoul"], "core"),
    ("퍼니싱: 그레이 레이븐", ["Punishing Gray Raven"], "core"),
    ("에테르 게이저", ["Aether Gazer"], "core"),
    ("백야극광", ["Alchemy Stars"], "core"),
    ("메멘토 모리", ["Memento Mori"], "core"),
    ("라스트 오리진", ["Last Origin"], "core"),
    ("아르케랜드", ["Archeland"], "core"),
    ("소울타이드", ["Soul Tide"], "core"),
    ("마스터 오브 나이츠", ["Master of Knights"], "core"),
    ("로스트 소드", ["Lost Sword"], "core"),
    ("아스트라: 나이츠 오브 베다", ["Astra Knights of Veda"], "core"),
    ("소드 오브 콘발라리아", ["Sword of Convallaria"], "core"),
    ("프린세스 커넥트! Re:Dive", ["Princess Connect", "프리코네"], "core"),
    ("어나더 에덴", ["Another Eden"], "core"),
    ("월드 플리퍼", ["World Flipper"], "core"),

    ("프로젝트 세카이", ["Project Sekai", "프로세카"], "broad"),
    ("앙상블 스타즈!!", ["Ensemble Stars", "앙스타"], "broad"),
    ("뱅드림! 걸즈 밴드 파티!", ["BanG Dream", "뱅드림"], "broad"),
    ("D4DJ Groovy Mix", ["D4DJ"], "broad"),
    ("아이돌마스터 신데렐라 걸즈", ["Cinderella Girls"], "broad"),
    ("아이돌마스터 밀리언 라이브", ["Million Live"], "broad"),
    ("아이돌마스터 샤이니 컬러즈", ["Shiny Colors"], "broad"),
    ("학원 아이돌마스터", ["Gakuen Idolmaster"], "broad"),
    ("러브라이브!", ["Love Live"], "broad"),

    ("일곱 개의 대죄: 그랜드 크로스", ["Seven Deadly Sins"], "broad"),
    ("소드 아트 온라인: 인테그럴 팩터", ["Sword Art Online Integral Factor"], "broad"),
    ("드래곤볼 레전즈", ["Dragon Ball Legends"], "broad"),
    ("블리치 브레이브 소울즈", ["Bleach Brave Souls"], "broad"),
    ("주술회전 팬텀 퍼레이드", ["Jujutsu Kaisen Phantom Parade"], "broad"),
    ("원피스 트레저 크루즈", ["One Piece Treasure Cruise"], "broad"),
    ("전생했더니 슬라임이었던 건에 대하여", ["That Time I Got Reincarnated as a Slime"], "broad"),
    ("코노스바", ["KonoSuba"], "broad"),
    ("데이트 어 라이브", ["Date A Live"], "broad"),
    ("던전에서 만남을 추구하면 안 되는 걸까", ["DanMachi"], "broad"),
    ("퍼즐앤드래곤", ["Puzzle Dragons"], "broad"),
    ("섀도우버스", ["Shadowverse"], "broad"),
    ("유희왕 마스터 듀얼", ["Yu-Gi-Oh Master Duel"], "broad"),
    ("마기아 레코드", ["Magia Record"], "broad"),
    ("그랑블루 판타지", ["Granblue Fantasy"], "broad"),
    ("아이돌리쉬 세븐", ["IDOLiSH7"], "broad"),
]

REVIEW_GAMES = [
    "가디언 테일즈",
    "그랑사가",
    "세븐나이츠",
    "드래곤 트래블러",
    "이환",
    "아즈르 프로밀리아",
    "ANANTA",
    "실버 팰리스",
    "리미트 제로 브레이커스",
    "테르비스",
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


def get_catalog_match(name):
    target = normalize(name)

    for official_name, aliases, category in SUBCULTURE_CATALOG:
        for candidate in [official_name] + aliases:
            if target == normalize(candidate):
                return official_name

    return None


def new_game(name):
    return {
        "name": name,
        "developer": "",
        "icon": "",
        "description": "",
        "apple_rank": None,
        "google_rank": None,
        "apple_url": "",
        "google_url": "",
    }


# ==========================================
# Apple 순위
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

    entries = response.json().get("feed", {}).get("entry", [])

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
# Google 순위
# ==========================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_google_chart():
    from gplay_scraper import GPlayScraper

    scraper = GPlayScraper()

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
# 게임별 아이콘 검색
#
# 검색 결과 중 이름이 일치하는 게임만 채택
# 한 번 검색한 결과는 캐시
# ==========================================

@st.cache_data(ttl=604800, show_spinner=False)
def get_game_icon(game_name):

    from gplay_scraper import GPlayScraper

    scraper = GPlayScraper()

    results = scraper.search_analyze(
        game_name,
        count=15,
        lang="ko",
        country="kr"
    )

    target = normalize(game_name)

    aliases = []

    for official_name, game_aliases, category in SUBCULTURE_CATALOG:
        if normalize(official_name) == target:
            aliases = game_aliases
            break

    accepted_names = {
        target,
        *[normalize(alias) for alias in aliases]
    }

    # 이름이 정확하게 일치하는 결과 우선
    for item in results:
        result_name = normalize(item.get("title", ""))

        if result_name in accepted_names:
            return item.get("icon", "")

    # 정확히 일치하지 않으면 긴 이름의 포함 관계만 허용
    for item in results:
        result_name = normalize(item.get("title", ""))

        if len(target) >= 5 and (
            target in result_name or result_name in target
        ):
            return item.get("icon", "")

    return ""


# ==========================================
# 전체 데이터 수집
# ==========================================

def collect_games():

    database = {}
    errors = []

    # 서브컬처 카탈로그 우선 등록
    for name, aliases, category in SUBCULTURE_CATALOG:
        database[normalize(name)] = new_game(name)

    # Apple 순위
    try:
        for item in get_apple_chart():

            name = item["name"]
            if not name:
                continue

            official_name = get_catalog_match(name)
            display_name = official_name or name
            key = normalize(display_name)

            if key not in database:
                database[key] = new_game(display_name)

            game = database[key]
            game["apple_rank"] = item["rank"]
            game["apple_url"] = item["url"]
            game["icon"] = item["icon"] or game["icon"]
            game["developer"] = (
                item["developer"] or game["developer"]
            )

    except Exception as e:
        errors.append("Apple 순위 오류: " + str(e))

    # Google 순위
    try:
        for item in get_google_chart():

            name = item["name"]
            if not name:
                continue

            official_name = get_catalog_match(name)
            display_name = official_name or name
            key = normalize(display_name)

            if key not in database:
                database[key] = new_game(display_name)

            game = database[key]
            game["google_rank"] = item["rank"]
            game["google_url"] = item["url"]
            game["icon"] = item["icon"] or game["icon"]
            game["developer"] = (
                item["developer"] or game["developer"]
            )
            game["description"] = (
                item.get("description", "")
                or game["description"]
            )

    except Exception as e:
        errors.append("Google 순위 오류: " + str(e))

    return list(database.values()), errors


# ==========================================
# 순위 필터
# ==========================================

def filter_store(games, store):

    if store == "Apple App Store":
        return [
            g for g in games
            if g["apple_rank"] is not None
        ]

    if store == "Google Play":
        return [
            g for g in games
            if g["google_rank"] is not None
        ]

    return games


# ==========================================
# 정렬
# ==========================================

def sort_games(games, store):

    if store == "Apple App Store":
        return sorted(
            games,
            key=lambda g: (
                g["apple_rank"] is None,
                g["apple_rank"] or 9999
            )
        )

    if store == "Google Play":
        return sorted(
            games,
            key=lambda g: (
                g["google_rank"] is None,
                g["google_rank"] or 9999
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
            )
        )
    )


# ==========================================
# 게임 표시
# ==========================================

def show_games(games, store, subculture=False):

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
                st.markdown(
                    "<div style='width:75px;height:75px;"
                    "display:flex;align-items:center;"
                    "justify-content:center;"
                    "background:#333;border-radius:12px;"
                    "font-size:30px'>🎮</div>",
                    unsafe_allow_html=True
                )

        with col2:

            st.markdown(
                f"**{index}. {game['name']}**"
            )

            if subculture:
                if (
                    game["apple_rank"] is None
                    and game["google_rank"] is None
                ):
                    st.caption(
                        "✨ 서브컬처 · 스토어 순위 정보 없음"
                    )
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

                if game["apple_rank"] is not None:
                    st.caption(
                        f"애플 무료 게임 {game['apple_rank']}위"
                    )

                if game["apple_url"]:
                    st.markdown(
                        f"[Apple App Store]({game['apple_url']})"
                    )

            else:

                if game["google_rank"] is not None:
                    st.caption(
                        f"구글 무료 게임 {game['google_rank']}위"
                    )

                if game["google_url"]:
                    st.markdown(
                        f"[Google Play]({game['google_url']})"
                    )

            if game["developer"]:
                st.caption("개발사: " + game["developer"])

            with st.expander("게임 정보"):
                if game["description"]:
                    st.write(game["description"][:500])
                else:
                    st.write("상세 설명 정보가 없습니다.")

        st.divider()


# ==========================================
# 사이드바
# ==========================================

st.sidebar.header("⚙️ 설정")

store_choice = st.sidebar.selectbox(
    "스토어 선택",
    ["통합 순위", "Google Play", "Apple App Store"]
)

if st.sidebar.button("🔄 순위 새로고침"):
    get_apple_chart.clear()
    get_google_chart.clear()
    st.session_state["subculture_count"] = PAGE_SIZE
    st.rerun()


# ==========================================
# 데이터 불러오기
# ==========================================

with st.spinner("게임 순위를 불러오는 중입니다..."):
    all_games, errors = collect_games()

for error in errors:
    st.warning(error)


# ==========================================
# 서브컬처 게임 목록 구성
# ==========================================

subculture_games = []

for name, aliases, category in SUBCULTURE_CATALOG:

    key = normalize(name)

    game = next(
        (
            g for g in all_games
            if normalize(g["name"]) == key
        ),
        None
    )

    if game:
        subculture_games.append(game)


# ==========================================
# 아이콘이 없는 게임 목록
# ==========================================

missing_icons = [
    game for game in subculture_games
    if not game["icon"]
]


# ==========================================
# 탭 구성
# ==========================================

all_tab, sub_tab, review_tab = st.tabs([
    "🌏 전체 게임",
    "✨ 서브컬처",
    "🔎 분류 검토"
])


# ==========================================
# 전체 게임 탭
# ==========================================

with all_tab:

    st.subheader("🌏 전체 모바일 게임")

    chart_games = [
        game for game in all_games
        if (
            game["apple_rank"] is not None
            or game["google_rank"] is not None
        )
    ]

    selected = filter_store(
        chart_games,
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
        "캐릭터 수집·육성, 애니메이션 IP, 캐릭터 중심 RPG, "
        "아이돌·리듬 게임 등을 포함합니다."
    )

    selected = filter_store(
        subculture_games,
        store_choice
    )

    st.metric(
        "서브컬처 게임 데이터베이스",
        len(subculture_games)
    )

    # 아이콘 검색 기능
    st.divider()
    st.subheader("🖼️ 게임 아이콘")

    st.write(
        f"아이콘이 없는 게임: {len(missing_icons)}개"
    )

    if missing_icons:

        if "icon_cursor" not in st.session_state:
            st.session_state["icon_cursor"] = 0

        cursor = st.session_state["icon_cursor"]

        if cursor >= len(missing_icons):
            cursor = 0
            st.session_state["icon_cursor"] = 0

        remaining = len(missing_icons) - cursor

        st.caption(
            f"아이콘 검색 진행: "
            f"{min(cursor, len(missing_icons))} / "
            f"{len(missing_icons)}"
        )

        if st.button(
            f"아이콘 {min(ICON_BATCH_SIZE, remaining)}개 가져오기",
            use_container_width=True
        ):

            batch = missing_icons[
                cursor:cursor + ICON_BATCH_SIZE
            ]

            progress = st.progress(0)
            status = st.empty()

            for i, game in enumerate(batch):

                status.caption(
                    f"아이콘 검색 중: {game['name']}"
                )

                try:
                    icon_url = get_game_icon(game["name"])

                    if icon_url:
                        game["icon"] = icon_url

                except Exception as e:
                    st.warning(
                        f"{game['name']} 아이콘 검색 실패: {e}"
                    )

                progress.progress((i + 1) / len(batch))

                # 요청을 한꺼번에 보내지 않도록 간격 유지
                time.sleep(1)

            st.session_state["icon_cursor"] += len(batch)

            progress.empty()
            status.empty()

            st.rerun()

    else:
        st.success("모든 게임에 아이콘이 있습니다.")

    st.divider()

    # 더보기
    if "subculture_count" not in st.session_state:
        st.session_state["subculture_count"] = PAGE_SIZE

    visible_count = st.session_state["subculture_count"]

    visible_games = selected[:visible_count]

    show_games(
        visible_games,
        store_choice,
        subculture=True
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

    elif selected:
        st.success("게임 목록을 모두 표시했습니다.")


# ==========================================
# 분류 검토 탭
# ==========================================

with review_tab:

    st.subheader("🔎 분류 검토 대상")

    st.info(
        "아직 서브컬처 게임으로 확정하지 않은 게임입니다."
    )

    for name in REVIEW_GAMES:
        st.write("• " + name)

    st.divider()

    st.markdown(
        """
        **포함 기준**
        - 캐릭터 수집 및 육성이 핵심인 게임
        - 애니메이션풍 캐릭터 중심 RPG
        - 미소녀·미소년 중심 게임
        - 캐릭터 중심 스토리 게임
        - 애니메이션 IP 기반 캐릭터 게임
        - 아이돌 및 캐릭터 중심 리듬 게임

        **제외 기준**
        - 일반 생존·경영·퍼즐 게임
        - 로블록스와 같은 게임 플랫폼
        - 단순히 애니메이션풍 그래픽만 사용하는 게임
        - 서브컬처 요소가 핵심이 아닌 일반 게임
        """
    )


# ==========================================
# 하단 정보
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    f"전체 게임: {len(all_games)}개"
)

st.sidebar.caption(
    f"서브컬처 게임: {len(subculture_games)}개"
)

st.sidebar.caption(
    f"아이콘 미등록: {len(missing_icons)}개"
)

st.sidebar.caption(
    "순위 데이터 캐시: 30분"
)

st.sidebar.caption(
    "아이콘 검색 캐시: 7일"
)
