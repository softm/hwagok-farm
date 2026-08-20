import Link from "next/link";
import { ProjectNav } from "../project-nav";

const contacts = [
  {
    name: "대산농협 하나로마트",
    phone: "041-660-9930",
    kind: "농협 하나로마트",
    status: "가격 확인",
    tone: "confirmed",
    result: "15kg 1망 15,000원",
    note: "30망 기준 총 450kg · 450,000원",
  },
  {
    name: "제일유통",
    phone: "041-662-1572",
    kind: "농산물 유통",
    status: "회신 대기",
    tone: "pending",
    result: "15kg × 30망 문의",
    note: "2026년 8월 10일 오후 3시 연락 예정",
  },
  {
    name: "서산농협 하나로마트",
    phone: "041-660-4850",
    kind: "농협 하나로마트",
    status: "회신 대기",
    tone: "pending",
    result: "공급 가능 여부·가격 문의",
    note: "확인 후 연락 주기로 함",
  },
  {
    name: "경매가격 판매처",
    phone: "010-9642-6988",
    kind: "개별 판매처",
    status: "문자 대기",
    tone: "pending",
    result: "경매가격 기준 판매",
    note: "가격을 문자로 알려주기로 함",
  },
  {
    name: "팔봉 소규모 농가",
    phone: "010-4768-8693",
    kind: "농가 직거래",
    status: "내년 재문의",
    tone: "next",
    result: "15kg 1망 10,000원에 판매 이력",
    note: "어머니가 생산한 양파를 소규모로 판매",
  },
  {
    name: "억대영농조합법인",
    phone: "010-5430-2204",
    kind: "영농조합법인",
    status: "판매 마감",
    tone: "closed",
    result: "2026년 양파 판매 종료",
    note: "이번 구매 후보에서 제외 · 내년 재문의 가능",
  },
];

const alternatives = [
  ["부석농협 채소류 출하조절센터", "041-669-8870", "양파 재고·출하 농가·대량 구매 연결"],
  ["동부야채", "041-665-9995 / 010-7182-1882", "서산동부전통시장 야채·식자재 대량 문의"],
  ["서산동부전통시장 상인회", "041-665-5478", "망 단위 판매 채소상 연결 요청"],
];

export default function OnionSourcingPage() {
  return (
    <main className="site-page spray-page source-page">
      <ProjectNav current="onionSource" />

      <section className="spray-hero source-hero">
        <div>
          <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span>구매·거래처 조사</p>
          <p className="kicker">ONION SOURCING LOG · 2026. 08. 10.</p>
          <h1>양파 30망<br /><em>구매처 조사</em></h1>
          <p className="hero-description">기존 예정 거래가 취소된 뒤 식당용 국산 양파를 급히 확보하기 위해 서산 지역 농가·농협·유통업체에 문의한 결과를 정리했습니다.</p>
          <div className="hero-actions"><a className="primary-button" href="#prices">가격 비교</a><a className="outline-button" href="#contacts">문의 현황</a></div>
        </div>
        <aside className="spray-dose-card" aria-label="구매 목표 요약">
          <small>목표 구매량</small><strong>450<em>kg</em></strong>
          <dl>
            <div><dt>망당 중량</dt><dd>15kg</dd></div>
            <div><dt>필요 수량</dt><dd>30망</dd></div>
            <div><dt>용도</dt><dd>식당용 국산 양파</dd></div>
          </dl>
        </aside>
      </section>

      <section className="spray-summary-strip" aria-label="조사 핵심 정보">
        <div><span>01</span><p><small>조사일</small><b>2026년 8월 10일</b></p></div>
        <div><span>02</span><p><small>기준 규격</small><b>15kg × 30망</b></p></div>
        <div><span>03</span><p><small>확인 가격</small><b>망당 10,000~15,000원</b></p></div>
        <div><span>04</span><p><small>총액 범위</small><b>300,000~450,000원</b></p></div>
      </section>

      <section className="content-section" id="prices">
        <div className="section-title"><p>PRICE COMPARISON</p><h2>확인된 가격 비교</h2><span>팔봉 농가는 과거 판매가격이며, 대산농협은 당시 실제 문의가격입니다.</span></div>
        <div className="source-price-grid">
          <article className="source-price-card highlight">
            <div><span>팔봉 소규모 농가</span><b>내년 재문의</b></div>
            <strong>10,000<small>원 / 15kg</small></strong>
            <p>30망 환산 <b>300,000원</b></p>
          </article>
          <article className="source-price-card">
            <div><span>대산농협 하나로마트</span><b>가격 확인</b></div>
            <strong>15,000<small>원 / 15kg</small></strong>
            <p>30망 합계 <b>450,000원</b></p>
          </article>
        </div>
        <div className="source-difference"><span>두 가격의 차이</span><strong>망당 5,000원 · 30망 기준 총 150,000원</strong></div>
      </section>

      <section className="content-section tint" id="contacts">
        <div className="section-title"><p>CONTACT STATUS</p><h2>문의처 진행 현황</h2><span>전화번호를 누르면 기기에서 전화 연결 화면이 열립니다.</span></div>
        <div className="source-contact-grid">
          {contacts.map((contact) => (
            <article key={contact.phone}>
              <div className="source-card-top"><small>{contact.kind}</small><span className={contact.tone}>{contact.status}</span></div>
              <h3>{contact.name}</h3>
              <a href={`tel:${contact.phone}`}>{contact.phone}</a>
              <strong>{contact.result}</strong>
              <p>{contact.note}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="content-section">
        <div className="section-title"><p>ALTERNATIVE SOURCES</p><h2>추가 확보 경로</h2><span>농가 직거래가 어려울 때 확인할 수 있는 서산 지역 창구입니다.</span></div>
        <div className="spray-table-card source-route-list">
          {alternatives.map(([name, phone, purpose]) => (
            <div key={name}><span>{name}</span><strong>{purpose}<a href={`tel:${phone.split(" / ")[0]}`}>{phone}</a></strong></div>
          ))}
        </div>
      </section>

      <section className="spray-check-section">
        <div><p>CALL CHECKLIST</p><h2>통화할 때<br />확인할 항목</h2></div>
        <ul>
          <li><span>01</span><div><b>가격·공급량</b><p>15kg 망당 가격과 30망 공급 가능 여부</p></div></li>
          <li><span>02</span><div><b>원산지·품질</b><p>국산 여부, 생산지역, 양파 크기와 상태</p></div></li>
          <li><span>03</span><div><b>수령·배송</b><p>직접 수령 위치와 대산 배송 가능 여부</p></div></li>
          <li><span>04</span><div><b>계속 거래</b><p>일회성 구매 이후 정기 공급 가능 여부</p></div></li>
        </ul>
      </section>

      <section className="download-banner source-next-record">
        <div><p>NEXT RECORD · 2026. 08. 11.</p><h2>실제 구입·보관 기록</h2><span>조사 다음 날 농협 하나로마트 두 곳에서 양파를 구입해 화곡농장 저온창고에 보관했습니다.</span></div>
        <Link href="/onion-purchase-20260811">다음 기록 보기</Link>
      </section>

      <footer className="site-footer"><b>화곡농장 · 양파 구매처 조사</b><span>2026년 8월 10일</span></footer>
    </main>
  );
}
