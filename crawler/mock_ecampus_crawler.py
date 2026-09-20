import requests
from bs4 import BeautifulSoup

MOCK_URL = "https://nxtcloud-edu.github.io/2026-kmuct-kt-team03/"
TIMEOUT = 10

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_text(text):
    return " ".join((text or "").split())


def get_mock_ecampus_notices():
    """로컬 Mock eCampus의 과제·공지 데이터를 수집한다."""
    try:
        response = requests.get(
            MOCK_URL,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"[Mock eCampus 접속 실패] {error}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # 과제 카드 수집: 마감일을 date에 넣는다.
    for item in soup.select(".modtype_assign"):
        results.append({
            "title": clean_text(item.get("data-title")),
            "url": MOCK_URL,
            "date": clean_text(item.get("data-deadline")) or None,
            "content": (
                f"과목: {clean_text(item.get('data-course'))} / "
                f"내용: {clean_text(item.get('data-description'))}"
            ),
            "source": "Mock eCampus 과제"
        })

    # eCampus 공지 카드 수집
    for item in soup.select(".modtype_notice"):
        results.append({
            "title": clean_text(item.get("data-title")),
            "url": MOCK_URL,
            "date": clean_text(item.get("data-deadline")) or None,
            "content": (
                f"과목: {clean_text(item.get('data-course'))} / "
                f"내용: {clean_text(item.get('data-description'))}"
            ),
            "source": "Mock eCampus 공지"
        })

    return results


if __name__ == "__main__":
    notices = get_mock_ecampus_notices()

    print(f"\n수집한 Mock eCampus 항목: {len(notices)}개\n")

    for notice in notices:
        print(f"제목: {notice['title']}")
        print(f"날짜/마감일: {notice['date']}")
        print(f"출처: {notice['source']}")
        print(f"링크: {notice['url']}")
        print("-" * 60)