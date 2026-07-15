(() => {
  const main = document.querySelector("body > main");
  if (!main) return;

  const labels = [
    "환경 준비",
    "AI 호출",
    "형식 검증",
    "문서 근거",
    "Workflow",
    "Linux 특강",
    "문서 분할",
    "Vector 검색",
    "Retriever 평가",
    "Vector RAG",
    "RAG 평가",
    "Tool과 Agent",
    "미니 프로젝트",
  ];
  const current = Number.parseInt(location.pathname.match(/\/(\d{2})\.html$/)?.[1] ?? "-1", 10);

  const shell = document.createElement("div");
  shell.className = "section-page-shell";

  const aside = document.createElement("aside");
  aside.className = "section-menu";
  aside.setAttribute("aria-label", "전체 학습 Section");
  aside.innerHTML = `<p class="section-menu-title">전체 학습 Section</p><nav class="section-menu-list">${labels
    .map((label, index) => {
      const number = String(index).padStart(2, "0");
      const currentAttribute = index === current ? ' aria-current="page"' : "";
      return `<a class="section-menu-link" href="${number}.html"${currentAttribute}>${index}. ${label}</a>`;
    })
    .join("")}</nav>`;

  main.parentNode.insertBefore(shell, main);
  shell.append(aside, main);
})();
