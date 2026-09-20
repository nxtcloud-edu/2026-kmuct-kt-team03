# Mock eCampus

2026학년도 2학기 eCampus를 본떠 만든 시연용 Mock 웹사이트입니다.

## 구현 기능

- 5개 강의 카드 표시
- 강의별 주차 활동 표시
- 과제, 온라인 강의, 공지사항 구분
- 과제 상세 화면 표시
- BeautifulSoup 크롤링 가능 구조

## 실행 방법

1. VS Code에서 `index.html`을 엽니다.
2. `index.html`을 우클릭합니다.
3. `Open with Live Server`를 클릭합니다.
4. 브라우저에서 사이트를 확인합니다.

## 크롤러 실행

먼저 터미널에서 라이브러리를 설치합니다.

```bash
python -m pip install -r crawler/requirements.txt