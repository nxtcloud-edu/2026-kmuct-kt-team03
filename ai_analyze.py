import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# --------------------------------------------------
# Gemini API 설정
# --------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 키가 없어도 파일 import 자체는 가능하게 처리한다.
client = (
    genai.Client(api_key=GEMINI_API_KEY)
    if GEMINI_API_KEY
    else None
)


def make_fallback_result(notice):
    """
    AI 분석에 실패했을 때 반환할 기본 결과.
    API 오류가 발생해도 전체 프로그램이 멈추지 않게 한다.
    """

    return {
        "title": notice.get("title", ""),
        "url": notice.get("url", ""),
        "date": notice.get("date"),
        "content": notice.get("content", ""),
        "source": notice.get("source", ""),
        "category": "기타",
        "deadline": None,
        "target": "확인 필요",
        "summary": "AI 분석에 실패했습니다.",
        "action": "원문 확인 필요",
        "relevance": 0,
        "reason": "AI 분석 중 오류가 발생했습니다."
    }


def normalize_relevance(value):
    """relevance를 항상 0~100 사이 정수로 만든다."""

    try:
        value = int(value)
    except (TypeError, ValueError):
        return 0

    return max(0, min(value, 100))


def analyze_notice(notice: dict, user: dict) -> dict:
    """
    크롤러에서 받은 공지 하나를 사용자 정보와 비교하여
    Gemini API로 분석한다.
    """

    if not isinstance(notice, dict):
        notice = {}

    if not isinstance(user, dict):
        user = {}

    title = notice.get("title", "")
    url = notice.get("url", "")
    date = notice.get("date")
    content = notice.get("content", "")
    source = notice.get("source", "")

    school = user.get("school", "")
    major = user.get("major", "")
    grade = user.get("grade", "")
    activities = user.get("activities", [])
    interests = user.get("interests", [])
    custom_interests = user.get("custom_interests", [])

    prompt = f"""
당신은 대학생을 위한 개인 맞춤형 공지 분석 AI입니다.

아래 사용자 정보와 공지사항을 비교하여
공지의 핵심 정보를 추출하고 사용자와의 관련성을 판단하세요.

[사용자 정보]

학교: {school}
학과: {major}
학년: {grade}
원하는 활동 유형: {activities}
관심 기술 분야: {interests}
기타 관심 분야: {custom_interests}

[공지사항]

제목: {title}
출처: {source}
작성일 또는 마감일: {date}

본문:
{content}

[분석 항목]

1. category

다음 중 가장 적절한 종류 하나를 선택하세요.

- 장학금
- 인턴
- 현장실습
- 취업
- 채용
- 공모전
- 해커톤
- 대외활동
- 연구
- 학부연구생
- 창업
- 교환학생
- 해외 프로그램
- 봉사활동
- 동아리
- 자격증
- 교육 프로그램
- 대학원
- 진학
- 과제
- 특강
- 교내활동
- 기타

2. deadline

신청, 접수 또는 과제 제출 마감일을 추출하세요.

가능하면 YYYY-MM-DD 형식으로 반환하세요.

작성일과 마감일을 혼동하지 마세요.
마감일을 확인할 수 없다면 null을 반환하세요.

3. target

공지에 실제로 명시된 지원 대상 또는 참가 대상을
간단하게 정리하세요.

지원 대상이 명시되지 않았다면
"명시되지 않음"이라고 작성하세요.

4. summary

공지의 핵심 내용을 사용자가 빠르게 이해할 수 있도록
1~2문장으로 요약하세요.

5. action

사용자가 해야 할 행동을 간단하게 작성하세요.

예:
"9월 25일까지 온라인 지원서 제출"

신청 방법이나 행동을 알 수 없다면
"원문 확인"이라고 작성하세요.

6. relevance

사용자와의 관련성을 0~100 사이 정수로 평가하세요.

다음 사항을 종합적으로 고려하세요.

- 사용자 학교
- 사용자 학과
- 사용자 학년
- 원하는 활동 유형
- 관심 기술 분야
- 기타 관심 분야
- 공지의 실제 지원 대상

사용자가 필수 지원 조건을 충족하지 못하면
관련성 점수를 낮게 평가하세요.

같은 단어가 있다는 이유만으로 높은 점수를 주지 말고
공지의 실제 의미와 지원 조건을 판단하세요.

7. reason

해당 관련성 점수를 준 이유를
사용자 정보와 공지 내용을 비교하여 1~2문장으로 설명하세요.

[중요 규칙]

공지에 없는 정보를 만들어내지 마세요.

지원 자격, 날짜, 혜택, 신청 방법을
임의로 추측하지 마세요.

확인할 수 없는 정보는 null 또는
"명시되지 않음"으로 처리하세요.

공지에 특정 학과나 학년 제한이 없다면
제한이 있다고 가정하지 마세요.
"""

    try:
        if client is None:
            raise ValueError(
                "GEMINI_API_KEY가 없습니다. "
                "프로젝트 최상단의 .env 파일을 확인하세요."
            )

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string"
                        },
                        "deadline": {
                            "type": ["string", "null"]
                        },
                        "target": {
                            "type": "string"
                        },
                        "summary": {
                            "type": "string"
                        },
                        "action": {
                            "type": "string"
                        },
                        "relevance": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "reason": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "category",
                        "deadline",
                        "target",
                        "summary",
                        "action",
                        "relevance",
                        "reason"
                    ]
                }
            )
        )

        if not response.text:
            raise ValueError("Gemini가 빈 응답을 반환했습니다.")

        ai_result = json.loads(response.text)

        return {
            "title": title,
            "url": url,
            "date": date,
            "content": content,
            "source": source,
            "category": ai_result.get("category", "기타"),
            "deadline": ai_result.get("deadline"),
            "target": ai_result.get(
                "target",
                "명시되지 않음"
            ),
            "summary": ai_result.get("summary", ""),
            "action": ai_result.get(
                "action",
                "원문 확인"
            ),
            "relevance": normalize_relevance(
                ai_result.get("relevance", 0)
            ),
            "reason": ai_result.get(
                "reason",
                "관련성 판단 이유를 확인할 수 없습니다."
            )
        }

    except Exception as error:
        print(f"[AI 분석 실패] {title} - {error}")
        return make_fallback_result(notice)


def analyze_notices(notices: list[dict], user: dict) -> list[dict]:
    """
    크롤러가 반환한 여러 공지를 하나씩 분석한다.
    공지 하나가 실패해도 나머지 공지는 계속 분석한다.
    """

    if not isinstance(notices, list):
        return []

    analyzed_results = []

    for notice in notices:
        analyzed_results.append(
            analyze_notice(notice, user)
        )

    return analyzed_results