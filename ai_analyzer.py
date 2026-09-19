def analyze_notice(notice, user):

    relevance = 20
    reason = "사용자와 관련성이 낮습니다."

    text = notice["title"] + notice["content"]

    for interest in user["interests"]:
        if interest.lower() in text.lower():
            relevance = 90
            reason = f"관심 분야인 {interest}와 관련된 정보입니다."

    return {
        "title": notice["title"],
        "category": "기타",
        "deadline": "미정",
        "target": "대학생",
        "summary": notice["content"],
        "action": "공지 확인",
        "relevance": relevance,
        "reason": reason,
        "url": notice["url"]
    }