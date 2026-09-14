import { ProjectNav } from "../project-nav";

export default function DangolSprayPage() {
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  return (
    <main className="site-page spray-page">
      <ProjectNav current="dangol" />
      <section className="spray-hero">
        <div>
          <p className="breadcrumb"><a href={`${basePath}/`}>화곡농장</a><span>›</span>방제 기록</p>
          <p className="kicker">FIELD LOG · 2026. 08. 11.</p>
          <h1>농막 아래 들깨밭<br /><em>단골 제초제 살포</em></h1>
          <p className="hero-description">농막 아래 농지의 들깨 포기 사이와 고랑 잡초를 대상으로 차폐갓을 사용해 선택 살포한 작업 기록입니다.</p>
          <div className="hero-actions"><a className="primary-button" href="#record">작업 기록 보기</a><a className="outline-button" href="#label">라벨 기준 보기</a></div>
        </div>
        <aside className="spray-dose-card" aria-label="살포량 요약">
          <small>총 살포액</small><strong>40<em>L</em></strong>
          <dl><div><dt>분무기</dt><dd>20L × 2통</dd></div><div><dt>라벨 기준</dt><dd>100mL / 20L</dd></div><div><dt>40L 환산</dt><dd>200mL</dd></div></dl>
        </aside>
      </section>
      <section className="spray-summary-strip" aria-label="작업 핵심 정보">
        <div><span>01</span><p><small>작업 일시</small><b>2026년 8월 11일</b></p></div>
        <div><span>02</span><p><small>작업 장소</small><b>농막 아래 농지</b></p></div>
        <div><span>03</span><p><small>재배 작물</small><b>들깨</b></p></div>
        <div><span>04</span><p><small>사용 약제</small><b>단골 500mL</b></p></div>
      </section>
      <section className="content-section" id="record">
        <div className="section-title"><p>APPLICATION RECORD</p><h2>살포 기록</h2><span>실제 현장 작업과 제품 라벨을 기준으로 정리했습니다.</span></div>
        <div className="spray-record-layout">
          <article className="spray-table-card">
            <div><span>작업 일시</span><strong>2026년 8월 11일</strong></div>
            <div><span>작업 장소</span><strong>화곡농장 농막 아래 농지</strong></div>
            <div><span>재배 작물</span><strong>들깨</strong></div>
            <div><span>사용 약제</span><strong>단골 500mL</strong></div>
            <div><span>총 살포량</span><strong>20L × 2통 = 40L</strong></div>
            <div><span>살포 방식</span><strong>차폐갓 장착 · 고랑 선택 살포</strong></div>
          </article>
          <aside className="spray-note-card"><small>WORK NOTE</small><h3>들깨 포기 사이<br />고랑 잡초 선택 살포</h3><p>노즐을 지면 가까이 낮게 유지하고 차폐갓을 사용해 들깨 잎에 직접 약액이 닿는 것을 줄이는 방식으로 작업했습니다.</p></aside>
        </div>
      </section>
      <section className="content-section tint" id="label">
        <div className="section-title"><p>LABEL GUIDE</p><h2>단골 라벨 기준</h2><span>사진으로 확인한 들깨밭 등록 사용기준입니다.</span></div>
        <div className="spray-record-layout">
          <article className="spray-table-card">
            <div><span>적용잡초</span><strong>일년생잡초</strong></div>
            <div><span>사용 적기</span><strong>잡초 생육기</strong></div>
            <div><span>화본과잡초</span><strong>3엽기 이내</strong></div>
            <div><span>살포 위치</span><strong>밭고랑(휴간) 잡초 경엽처리</strong></div>
            <div><span>물 20L당</span><strong>약제 100mL</strong></div>
            <div><span>10a당</span><strong>약량 500mL · 살포량 100L</strong></div>
          </article>
          <aside className="spray-note-card"><small>DOSE NOTE</small><h3>40L 기준<br />라벨 환산 200mL</h3><p>이번 실제 투입 약제량은 별도 확인되지 않았으므로 200mL는 라벨 비율에 따른 환산값으로만 기록합니다.</p></aside>
        </div>
      </section>
      <section className="spray-check-section">
        <div><p>FIELD ARCHIVE</p><h2>현장 사진<br />25장 보관</h2></div>
        <ul><li><span>01</span><div><b>약제·분무기</b><p>단골 용기, 사용량 라벨, TS-1100N 20L 분무기</p></div></li><li><span>02</span><div><b>농지 전경</b><p>농막 아래 들깨 구역과 비닐멀칭 구역·주변 경사지</p></div></li><li><span>03</span><div><b>살포 장면</b><p>차폐갓을 지면 가까이 두고 고랑을 따라 살포한 작업 사진</p></div></li><li><span>04</span><div><b>후속 관찰</b><p>3~5일 생육 정지·변색, 7~10일 고사 진행 확인</p></div></li></ul>
      </section>
      <footer className="site-footer"><b>화곡농장 · 방제 작업 기록</b><span>2026년 8월 11일 농막 아래 들깨밭</span></footer>
    </main>
  );
}
