import Link from "next/link";
import { ProjectNav } from "../project-nav";

const offices = [
  ["본소","인지면 무학재1길 99","041-669-5951"],
  ["중부","성연면 생동사동길 21","041-662-3315"],
  ["동부","운산면 홍안벌로 501","041-688-7766"],
  ["북부","대산읍 대산1로 70","041-681-1006"],
];

export default function MachineRentalVisitPage(){
  return <main className="site-page detail-page machine-page">
    <ProjectNav current="machineVisit" />
    <section className="detail-hero machine-hero"><div>
      <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>관리기 임대·출고 기록</b></p>
      <p className="kicker">2026. 9. 24. · 서산시농업기술센터 북부 농업기계 임대사업소</p>
      <h1>아세아 관리기<br/><em>임대·출고·운송 기록</em></h1>
      <p className="hero-description">북부 농업기계 임대사업소를 방문해 이용조건을 확인하고 아세아 관리기를 출고한 뒤, 농업기술센터 차량으로 운송해 현장에서 크레인으로 하차한 기록입니다.</p>
      <div className="hero-actions"><a className="primary-button" href="tel:0416811006">북부사업소 전화</a><Link className="outline-button" href="/farm-machine-rental">기존 임대 안내</Link></div>
    </div><aside className="metric-card machine-card"><small>현장 기록</small><h2>2026-09-24</h2><dl>
      <div><dt>사업소</dt><dd>북부 · 대산</dd></div><div><dt>장비</dt><dd>아세아 관리기</dd></div><div><dt>임대</dt><dd>1농가 1대 · 3일 이내</dd></div><div><dt>운송</dt><dd>농업기술센터 차량</dd></div>
    </dl></aside></section>

    <section className="quick-strip machine-strip"><div><span>01</span><p><b>경영체</b>등록증 제출</p></div><div><span>02</span><p><b>안전보험</b>NH 가입증명서</p></div><div><span>03</span><p><b>출고</b>안전교육 실시</p></div><div><span>04</span><p><b>반납</b>세척·연료 보충</p></div></section>

    <section className="content-section"><div className="section-title"><p>RENTAL RULES</p><h2>현장에서 확인한 이용조건</h2><span>2026-09-24 사업소 안내문을 기준으로 정리했습니다.</span></div>
      <div className="data-cards three"><article><h3>임대 대상·서류</h3><p>관내 농업인 대상이며 농업경영체등록증 제출이 필요합니다. 자주형 농기계·작업기 사용자는 농업인 NH안전보험 가입 증명서를 제출하도록 안내되어 있습니다.</p></article>
      <article><h3>기간·교육</h3><p>1농가당 1대 임대 원칙이며 사용기간은 3일 이내입니다. 장비 출고 시 안전교육을 실시하고 농업용 굴착기 사용자는 면허증을 제출합니다.</p></article>
      <article><h3>반납·책임</h3><p>사용 후 세척하고 연료를 보충해 반납합니다. 출고 후 고장·파손은 안내문상 사용자 수리·배상 책임이 명시되어 있습니다.</p></article></div>
    </section>

    <section className="content-section tint"><div className="section-title"><p>FIELD LOG</p><h2>관리기 출고부터 현장 하차까지</h2></div>
      <div className="process-grid"><article><span>01</span><div><h3>사업소 방문</h3><p>북부 농업기계 임대사업소에서 이용조건과 준비서류를 확인했습니다.</p></div></article>
      <article><span>02</span><div><h3>관리기 확인</h3><p>사업소 내부에서 아세아 관리기의 엔진·배터리·로터리 작업부·조작 레버를 확인하고 취급 설명을 받았습니다.</p></div></article>
      <article><span>03</span><div><h3>출고·운송</h3><p>관리기를 농업기술센터 크레인 장착 화물차에 적재해 현장으로 운송했습니다.</p></div></article>
      <article><span>04</span><div><h3>현장 하차</h3><p>현장에서 크레인을 이용해 관리기를 하차하고 장비 상태와 조작 상태를 확인했습니다.</p></div></article></div>
      <div className="info-note"><b>자료 보유:</b> 이 기록의 원본 정리본에는 현장 사진 18장과 동영상 2개가 포함되어 있습니다. 공개 저장소에는 현재 텍스트 기록을 우선 반영했습니다.</div>
    </section>

    <section className="content-section dark-section"><div className="section-title light"><p>CONTACT</p><h2>서산시 농업기계 임대사업소</h2></div>
      <div className="office-table" role="table">{offices.map(([n,a,p])=><div className={n==="북부"?"featured":""} role="row" key={n}><strong>{n}</strong><span>{a}</span><a href={"tel:"+p.replaceAll("-","")}>{p}</a></div>)}</div>
      <div className="info-note"><b>현장 수기 메모:</b> 대산농협 · 041-660-9900 · 7916. 메모의 용도는 원기록만 보존하고 별도 확정하지 않았습니다.</div>
    </section>
    <footer className="site-footer"><b>화곡농장 · 2026-09-24 관리기 임대·출고</b><div><Link href="/">프로젝트 홈</Link><a href="https://softm.github.io/projects/">전체 프로젝트</a></div></footer>
  </main>
}