
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

try:
    # 다른 팀원이 from crawler import get_notices로 사용할 때
    from .mock_ecampus_crawler import get_mock_ecampus_notices
    from .nccoss_notice_crawler import crawl_nccoss_notices
    from .cieek_notice_crawler import crawl_cieek_notices
    from .kmu_cts_notice_crawler import crawl_kmu_cts_notices

except ImportError:
    # python crawler/crawler.py로 직접 실행할 때
    from mock_ecampus_crawler import get_mock_ecampus_notices
    from nccoss_notice_crawler import crawl_nccoss_notices
    from cieek_notice_crawler import crawl_cieek_notices
    from kmu_cts_notice_crawler import crawl_kmu_cts_notices



EE_NOTICE_URL = "https://ee.kookmin.ac.kr/community/board/notice/"
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

        return BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as error:
        print(f"[접속 실패] {url} - {error}")
        return None


def get_notice_content(url):
    """공지 상세 페이지에서 본문을 가져온다."""
    soup = get_soup(url)

    if soup is None:
        return ""

    content_cell = soup.select_one("td.board-view-content")

    if content_cell is None:
        return ""

    return clean_text(
        content_cell.get_text(" ", strip=True)
    )


def crawl_ee_notices():
    """국민대학교 전자공학부 학부공지를 수집한다."""
    soup = get_soup(EE_NOTICE_URL)

    if soup is None:
        return []

    notices = []
    rows = soup.select("table tbody tr")

    for row in rows:
        try:
            cells = row.find_all("td")

            if len(cells) < 4:
                continue

            title_link = cells[1].find("a", href=True)

            if title_link is None:
                continue

            published_date = (
                clean_text(cells[3].get_text()) or None
            )

            # 2026-07-01 이전 공지와 날짜 없는 공지는 제외한다.
            if (
                published_date is None
                or published_date < CUTOFF_DATE
            ):
                continue

            article_url = urljoin(
                EE_NOTICE_URL,
                title_link["href"]
            )

            notice = {
                "title": clean_text(title_link.get_text()),
                "url": article_url,
                "date": published_date,
                "content": get_notice_content(article_url),
                "source": "국민대학교 전자공학부"
            }

            notices.append(notice)

            if len(notices) >= MAX_NOTICES:
                break

        except Exception as error:
            # 한 게시글이 실패해도 다음 게시글은 계속 수집한다.
            print(f"[게시글 수집 실패] {error}")
            continue

    return notices
def normalize_title(title):
    """제목을 비교하기 쉽게 정리한다."""
    return "".join(
        character.lower()
        for character in (title or "")
        if character.isalnum()
    )

def remove_duplicates(notices):
    """정리된 제목이 같은 공지를 제거한다."""
    unique_notices = []
    seen_titles = set()

    for notice in notices:
        title_key = normalize_title(
            notice.get("title", "")
        )

        if title_key and title_key in seen_titles:
            continue

        unique_notices.append(notice)

        if title_key:
            seen_titles.add(title_key)

    return unique_notices

def get_notices(user: dict) -> list[dict]:
    """
    국민대학교 공개 홈페이지와 Mock eCampus에서
    공지 및 과제 정보를 수집한다.
    """
    school = str(
        user.get("school", "")
    ).strip()

    major = str(
        user.get("major", "")
    ).strip()

    if "국민" not in school:
        return []

    results = []

    # 전자공학부 공지
    if not major or "전자" in major:
        try:
            results.extend(
                crawl_ee_notices()
            )
        except Exception as error:
            print(
                f"[전자공학부 전체 수집 실패] "
                f"{error}"
            )

    # 차세대통신사업단 공지
    try:
        results.extend(
            crawl_nccoss_notices()
        )
    except Exception as error:
        print(
            f"[차세대통신사업단 전체 수집 실패] "
            f"{error}"
        )

    # 공학교육혁신센터 공지
    try:
        results.extend(
            crawl_cieek_notices()
        )
    except Exception as error:
        print(
            f"[공학교육혁신센터 전체 수집 실패] "
            f"{error}"
        )

    # 미래융합대학 공지
    try:
        results.extend(
            crawl_kmu_cts_notices()
        )
    except Exception as error:
        print(
            f"[미래융합대학 전체 수집 실패] "
            f"{error}"
        )

    # Mock eCampus 과제 및 공지
    try:
        results.extend(
            get_mock_ecampus_notices()
        )
    except Exception as error:
        print(
            f"[Mock eCampus 전체 수집 실패] "
            f"{error}"
        )

    return remove_duplicates(results)