import streamlit as st
from urllib.parse import quote
from datetime import datetime, timedelta


# =========================================================
# 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="ALL챙이",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# 디자인
# =========================================================

def apply_styles():
    st.markdown(
        """
        <style>

        .stApp {
            background-color: #f7f9f6;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .service-title {
            text-align: center;
            font-size: 48px;
            font-weight: 800;
            color: #456451;
            margin-top: 5px;
            margin-bottom: 5px;
        }

        .service-subtitle {
            text-align: center;
            font-size: 18px;
            color: #718077;
            margin-bottom: 35px;
        }

        .section-title {
            font-size: 25px;
            font-weight: 750;
            color: #34453b;
            margin-top: 25px;
            margin-bottom: 15px;
        }

        .small-description {
            font-size: 14px;
            color: #7c8981;
            margin-bottom: 15px;
        }

        .notice-card {
            background-color: white;
            border: 1px solid #e4e9e5;
            border-radius: 18px;
            padding: 22px;
            margin-bottom: 18px;
            box-shadow: 0px 3px 12px rgba(0, 0, 0, 0.04);
        }

        .notice-title {
            font-size: 20px;
            font-weight: 750;
            color: #26362d;
            margin-bottom: 10px;
        }

        .notice-meta {
            font-size: 14px;
            color: #69766e;
            margin-bottom: 7px;category
        }

        .notice-summary {
            background-color: #f5f8f5;
            padding: 13px 15px;
            border-radius: 12px;
            margin-top: 12px;
            margin-bottom: 10px;
            color: #3f4f46;
            line-height: 1.6;
        }

        .notice-reason {
            background-color: #fff9e9;
            padding: 12px 15px;
            border-radius: 12px;
            color: #665b3e;
            margin-top: 10px;
            margin-bottom: 12px;
        }

        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            margin-right: 6px;
            margin-bottom: 8px;
        }

        .badge-category {
            background-color: #e8f3eb;
            color: #3e6a4d;
        }

        .badge-relevance {
            background-color: #e8efff;
            color: #4866a4;
        }

        .badge-dday {
            background-color: #fff0ef;
            color: #c85750;
        }

        .choice-card {
            background-color: white;
            border: 1px solid #e1e7e2;
            border-radius: 22px;
            padding: 32px 25px;
            min-height: 170px;
            text-align: center;
            box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.04);
        }

        .choice-icon {
            font-size: 46px;
            margin-bottom: 12px;
        }

        .choice-title {
            font-size: 26px;
            font-weight: 800;
            color: #34483b;
            margin-bottom: 8px;
        }

        .choice-description {
            font-size: 15px;
            color: #79867e;
            line-height: 1.6;
        }

        div.stButton > button {
            border-radius: 12px;
            font-weight: 700;
            min-height: 44px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


apply_styles()


# =========================================================
# 빈 사용자 데이터
# =========================================================

def empty_user():
    return {
        "school": "",
        "major": "",
        "grade": 1,
        "activities": [],
        "interests": [],
        "custom_interests": []
    }


# =========================================================
# 사용자 입력 화면
# =========================================================

def get_user_input():

    if "page" not in st.session_state:
        st.session_state.page = "input"

    if "user_data" not in st.session_state:
        st.session_state.user_data = None

    if "result_type" not in st.session_state:
        st.session_state.result_type = None


    if st.session_state.page != "input":

        if st.session_state.user_data:
            return st.session_state.user_data

        return empty_user()


    # =====================================================
    # 로고 이미지
    # =====================================================

    image_col1, image_col2, image_col3 = st.columns([1, 1.3, 1])

    with image_col2:
        st.image(
            "allchaeng.png",
            use_container_width=True
        )


    # =====================================================
    # 서비스 이름
    # =====================================================

    st.markdown(
        '<div class="service-title">ALL챙이</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="service-subtitle">
            모든 것을 챙겨주는 에이아이
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # 기본 정보
    # =====================================================

    st.markdown(
        '<div class="section-title">👤 나를 알려주세요</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="small-description">
            입력한 정보를 바탕으로 나에게 필요한 공지와 기회를 찾아드려요.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        school = st.text_input(
            "학교",
            placeholder="예: 국민대학교"
        )

    with col2:
        major = st.text_input(
            "학과 / 전공",
            placeholder="예: 전자공학부"
        )

    with col3:
        grade = st.selectbox(
            "학년",
            [1, 2, 3, 4, 5, 6]
        )


    # =====================================================
    # 관심 활동 체크박스
    # =====================================================

    st.markdown(
        '<div class="section-title">🎯 관심 활동</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="small-description">
            관심 있는 활동을 모두 선택해주세요.
        </div>
        """,
        unsafe_allow_html=True
    )

    activity_options = [
        "장학금",
        "인턴 / 현장실습",
        "취업 / 채용",
        "공모전 / 해커톤",
        "대외활동",
        "연구 / 학부연구생",
        "창업",
        "교환학생 / 해외 프로그램"
    ]

    selected_activities = []

    activity_cols = st.columns(4)

    for index, activity in enumerate(activity_options):

        with activity_cols[index % 4]:

            checked = st.checkbox(
                activity,
                key=f"activity_{index}"
            )

            if checked:
                selected_activities.append(activity)


    # =====================================================
    # 관심 기술 분야 체크박스
    # =====================================================

    st.markdown(
        '<div class="section-title">💡 관심 기술 분야</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="small-description">
            관심 있는 기술 분야를 모두 선택해주세요.
        </div>
        """,
        unsafe_allow_html=True
    )

    interest_options = [
        "반도체",
        "AI / 머신러닝",
        "임베디드 / IoT",
        "로봇",
        "통신",
        "회로 / 하드웨어",
        "소프트웨어 / 개발",
        "데이터 분석"
    ]

    selected_interests = []

    interest_cols = st.columns(4)

    for index, interest in enumerate(interest_options):

        with interest_cols[index % 4]:

            checked = st.checkbox(
                interest,
                key=f"interest_{index}"
            )

            if checked:
                selected_interests.append(interest)


    # =====================================================
    # 추가 관심 분야
    # =====================================================

    st.markdown(
        '<div class="section-title">✏️ 추가 관심 분야</div>',
        unsafe_allow_html=True
    )

    custom_interest_text = st.text_input(
        "목록에 없는 관심사가 있다면 입력해주세요.",
        placeholder="예: 자율주행, FPGA, 컴퓨터 비전"
    )

    custom_interests = []

    if custom_interest_text.strip():

        custom_interests = [
            item.strip()
            for item in custom_interest_text.split(",")
            if item.strip()
        ]


    st.write("")


    # =====================================================
    # 맞춤 정보 찾기
    # =====================================================

    if st.button(
        "맞춤 정보 찾기 →",
        use_container_width=True,
        type="primary"
    ):

        if not school.strip():

            st.warning("학교를 입력해주세요.")
            return empty_user()

        if not major.strip():

            st.warning("학과 또는 전공을 입력해주세요.")
            return empty_user()


        user = {
            "school": school.strip(),
            "major": major.strip(),
            "grade": int(grade),
            "activities": selected_activities,
            "interests": selected_interests,
            "custom_interests": custom_interests
        }


        st.session_state.user_data = user
        st.session_state.page = "category"

        st.rerun()


    return empty_user()


# =========================================================
# Google Calendar 링크 생성
# =========================================================

def make_google_calendar_link(item):

    deadline = item.get("deadline")

    if not deadline:
        return None

    try:

        deadline_date = datetime.strptime(
            deadline,
            "%Y-%m-%d"
        )

    except ValueError:

        return None


    start_date = deadline_date.strftime("%Y%m%d")

    end_date = (
        deadline_date + timedelta(days=1)
    ).strftime("%Y%m%d")


    title = item.get(
        "title",
        "일정"
    )


    details = item.get("summary") or item.get("content") or ""


    calendar_url = (
        "https://calendar.google.com/calendar/render"
        "?action=TEMPLATE"
        f"&text={quote(title)}"
        f"&dates={start_date}/{end_date}"
        f"&details={quote(details)}"
    )


    return calendar_url


# =========================================================
# 공지 카드
# =========================================================

def show_notice_card(item):

    title = item.get("title", "제목 없음")
    source = item.get("source", "")
    category = item.get("category", "기타")
    deadline = item.get("deadline")
    target = item.get("target")
    summary = item.get("summary")
    action = item.get("action")
    relevance = item.get("relevance")
    reason = item.get("reason")
    dday = item.get("dday")
    url = item.get("url")


    if dday is None:
        dday_text = ""

    elif dday == 0:
        dday_text = "D-DAY"

    elif dday > 0:
        dday_text = f"D-{dday}"

    else:
        dday_text = f"D+{abs(dday)}"


    badge_html = f"""
        <span class="badge badge-category">
            {category}
        </span>
    """


    if relevance is not None:

        badge_html += f"""
            <span class="badge badge-relevance">
                관련도 {relevance}%
            </span>
        """


    if dday_text:

        badge_html += f"""
            <span class="badge badge-dday">
                {dday_text}
            </span>
        """


    html = f"""
    <div class="notice-card">

        <div>
            {badge_html}
        </div>

        <div class="notice-title">
            {title}
        </div>
    """


    if source:

        html += f"""
        <div class="notice-meta">
            🏫 출처 : {source}
        </div>
        """


    if deadline:

        html += f"""
        <div class="notice-meta">
            📅 마감일 : {deadline}
        </div>
        """


    if target:

        html += f"""
        <div class="notice-meta">
            👤 대상 : {target}
        </div>
        """


    if summary:

        html += f"""
        <div class="notice-summary">
            <b>AI 요약</b><br>
            {summary}
        </div>
        """


    if action:

        html += f"""
        <div class="notice-meta">
            ✅ 해야 할 일 : {action}
        </div>
        """


    if reason:

        html += f"""
        <div class="notice-reason">
            <b>왜 추천했나요?</b><br>
            {reason}
        </div>
        """


    html += "</div>"


    st.markdown(
        html,
        unsafe_allow_html=True
    )


    button_col1, button_col2 = st.columns(2)


    if url:

        with button_col1:

            st.link_button(
                "원문 보기 ↗",
                url,
                use_container_width=True
            )


    calendar_link = make_google_calendar_link(item)


    if calendar_link:

        with button_col2:

            st.link_button(
                "Google Calendar 추가 📅",
                calendar_link,
                use_container_width=True
            )


# =========================================================
# 마감일 정렬
# =========================================================

def sort_by_deadline(items):

    def key_function(item):

        deadline = item.get("deadline")

        if not deadline:
            return datetime.max

        try:

            return datetime.strptime(
                deadline,
                "%Y-%m-%d"
            )

        except ValueError:

            return datetime.max


    return sorted(
        items,
        key=key_function
    )


# =========================================================
# 결과 화면
# =========================================================

def show_results(results):

    if st.session_state.get("page") == "input":
        return


    # =====================================================
    # 과제 / 공지 선택 화면
    # =====================================================

    if st.session_state.page == "category":

        st.markdown(
            '<div class="service-title">어떤 정보를 확인할까요?</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="service-subtitle">
        원하는 정보 유형을 선택하면 맞춤 결과를 보여드립니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):

            st.markdown(
                """
                <div class="choice-icon">
                    📚
                </div>

                <div class="choice-title">
                    과제
                </div>

                <div class="choice-description">
                    마감이 가까운 과제부터<br>
                    중요한 과제를 한눈에 확인해요.
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "과제 확인하기",
                key="assignment_button",
                width="stretch"
            ):
                st.session_state.result_type = "과제"
                st.session_state.page = "results"
                st.rerun()

    with col2:
        with st.container(border=True):

            st.markdown(
                """
                <div class="choice-icon">
                    📢
                </div>

                <div class="choice-title">
                    공지
                </div>

                <div class="choice-description">
                    장학금, 인턴, 공모전 등<br>
                    나에게 필요한 정보를 확인해요.
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "공지 확인하기",
                key="notice_button",
                width="stretch"
            ):
                st.session_state.result_type = "공지"
                st.session_state.page = "results"
                st.rerun()

    st.write("")

    if st.button("← 검색 조건 수정"):
        st.session_state.page = "input"
        st.rerun()

    return


    # =====================================================
    # 결과 페이지
    # =====================================================

    if st.session_state.page == "results":

        result_type = st.session_state.get(
            "result_type",
            "notice"
        )


        assignment_names = [
            "과제",
            "assignment",
            "과제/시험"
        ]


        if result_type == "assignment":

            filtered_results = [
                item
                for item in results
                if str(
                    item.get(
                        "category",
                        ""
                    )
                ).lower()
                in assignment_names
            ]

            page_title = "📚 나의 과제"


        else:

            filtered_results = [
                item
                for item in results
                if str(
                    item.get(
                        "category",
                        ""
                    )
                ).lower()
                not in assignment_names
            ]

            page_title = "📢 나의 맞춤 공지"


        st.markdown(
            f'<div class="section-title">{page_title}</div>',
            unsafe_allow_html=True
        )


        deadline_items = [
            item
            for item in filtered_results
            if item.get("deadline")
        ]


        no_deadline_items = [
            item
            for item in filtered_results
            if not item.get("deadline")
        ]


        left_col, right_col = st.columns(2)


        # =================================================
        # 왼쪽 : 마감 있는 정보
        # =================================================

        with left_col:

            st.subheader("⏰ 마감이 있는 정보")


            left_sort = st.selectbox(
                "정렬",
                [
                    "마감일 임박순",
                    "중요도순"
                ],
                key="deadline_sort"
            )


            if left_sort == "마감일 임박순":

                deadline_items = sort_by_deadline(
                    deadline_items
                )

            else:

                deadline_items = sorted(
                    deadline_items,
                    key=lambda x: x.get(
                        "priority",
                        0
                    ),
                    reverse=True
                )


            if not deadline_items:

                st.info(
                    "현재 마감이 있는 정보가 없습니다."
                )


            for item in deadline_items:

                show_notice_card(item)


        # =================================================
        # 오른쪽 : 마감 없는 정보
        # =================================================

        with right_col:

            st.subheader("📌 마감이 없는 정보")


            right_sort = st.selectbox(
                "정렬",
                [
                    "중요도순",
                    "최신순"
                ],
                key="no_deadline_sort"
            )


            if right_sort == "중요도순":

                no_deadline_items = sorted(
                    no_deadline_items,
                    key=lambda x: x.get(
                        "priority",
                        0
                    ),
                    reverse=True
                )

            else:

                no_deadline_items = sorted(
                    no_deadline_items,
                    key=lambda x: x.get(
                        "date",
                        ""
                    ) or "",
                    reverse=True
                )


            if not no_deadline_items:

                st.info(
                    "현재 마감이 없는 정보가 없습니다."
                )


            for item in no_deadline_items:

                show_notice_card(item)


        st.divider()


        # =================================================
        # 뒤로가기
        # =================================================

        back_col1, back_col2 = st.columns(2)


        with back_col1:

            if st.button(
                "← 과제 / 공지 선택으로",
                use_container_width=True
            ):

                st.session_state.page = "category"

                st.rerun()


        with back_col2:

            if st.button(
                "검색 조건 다시 입력",
                use_container_width=True
            ):

                st.session_state.page = "input"

                st.rerun()