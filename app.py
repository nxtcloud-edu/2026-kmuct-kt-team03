from crawler import get_notices
from ai_analyzer import analyze_notice
from agent import rank_notices


user = {
    "school": "국민대학교",
    "major": "전자공학부",
    "grade": 2,
    "interests": ["반도체", "AI"]
}


# 1. 공지 가져오기
notices = get_notices()

print("===== 크롤링 결과 =====")
print(notices)


# 2. 공지 분석
analyzed = []

for notice in notices:
    result = analyze_notice(notice, user)
    analyzed.append(result)


print("\n===== AI 분석 결과 =====")
print(analyzed)


# 3. 관련도 순 정렬
results = rank_notices(analyzed)


print("\n===== 최종 결과 =====")

for result in results:
    print()
    print("제목:", result["title"])
    print("관련도:", result["relevance"])
    print("이유:", result["reason"])