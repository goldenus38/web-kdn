"""바이브조 자기소개 웹페이지 — Streamlit 인터랙티브 버전.

Streamlit의 강점(위젯·차트·탭·폼·메트릭·테마)을 살려 구성했다.
내용을 바꾸려면 아래 PROFILE 딕셔너리만 수정하면 된다.
실행: streamlit run app.py
"""

import base64
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# 여기 값만 본인 정보로 바꾸세요.
# ----------------------------------------------------------------------------
PROFILE = {
    "name": "바이브조",
    "title": "백엔드 · 데이터 앱 개발자",
    "tagline": "헤드폰 끼고 일단 만들어보는 바이브코딩러.",
    "photo": "assets/profile.png",
    "about": (
        "안녕하세요! 헤드폰을 끼고 '일단 만들어보는' 바이브코딩을 즐기는 개발자 "
        "바이브조입니다. 머릿속 아이디어를 Streamlit으로 하루 만에 프로토타입으로 "
        "만들고, 데이터로 검증하며 다듬어 가는 과정을 가장 좋아합니다. 화려한 "
        "기술보다 '끝까지 동작하는 작은 것'을 만드는 데 진심입니다."
    ),
    "location": "서울, 대한민국",
    "email": "vibejo@example.com",
    # 메트릭: (라벨, 값, 보조설명)
    "metrics": [
        ("개발 경력", "4년+", "백엔드·데이터"),
        ("출시 프로젝트", "12", "토이 포함"),
        ("GitHub 커밋", "1.2k", "최근 1년"),
        ("커피", "∞", "오늘도 함께"),
    ],
    "highlights": [
        "🚀 아이디어를 하루 만에 프로토타입으로",
        "📊 데이터로 가설을 검증하는 습관",
        "🤝 비개발 동료도 쓰는 사내 도구 제작",
        "🧪 작게 실험하고 빠르게 회고",
    ],
    "fun_facts": [
        "코딩할 때 로파이(lo-fi) 플레이리스트는 필수입니다.",
        "주말엔 토이 프로젝트로 또 코딩합니다.",
        "가장 좋아하는 단축키는 Ctrl+Z 입니다.",
    ],
    # 카테고리별 스킬 (0~100)
    "skills": {
        "언어 & 백엔드": {"Python": 90, "FastAPI": 78, "SQL": 82},
        "데이터 & 시각화": {"Pandas": 85, "Streamlit": 88, "Plotly": 72},
        "협업 & 인프라": {"Git": 80, "Docker": 65, "AWS": 58},
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
            "emoji": "📊",
            "name": "사내 운영 대시보드",
            "desc": "흩어진 운영 지표를 한곳에 모아 실시간으로 보여주는 "
                    "Streamlit 대시보드. 비개발 동료의 수작업 집계를 없앴습니다.",
            "tags": ["Streamlit", "Pandas", "Plotly"],
            "link": "https://github.com/goldenus38/web-kdn",
        },
        {
            "emoji": "🤖",
            "name": "추천 API 서비스",
            "desc": "사용자 행동 로그를 기반으로 콘텐츠를 추천하는 FastAPI "
                    "서버. 캐싱과 배치 파이프라인으로 응답 속도를 개선했습니다.",
            "tags": ["FastAPI", "Python", "AWS"],
            "link": "https://github.com/goldenus38",
        },
        {
            "emoji": "🧾",
            "name": "정산 자동화 툴",
            "desc": "엑셀로 하던 월별 정산을 자동화한 내부 도구. 마감 시간을 "
                    "반나절에서 10분으로 단축했습니다.",
            "tags": ["Python", "SQL", "Streamlit"],
            "link": "https://github.com/goldenus38",
        },
        {
            "emoji": "🎧",
            "name": "바이브코딩 타이머",
            "desc": "집중 세션과 플레이리스트를 연결한 주말 토이 프로젝트. "
                    "포모도로 통계를 차트로 보여줍니다.",
            "tags": ["Streamlit", "Plotly"],
            "link": "https://github.com/goldenus38",
        },
    ],
    "socials": {
        "🐙 GitHub": "https://github.com/goldenus38",
        "✉️ Email": "mailto:vibejo@example.com",
        "💼 LinkedIn": "https://linkedin.com",
    },
}


# ----------------------------------------------------------------------------
# 헬퍼
# ----------------------------------------------------------------------------
def img_data_uri(path: str) -> str:
    """로컬 이미지를 data URI로 인코딩 (HTML 임베드용)."""
    p = Path(path)
    if not p.exists():
        return ""
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/png;base64,{b64}"


def inject_css():
    st.markdown(
        """
        <style>
        .block-container { padding-top: 2rem; max-width: 1100px; }
        #MainMenu, footer { visibility: hidden; }

        .hero {
            background: linear-gradient(120deg, #FF4B4B 0%, #3D5A80 100%);
            border-radius: 22px; padding: 2rem 2.4rem; margin-bottom: .5rem;
            display: flex; align-items: center; gap: 1.8rem;
            box-shadow: 0 12px 40px rgba(0,0,0,.35);
        }
        .hero img {
            width: 132px; height: 132px; border-radius: 50%;
            border: 4px solid rgba(255,255,255,.7);
            box-shadow: 0 6px 24px rgba(0,0,0,.35);
        }
        .hero-text h1 { margin: 0; font-size: 2.2rem; color: #fff; }
        .hero-text .role { font-size: 1.1rem; color: #ffe; opacity: .95; }
        .hero-text .tag {
            display: inline-block; margin-top: .6rem; padding: .25rem .8rem;
            background: rgba(255,255,255,.18); border-radius: 999px;
            color: #fff; font-size: .92rem;
        }

        .timeline-card {
            border-left: 3px solid #FF4B4B; padding: .2rem 0 .2rem 1.1rem;
            margin: 0 0 1.3rem .4rem;
        }
        .timeline-card .period {
            color: #FF4B4B; font-weight: 700; font-size: .9rem;
        }
        .timeline-card .role { font-weight: 600; font-size: 1.05rem; }
        .timeline-card .desc { opacity: .85; font-size: .95rem; }

        .tag-pill {
            display: inline-block; padding: .12rem .6rem; margin: .15rem .2rem 0 0;
            background: rgba(255,75,75,.15); color: #FF6B6B;
            border-radius: 999px; font-size: .78rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# 섹션
# ----------------------------------------------------------------------------
def sidebar():
    with st.sidebar:
        if Path(PROFILE["photo"]).exists():
            st.image(PROFILE["photo"], use_container_width=True)
        st.markdown(f"### {PROFILE['name']}")
        st.caption(PROFILE["title"])
        st.caption(f"📍 {PROFILE['location']}")
        st.divider()
        for label, url in PROFILE["socials"].items():
            st.link_button(label, url, use_container_width=True)
        st.divider()
        if st.button("🎉 응원 한 방!", use_container_width=True):
            st.balloons()
        st.caption("Made with ❤️ + Streamlit")


def hero():
    uri = img_data_uri(PROFILE["photo"])
    img_tag = f'<img src="{uri}">' if uri else ""
    st.markdown(
        f"""
        <div class="hero">
            {img_tag}
            <div class="hero-text">
                <h1>안녕하세요, {PROFILE['name']}입니다 👋</h1>
                <div class="role">{PROFILE['title']}</div>
                <div class="tag">{PROFILE['tagline']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(len(PROFILE["metrics"]))
    for col, (label, value, helptext) in zip(cols, PROFILE["metrics"]):
        col.metric(label, value, helptext)


def tab_about():
    st.subheader("소개")
    st.write(PROFILE["about"])
    st.write("")
    cols = st.columns(2)
    for i, hl in enumerate(PROFILE["highlights"]):
        cols[i % 2].success(hl)
    with st.expander("🎈 소소한 TMI"):
        for fact in PROFILE["fun_facts"]:
            st.markdown(f"- {fact}")


def tab_skills():
    st.subheader("기술 스택")
    category = st.selectbox("카테고리 선택", list(PROFILE["skills"].keys()))
    skills = PROFILE["skills"][category]

    col_chart, col_bars = st.columns([1, 1], gap="large")
    with col_chart:
        labels = list(skills.keys())
        values = list(skills.values())
        fig = go.Figure(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill="toself",
                line_color="#FF4B4B",
                fillcolor="rgba(255,75,75,.35)",
            )
        )
        fig.update_layout(
            polar=dict(radialaxis=dict(range=[0, 100], showticklabels=False)),
            showlegend=False,
            height=320,
            margin=dict(l=40, r=40, t=30, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FAFAFA",
        )
        st.plotly_chart(fig, use_container_width=True)
    with col_bars:
        for skill, level in skills.items():
            st.markdown(f"**{skill}** &nbsp;·&nbsp; {level}%")
            st.progress(level / 100)

    avg = round(sum(skills.values()) / len(skills))
    st.caption(f"이 영역 평균 숙련도: **{avg}%**")


def tab_experience():
    st.subheader("경력 타임라인")
    for exp in PROFILE["experiences"]:
        st.markdown(
            f"""
            <div class="timeline-card">
                <div class="period">{exp['period']}</div>
                <div class="role">{exp['role']}</div>
                <div class="desc">{exp['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def tab_projects():
    st.subheader("프로젝트")
    all_tags = sorted({t for p in PROFILE["projects"] for t in p["tags"]})
    selected = st.multiselect("기술 태그로 필터", all_tags, placeholder="전체 보기")

    projects = [
        p for p in PROFILE["projects"]
        if not selected or set(selected) & set(p["tags"])
    ]
    if not projects:
        st.info("선택한 태그에 해당하는 프로젝트가 없습니다.")
        return

    for row_start in range(0, len(projects), 2):
        cols = st.columns(2, gap="medium")
        for col, proj in zip(cols, projects[row_start:row_start + 2]):
            with col, st.container(border=True):
                st.markdown(f"### {proj['emoji']} {proj['name']}")
                st.write(proj["desc"])
                pills = "".join(
                    f'<span class="tag-pill">{t}</span>' for t in proj["tags"]
                )
                st.markdown(pills, unsafe_allow_html=True)
                st.write("")
                st.link_button("자세히 보기 →", proj["link"])


def tab_contact():
    st.subheader("연락처")
    col_form, col_links = st.columns([1.4, 1], gap="large")

    with col_form:
        with st.form("contact_form", clear_on_submit=True):
            st.markdown("**메시지 보내기**")
            name = st.text_input("이름")
            email = st.text_input("이메일")
            message = st.text_area("내용", height=120)
            submitted = st.form_submit_button("보내기 ✉️", type="primary")
            if submitted:
                if name and message:
                    st.success(f"{name}님, 메시지 잘 받았습니다! 곧 회신드릴게요.")
                    st.balloons()
                else:
                    st.warning("이름과 내용을 입력해 주세요.")

    with col_links:
        st.markdown("**바로 연결**")
        for label, url in PROFILE["socials"].items():
            st.link_button(label, url, use_container_width=True)
        resume = (
            f"{PROFILE['name']} ({PROFILE['title']})\n"
            f"{PROFILE['location']} · {PROFILE['email']}\n\n"
            f"{PROFILE['about']}\n"
        )
        st.download_button(
            "📄 이력 요약 다운로드", resume,
            file_name="vibejo_intro.txt", use_container_width=True,
        )


def main():
    st.set_page_config(
        page_title=f"{PROFILE['name']} | 자기소개",
        page_icon="👋",
        layout="wide",
    )
    inject_css()
    sidebar()
    hero()
    st.write("")

    tabs = st.tabs(["👋 소개", "🛠️ 기술", "💼 경력", "🚀 프로젝트", "📬 연락처"])
    with tabs[0]:
        tab_about()
    with tabs[1]:
        tab_skills()
    with tabs[2]:
        tab_experience()
    with tabs[3]:
        tab_projects()
    with tabs[4]:
        tab_contact()


if __name__ == "__main__":
    main()
