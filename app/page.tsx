import { ProjectNav } from "./project-nav";

const chats = [
  {
    href: "/white-clover",
    number: "01",
    label: "재배·파종",
    title: "화이트클로버 파종계획",
    description: "엄나무밭 약 622평에 종자 2kg을 저밀도로 도입하는 살포구역, 황토 배합, 현장 작업안입니다.",
    facts: ["종자 2kg", "1kg / 300평", "황토 40kg"],
  },
  {
    href: "/farm-machine-rental",
    number: "02",
    label: "농기계·행정",
    title: "서산시 농기계 임대·운반 서비스",
    description: "대산읍 북부분소를 기준으로 임대 조건, 준비서류, 운반 절차와 파종 장비를 정리했습니다.",
    facts: ["북부분소", "041-681-1006", "파종 장비"],
  },
];

export default function Home() {
  return (
    <main className="site-page">
      <ProjectNav />
      <section className="hub-hero">
        <div className="hub-hero-copy">
          <p className="kicker">PROJECT HUB · 충남 서산시 대산읍</p>
          <h1>화곡농장의 모든 작업을<br /><em>한곳에서 관리합니다.</em></h1>
          <p>프로젝트당 하나의 웹사이트를 사용하고, 각 채팅 작업은 하위 페이지로 계속 추가합니다. 지도·보고서·현장 실행안을 공통 메뉴에서 바로 찾을 수 있습니다.</p>
          <a className="primary-button" href="#chats">채팅별 페이지 보기</a>
        </div>
        <aside className="hub-status" aria-label="프로젝트 현황">
          <span className="status-label">화곡농장 프로젝트</span>
          <strong>2</strong><b>현재 등록된 채팅 페이지</b>
          <div><span>최근 갱신</span><b>2026. 8. 19.</b></div>
          <div><span>기준 지역</span><b>서산시 대산읍 화곡리</b></div>
          <div><span>배포 방식</span><b>프로젝트 중앙화</b></div>
        </aside>
      </section>

      <section className="hub-section" id="chats">
        <div className="section-title">
          <p>PROJECT CHATS</p>
          <h2>채팅별 웹사이트</h2>
          <span>아래 작업은 모두 화곡농장 프로젝트의 하위 페이지입니다.</span>
        </div>
        <div className="chat-grid">
          {chats.map((chat) => (
            <a className="chat-card" href={chat.href} key={chat.href}>
              <div className="chat-card-top"><span>{chat.number}</span><small>{chat.label}</small></div>
              <h3>{chat.title}</h3>
              <p>{chat.description}</p>
              <ul>{chat.facts.map((fact) => <li key={fact}>{fact}</li>)}</ul>
              <b className="chat-card-link">페이지 열기 <span>→</span></b>
            </a>
          ))}
        </div>
      </section>

      <section className="structure-section">
        <div>
          <p>GLOBAL DEPLOYMENT RULE</p>
          <h2>앞으로도 같은 구조로 누적됩니다.</h2>
        </div>
        <ol>
          <li><span>01</span><div><b>프로젝트당 사이트 1개</b><p>화곡농장은 이 프로젝트 사이트를 계속 사용합니다.</p></div></li>
          <li><span>02</span><div><b>채팅당 하위 페이지 1개</b><p>새 작업은 독립된 경로와 메뉴 항목으로 추가합니다.</p></div></li>
          <li><span>03</span><div><b>자료는 레이어로 확인</b><p>이미지·문서·영상은 목록에서 누르면 확대해 볼 수 있게 구성합니다.</p></div></li>
        </ol>
      </section>
      <footer className="site-footer"><b>화곡농장 프로젝트</b><span>프로젝트 홈 · 채팅별 하위 페이지 · 중앙화 배포</span></footer>
    </main>
  );
}
