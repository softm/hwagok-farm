import Link from "next/link";

type ProjectNavProps = { current?: "clover" | "machine" };

export function ProjectNav({ current }: ProjectNavProps) {
  return (
    <header className="project-header">
      <Link className="project-brand" href="/" aria-label="화곡농장 프로젝트 홈">
        <span>화</span><b>화곡농장</b>
      </Link>
      <nav aria-label="화곡농장 프로젝트 메뉴">
        <Link className={!current ? "active" : ""} href="/">프로젝트 홈</Link>
        <details className="chat-switcher">
          <summary><span>채팅별 페이지</span><b>2개</b></summary>
          <div className="chat-menu-panel">
            <p><small>화곡농장 프로젝트</small><strong>채팅별 웹사이트</strong></p>
            <Link className={current === "clover" ? "current" : ""} href="/white-clover">
              <small>{current === "clover" ? "현재 페이지" : "재배·파종"}</small>
              <strong>화이트클로버 파종계획</strong>
              <span>2kg 종자·황토 배합·75평 살포구역</span>
            </Link>
            <Link className={current === "machine" ? "current" : ""} href="/farm-machine-rental">
              <small>{current === "machine" ? "현재 페이지" : "농기계·행정"}</small>
              <strong>서산시 농기계 임대·운반 서비스</strong>
              <span>북부분소·준비서류·파종 장비</span>
            </Link>
          </div>
        </details>
      </nav>
    </header>
  );
}
