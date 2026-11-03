
import re
import time
import requests
import streamlit as st


# ---------------------------------------
# 기본 설정
# ---------------------------------------

st.set_page_config(
    page_title="모바일 게임 순위",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 모바일 게임 순위")
st.caption("대한민국 Google Play와 Apple App Store의 무료 게임 순위")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}


# ---------------------------------------
# 게임 이름 비교용
# ---------------------------------------

def normalize_name(name):
    return re.sub(r"[\W_]+", "", str(name).lower())


# ---------------------------------------
# Apple App Store 데이터
# ---------------------------------------

@st.cache_data(ttl=1800, show_spinner=False)
def get_apple_games(limit):

    url = (
        "https://itunes.apple.com/kr/rss/"
        f"topfreeapplications/limit={limit}/genre=6014/json"
    )

    last_error = None

    for attempt in range(3):
        try:
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

            if not entries:
                raise ValueError("Apple에서 게임 목록을 받지 못했습니다.")

            games = []

            for rank, item in enumerate(entries, start=1):

                name = item.get("im:name", {}).get("label", "")
                developer = item.get("im:artist", {}).get("label", "")

                images = item.get("im:image", [])
                icon = images[-1].get("label", "") if images else ""

                app_id = item.get("id", {})
                app_url = app_id.get("label", "")

                if not name:
                    continue

                games.append({
                    "rank": rank,
                    "name": name,
                    "developer": developer,
                    "icon": icon,
                    "url": app_url,
                    "store": "Apple"
                })

            return games, None

        except Exception as e:
            last_error = str(e)
            time.sleep(1)

    return [], last_error


# ---------------------------------------
# Google Play 데이터
# ---------------------------------------

@st.cache_data(ttl=1800, show_spinner=False)
def get_google_games(limit):

    try:
        from gplay_scraper import GPlayScraper

        scraper = GPlayScraper()

        result = scraper.list_analyze(
            "TOP_FREE",
            "GAME",
            count=limit,
            lang="ko",
            country="kr"
        )

        if not result:
            raise ValueError("Google Play에서 게임 목록을 받지 못했습니다.")

        games = []

        for rank, item in enumerate(result, start=1):

            name = item.get("title", "")

            if not name:
                continue

            app_id = item.get("appId", "")

            app_url = item.get(
                "url",
                f"https://play.google.com/store/apps/details?id={app_id}"
            )

            games.append({
                "rank": rank,
                "name": name,
                "developer": item.get("developer", ""),
                "icon": item.get("icon", ""),
                "url": app_url,
                "store": "Google Play"
            })

        return games, None

    except Exception as e:
        return [], str(e)


# ---------------------------------------
# 통합 순위 계산
# ---------------------------------------

def make_combined_ranking(apple_games, google_games):

    combined = {}

    for store_games, store_name in [
        (apple_games, "Apple"),
        (google_games, "Google")
    ]:

        for game in store_games:

            key = normalize_name(game["name"])

            if not key:
                continue

            if key not in combined:
                combined[key] = {
                    "name": game["name"],
                    "developer": game["developer"],
                    "icon": game["icon"],
                    "apple_rank": None,
                    "google_rank": None,
                    "apple_url": "",
                    "google_url": "",
                    "score": 0
                }

            target = combined[key]

            if not target["icon"] and game["icon"]:
                target["icon"] = game["icon"]

            if store_name == "Apple":
                target["apple_rank"] = game["rank"]
                target["apple_url"] = game["url"]
                target["score"] += 101 - game["rank"]

            else:
                target["google_rank"] = game["rank"]
                target["google_url"] = game["url"]
                target["score"] += 101 - game["rank"]

    result = list(combined.values())

    result.sort(
        key=lambda x: (
            -x["score"],
            min(
                x["apple_rank"] or 999,
                x["google_rank"] or 999
            )
        )
    )

    return result


# ---------------------------------------
# 게임 목록 화면
# ---------------------------------------

def show_games(games, store_type):

    if not games:
        st.warning("표시할 게임이 없습니다.")
        return

    for index, game in enumerate(games, start=1):

        col1, col2 = st.columns([1, 6])

        with col1:
            if game.get("icon"):
                try:
                    st.image(game["icon"], width=75)
                except Exception:
                    st.write("🎮")
            else:
                st.write("🎮")

        with col2:

            st.markdown(f"**{index}위. {game['name']}**")

            if store_type == "통합":
                apple_rank = game["apple_rank"]
                google_rank = game["google_rank"]

                apple_text = (
                    f"Apple {apple_rank}위"
                    if apple_rank else "Apple 순위 없음"
                )

                google_text = (
                    f"Google {google_rank}위"
                    if google_rank else "Google 순위 없음"
                )

                st.caption(f"{apple_text} · {google_text}")

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

            else:
                st.caption(game.get("developer", ""))

                if game.get("url"):
                    st.markdown(f"[스토어에서 보기]({game['url']})")

        st.divider()


# ---------------------------------------
# 사이드바
# ---------------------------------------

st.sidebar.header("순위 설정")

store_choice = st.sidebar.selectbox(
    "순위 종류",
    [
        "통합 순위",
        "Google Play",
        "Apple App Store"
    ]
)

limit = st.sidebar.slider(
    "가져올 게임 수",
    min_value=10,
    max_value=100,
    value=50,
    step=10
)

if st.sidebar.button("🔄 순위 새로고침"):
    st.cache_data.clear()
    st.rerun()


# ---------------------------------------
# 데이터 가져오기
# ---------------------------------------

with st.spinner("게임 순위를 불러오는 중입니다..."):

    apple_games, apple_error = get_apple_games(limit)
    google_games, google_error = get_google_games(limit)


# ---------------------------------------
# 오류 표시
# ---------------------------------------

if apple_error:
    st.error(f"Apple App Store 오류: {apple_error}")

if google_error:
    st.error(f"Google Play 오류: {google_error}")


# ---------------------------------------
# 순위 표시
# ---------------------------------------

if store_choice == "Apple App Store":

    st.subheader("🍎 Apple App Store 무료 게임 순위")

    if apple_games:
        show_games(apple_games, "Apple")

elif store_choice == "Google Play":

    st.subheader("🤖 Google Play 무료 게임 순위")

    if google_games:
        show_games(google_games, "Google")

else:

    st.subheader("🌏 모바일 게임 통합 순위")

    if apple_games or google_games:

        combined_games = make_combined_ranking(
            apple_games,
            google_games
        )

        show_games(combined_games, "통합")

    else:
        st.warning("두 스토어에서 모두 데이터를 가져오지 못했습니다.")


# ---------------------------------------
# 안내
# ---------------------------------------

st.sidebar.divider()
st.sidebar.caption(
    "데이터는 각 스토어의 무료 게임 차트를 기준으로 합니다."
)
st.sidebar.caption(
    "통합 순위는 각 스토어 순위에 점수를 부여해 계산한 참고 순위입니다."
)
st.sidebar.caption(
    "데이터는 약 30분 동안 캐시됩니다."
)
