import Link from "next/link";

type ProjectNavProps = { current?: "clover" | "machine" | "spray" };

export function ProjectNav({ current }: ProjectNavProps) {
  if (!current) {
    return (
      <header className="project-header global-header">
        <Link className="project-brand" href="/" aria-label="전체 프로젝트 허브 홈">
          <span>H</span><b>프로젝트 허브</b>
        </Link>
        <nav aria-label="전체 프로젝트 메뉴">
          <Link className="active" href="/">전체 프로젝트</Link>
          <details className="chat-switcher">
            <summary><span>프로젝트 메뉴</span><b>4개</b></summary>
            <div className="chat-menu-panel global-menu-panel">
              <p><small>SOFTM PROJECT HUB</small><strong>프로젝트 바로가기</strong></p>
              <Link href="/#hwagok"><small>농업·현장</small><strong>화곡농장</strong><span>파종계획 · 농기계 · 방제 · 농장 기록</span></Link>
              <a href="https://ungdo.softm.chatgpt.site"><small>토지·민원</small><strong>웅도 프로젝트</strong><span>토지현황 · 경계 · 성토 · 통화기록</span></a>
              <Link href="/#baksok"><small>음식점·경영</small><strong>서해박속낙지</strong><span>세무·매출 · 설비 · 매장 운영</span></Link>
              <a href="https://gyeongju-trip-map.softm.chatgpt.site"><small>가족·여행</small><strong>가족여행</strong><span>일정 · 동선 · 숙박 · 관광지</span></a>
            </div>
          </details>
        </nav>
      </header>
    );
  }

  return (
    <header className="project-header">
      <Link className="project-brand" href="/#hwagok" aria-label="전체 프로젝트 허브의 화곡농장 구역">
        <span>화</span><b>화곡농장</b>
      </Link>
      <nav aria-label="화곡농장 프로젝트 메뉴">
        <Link href="/">전체 프로젝트</Link>
        <Link href="/#hwagok">화곡농장 홈</Link>
        <details className="chat-switcher">
          <summary><span>채팅별 페이지</span><b>3개</b></summary>
          <div className="chat-menu-panel">
            <p><small>화곡농장 프로젝트</small><strong>채팅별 웹사이트</strong></p>
            <Link className={current === "clover" ? "current" : ""} href="/white-clover">
              <small>{current === "clover" ? "현재 페이지" : "재배·파종"}</small>
              <strong>화이트클로버 파종계획</strong>
              <span>2kg 종자·황토 배합·살포구역</span>
            </Link>
            <Link className={current === "machine" ? "current" : ""} href="/farm-machine-rental">
              <small>{current === "machine" ? "현재 페이지" : "농기계·행정"}</small>
              <strong>서산시 농기계 임대·운반 서비스</strong>
              <span>북부분소·준비서류·파종 장비</span>
            </Link>
            <Link className={current === "spray" ? "current" : ""} href="/spray-record-20260813">
              <small>{current === "spray" ? "현재 페이지" : "방제·작업기록"}</small>
              <strong>농막 아랫밭 나방노린채 살포</strong>
              <span>오전 7시·20L 2통·약제 20mL</span>
            </Link>
          </div>
        </details>
      </nav>
    </header>
  );
}
