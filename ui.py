from textwrap import dedent
import streamlit as st
from urllib.parse import quote
from datetime import datetime, timedelta
from pathlib import Path
from html import escape


# =========================================================
# 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="ALL챙이",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# 페이지 이동 함수
# =========================================================

def go_to_results(result_type):
    st.session_state.result_type = result_type


def go_to_category():
    st.session_state.result_type = None


def go_to_input():
    st.session_state.user_data = None
    st.session_state.result_type = None
    st.session_state.pop("final_results", None)
    st.session_state.pop("processed_user", None)


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
            margin-bottom: 7px;
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
            min-height: 190px;
            text-align: center;
            box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.04);
        }

        .choice-icon {
            text-align: center;
            font-size: 46px;
            margin-bottom: 12px;
        }

        .choice-title {
            text-align: center;
            font-size: 26px;
            font-weight: 800;
            color: #34483b;
            margin-bottom: 8px;
        }

        .choice-description {
            text-align: center;
            font-size: 15px;
            color: #79867e;
            line-height: 1.6;
            min-height: 75px;
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

    if "user_data" not in st.session_state:
        st.session_state.user_data = None

    if "result_type" not in st.session_state:
        st.session_state.result_type = None

    # 사용자 정보 입력이 끝났으면 입력 UI를 다시 그리지 않는다.
    if st.session_state.user_data:
        return st.session_state.user_data

    # =====================================================
    # 로고 이미지
    # =====================================================

    image_path = (
        Path(__file__).resolve().parent
        / "allchaeng.png"
    )

    if image_path.exists():

        image_col1, image_col2, image_col3 = st.columns(
            [1, 1.3, 1]
        )

        with image_col2:

            st.image(
                str(image_path),
                width="stretch"
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
            입력한 정보를 바탕으로
            나에게 필요한 공지와 기회를 찾아드려요.
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(
        [2, 2, 1]
    )


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
    # 관심 활동
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


    for index, activity in enumerate(
        activity_options
    ):

        with activity_cols[index % 4]:

            checked = st.checkbox(
                activity,
                key=f"activity_{index}"
            )

            if checked:
                selected_activities.append(
                    activity
                )


    # =====================================================
    # 관심 기술 분야
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


    for index, interest in enumerate(
        interest_options
    ):

        with interest_cols[index % 4]:

            checked = st.checkbox(
                interest,
                key=f"interest_{index}"
            )

            if checked:
                selected_interests.append(
                    interest
                )


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
    # 맞춤 정보 찾기 버튼
    # =====================================================

    if st.button(
        "맞춤 정보 찾기 →",
        width="stretch",
        type="primary",
        key="search_button"
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
        st.session_state.result_type = None
        st.session_state.pop("final_results", None)
        st.session_state.pop("processed_user", None)
        st.rerun()

    return empty_user()


# =========================================================
# Google Calendar 링크
# =========================================================

def make_google_calendar_link(item):

    deadline = item.get(
        "deadline"
    )

    if not deadline:
        return None


    try:

        deadline_date = datetime.strptime(
            deadline,
            "%Y-%m-%d"
        )


    except ValueError:

        return None


    start_date = deadline_date.strftime(
        "%Y%m%d"
    )

    end_date = (
        deadline_date
        + timedelta(days=1)
    ).strftime(
        "%Y%m%d"
    )


    title = item.get(
        "title",
        "일정"
    )

    details = (
        item.get("summary")
        or item.get("content")
        or ""
    )


    calendar_url = (
        "https://calendar.google.com/calendar/render"
        "?action=TEMPLATE"
        f"&text={quote(str(title))}"
        f"&dates={start_date}/{end_date}"
        f"&details={quote(str(details))}"
    )


    return calendar_url


# =========================================================
# 공지 카드
# =========================================================

def show_assignment_card(item):

    title = str(
        item.get("title", "제목 없음")
    )

    source = str(
        item.get("source", "") or ""
    )

    deadline = item.get("deadline")

    content = str(
        item.get("content", "") or ""
    )

    dday = item.get("dday")

    url = item.get("url")


    # ==========================================
    # D-Day
    # ==========================================

    if dday is None:
        dday_text = "마감일 미정"

    elif dday == 0:
        dday_text = "D-DAY"

    elif dday > 0:
        dday_text = f"D-{dday}"

    else:
        dday_text = f"D+{abs(dday)}"


    # ==========================================
    # 카드
    # ==========================================

    with st.container(border=True):

        st.caption(
            f"📚 과제 · ⏰ {dday_text}"
        )

        st.subheader(title)


        if source:

            st.write(
                f"🏫 **출처:** {source}"
            )


        if deadline:

            st.write(
                f"📅 **마감일:** {deadline}"
            )


        if content:

            st.markdown(
                "#### 📝 과제 내용"
            )

            st.write(content)


        st.markdown(
            "#### ✅ 해야 할 일"
        )

        st.write(
            "마감일까지 과제를 제출하세요."
        )


        # 과제에는
        # AI 요약 / 관련도 / 추천 이유 / AI 실패
        # 전부 표시하지 않음


        if url:

            st.link_button(
                "eCampus 열기 ↗",
                url,
                width="stretch"
            )


        calendar_link = (
            make_google_calendar_link(item)
        )


        if calendar_link:

            st.link_button(
                "Google Calendar 추가 📅",
                calendar_link,
                width="stretch"
            )
def show_notice_card(item):

    title = str(
        item.get("title", "제목 없음")
    )

    source = str(
        item.get("source", "") or ""
    )

    category = str(
        item.get("category", "기타") or "기타"
    )

    deadline = item.get("deadline")

    target = str(
        item.get("target", "") or ""
    )

    content = str(
        item.get("content", "") or ""
    )

    summary = str(
        item.get("summary", "") or ""
    )

    action = str(
        item.get("action", "") or ""
    )

    reason = str(
        item.get("reason", "") or ""
    )

    relevance = item.get("relevance")

    dday = item.get("dday")

    url = item.get("url")

    analysis_failed = item.get(
        "analysis_failed",
        False
    )


    # ==========================================
    # D-Day
    # ==========================================

    if dday is None:
        dday_text = None

    elif dday == 0:
        dday_text = "D-DAY"

    elif dday > 0:
        dday_text = f"D-{dday}"

    else:
        dday_text = f"D+{abs(dday)}"


    # ==========================================
    # 카드
    # ==========================================

    with st.container(border=True):

        badge_parts = [
            f"🏷️ {category}"
        ]


        # AI 분석 성공했을 때만 관련도 표시
        if (
            relevance is not None
            and not analysis_failed
        ):

            badge_parts.append(
                f"🎯 관련도 {relevance}%"
            )


        if dday_text:

            badge_parts.append(
                f"⏰ {dday_text}"
            )


        st.caption(
            " · ".join(badge_parts)
        )


        st.subheader(title)


        if source:

            st.write(
                f"🏫 **출처:** {source}"
            )


        if deadline:

            st.write(
                f"📅 **마감일:** {deadline}"
            )


        if target and not analysis_failed:

            st.write(
                f"👤 **대상:** {target}"
            )


        # ======================================
        # AI 분석 성공
        # ======================================

        if not analysis_failed:

            if summary:

                st.markdown(
                    "#### 🤖 AI 요약"
                )

                st.write(summary)


            if action:

                st.markdown(
                    "#### ✅ 해야 할 일"
                )

                st.write(action)


            if reason:

                st.markdown(
                    "#### 💡 왜 추천했나요?"
                )

                st.info(reason)


        # ======================================
        # AI 분석 실패
        # 실패 문구를 사용자에게 노출하지 않음
        # ======================================

        else:

            if content:

                st.markdown(
                    "#### 📄 공지 내용"
                )

                # 너무 길면 앞부분만
                if len(content) > 500:

                    st.write(
                        content[:500] + "..."
                    )

                else:

                    st.write(content)


        # ======================================
        # 버튼
        # ======================================

        button_col1, button_col2 = (
            st.columns(2)
        )


        if url:

            with button_col1:

                st.link_button(
                    "원문 보기 ↗",
                    url,
                    width="stretch"
                )


        calendar_link = (
            make_google_calendar_link(item)
        )


        if calendar_link:

            with button_col2:

                st.link_button(
                    "Google Calendar 추가 📅",
                    calendar_link,
                    width="stretch"
                )


def sort_by_deadline(items):

    def key_function(item):

        deadline = item.get(
            "deadline"
        )


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
# 과제 판별
# =========================================================

def is_assignment(item):

    category = str(
        item.get(
            "category",
            ""
        )
    ).strip().lower()


    source = str(
        item.get(
            "source",
            ""
        )
    ).strip().lower()


    assignment_names = {
        "과제",
        "assignment",
        "과제/시험"
    }


    if category in assignment_names:
        return True


    # Mock eCampus 과제도 과제로 처리
    if (
        "ecampus" in source
        and "과제" in source
    ):
        return True


    return False


# =========================================================
# 결과 화면
# =========================================================

def show_results(results):

    if "result_type" not in st.session_state:
        st.session_state.result_type = None

    # 사용자 입력 전에는 결과 화면을 표시하지 않음
    if not st.session_state.get("user_data"):
        return

    result_type = st.session_state.get("result_type")

    # =====================================================
    # 과제 / 공지 선택 화면
    # =====================================================
    if result_type not in ("과제", "공지"):

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
                    <div class="choice-icon">📚</div>
                    <div class="choice-title">과제</div>
                    <div class="choice-description">
                        제출해야 할 과제와 학업 일정을 확인합니다.<br><br>
                        마감이 가까운 과제부터 빠르게 확인할 수 있어요.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.write("")

                if st.button(
                    "과제 확인하기 →",
                    key="assignment_button",
                    width="stretch",
                    type="primary"
                ):
                    st.session_state.result_type = "과제"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="choice-icon">📢</div>
                    <div class="choice-title">공지</div>
                    <div class="choice-description">
                        장학금, 인턴, 공모전, 연구, 취업 등<br><br>
                        나에게 필요한 학교 정보를 확인할 수 있어요.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.write("")

                if st.button(
                    "공지 확인하기 →",
                    key="notice_button",
                    width="stretch",
                    type="primary"
                ):
                    st.session_state.result_type = "공지"
                    st.rerun()

        st.write("")

        if st.button(
            "← 검색 조건 수정",
            key="edit_search_button",
            width="stretch"
        ):
            go_to_input()
            st.rerun()

        return

    # =====================================================
    # 결과 페이지
    # =====================================================
    if result_type == "과제":
        filtered_results = [item for item in results if is_assignment(item)]
        page_title = "📚 나의 과제"
    else:
        filtered_results = [item for item in results if not is_assignment(item)]
        page_title = "📢 나의 맞춤 공지"

    st.markdown(
        f'<div class="section-title">{page_title}</div>',
        unsafe_allow_html=True
    )

    if not filtered_results:
        if result_type == "과제":
            st.info("현재 표시할 과제가 없습니다.")
        else:
            st.info("현재 표시할 맞춤 공지가 없습니다.")

        if st.button(
            "← 과제 / 공지 선택으로",
            key=f"empty_back_{result_type}",
            width="stretch"
        ):
            st.session_state.result_type = None
            st.rerun()
        return

    deadline_items = [item for item in filtered_results if item.get("deadline")]
    no_deadline_items = [item for item in filtered_results if not item.get("deadline")]

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("⏰ 마감이 있는 정보")

        left_sort = st.selectbox(
            "정렬",
            ["마감일 임박순", "중요도순"],
            key=f"deadline_sort_{result_type}"
        )

        if left_sort == "마감일 임박순":
            deadline_items = sort_by_deadline(deadline_items)
        else:
            deadline_items = sorted(
                deadline_items,
                key=lambda x: x.get("priority", 0),
                reverse=True
            )

        if not deadline_items:
            st.info("현재 마감이 있는 정보가 없습니다.")

        for item in deadline_items:
            if is_assignment(item):
                show_assignment_card(item)
            else:
                show_notice_card(item)

    with right_col:
        st.subheader("📌 마감이 없는 정보")

        right_sort = st.selectbox(
            "정렬",
            ["중요도순", "최신순"],
            key=f"no_deadline_sort_{result_type}"
        )

        if right_sort == "중요도순":
            no_deadline_items = sorted(
                no_deadline_items,
                key=lambda x: x.get("priority", 0),
                reverse=True
            )
        else:
            no_deadline_items = sorted(
                no_deadline_items,
                key=lambda x: x.get("date", "") or "",
                reverse=True
            )

        if not no_deadline_items:
            st.info("현재 마감이 없는 정보가 없습니다.")

        for item in no_deadline_items:
            if is_assignment(item):
                show_assignment_card(item)
            else:
                show_notice_card(item)

    st.divider()
    back_col1, back_col2 = st.columns(2)

    with back_col1:
        if st.button(
            "← 과제 / 공지 선택으로",
            key=f"back_category_{result_type}",
            width="stretch"
        ):
            st.session_state.result_type = None
            st.rerun()

    with back_col2:
        if st.button(
            "검색 조건 다시 입력",
            key=f"back_input_{result_type}",
            width="stretch"
        ):
            go_to_input()
            st.rerun()

