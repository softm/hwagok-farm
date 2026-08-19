import Link from "next/link";
import { ProjectNav } from "../project-nav";

const offices = [
  ["본소", "인지면 무학재1길 99", "041-669-5951"],
  ["북부분소", "대산읍 대산1로 70", "041-681-1006"],
  ["동부분소", "운산면 홍안벌로 501", "041-688-7766"],
  ["중부분소", "성연면 생동사동길 21", "041-662-3315"],
];

const steps = [
  ["01", "장비·일정 확인", "북부분소에 필요한 장비, 사용일, 운반 가능 여부를 먼저 확인합니다."],
  ["02", "서류 준비", "농업경영체 등록자료와 농업인 NH안전보험 가입증명서를 준비합니다."],
  ["03", "임대·운반 예약", "농지 주소, 작업 목적, 왕복 운반 여부와 진입 조건을 함께 전달합니다."],
  ["04", "계약·결제", "임대차계약서를 작성하고 임대료와 운반료를 카드로 납부합니다."],
  ["05", "안전 사용", "작동 설명을 듣고 사용한 뒤 세척·연료 보충 후 약속한 시각에 반납합니다."],
];

const equipment = [
  ["기존 풀 제거", "예초기·보행형 제초기", "큰 풀을 낮게 제거하고 씨앗이 맺히기 전에 작업"],
  ["표면 정리", "소형 관리기·보행형 로터리", "엄나무 뿌리를 피해 흙 표면만 얕게 정리"],
  ["파종", "손 회전식 살포기·소형 파종기", "작은 씨앗을 마른 황토와 섞어 고르게 살포"],
  ["진압", "소형 진압기", "복토를 두껍게 하지 않고 씨앗과 흙을 밀착"],
];

export default function FarmMachineRentalPage() {
  return (
    <main className="site-page detail-page machine-page">
      <ProjectNav current="machine" />
      <section className="detail-hero machine-hero" id="top">
        <div>
          <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>농기계 임대·운반 서비스</b></p>
          <p className="kicker">2026. 8. 18. · 충남 서산시 대산읍 화곡리</p>
          <h1>농기계는 빌리고,<br /><em>밭까지 운반</em>받으세요.</h1>
          <p className="hero-description">화곡농장의 화이트클로버 파종 준비에 맞춰 임대 대상, 준비서류, 추천 장비와 연락처를 한곳에 정리했습니다.</p>
          <div className="hero-actions"><a className="primary-button" href="tel:0416811006">북부분소 전화하기</a><a className="outline-button" href="https://seosan.amlend.kr/" target="_blank" rel="noreferrer">공식 임대 사이트</a></div>
          <p className="updated">확인 기준일 2026. 8. 18. · 예약 시 현행 조건 재확인</p>
        </div>
        <aside className="metric-card machine-card">
          <small>이용 가능성 높음</small><h2>화곡농장 적용 판단</h2>
          <dl><div><dt>농지</dt><dd>서산시 관내</dd></div><div><dt>면적</dt><dd>1,641㎡ · 약 496평</dd></div><div><dt>담당</dt><dd>북부분소</dd></div><div><dt>우선 장비</dt><dd>소형 관리기 + 살포기 + 진압기</dd></div></dl>
          <a className="big-phone" href="tel:0416811006">041-681-1006</a>
        </aside>
      </section>

      <section className="quick-strip machine-strip" aria-label="핵심 요약">
        <div><span>01</span><p><b>농업경영체</b>등록 확인자료 준비</p></div>
        <div><span>02</span><p><b>안전보험</b>NH안전보험 증명서</p></div>
        <div><span>03</span><p><b>임대 기간</b>1농가 1대, 최대 3일</p></div>
        <div><span>04</span><p><b>운반료</b>왕복 4만 원 노출·확인</p></div>
      </section>

      <section className="content-section" id="eligibility">
        <div className="section-title"><p>ELIGIBILITY</p><h2>화곡농장이 이용할 수 있나요?</h2><span>현재 확인된 조건으로는 임대 대상에 해당할 가능성이 높습니다.</span></div>
        <div className="eligibility-layout">
          <div className="check-list"><div><b>✓</b><span><strong>관내 농지</strong>서산시 대산읍 화곡리</span></div><div><b>✓</b><span><strong>농업경영체</strong>등록 보유</span></div><div><b>✓</b><span><strong>경작면적</strong>약 0.1641ha</span></div><div><b>!</b><span><strong>안전보험</strong>가입증명서 발급·제출 필요</span></div></div>
          <aside className="notice-card"><small>운반 전 확인</small><h3>농지 안쪽 배송은 현장 조건에 따라 달라집니다.</h3><p>운반차 진입로 폭, 경사, 지반 상태와 농지 입구의 회차 공간을 전화로 설명하세요.</p></aside>
        </div>
      </section>

      <section className="content-section tint" id="process">
        <div className="section-title"><p>HOW TO</p><h2>임대·운반 신청 절차</h2><span>온라인 화면이 열리지 않으면 전화 예약이 가장 빠릅니다.</span></div>
        <div className="process-grid">{steps.map(([no,title,body]) => <article key={no}><span>{no}</span><div><h3>{title}</h3><p>{body}</p></div></article>)}</div>
        <div className="call-script"><div><small>전화 문의 예시</small><h3>그대로 읽어도 됩니다</h3></div><blockquote>“대산읍 화곡리에 농업경영체가 등록된 농업인입니다. 엄나무밭 약 100평에 화이트클로버를 파종하려고 합니다. 소형 관리기나 로터리와 진압기 임대가 가능한지, 농지까지 왕복 운반서비스를 신청할 수 있는지 확인 부탁드립니다.”</blockquote></div>
      </section>

      <section className="content-section" id="equipment">
        <div className="section-title"><p>EQUIPMENT</p><h2>화이트클로버 파종 장비</h2><span>약 100평 엄나무밭이라면 대형 트랙터보다 소형 장비 조합이 현실적입니다.</span></div>
        <div className="equipment-grid">{equipment.map(([work,machine,opinion], index) => <article key={work}><span>{String(index + 1).padStart(2,"0")}</span><p>{work}</p><h3>{machine}</h3><small>{opinion}</small></article>)}</div>
        <div className="info-note"><b>엄나무 보호:</b> 줄기 주변 30~50cm는 비워두고, 뿌리 손상을 막기 위해 깊은 로터리 작업은 피하세요.</div>
      </section>

      <section className="content-section dark-section" id="contact">
        <div className="section-title light"><p>CONTACT</p><h2>담당 사업소와 준비물</h2><span>화곡농장은 대산읍 북부분소에 먼저 문의하세요.</span></div>
        <div className="contact-layout">
          <article><small>화곡농장 우선 연락처</small><h3>서산시 농업기계임대사업소<br />북부분소</h3><p>충남 서산시 대산읍 대산1로 70</p><a href="tel:0416811006">041-681-1006</a><a className="minor-link" href="https://map.kakao.com/link/search/서산시%20농업기계임대사업소%20북부분소" target="_blank" rel="noreferrer">지도에서 위치 보기 →</a></article>
          <article><h3>방문 전 준비</h3><ul><li>신분증</li><li>농업경영체 등록확인서 또는 등록번호</li><li>농업인 NH안전보험 가입증명서</li><li>결제용 카드</li><li>농지 소재지와 지번 자료</li></ul></article>
        </div>
        <div className="office-table" role="table" aria-label="서산시 농업기계임대사업소 연락처">{offices.map(([name,address,phone]) => <div className={name === "북부분소" ? "featured" : ""} role="row" key={name}><strong role="cell">{name}</strong><span role="cell">{address}</span><a role="cell" href={`tel:${phone.replaceAll("-","")}`}>{phone}</a></div>)}</div>
      </section>

      <section className="content-section">
        <div className="section-title"><p>BEFORE YOU GO</p><h2>마지막 확인 사항</h2></div>
        <div className="data-cards three"><article><h3>비용</h3><p>2026년 홍보물 노출정보는 편도 2만 원·왕복 4만 원입니다. 현행 금액을 전화로 확인하세요.</p></article><article><h3>이용자 책임</h3><p>사용 중 고장·파손·사고는 임차인 부담으로 안내됩니다. 이상이 생기면 즉시 사업소에 연락하세요.</p></article><article><h3>교육·자격</h3><p>트랙터·굴착기 등 일부 장비는 안전교육이나 별도 자격 요건이 있을 수 있습니다.</p></article></div>
      </section>

      <footer className="site-footer"><b>화곡농장 · 농기계 임대·운반 서비스</b><div><Link href="/">프로젝트 홈</Link><a href="https://www.seosan.go.kr/agritech/selectBbsNttView.do?bbsNo=1904&integrDeptCode=&key=6649&nttNo=333500&pageIndex=1&searchCnd=all&searchCtgry=&searchKrwd=" target="_blank" rel="noreferrer">2026 이용안내</a></div></footer>
      <a className="floating-call" href="tel:0416811006"><small>북부분소</small><b>전화 문의</b></a>
    </main>
  );
}
