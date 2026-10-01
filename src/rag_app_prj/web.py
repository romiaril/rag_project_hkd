import base64
from pathlib import Path

import streamlit as st

from rag import ask


HERO_IMAGE = Path(__file__).resolve().parent / "assets" / "gamcheon.jpg"


EXAMPLES = [
    ("2일차 일정", "2일차에는 어디에 가나요?"),
    ("태종대 입장료", "태종대 입장료는 얼마인가요?"),
    ("공항에서 남포동", "김해공항에서 남포동까지 어떻게 가나요?"),
    ("환불 규정", "환불 규정은 어떻게 되나요?"),
]

DAYS = [
    ("1일차", "남포 · 자갈치", "국제시장, 자갈치 저녁, 부산타워"),
    ("2일차", "해운대 · 광안", "동백섬, 밀면, 광안대교 야경"),
    ("3일차", "감천 · 태종대", "감천문화마을, 태종대, 출발"),
]


st.set_page_config(
    page_title="부산 2박 3일",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #e4eef2 0%, #f6f3ee 240px);
        color: #1c2a33;
        font-family: "Malgun Gothic", sans-serif;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stSidebar"] {
        background: #0e4d6c;
    }
    [data-testid="stSidebar"] * {
        color: #f6f3ee !important;
    }
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 12px;
        text-align: left;
        height: auto !important;
        min-height: 2.5rem;
        padding: 0.65rem 0.85rem;
        white-space: normal;
        line-height: 1.35;
    }
    [data-testid="stSidebar"] .stButton button p {
        white-space: normal;
        text-align: left;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        border-color: #e07a3d;
        background: rgba(224, 122, 61, 0.22);
    }
    [data-testid="stMain"] [data-testid="stVerticalBlock"],
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
        overflow: visible;
    }
    [data-testid="stElementContainer"]:has(.hero) {
        position: sticky;
        top: 0;
        z-index: 40;
        background: #f6f3ee;
        padding-bottom: 0.35rem;
    }
    .hero {
        color: #0e4d6c;
        border-radius: 22px;
        min-height: 280px;
        display: flex;
        align-items: flex-end;
        padding: 1.5rem 1.8rem 1.45rem;
        margin-bottom: 0;
        overflow: hidden;
        background-color: #d7e4ea;
        background-size: cover;
        background-position: center center;
        box-shadow: 0 12px 28px rgba(14, 77, 108, 0.18);
    }
    .hero-kicker {
        letter-spacing: 0.16em;
        font-size: 0.78rem;
        opacity: 0.92;
        margin-bottom: 0.35rem;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.4rem;
    }
    .hero-sub {
        font-size: 1rem;
        line-height: 1.55;
        max-width: 36rem;
        opacity: 0.96;
    }
    .hero-copy {
        text-shadow: 0 1px 0 rgba(255, 255, 255, 0.9), 0 0 16px rgba(255, 255, 255, 0.95);
    }
    .day-card, .welcome-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 0.95rem 1rem 0.85rem;
        box-shadow: 0 8px 20px rgba(28, 42, 51, 0.06);
        border-top: 4px solid #1f8a70;
        min-height: 7.2rem;
    }
    .day-card .label, .welcome-card .label {
        color: #e07a3d;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .day-card .name, .welcome-card .name {
        color: #0e4d6c;
        font-size: 1.12rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .day-card .detail, .welcome-card .detail {
        color: #3d5160;
        font-size: 0.92rem;
        line-height: 1.45;
    }
    [data-testid="stChatMessage"] {
        background: transparent;
        margin-bottom: 0.55rem;
    }
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        background: #0e4d6c;
        border-radius: 16px;
        padding: 0.25rem 0.45rem;
    }
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) [data-testid="stChatMessageContent"] p {
        color: #f6f3ee !important;
    }
    [data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(28, 42, 51, 0.06);
        padding: 0.25rem 0.45rem;
    }
    .source-pill {
        display: inline-block;
        margin-top: 0.35rem;
        background: #e7f5f1;
        color: #1f8a70;
        border-radius: 999px;
        padding: 0.2rem 0.7rem;
        font-size: 0.85rem;
    }
    .cite-warn {
        color: #a14b24;
        font-size: 0.85rem;
        margin-top: 0.35rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def source_label(sources):
    pages = []
    for source in sources:
        page = source["page"]
        if page not in pages:
            pages.append(page)
    pages.sort()
    page_text = ", ".join(str(page) for page in pages)
    return f"가이드 {page_text}페이지"


def remember(question):
    with st.spinner("가이드에서 찾는 중..."):
        result = ask(question)
    st.session_state.history.append((question, result))


if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("### 일정")
    st.caption("숙소는 남포동, 체크인 15:00")
    for day, title, detail in DAYS:
        st.markdown(f"**{day}**  {title}")
        st.caption(detail)
    st.markdown("---")
    st.markdown("### 예시 질문")
    picked = None
    for label, question in EXAMPLES:
        if st.button(label, use_container_width=True, key=f"ex-{label}"):
            picked = question

hero_bytes = base64.b64encode(HERO_IMAGE.read_bytes()).decode("ascii")
st.markdown(
    f"""
    <style>
    .hero {{
        background-image: url("data:image/jpeg;base64,{hero_bytes}");
    }}
    </style>
    <div class="hero">
        <div class="hero-copy">
            <div class="hero-kicker">BUSAN · 2 NIGHTS 3 DAYS</div>
            <div class="hero-title">부산 2박 3일 여행 가이드</div>
            <div class="hero-sub">일정, 교통, 입장료, 식사를 가이드에 있는 내용만 안내합니다.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

columns = st.columns(3)
for column, (day, title, detail) in zip(columns, DAYS):
    with column:
        st.markdown(
            f"""
            <div class="day-card">
                <div class="label">{day}</div>
                <div class="name">{title}</div>
                <div class="detail">{detail}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

typed = st.chat_input("일정, 교통, 입장료, 식사를 물어보세요")
question = picked or typed
if question:
    remember(question)

if not st.session_state.history:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="label">가이드에게 물어보세요</div>
            <div class="name">요금과 시간은 문서에 적힌 숫자만 답합니다.</div>
            <div class="detail">왼쪽 예시 질문을 누르거나, 아래에 직접 입력하세요. 가이드에 없는 내용은 없다고 말합니다.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

for question, result in st.session_state.history:
    with st.chat_message("user", avatar="🧳"):
        st.write(question)

    with st.chat_message("assistant", avatar="🌊"):
        st.write(result["answer"])
        if result["sources"]:
            st.markdown(
                f'<span class="source-pill">{source_label(result["sources"])}</span>',
                unsafe_allow_html=True,
            )
        if result.get("cited") is False:
            st.markdown(
                '<div class="cite-warn">인용 표시가 확인되지 않았습니다.</div>',
                unsafe_allow_html=True,
            )

# streamlit run web.py
