import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="점심 추천 생성기",
    page_icon="🍱",
    layout="centered"
)

st.title("🍱 점심 추천 생성기")
st.write("오늘 뭐 먹을지 모르겠다면 AI에게 추천받아보세요!")

# OpenAI API Key
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("OPENAI_API_KEY가 Streamlit Secrets에 설정되어 있지 않습니다.")
    st.stop()

client = OpenAI(api_key=api_key)

# 사용자 입력
st.subheader("🍚 오늘의 조건")

food_type = st.selectbox(
    "먹고 싶은 종류",
    [
        "상관없음",
        "한식",
        "중식",
        "일식",
        "양식",
        "분식",
        "패스트푸드",
        "면 요리",
        "밥 요리"
    ]
)

budget = st.selectbox(
    "예산",
    [
        "상관없음",
        "5,000원 이하",
        "8,000원 이하",
        "10,000원 이하",
        "15,000원 이하",
        "15,000원 이상"
    ]
)

amount = st.selectbox(
    "먹는 양",
    [
        "적당히",
        "든든하게",
        "최대한 배부르게"
    ]
)

preference = st.text_input(
    "추가로 원하는 조건",
    placeholder="예: 매운 음식은 싫어요 / 고기가 먹고 싶어요"
)

# 추천 버튼
if st.button("🍴 점심 추천받기", use_container_width=True):

    with st.spinner("맛있는 점심을 고민하는 중..."):

        prompt = f"""
너는 점심 메뉴를 추천해주는 AI야.

사용자의 조건:
- 음식 종류: {food_type}
- 예산: {budget}
- 먹는 양: {amount}
- 추가 조건: {preference if preference else "없음"}

위 조건을 고려해서 점심 메뉴를 추천해줘.

다음 형식으로 답변해줘.

1. 가장 추천하는 메뉴
2. 추천 이유
3. 함께 먹으면 좋은 메뉴
4. 비슷한 대안 메뉴 2개

너무 장황하게 설명하지 말고,
학생이 실제 점심으로 먹기 좋은 메뉴를 중심으로 추천해줘.
"""

        try:
            response = client.responses.create(
                model="gpt-5.4-nano",
                input=prompt
            )

            result = response.output_text

            st.success("🍱 추천 완료!")
            st.markdown(result)

        except Exception as e:
            st.error("추천을 생성하는 중 오류가 발생했습니다.")
            st.code(str(e))
