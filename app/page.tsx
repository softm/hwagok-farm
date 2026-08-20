import Link from "next/link";
import { ProjectNav } from "./project-nav";

const chats = [
  {
    href: "/perilla-sowing-after-rain",
    kind: "재배·파종",
    title: "12mm 강우 후 늦파종 들깨 파종",
    description: "비가 그친 뒤 두둑의 흙 상태를 확인하고 늦파종 들깨 종자를 얕게 심는 시점과 방법을 정리했습니다.",
    meta: ["강수량 12mm", "파종 깊이 0.5~1cm", "표면 물기 확인"],
  },
  {
    href: "/cctv-internet-20260821",
    kind: "통신·CCTV",
    title: "농막·하우스 CCTV 인터넷 연결",
    description: "핫스팟, Extender N3, 유심·라우터와 Tapo 모델을 비교해 농막 CCTV 연결 방식을 정리했습니다.",
    meta: ["핫스팟", "Extender N3", "Tapo 모델 비교"],
  },
  {
    href: "/shade-net-20260807",
    kind: "시설·차양",
    title: "6평 농막 그늘막 예상 설치",
    description: "농막 차양막 하단에서 난간 상단까지 설치할 쉐이드네트의 예상 위치와 바닥 기준 치수를 사진으로 추정했습니다.",
    meta: ["긴 면 약 7.3m", "세로 1.8~1.9m", "권장 2×8m·2×5m"],
  },
  {
    href: "/white-clover",
    kind: "재배·파종",
    title: "화이트클로버 파종계획",
    description: "1kg 종자 기준 300평, 황토 배합과 살포 구역을 중심으로 정리한 파종 계획입니다.",
    meta: ["화이트클로버", "황토 배합", "파종 구역"],
  },
  {
    href: "/farm-machine-rental",
    kind: "농기계·행정",
    title: "서산시 농기계 임대·운반 서비스",
    description: "북부분소 이용 절차와 준비서류, 파종 장비 및 운반 서비스 정보를 정리했습니다.",
    meta: ["북부분소", "준비서류", "파종 장비"],
  },
  {
    href: "/moskill-20260527",
    kind: "방제·작업기록",
    title: "2026-05-27 모스킬 잎벌레 방제",
    description: "박밭 3개 두둑에 모스킬 약 50L를 살포하고 약 3시간 30분 뒤 비가 내린 현장 기록입니다.",
    meta: ["박밭 3개 두둑", "약 50L", "강우 전 3시간 30분"],
  },
  {
    href: "/spray-record-20260813",
    kind: "방제·작업기록",
    title: "농막 아랫밭 나방노린채 살포",
    description: "2026년 8월 13일 오전 7시, 농막 아랫밭에 20L 두 통을 살포한 현장 기록입니다.",
    meta: ["오전 7시", "20L 2통", "약제 10mL/통"],
  },
  {
    href: "/20260811-gourd-harvest/",
    kind: "수확·작업기록",
    title: "2026-08-11 박 수확 기록",
    description: "화곡농장에서 박 약 50통을 수확한 작업 과정과 현장 사진을 모았습니다.",
    meta: ["박 약 50통", "사진 53장", "재배지 전경"],
  },
  {
    href: "/onion-purchase-20260811",
    kind: "구매·보관",
    title: "2026-08-11 양파 구입·저온창고 보관",
    description: "농협 하나로마트 두 곳에서 양파를 구입해 차량으로 운반하고 화곡농장 저온창고에 보관한 기록입니다.",
    meta: ["구매비 453,000원", "약 37망 참고", "저온창고 보관"],
  },
  {
    href: "/sprinkler-thread-20260820",
    kind: "관수·부품",
    title: "스프링클러 나사 규격",
    description: "1/2인치와 3/4인치 배관 나사의 호칭과 실제 수나사 외경을 비교했습니다.",
    meta: ["1/2인치", "3/4인치", "수나사 외경"],
  },
  {
    href: "/fertilizer-plan",
    kind: "재배·시비",
    title: "들깨·열무 밑거름 시비계획",
    description: "4개 필지 1,641.3㎡의 작목 배치와 맞춤18호 살포량, 비황골드·명품비료의 역할을 정리했습니다.",
    meta: ["4개 필지", "맞춤18호 5포", "비료 비교"],
  },
  {
    href: "/freezer-electric-20260711",
    kind: "시설·전기",
    title: "2026-07-11 냉동고 전기 증설",
    description: "냉동고 전용 10SQ 전선 약 20m를 연결하고 누전차단기를 40A로 증설한 작업 기록입니다.",
    meta: ["10SQ 20m", "누전차단기 40A", "냉동고 전용"],
  },
  {
    href: "/farm-awning-repair-20260711",
    kind: "시설·행정",
    title: "2026-07-11 농막 차양막 시정조치",
    description: "지면까지 내려온 차양막 지지구조를 농막 본체의 대각선 보강 방식으로 수정한 전후 기록입니다.",
    meta: ["지면 기둥 개선", "대각선 보강", "전후 사진 8장"],
  },
];

export default function Home() {
  return (
    <main className="site-page">
      <ProjectNav />

      <section className="hub-hero">
        <div className="hub-hero-copy">
          <p className="kicker">HWAGOK FARM · CHAT ARCHIVE</p>
          <h1>화곡농장의 기록을<br /><em>채팅별로 모읍니다.</em></h1>
          <p>재배 계획부터 농기계, 방제, 관수와 수확까지 화곡농장에 해당하는 공개 기록만 이 프로젝트 안에서 관리합니다.</p>
          <a className="primary-button" href="#chats">채팅별 페이지 보기</a>
        </div>
        <aside className="hub-status">
          <span className="status-label">화곡농장 프로젝트</span>
          <strong>{chats.length}</strong>
          <b>공개 채팅 페이지</b>
          <div><span>프로젝트</span><b>화곡농장</b></div>
          <div><span>위치</span><b>충남 서산시 대산읍 화곡리</b></div>
          <div><span>최근 추가</span><b>2026. 8. 21.</b></div>
        </aside>
      </section>

      <section className="hub-section" id="chats">
        <div className="section-title">
          <p>HWAGOK FARM PAGES</p>
          <h2>화곡농장 채팅별 페이지</h2>
          <span>다른 프로젝트는 섞지 않고 화곡농장에 해당하는 배포 페이지만 표시합니다.</span>
        </div>
        <div className="chat-grid">
          {chats.map((chat, index) => (
            <article className="chat-card" key={chat.href}>
              <div className="chat-card-top"><span>{String(index + 1).padStart(2, "0")}</span><small>{chat.kind}</small></div>
              <h3>{chat.title}</h3>
              <p>{chat.description}</p>
              <ul>{chat.meta.map((item) => <li key={item}>{item}</li>)}</ul>
              <Link className="chat-card-link" href={chat.href}><b>페이지 열기</b><span>↗</span></Link>
            </article>
          ))}
        </div>
      </section>

      <section className="structure-section">
        <div><p>PROJECT BOUNDARY</p><h2>한 프로젝트에는<br />그 프로젝트의 기록만</h2></div>
        <ol>
          <li><span>01</span><div><b>화곡농장 전용 홈</b><p>화곡농장과 직접 관련된 채팅별 공개 페이지만 누적합니다.</p></div></li>
          <li><span>02</span><div><b>전체 프로젝트는 상위 인덱스</b><p>다른 프로젝트는 화곡농장 안에 나열하지 않고 전체 프로젝트 페이지에서 선택합니다.</p></div></li>
          <li><span>03</span><div><b>공개·비공개는 같은 프로젝트끼리</b><p><a href="https://hwagok.softm.chatgpt.site/#hwagok">화곡농장 비공개 사이트</a>와 이 공개 사이트를 서로 연결합니다.</p></div></li>
        </ol>
      </section>

      <footer className="site-footer">
        <b>화곡농장 프로젝트</b>
        <div><a href="https://softm.github.io/projects/">전체 프로젝트</a><a href="https://hwagok.softm.chatgpt.site/#hwagok">비공개 사이트</a><a href="#chats">채팅별 페이지</a></div>
      </footer>
    </main>
  );
}
