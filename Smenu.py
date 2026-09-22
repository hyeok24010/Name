import streamlit as st
import requests
from datetime import date, timedelta
import re

# -----------------------------------
# 기본 설정
# -----------------------------------

st.set_page_config(
    page_title="보라고등학교 급식",
    page_icon="🍱",
    layout="centered"
)

# 보라고등학교 정보
ATPT_OFCDC_SC_CODE = "J10"
SD_SCHUL_CODE = "7530882"

st.title("🍱 보라고등학교 급식")
st.caption("NEIS 교육정보 개방 API를 이용한 급식 메뉴 조회")

# -----------------------------------
# NEIS API 호출 함수
# -----------------------------------

def get_meal_data(start_date, end_date):
    """
    NEIS 급식식단정보 API에서
    지정한 날짜 범위의 급식 정보를 가져옵니다.
    """

    api_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"

    params = {
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "ATPT_OFCDC_SC_CODE": ATPT_OFCDC_SC_CODE,
        "SD_SCHUL_CODE": SD_SCHUL_CODE,
        "MLSV_FROM_YMD": start_date.strftime("%Y%m%d"),
        "MLSV_TO_YMD": end_date.strftime("%Y%m%d")
    }

    try:
        response = requests.get(
            api_url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # 데이터가 없는 경우
        if "mealServiceDietInfo" not in data:
            return []

        rows = data["mealServiceDietInfo"][1]["row"]

        return rows

    except requests.exceptions.RequestException as e:
        st.error(f"NEIS API 연결 오류: {e}")
        return []

    except (KeyError, IndexError, TypeError):
        return []


# -----------------------------------
# 메뉴 문자열 정리
# -----------------------------------

def clean_menu(menu_text):
    """
    NEIS에서 제공하는 <br/> 태그를
    Streamlit에서 보기 좋은 형태로 변경합니다.
    """

    if not menu_text:
        return []

    # <br/> 등을 줄바꿈으로 변경
    menu_text = re.sub(
        r"<br\s*/?>",
        "\n",
        menu_text,
        flags=re.IGNORECASE
    )

    # 알레르기 번호 제거
    menu_text = re.sub(
        r"\d+(?:\.\d+)*",
        "",
        menu_text
    )

    # 빈 줄 제거
    menus = []

    for item in menu_text.split("\n"):
        item = item.strip()

        if item:
            menus.append(item)

    return menus


# -----------------------------------
# 날짜 선택
# -----------------------------------

st.subheader("📅 급식 날짜")

selected_date = st.date_input(
    "날짜를 선택하세요",
    value=date.today()
)

# -----------------------------------
# 조회
# -----------------------------------

if st.button("🍴 급식 조회", use_container_width=True):

    with st.spinner("급식 정보를 가져오는 중..."):

        meals = get_meal_data(
            selected_date,
            selected_date
        )

    if not meals:
        st.warning(
            "선택한 날짜에는 등록된 급식 정보가 없습니다."
        )

    else:

        # 날짜가 여러 개일 가능성을 고려해서 정렬
        meals = sorted(
            meals,
            key=lambda x: (
                x.get("MLSV_YMD", ""),
                x.get("MMEAL_SC_CODE", "")
            )
        )

        st.success(
            f"{selected_date.strftime('%Y년 %m월 %d일')} 급식"
        )

        for meal in meals:

            meal_name = meal.get(
                "MMEAL_SC_NM",
                "급식"
            )

            menu = clean_menu(
                meal.get("DDISH_NM", "")
            )

            calorie = meal.get(
                "CAL_INFO",
                ""
            )

            nutrition = meal.get(
                "NTR_INFO",
                ""
            )

            # -----------------------------------
            # 급식 카드
            # -----------------------------------

            st.markdown(
                f"## 🍽️ {meal_name}"
            )

            if menu:

                for food in menu:
                    st.write(f"• {food}")

            else:
                st.write("등록된 메뉴가 없습니다.")

            if calorie:
                st.info(f"🔥 열량: {calorie}")

            # 영양정보
            if nutrition:

                with st.expander("🥗 영양정보"):
                    nutrition_items = nutrition.split("<br/>")

                    for item in nutrition_items:
                        item = item.strip()

                        if item:
                            st.write(f"• {item}")

            st.divider()


# -----------------------------------
# 오늘 / 내일 바로가기
# -----------------------------------

st.subheader("📌 빠른 조회")

col1, col2 = st.columns(2)

with col1:

    if st.button("오늘 급식", use_container_width=True):

        meals = get_meal_data(
            date.today(),
            date.today()
        )

        if not meals:
            st.warning("오늘은 등록된 급식 정보가 없습니다.")

        else:

            st.success(
                f"오늘은 {len(meals)}개의 급식 정보가 있습니다."
            )

            for meal in meals:

                st.markdown(
                    f"### 🍽️ {meal.get('MMEAL_SC_NM', '급식')}"
                )

                menu = clean_menu(
                    meal.get("DDISH_NM", "")
                )

                for food in menu:
                    st.write(f"• {food}")

                calorie = meal.get("CAL_INFO", "")

                if calorie:
                    st.caption(f"열량: {calorie}")


with col2:

    if st.button("내일 급식", use_container_width=True):

        tomorrow = date.today() + timedelta(days=1)

        meals = get_meal_data(
            tomorrow,
            tomorrow
        )

        if not meals:
            st.warning("내일은 등록된 급식 정보가 없습니다.")

        else:

            st.success(
                f"내일은 {len(meals)}개의 급식 정보가 있습니다."
            )

            for meal in meals:

                st.markdown(
                    f"### 🍽️ {meal.get('MMEAL_SC_NM', '급식')}"
                )

                menu = clean_menu(
                    meal.get("DDISH_NM", "")
                )

                for food in menu:
                    st.write(f"• {food}")

                calorie = meal.get("CAL_INFO", "")

                if calorie:
                    st.caption(f"열량: {calorie}")


# -----------------------------------
# 안내
# -----------------------------------

st.markdown("---")

st.caption(
    "급식 정보는 NEIS 교육정보 개방 API에서 제공하는 데이터를 사용합니다."
)
