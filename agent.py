import datetime

def remove_duplicates(notices):

    if not notices or not isinstance(notices, list):
        return []

    seen_keys = set()
    unique_notices = []

    for notice in notices:

        if not isinstance(notice, dict):
            continue

        url = str(
            notice.get("url", "")
        ).strip()

        title = str(
            notice.get("title", "")
        ).strip()

        if not title:
            continue

        # URL만 비교하면 Mock eCampus 항목들이
        # 전부 같은 URL이라 하나로 합쳐지므로
        # URL + 제목 조합으로 중복 판단
        unique_key = (
            url,
            title
        )

        if unique_key in seen_keys:
            continue

        seen_keys.add(unique_key)
        unique_notices.append(notice)

    return unique_notices

def filter_notices(notices, min_relevance=50):

    filtered_notices = []

    for notice in notices:

        # Mock eCampus 과제는
        # 사용자의 실제 과제로 간주하므로 무조건 유지
        source = str(
            notice.get("source", "")
        )

        category = str(
            notice.get("category", "")
        ).strip()

        if (
            source == "Mock eCampus 과제"
            or category == "과제"
        ):
            filtered_notices.append(notice)
            continue

        relevance = notice.get(
            "relevance",
            0
        )

        if not isinstance(
            relevance,
            (int, float)
        ):
            relevance = 0

        if relevance >= min_relevance:
            filtered_notices.append(notice)

    return filtered_notices

def calculate_dday(deadline_str):
    if not deadline_str or str(deadline_str).strip() == "미정":
        return None
        
    try:
        today = datetime.date.today() 
        target_date = datetime.datetime.strptime(str(deadline_str).strip(), "%Y-%m-%d").date()
        delta = target_date - today
        return delta.days
    except ValueError:
        return None


def calculate_priority(notice):
    relevance = notice.get("relevance", 0)
    if not isinstance(relevance, (int, float)):
        relevance = 0
        
    dday = notice.get("dday")
    bonus = 0
    
    if dday is not None:
        if 0 <= dday <= 1:
            bonus = 30
        elif 2 <= dday <= 3:
            bonus = 15
        elif 4 <= dday <= 7:
            bonus = 5
        else:
            bonus = 0
            
    return relevance + bonus


def get_urgency_label(dday):
    """[추가 1] UI 렌더링용 상태 라벨 생성"""
    if dday is None:
        return "상시/미정"
    elif dday < 0:
        return "기간만료"
    elif 0 <= dday <= 1:
        return "🔥 마감임박"
    elif 2 <= dday <= 3:
        return "⚡ 이번주 마감"
    else:
        return "☕ 여유"


def rank_notices(notices):
    """[추가 2] 뱃지 부착 및 동점자 2차 정렬 적용"""
    for notice in notices:
        deadline = notice.get("deadline")
        dday = calculate_dday(deadline)
        notice["dday"] = dday
        notice["priority"] = calculate_priority(notice)
        notice["urgency_label"] = get_urgency_label(dday)
        
    # 1순위: priority 내림차순, 2순위: dday 오름차순(미정/None은 뒤로 보내기 위한 처리)
    ranked_notices = sorted(
        notices,
        key=lambda x: (
            x.get("priority", 0),
            -(x.get("dday") if x.get("dday") is not None else -9999) # dday가 작을수록(임박할수록) 우선 순위 부여 조율
        ),
        reverse=True
    )
    # 람다 정렬 가독성/직관성을 위해 단순화된 2차 정렬(점수 같으면 마감 가까운 것 우선)
    # Python은 stable sort이므로 우선순위 기준으로 먼저 정렬 후 2차 키 적용 가능
    # 직관적 안전 정렬:
    ranked_notices = sorted(
        notices,
        key=lambda x: (
            x.get("priority", 0),
            -(999 if x.get("dday") is None else x.get("dday")) # dday가 작을수록 음수 부호 활용 등 직관 정렬
        ),
        reverse=True
    )
    return ranked_notices


def group_by_category(ranked_notices):
    """[추가 3] UI 탭 분할용 카테고리 묶음 헬퍼"""
    grouped = {}
    for notice in ranked_notices:
        cat = notice.get("category", "기타")
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(notice)
    return grouped


def process_notices(analyzed_notices, user=None):
    if not analyzed_notices or not isinstance(analyzed_notices, list):
        return []
        
    step1_unique = remove_duplicates(analyzed_notices)
    step2_filtered = filter_notices(step1_unique, min_relevance=50)
    
    active_notices = []
    for notice in step2_filtered:
        dday = calculate_dday(notice.get("deadline"))
        if dday is None or dday >= 0:
            active_notices.append(notice)
            
    final_result = rank_notices(active_notices)
    return final_result


if __name__ == "__main__":
    mock_user = {
        "school": "국민대학교",
        "major": "전자공학부",
        "grade": 2,
        "activities": ["인턴", "공모전"],
        "interests": ["반도체", "AI"],
        "custom_interests": ["회로설계"]
    }

    mock_notices = [
        {"title": "[일반] 반도체 기업 인턴 참가자 모집", "category": "인턴", "deadline": "2026-10-15", "relevance": 95, "url": "https://example.com/1"},
        {"title": "[긴급] 전자공학부 장학금 추가 신청", "category": "장학금", "deadline": "2026-09-21", "relevance": 80, "url": "https://example.com/2"},
        {"title": "[안내] 디자인대학원 졸업 전시회", "category": "교내활동", "deadline": "2026-09-30", "relevance": 30, "url": "https://example.com/3"},
        {"title": "[재공지] 전자공학부 장학금 추가 신청합니다!", "category": "장학금", "deadline": "2026-09-21", "relevance": 80, "url": "https://example.com/2"},
        {"title": "[마감] 이미 기한이 지난 특강 안내", "category": "특강", "deadline": "2026-09-10", "relevance": 90, "url": "https://example.com/5"},
        {"title": "[안내] 창업동아리 상시 모집", "category": "교내활동", "deadline": "미정", "relevance": 70, "url": "https://example.com/4"}
    ]

    print("=== [단독 테스트: 뱃지 및 정렬 확인] ===")
    results = process_notices(mock_notices, user=mock_user)
    
    for r in results:
        print(f"[{r.get('urgency_label')}] 점수:{r.get('priority')} | {r.get('title')} ({r.get('category')})")
        
    print("\n=== [카테고리별 그룹화 결과 샘플] ===")
    grouped_res = group_by_category(results)
    print(list(grouped_res.keys()))