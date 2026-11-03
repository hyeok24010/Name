
import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="오늘의 게임",
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
.game-card {
    background: #1c2638;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
}
.game-card img {
    border-radius: 15px;
}
.rank {
    font-size: 25px;
    font-weight: bold;
    color: #8eb7ff;
}
.game-name {
    font-size: 19px;
    font-weight: bold;
}
.description {
    color: #b8c3d6;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 국가 설정
# -------------------------
COUNTRIES = {
    "대한민국": "kr",
    "미국": "us",
    "일본": "jp",
    "영국": "gb"
}

# -------------------------
# 앱스토어 데이터 가져오기
# -------------------------
@st.cache_data(ttl=3600)
def get_games(country, limit=50):

    url = (
        f"https://itunes.apple.com/{country}/rss/"
        f"topfreeapplications/limit={limit}/genre=6014/json"
    )

    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    data = response.json()
    entries = data.get("feed", {}).get("entry", [])

    if isinstance(entries, dict):
        entries = [entries]

    games = []

    for rank, entry in enumerate(entries, 1):
        app_id = entry.get("id", {}).get(
            "attributes", {}
        ).get("im:id")

        if not app_id:
            continue

        games.append({
            "rank": rank,
            "id": app_id,
            "name": entry.get("im:name", {}).get(
                "label", "이름 없음"
            ),
            "developer": entry.get("im:artist", {}).get(
                "label", "정보 없음"
            ),
            "icon": entry.get("im:image", [{}])[-1].get(
                "label", ""
            ),
            "url": entry.get("id", {}).get("label", "")
        })

    # 상세 정보 가져오기
    if games:
        ids = ",".join(game["id"] for game in games)

        lookup_url = (
            f"https://itunes.apple.com/lookup"
            f"?id={ids}&country={country}"
        )

        detail_response = requests.get(
            lookup_url,
            timeout=20
        )
        detail_response.raise_for_status()

        details = detail_response.json().get(
            "results", []
        )

        detail_map = {
            str(item["trackId"]): item
            for item in details
        }

        for game in games:
            detail = detail_map.get(game["id"], {})

            game["description"] = detail.get(
                "description", "설명이 없습니다."
            )
            game["icon"] = detail.get(
                "artworkUrl512", game["icon"]
            )
            game["genre"] = detail.get(
                "primaryGenreName", "게임"
            )
            game["rating"] = detail.get(
                "averageUserRating", 0
            )
            game["rating_count"] = detail.get(
                "userRatingCount", 0
            )
            game["url"] = detail.get(
                "trackViewUrl", game["url"]
            )

    return games


# -------------------------
# 상단 화면
# -------------------------
st.title("🎮 오늘의 게임")
st.caption("APPLE APP STORE · TODAY'S TOP GAMES")

today = datetime.now(
    ZoneInfo("Asia/Seoul")
).strftime("%Y년 %m월 %d일")

st.write(f"📅 {today}")

col1, col2 = st.columns([3, 1])

with col1:
    country_name = st.selectbox(
        "앱스토어 국가",
        list(COUNTRIES.keys())
    )

with col2:
    st.write("")
    st.write("")
    refresh = st.button(
        "🔄 새로고침",
        use_container_width=True
    )

if refresh:
    get_games.clear()

# -------------------------
# 게임 데이터 출력
# -------------------------
try:
    with st.spinner("인기 게임을 불러오는 중..."):

        games = get_games(
            COUNTRIES[country_name]
        )

    if not games:
        st.warning("게임 정보를 찾지 못했습니다.")

    else:
        st.success(
            f"{len(games)}개의 인기 게임을 불러왔습니다."
        )

        # 오늘의 추천 게임
        st.subheader("⭐ 오늘의 인기 게임 TOP 5")

        featured = st.columns(5)

        for i, game in enumerate(games[:5]):
            with featured[i]:
                if game["icon"]:
                    st.image(
                        game["icon"],
                        use_container_width=True
                    )

                st.markdown(f"**{i+1}위**")
                st.write(game["name"])
                st.caption(game["genre"])

        st.divider()

        # 검색
        st.subheader("🔍 게임 검색")

        keyword = st.text_input(
            "게임 이름을 입력하세요",
            placeholder="예: Roblox"
        )

        # 전체 순위
        st.subheader("🏆 인기 게임 순위")

        filtered = [
            game for game in games
            if keyword.lower() in game["name"].lower()
        ]

        if not filtered:
            st.info("검색 결과가 없습니다.")

        for game in filtered:

            with st.container(border=True):

                left, right = st.columns(
                    [1, 4]
                )

                with left:
                    if game["icon"]:
                        st.image(
                            game["icon"],
                            use_container_width=True
                        )

                with right:
                    st.markdown(
                        f"### #{game['rank']} {game['name']}"
                    )

                    st.caption(
                        f"제작사: {game['developer']}"
                    )

                    st.write(
                        f"장르: {game['genre']} "
                        f"| ⭐ 평점: {game['rating']:.1f}"
                        if game["rating"]
                        else f"장르: {game['genre']} "
                        "| ⭐ 평점 정보 없음"
                    )

                    st.caption(
                        f"평가 수: {game['rating_count']:,}"
                    )

                    with st.expander("게임 설명 보기"):
                        st.write(game["description"])

                    st.link_button(
                        "앱스토어에서 보기 ↗",
                        game["url"]
                    )

        st.divider()

        st.caption(
            "데이터 출처: Apple App Store 공개 차트 및 iTunes Lookup API"
        )
        st.caption(
            "순위는 애플 차트 기준이며 실제 게임의 품질이나 "
            "다운로드 수를 직접 나타내지는 않습니다."
        )

except requests.RequestException as e:
    st.error("앱스토어 데이터를 가져오지 못했습니다.")
    st.caption(str(e))

except Exception as e:
    st.error("데이터 처리 중 오류가 발생했습니다.")
    st.caption(str(e))
