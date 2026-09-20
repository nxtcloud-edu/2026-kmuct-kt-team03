import requests
from bs4 import BeautifulSoup


URL = "http://127.0.0.1:5500/index.html"


response = requests.get(URL, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(
    response.text,
    "html.parser"
)


assignments = soup.select(".modtype_assign")
videos = soup.select(".modtype_xncommons")
notices = soup.select(".modtype_notice")


print("\n========== 과제 ==========")

for item in assignments:
    print("\n과목:", item.get("data-course"))
    print("제목:", item.get("data-title"))
    print("설명:", item.get("data-description"))
    print("마감일:", item.get("data-deadline"))


print("\n========== 온라인 강의 ==========")

for item in videos:
    print("\n과목:", item.get("data-course"))
    print("제목:", item.get("data-title"))
    print("설명:", item.get("data-description"))
    print("학습 마감일:", item.get("data-deadline"))


print("\n========== 공지사항 ==========")

for item in notices:
    print("\n과목:", item.get("data-course"))
    print("제목:", item.get("data-title"))
    print("내용:", item.get("data-description"))