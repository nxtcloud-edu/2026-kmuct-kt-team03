import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


NCCOSS_NOTICE_URL = (
    "https://nccoss.kookmin.ac.kr/NCCOSS/community/notice.do"
)

TIMEOUT = 10
MAX_NOTICES = 20
CUTOFF_DATE = "2026-07-01"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_text(text):
    return " ".join((text or "").split())


def get_soup(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        return BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as error:
        print(f"[차세대통신사업단 접속 실패] {error}")
        return None


def extract_date(text):
    """문자열 안에서 YYYY-MM-DD 날짜를 찾아 반환한다."""
    match = re.search(r"\d{4}-\d{2}-\d{2}", text or "")

    if match is None:
        return None

    return match.group()


def get_nccoss_notice_content(url):
    """상세 공지 페이지에서 본문을 가져온다."""
    soup = get_soup(url)

    if soup is None:
        return ""

    selectors = [
        ".fr-view",
        ".board-view-content",
        ".board_view_content",
        ".bbs_view",
        ".view_cont",
        ".view-content"
    ]

    for selector in selectors:
        content_area = soup.select_one(selector)

        if content_area is not None:
            return clean_text(
                content_area.get_text(" ", strip=True)
            )

    return ""


def crawl_nccoss_notices():
    """차세대통신사업단 공지사항을 수집한다."""
    soup = get_soup(NCCOSS_NOTICE_URL)

    if soup is None:
        return []

    notices = []
    rows = soup.select("table tbody tr")

    for row in rows:
        try:
            title_link = row.select_one(
                "a[href*='articleNo=']"
            )

            if title_link is None:
                continue

            published_date = extract_date(
                row.get_text(" ", strip=True)
            )

            if (
                published_date is None
                or published_date < CUTOFF_DATE
            ):
                continue

            article_url = urljoin(
                NCCOSS_NOTICE_URL,
                title_link["href"]
            )

            notices.append({
                "title": clean_text(title_link.get_text()),
                "url": article_url,
                "date": published_date,
                "content": get_nccoss_notice_content(article_url),
                "source": "국민대학교 차세대통신사업단"
            })

            if len(notices) >= MAX_NOTICES:
                break

        except Exception as error:
            print(f"[차세대통신사업단 게시글 수집 실패] {error}")
            continue

    return notices


if __name__ == "__main__":
    notices = crawl_nccoss_notices()

    print(f"\n수집한 공지 개수: {len(notices)}개\n")

    for notice in notices:
        print(f"제목: {notice['title']}")
        print(f"날짜: {notice['date']}")
        print(f"출처: {notice['source']}")
        print(f"링크: {notice['url']}")
        print("-" * 60)