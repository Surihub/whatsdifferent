import streamlit as st
import difflib

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='변경 내용 추적기',
    page_icon='🔍',
)

# CSS 스타일 추가 (hover 기능 제거)
st.markdown("""
    <style>
    /* 리셋 버튼 스타일  */
    div[data-testid="stHorizontalBlock"] > div:first-child button {
        background-color: #32CD32; /* 리셋 버튼 - 토마토색 */
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        width: 100%;
        padding: 10px;
    }

    /* 샘플 버튼 스타일  */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background-color: #4682B4; /* 샘플 버튼 - 파란색 */
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        width: 100%;
        padding: 10px;
    }

    /* 비교하기 버튼 스타일 (hover 없음) */
    button[data-testid="stButton"] {
        background-color: #32CD32; /* 비교 버튼 - 연한 초록색 */
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        width: 100%;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 페이지 제목 설정
st.title("🧐 변경 내용 추적기")
st.info("**변경 내용 추적기**에 오신 것을 환영합니다. 수정 전 후 내용에서 어떤 내용이 바뀌었는지 쉽게 비교해보세요.")

# 리셋 버튼 클릭 시 텍스트 초기화 함수
def reset_text():
    st.session_state["text1"] = ""
    st.session_state["text2"] = ""

# 샘플 입력 버튼 클릭 시 샘플 텍스트 입력 함수
def sample_text():
    st.session_state["text1"] = "안뇽하셰요! 반 갑솝니다. my name is SBhwang. this app is for detecting differences in text. Write text before you revised."
    st.session_state["text2"] = "안녕하세요! 반갑습니다. My name is SBhwang. This app is for detecting differences in text. Write text after you revised."

# 버튼 나란히 배치
button_col1, button_col2 = st.columns(2)
with button_col1:
    if st.button("입력 내용 리셋"):
        reset_text()

with button_col2:
    if st.button("샘플 내용 입력"):
        sample_text()

# 글자 크기 설정
font_size = st.number_input("수정할 부분을 얼마나 크게 나타낼까요?", value=1.5, step=0.1)

# 텍스트 입력 받기
text_before, text_after = st.columns(2)
with text_before:
    text1 = st.text_area("수정 전 텍스트를 입력해주세요.", value=st.session_state.get("text1", ""), key="text1")
with text_after:
    text2 = st.text_area("수정 후 텍스트를 입력해주세요.", value=st.session_state.get("text2", ""), key="text2")

# 두 텍스트의 차이를 시각적으로 표시하는 함수
@st.cache_data
def show_diff(text1, text2, font_size):
    diff = difflib.ndiff(text1.split(), text2.split())
    diff_text = ""
    for token in diff:
        if token[0] == ' ':
            diff_text += token[2:] + " "
        elif token[0] == '-':
            diff_text += f"<span style='color: red; background-color: #fdd; font-weight: bold; font-size: {font_size}em; text-decoration: line-through;'>{token[2:]}</span> "
        elif token[0] == '+':
            diff_text += f"<span style='color: green; background-color: #dfd; font-weight: bold; font-size: {font_size}em; text-decoration: underline;'>{token[2:]}</span> "
    return diff_text

# 비교하기 버튼
if st.button("바뀐 내용 비교하기", type= 'primary', use_container_width=True):
    diff_result = show_diff(st.session_state["text1"], st.session_state["text2"], font_size)
    st.markdown(diff_result, unsafe_allow_html=True)

# 저작권 정보 추가
st.markdown("""
---
<div style="text-align: center; font-size: 14px; line-height: 1.8; color: #555;">
    <span>© 2024 <strong style="color: #333;">whatsdifferent</strong>. All rights reserved.</span><br>
    <span style="font-weight: bold; color: #333;">Created by 황수빈</span>
    <a href="mailto:sbhath17@gmail.com" style="color: #007ACC; text-decoration: none; margin-left: 10px; font-style: italic;">
        sbhath17@gmail.com
    </a>
    <a href="https://github.com/Surihub" style="margin-left: 8px;">
        <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub">
    </a>
</div>
""", unsafe_allow_html=True)
