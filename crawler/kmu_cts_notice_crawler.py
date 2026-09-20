import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


KMI_CTS_NOTICE_URL = (
    "https://kmu-cts.kookmin.ac.kr/kmu-cts/etc/sitemap016.do"
)

TIMEOUT = 10
MAX_NOTICES = 20
CUTOFF_DATE = "2026-07-01"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_text(text):
    """줄바꿈과 여러 공백을 한 칸으로 정리한다."""
    return " ".join((text or "").split())


def get_soup(url):
    """URL에 접속하여 BeautifulSoup 객체를 반환한다."""
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        return BeautifulSoup(
            response.text,
            "html.parser"
        )

    except requests.RequestException as error:
        print(f"[미래융합대학 접속 실패] {error}")
        return None


def extract_date(text):
    """문자열에서 YYYY-MM-DD 또는 YY.MM.DD 날짜를 추출한다."""
    text = text or ""

    # YYYY-MM-DD 형식
    match = re.search(
        r"\b(20\d{2})[-.](\d{1,2})[-.](\d{1,2})\b",
        text
    )

    if match is not None:
        year, month, day = match.groups()

        return (
            f"{year}-"
            f"{int(month):02d}-"
            f"{int(day):02d}"
        )

    # YY.MM.DD 형식
    match = re.search(
        r"\b(\d{2})[.](\d{1,2})[.](\d{1,2})\b",
        text
    )

    if match is not None:
        year, month, day = match.groups()

        return (
            f"20{year}-"
            f"{int(month):02d}-"
            f"{int(day):02d}"
        )

    return None


def get_kmu_cts_notice_content(url):
    """미래융합대학 공지 상세 페이지에서 본문을 가져온다."""
    soup = get_soup(url)

    if soup is None:
        return ""

    selectors = [
        ".fr-view",
        ".b-content-box",
        ".board-view-content",
        ".board_view_content",
        ".view-content",
        ".view_cont"
    ]

    for selector in selectors:
        content_area = soup.select_one(selector)

        if content_area is not None:
            content = clean_text(
                content_area.get_text(" ", strip=True)
            )

            if content:
                return content

    return ""


def crawl_kmu_cts_notices():
    """국민대학교 미래융합대학 공지를 수집한다."""
    soup = get_soup(KMI_CTS_NOTICE_URL)

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

            # 날짜가 없거나 2026-07-01 이전이면 제외한다.
            if (
                published_date is None
                or published_date < CUTOFF_DATE
            ):
                continue

            article_url = urljoin(
                KMI_CTS_NOTICE_URL,
                title_link.get("href", "")
            )

            notice = {
                "title": clean_text(
                    title_link.get_text(" ", strip=True)
                ),
                "url": article_url,
                "date": published_date,
                "content": get_kmu_cts_notice_content(
                    article_url
                ),
                "source": "국민대학교 미래융합대학"
            }

            notices.append(notice)

            if len(notices) >= MAX_NOTICES:
                break

        except Exception as error:
            # 공지 하나가 실패해도 다음 공지를 계속 수집한다.
            print(
                f"[미래융합대학 게시글 수집 실패] "
                f"{error}"
            )
            continue

    return notices


if __name__ == "__main__":
    notices = crawl_kmu_cts_notices()

    print(
        f"\n수집한 공지 개수: "
        f"{len(notices)}개\n"
    )

    for notice in notices:
        print(f"제목: {notice['title']}")
        print(f"날짜: {notice['date']}")
        print(f"출처: {notice['source']}")
        print(f"링크: {notice['url']}")
        print("-" * 60)