import Link from "next/link";

const bp = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const photos = [
  ["01-1000064667.jpg", "분리된 기존 회전 기어박스와 파손된 고정부"],
  ["01-20260906_085436.jpg", "선풍기 모터 외함과 제품 표시부 위치"],
  ["02-1000064668.jpg", "안전인증 표시사항과 모델명 TKF-30 S,P"],
  ["02-20260906_085439.jpg", "후면 커버를 분리한 선풍기 모터부"],
  ["03-1000064669.jpg", "모터 외함 전체 상태"],
  ["03-20260906_085443.jpg", "수리 전 선풍기 전체 모습"],
  ["04-20260906_085534.jpg", "타이거킹 30인치 공업용 선풍기 전면"],
  ["05-20260906_085538.jpg", "전면 중심부와 날개 상태"],
];
const asset = (name: string) => `${bp}/archive/fan-gearbox-repair-20260914/assets/${name}`;

export default function Page() {
  return <main className="site-page detail-page record-page" data-record-page>
    <header className="record-header">
      <nav className="breadcrumb" aria-label="현재 위치"><a href="https://softm.github.io/projects/hwagok-farm/">화곡농장</a><span>›</span><span>시설·장비수리</span></nav>
      <h1>{"2026-09-06 선풍기 기어박스 수리 안내"}</h1>
      <p className="record-lead">타이거킹 TKF-30 S,P의 좌우 회전 불량을 점검하고 교체용 기어박스 1개를 주문한 기록입니다.</p>
      <p className="kicker">현장 점검 2026. 9. 6. · 부품 주문 2026. 9. 14.</p>
    </header>
    <section className="record-section" id="diagnosis">
      <h2>고장 상태와 수리 결정</h2>
      <div className="record-columns">
        <div><h3>파손 진단</h3><p>좌우 회전이 되지 않는 30인치 공업용 선풍기를 분해했습니다. 주 모터보다 좌우 회전용 기어박스 파손이 핵심 원인으로 확인됐습니다.</p><p>흰색 플라스틱 하우징의 고정 날개와 장착부가 여러 군데 깨졌습니다. 접착제로 붙였던 흔적이 있으나 회전 부하와 진동을 견디지 못해 다시 파손됐습니다.</p></div>
        <div><h3>교체 부품 주문</h3><p>기어와 축만 재사용하거나 접착 보수하지 않고, 회전기어박스 전체를 교체하기로 결정했습니다.</p><p><strong>2026년 9월 14일</strong> 네이버 스마트스토어에서 교체용 기어박스 <strong>1개</strong>를 주문했습니다. 주문 당시 안내된 도착 예정일은 9월 16일이며, 이 기록만으로 실제 도착·교체 완료를 확인한 것은 아닙니다.</p></div>
      </div>
      <div className="warning-note"><b>안전:</b> 기어박스가 고정되지 않은 상태에서는 회전축이나 전선에 걸릴 수 있으므로 전원을 연결해 작동하지 않습니다.</div>
    </section>
    <section className="record-section" id="equipment">
      <h2>제품 표시사항·장착 전 확인</h2>
      <dl className="record-specs">
        <div><dt>제조사</dt><dd>DIP 동일정밀공업㈜ · Tiger King</dd></div>
        <div><dt>형명·규격</dt><dd>TKF-30 S,P · 30인치</dd></div>
        <div><dt>전기 규격</dt><dd>단상 220V · 60Hz · 310W</dd></div>
        <div><dt>제조 시기</dt><dd>2003년 7월</dd></div>
      </dl>
      <div className="info-note"><b>새 부품 비교:</b> 고정홀 간격, 모터축 맞물림 위치, 출력축 길이·굵기와 회전 연결봉 방향을 기존 부품과 나란히 비교합니다.</div>
    </section>
    <section className="record-section" id="photos">
      <h2>점검 사진 <small>8장</small></h2>
      <div className="record-gallery">{photos.map(([name,caption],i) => <figure key={name}>
        <img src={asset(name)} alt={caption} loading="lazy" decoding="async" />
        <figcaption>{String(i+1).padStart(2,"0")} · {caption}</figcaption>
      </figure>)}</div>
    </section>
    <section className="record-section" id="installation">
      <h2>부품 도착 후 작업 순서</h2>
      <div className="process-grid">
        <article><span>01</span><div><h3>전원 차단</h3><p>플러그를 뽑고 날개가 완전히 멈춘 상태에서 작업합니다.</p></div></article>
        <article><span>02</span><div><h3>규격 비교</h3><p>기존 기어박스와 새 부품의 축·홀·연결부 규격을 비교합니다.</p></div></article>
        <article><span>03</span><div><h3>수동 점검</h3><p>조립 후 전원 연결 전에 날개와 회전축을 손으로 움직여 걸림을 확인합니다.</p></div></article>
        <article><span>04</span><div><h3>시험 운전</h3><p>안전망을 조립한 뒤 저속으로 짧게 운전하고 이상 소음과 흔들림을 확인합니다.</p></div></article>
      </div>
    </section>
    <details className="record-reference"><summary>정리 원본·기록 정보</summary>
      <div className="record-actions"><a className="outline-button" href={`${bp}/archive/fan-gearbox-repair-20260914/record.html`}>HTML 정리본</a><a className="outline-button" href={`${bp}/archive/fan-gearbox-repair-20260914/record.md`}>Markdown 원본</a></div>
      <p>개인정보 보호를 위해 주문번호, 배송지와 전화번호가 포함된 주문 완료 화면은 공개 페이지에 싣지 않았습니다.</p>
    </details>
    <footer className="site-footer"><span>화곡농장 · 시설·장비수리</span><div><a href="https://softm.github.io/projects/hwagok-farm/">프로젝트 목록</a><Link href="/">농장 기록 홈</Link><a href="https://softm.github.io/projects/">전체 프로젝트</a></div></footer>
  </main>;
}
