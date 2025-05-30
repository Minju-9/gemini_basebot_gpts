import streamlit as st
from google.generativeai import configure, GenerativeModel

# Gemini API 키 연결
configure(api_key=st.secrets["gemini"]["api_key"])
model = GenerativeModel(model_name="gemini-1.5-flash")

# 대화 상태 초기화 (세션이 처음 시작될 때만)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_user_message" not in st.session_state:
    st.session_state.last_user_message = None
if "waiting_for_answer" not in st.session_state:
    st.session_state.waiting_for_answer = False

st.set_page_config(page_title="BaseBot", page_icon="⚾", layout="centered")

# CSS 스타일 추가
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        padding: 1rem;
        color: #1E3A8A;
    }
    .sub-title {
        text-align: center;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .team-header {
        color: #1E3A8A;
        font-weight: bold;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀과 설명
st.markdown("<h1 class='main-title'>⚾ BaseBot ⚾</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>🏟️ KBO 리그 구단 정보부터 야구 룰까지, 무엇이든 물어보세요! 🎯</p>", unsafe_allow_html=True)

# 구분선 추가
st.markdown("---")

# 동작1: 주제 선택
option = st.radio(
    "🎪 궁금한 내용을 선택해주세요 👇",
    ["KBO 구단 선택", "야구 룰이 궁금해요"],
    horizontal=True,
)

teams = [
    "LG 트윈스", "두산 베어스", "SSG 랜더스", "한화 이글스",
    "KIA 타이거즈", "롯데 자이언츠", "삼성 라이온즈",
    "키움 히어로즈", "KT 위즈", "NC 다이노스"
]

def process_user_message(content):
    if content != st.session_state.last_user_message and not st.session_state.waiting_for_answer:
        st.session_state.messages.append({"role": "user", "content": content})
        st.session_state.last_user_message = content
        st.session_state.waiting_for_answer = True
        return True
    return False

# KBO 구단 선택 옵션
if option == "KBO 구단 선택":
    st.info("🏟️ 오늘 궁금한 팀이 있으신가요? KBO 구단을 선택해보세요!")
    
    selected_team = st.selectbox("⚾ KBO 구단을 선택해주세요", [""] + teams)
    if selected_team:
        st.markdown(f"<h3 class='team-header'>✨ {selected_team} 관련해서 이런 건 어때요?</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        # 홈구장 정보 버튼
        if col1.button("🏟️ 홈구장 정보"):
            prompt = f"{selected_team}의 홈구장에 대해 설명해줘. 위치, 특징, 수용 인원 등을 포함해서 알려줘."
            process_user_message(prompt)
        
        # 팀 역사 버튼
        if col2.button("📜 팀 역사"):
            prompt = f"{selected_team}의 역사와 전통에 대해 설명해줘. 창단 연도부터 주요 사건들을 알려줘."
            process_user_message(prompt)
        
        # 우승 기록 버튼
        if col3.button("🏆 주요 우승 기록"):
            prompt = f"{selected_team}의 한국시리즈 우승 기록과 그 때의 주요 선수들에 대해 알려줘."
            process_user_message(prompt)

# 야구 룰 검색
else:
    st.info("⚾ 궁금한 야구 규칙이나 용어를 자유롭게 물어보세요!")

# 구분선 추가
st.markdown("---")

# 사용자 직접 입력
user_input = st.chat_input("⚾ 궁금한 걸 물어보세요!")

if user_input:
    process_user_message(user_input)

# 빈 선택 or 오류 발생 시 안내
if not st.session_state.messages:
    st.warning("🎯 먼저 궁금한 팀을 선택하거나 질문을 입력해보세요!")

# 대화 내용 출력 및 Gemini 응답 생성
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 새로운 사용자 메시지가 있고 응답을 기다리는 상태일 때만 응답 생성
if st.session_state.waiting_for_answer:
    with st.chat_message("assistant"):
        with st.spinner("⚾ 정보를 확인 중이에요..."):
            try:
                response = model.generate_content(st.session_state.last_user_message)
                answer = response.text
            except:
                answer = "⚠️ 죄송해요, 답변 중 오류가 발생했어요."
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.waiting_for_answer = False
