import streamlit as st

from ui import get_user_input, show_results
from crawler import get_notices
from ai_analyzer import analyze_notice
from agent import process_notices


user = get_user_input()

if st.session_state.get("user_data"):

    if (
        "final_results" not in st.session_state
        or st.session_state.get("processed_user") != user
    ):

        with st.spinner("AI Agent가 정보를 찾고 분석하고 있습니다..."):

            raw_notices = get_notices(user)

            # 공개 공지와 Mock eCampus 데이터를 분리
            mock_notices = [
                notice
                for notice in raw_notices
                if str(
                    notice.get("source", "")
                ).startswith("Mock eCampus")
            ]

            public_notices = [
                notice
                for notice in raw_notices
                if not str(
                    notice.get("source", "")
                ).startswith("Mock eCampus")
            ]

            # API 호출 수는 제한하되
            # Mock eCampus 과제는 반드시 포함
            raw_notices = (
                public_notices[:5]
                + mock_notices
            )

            analyzed_notices = []

            for notice in raw_notices:
                analyzed = analyze_notice(
                    notice,
                    user
                )
                analyzed_notices.append(analyzed)

            final_results = process_notices(
                analyzed_notices,
                user
            )

            st.session_state.final_results = final_results
            st.session_state.processed_user = user.copy()

    show_results(
        st.session_state.final_results
    )

else:
    show_results([])