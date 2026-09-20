import datetime


def remove_duplicates(notices):
    if not notices or not isinstance(notices, list):
        return []

    seen_keys = set()
    unique_notices = []

    for notice in notices:
        if not isinstance(notice, dict):
            continue

        url = notice.get("url", "").strip()
        title = notice.get("title", "").strip()

        unique_key = url if url else title
        if not unique_key:
            continue

        if unique_key not in seen_keys:
            seen_keys.add(unique_key)
            unique_notices.append(notice)

    return unique_notices


def filter_notices(notices, min_relevance=50):
    filtered_notices = []

    for notice in notices:
        relevance = notice.get("relevance")
        if not isinstance(relevance, (int, float)):
            relevance = 0

        if relevance >= min_relevance:
            filtered_notices.append(notice)

    return filtered_notices


def calculate_dday(deadline_str):
    if not deadline_str or str(deadline_str).strip() == "미정":
        return None

    try:
        today = datetime.date(2026, 9, 20)
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
        if dday < 0:
            bonus = -50
        elif 0 <= dday <= 1:
            bonus = 30
        elif 2 <= dday <= 3:
            bonus = 15
        elif 4 <= dday <= 7:
            bonus = 5
        else:
            bonus = 0

    return relevance + bonus


def rank_notices(notices):
    for notice in notices:
        deadline = notice.get("deadline")
        notice["dday"] = calculate_dday(deadline)
        notice["priority"] = calculate_priority(notice)

    ranked_notices = sorted(notices, key=lambda x: x.get("priority", 0), reverse=True)
    return ranked_notices


def process_notices(analyzed_notices, user=None):
    if not analyzed_notices or not isinstance(analyzed_notices, list):
        return []

    step1_unique = remove_duplicates(analyzed_notices)
    step2_filtered = filter_notices(step1_unique, min_relevance=50)
    final_result = rank_notices(step2_filtered)

    return final_result


if __name__ == "__main__":
    mock_user = {
        "school": "국민대학교",
        "major": "전자공학부",
        "grade": 2,
        "interests": ["반도체", "AI", "공모전"]
    }

    mock_notices = [
        {"title": "[일반] 반도체 기업 인턴 참가자 모집", "deadline": "2026-10-15", "relevance": 95, "url": "https://example.com/1"},
        {"title": "[긴급] 전자공학부 장학금 추가 신청", "deadline": "2026-09-21", "relevance": 80, "url": "https://example.com/2"},
        {"title": "[안내] 디자인대학원 졸업 전시회", "deadline": "2026-09-30", "relevance": 30, "url": "https://example.com/3"},
        {"title": "[재공지] 전자공학부 장학금 추가 신청합니다!", "deadline": "2026-09-21", "relevance": 80,
         "url": "https://example.com/2"},
        {"title": "[안내] 창업동아리 상시 모집", "deadline": "미정", "relevance": 70, "url": "https://example.com/4"}
    ]

    results = process_notices(mock_notices, user=mock_user)

    for r in results:
        title = r.get("title")
        rel = r.get("relevance")
        dday = r.get("dday")
        priority = r.get("priority")

        if dday is None:
            dday_str = "미정"
        elif dday < 0:
            dday_str = "마감됨"
        else:
            dday_str = f"D-{dday}"

        print(f"[{dday_str}] 최종 점수: {priority} (기본: {rel}) | {title}")

# 1. 중복된 공지를 제거한다.
# 들어온 공지가 없으면 빈 결과를 돌려준다.
# URL이 같거나, URL이 없는데 제목이 같으면 똑같은 공지로 취급한다.
# 처음 보는 공지만 남겨두고, 이미 본 공지는 버린다.
#
# 2. 나랑 관련 없는 공지는 버린다.
# AI가 매긴 관련도 점수가 없거나 이상하면 0점으로 처리한다.
# 관련도 점수가 50점 이상인 것만 합격시키고, 50점 미만은 가차 없이 버린다.
#
# 3. 마감일을 계산한다 (D-Day).
# 마감일이 적혀있지 않거나 '미정'이라고 되어있으면 계산하지 않는다.
# 오늘 날짜를 기준으로 마감일까지 며칠 남았는지 계산한다.
# 남은 날짜를 계산해 숫자로 돌려준다.
#
# 4. 최종 순위 점수를 계산한다.
# 마감일이 얼마나 남았는지에 따라 보너스 점수를 부여한다.
# 이미 지난 마감일은 점수를 크게 깎는다 (-50점).
# 0~1일 남았으면 아주 큰 보너스를 준다 (+30점).
# 2~3일 남았으면 중간 보너스를 준다 (+15점).
# 4~7일 남았으면 작은 보너스를 준다 (+5점).
# 8일 이상 넉넉히 남았으면 보너스를 주지 않는다.
# AI가 평가한 기본 점수에 이 마감일 보너스를 합산해서 돌려준다.
#
# 5. 최종 점수가 높은 순서대로 줄을 세운다.
# 모든 공지마다 마감일과 최종 점수를 계산해서 꼬리표를 달아준다.
# 최종 점수가 가장 높은 공지부터 맨 위에 오도록 차례대로 정렬한다.
#
# 6. 전체 실행 (메인 파이프라인)
# 1단계: 똑같은 공지를 버린다.
# 2단계: 50점 미만인 쓸모없는 공지를 버린다.
# 3단계: 살아남은 공지들의 마감일을 계산하고 우선순위 점수대로 줄을 세운다.
# 이 모든 정리를 마친 깔끔한 최종 결과물을 다음 팀원(UI 담당)에게 넘겨준다.