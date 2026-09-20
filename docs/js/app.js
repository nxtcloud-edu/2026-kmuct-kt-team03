const homePage = document.querySelector("#home-page");
const detailPage = document.querySelector("#detail-page");

const pages = document.querySelectorAll(".page");
const courseCards = document.querySelectorAll(".course-card");
const activities = document.querySelectorAll(".activity");
const backButtons = document.querySelectorAll(".back-button");

let previousPageId = "home-page";


function showPage(pageId) {
  pages.forEach(function (page) {
    page.classList.remove("active-page");
  });

  const targetPage = document.querySelector(
    "#" + pageId
  );

  targetPage.classList.add("active-page");

  window.scrollTo(0, 0);
}


courseCards.forEach(function (card) {
  card.addEventListener("click", function () {
    const courseId = card.dataset.course;

    previousPageId = courseId + "-page";

    showPage(previousPageId);
  });
});


activities.forEach(function (activity) {
  activity.addEventListener("click", function () {
    const type = activity.dataset.type;
    const course = activity.dataset.course;
    const title = activity.dataset.title;
    const description = activity.dataset.description;
    const deadline = activity.dataset.deadline;

    document.querySelector("#detail-type").textContent =
      type === "video"
        ? "온라인 강의"
        : type === "notice"
          ? "공지사항"
          : "과제";

    document.querySelector("#detail-title").textContent =
      title;

    document.querySelector("#detail-course").textContent =
      course;

    document.querySelector("#detail-description").textContent =
      description;

    document.querySelector("#detail-deadline").textContent =
      deadline === ""
        ? "별도 마감일 없음"
        : deadline;

    showPage("detail-page");
  });
});


backButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    if (button.id === "detail-back-button") {
      showPage(previousPageId);
    } else {
      showPage("home-page");
    }
  });
});


document
  .querySelector("#home-button")
  .addEventListener("click", function () {
    showPage("home-page");
  });


showPage("home-page");