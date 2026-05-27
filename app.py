"""자기소개 웹페이지 — Streamlit 멀티 섹션 한 페이지.

플레이스홀더 값으로 채워져 있으니 PROFILE 딕셔너리만 수정하면 됩니다.
실행: streamlit run app.py
"""

import streamlit as st

# ----------------------------------------------------------------------------
# 여기 값만 본인 정보로 바꾸세요.
# ----------------------------------------------------------------------------
PROFILE = {
    "name": "김도윤",
    "title": "백엔드 · 데이터 앱 개발자",
    "tagline": "헤드폰 끼고 일단 만들어보는 바이브코딩러.",
    "photo": "assets/profile.png",
    "about": (
        "안녕하세요! 헤드폰을 끼고 '일단 만들어보는' 바이브코딩을 즐기는 개발자 "
        "김도윤입니다. 머릿속 아이디어를 Streamlit으로 하루 만에 프로토타입으로 "
        "만들고, 데이터로 검증하며 다듬어 가는 과정을 가장 좋아합니다. 화려한 "
        "기술보다 '끝까지 동작하는 작은 것'을 만드는 데 진심입니다."
    ),
    "location": "서울, 대한민국",
    "email": "you@example.com",
    "skills": {
        "Python": 90,
        "Streamlit": 75,
        "SQL": 80,
        "Git": 70,
        "Data Analysis": 65,
    },
    "experiences": [
        {
            "period": "2024 - 현재",
            "role": "백엔드 · 데이터 개발자 · 모빌리티 스타트업",
            "desc": "Python/FastAPI로 추천 API와 데이터 파이프라인을 만들고, "
                    "운영 지표를 Streamlit 대시보드로 사내에 공유합니다.",
        },
        {
            "period": "2022 - 2024",
            "role": "웹 서비스 개발자 · 커머스 스타트업",
            "desc": "주문·정산 도메인 백엔드 기능을 개발하고, 반복 업무를 "
                    "줄이는 사내 운영툴을 Streamlit으로 빠르게 프로토타이핑했습니다.",
        },
        {
            "period": "2021 - 2022",
            "role": "개발 부트캠프 수료 & 사이드 프로젝트",
            "desc": "비전공에서 개발자로 전향했습니다. 데이터 분석과 웹 앱을 "
                    "독학하며 작은 토이 프로젝트를 직접 출시해 봤습니다.",
        },
    ],
    "projects": [
        {
            "name": "프로젝트 A",
            "desc": "Streamlit 기반 데이터 대시보드.",
            "link": "https://github.com/goldenus38/web-kdn",
        },
        {
            "name": "프로젝트 B",
            "desc": "사용자 피드백 분석 도구.",
            "link": "https://github.com/goldenus38",
        },
    ],
    "socials": {
        "GitHub": "https://github.com/goldenus38",
        "Email": "mailto:you@example.com",
        "LinkedIn": "https://linkedin.com",
    },
}


def setup_page():
    st.set_page_config(
        page_title=f"{PROFILE['name']} | 자기소개",
        page_icon="👋",
        layout="wide",
    )


def section_header():
    col_photo, col_intro = st.columns([1, 2], gap="large")
    with col_photo:
        st.image(PROFILE["photo"], width=240)
    with col_intro:
        st.title(f"안녕하세요, {PROFILE['name']}입니다 👋")
        st.subheader(PROFILE["title"])
        st.markdown(f"> {PROFILE['tagline']}")
        st.caption(f"📍 {PROFILE['location']}  ·  ✉️ {PROFILE['email']}")
    st.divider()


def section_about():
    st.header("소개")
    st.write(PROFILE["about"])
    st.divider()


def section_skills():
    st.header("기술 스택")
    for skill, level in PROFILE["skills"].items():
        st.markdown(f"**{skill}** — {level}%")
        st.progress(level / 100)
    st.divider()


def section_experience():
    st.header("경력")
    for exp in PROFILE["experiences"]:
        st.markdown(f"**{exp['role']}**  \n*{exp['period']}*")
        st.write(exp["desc"])
        st.write("")
    st.divider()


def section_projects():
    st.header("프로젝트")
    cols = st.columns(len(PROFILE["projects"]))
    for col, proj in zip(cols, PROFILE["projects"]):
        with col:
            with st.container(border=True):
                st.subheader(proj["name"])
                st.write(proj["desc"])
                st.link_button("자세히 보기", proj["link"])
    st.divider()


def section_contact():
    st.header("연락처")
    cols = st.columns(len(PROFILE["socials"]))
    for col, (label, url) in zip(cols, PROFILE["socials"].items()):
        with col:
            st.link_button(label, url, use_container_width=True)


def main():
    setup_page()
    section_header()
    section_about()
    section_skills()
    section_experience()
    section_projects()
    section_contact()
    st.caption("Made with ❤️ using Streamlit")


if __name__ == "__main__":
    main()
