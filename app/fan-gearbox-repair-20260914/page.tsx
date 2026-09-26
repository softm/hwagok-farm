import Link from "next/link";

const bp=process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const photos=[
  ["01-1000064667.jpg","분리된 기존 회전 기어박스와 파손된 고정부"],
  ["01-20260906_085436.jpg","선풍기 모터 외함과 제품 표시부 위치"],
  ["02-1000064668.jpg","안전인증 표시사항과 모델명 TKF-30 S,P"],
  ["02-20260906_085439.jpg","후면 커버를 분리한 선풍기 모터부"],
  ["03-1000064669.jpg","모터 외함 전체 상태"],
  ["03-20260906_085443.jpg","수리 전 선풍기 전체 모습"],
  ["04-20260906_085534.jpg","타이거킹 30인치 공업용 선풍기 전면"],
  ["05-20260906_085538.jpg","전면 중심부와 날개 상태"]
];
const asset=(name:string)=>`${bp}/archive/fan-gearbox-repair-20260914/assets/${name}`;

export default function Page(){return <main className="site-page detail-page machine-page">
  <section className="detail-hero machine-hero"><div><p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>공업용 선풍기 수리</b></p><p className="kicker">2026. 9. 6. 점검 · 2026. 9. 14. 부품 주문</p><h1>타이거킹 선풍기<br/><em>회전기어박스 교체 준비</em></h1><p className="hero-description">좌우 회전이 되지 않는 30인치 공업용 선풍기를 분해해 확인한 결과, 회전 기어박스의 플라스틱 하우징과 고정부가 파손된 상태였습니다. 접착 보수 대신 기어박스 전체 교체를 위해 부품 1개를 주문했습니다.</p></div>
  <aside className="metric-card machine-card"><small>장비 수리 기록</small><h2>TKF-30 S,P</h2><dl><div><dt>규격</dt><dd>30인치</dd></div><div><dt>소비전력</dt><dd>310W</dd></div><div><dt>제조</dt><dd>2003년 7월</dd></div><div><dt>주문수량</dt><dd>1개</dd></div></dl></aside></section>

  <section className="content-section"><div className="section-title"><p>01 · DIAGNOSIS</p><h2>고장 판단</h2><span>주 모터보다 좌우 회전용 기어박스 파손이 핵심 원인으로 확인됐습니다.</span></div>
  <div className="data-cards three"><article><h3>파손 부위</h3><p>흰색 플라스틱 기어박스의 고정 날개와 장착부가 여러 군데 깨졌습니다.</p></article><article><h3>기존 보수</h3><p>접착제로 붙였던 흔적이 있으나 회전 부하와 진동을 견디지 못해 다시 파손됐습니다.</p></article><article><h3>수리 방향</h3><p>기어와 축만 재사용하기보다 회전기어박스 전체를 교체하는 방식으로 결정했습니다.</p></article></div>
  <div className="info-note"><b>안전:</b> 기어박스가 고정되지 않은 상태에서는 회전축이나 전선에 걸릴 수 있으므로 전원을 연결해 작동하지 않습니다.</div></section>

  <section className="content-section tint"><div className="section-title"><p>02 · EQUIPMENT</p><h2>제품 표시사항</h2></div>
  <div className="process-grid"><article><span>01</span><div><h3>제조사</h3><p>DIP 동일정밀공업㈜ · Tiger King</p></div></article><article><span>02</span><div><h3>형명</h3><p>TKF-30 S,P</p></div></article><article><span>03</span><div><h3>전기 규격</h3><p>단상 220V, 60Hz, 310W</p></div></article><article><span>04</span><div><h3>제조 시기</h3><p>2003년 7월</p></div></article></div></section>

  <section className="content-section"><div className="section-title"><p>03 · ORDER</p><h2>교체 부품 주문</h2><span>2026년 9월 14일 네이버 스마트스토어에서 타이거킹 회전기어박스 1개를 주문했습니다.</span></div>
  <p>주문 당시 안내된 도착 예정일은 2026년 9월 16일이었습니다. 개인정보 보호를 위해 주문번호, 배송지와 전화번호가 포함된 주문 완료 화면은 공개 페이지에 싣지 않았습니다.</p>
  <div className="info-note"><b>장착 전 확인:</b> 기존 부품과 새 부품의 고정홀 간격, 모터축 맞물림 위치, 출력축 길이·굵기, 회전 연결봉 방향을 나란히 비교합니다.</div></section>

  <section className="content-section tint"><div className="section-title"><p>04 · PHOTO ARCHIVE</p><h2>점검 사진 8장</h2><span>파손 부품, 제품 표시사항, 모터부와 선풍기 전체 상태를 기록했습니다.</span></div>
  <div className="archive-media-grid">{photos.map(([name,caption],i)=><figure key={name}><img src={asset(name)} alt={caption}/><figcaption>{String(i+1).padStart(2,"0")} · {caption}</figcaption></figure>)}</div></section>

  <section className="content-section"><div className="section-title"><p>05 · INSTALLATION CHECK</p><h2>부품 도착 후 작업 순서</h2></div>
  <div className="process-grid"><article><span>01</span><div><h3>전원 차단</h3><p>플러그를 뽑고 날개가 완전히 멈춘 상태에서 작업합니다.</p></div></article><article><span>02</span><div><h3>규격 비교</h3><p>기존 기어박스와 새 부품의 축·홀·연결부 규격을 비교합니다.</p></div></article><article><span>03</span><div><h3>수동 점검</h3><p>조립 후 전원 연결 전에 날개와 회전축을 손으로 움직여 걸림을 확인합니다.</p></div></article><article><span>04</span><div><h3>시험 운전</h3><p>안전망을 조립한 뒤 저속으로 짧게 운전하고 이상 소음과 흔들림을 확인합니다.</p></div></article></div></section>

  <section className="content-section"><div className="section-title"><p>06 · SOURCE FILES</p><h2>정리 원본</h2></div><div className="hero-actions"><a className="primary-button" href={bp+"/archive/fan-gearbox-repair-20260914/record.html"}>HTML 정리본</a><a className="outline-button" href={bp+"/archive/fan-gearbox-repair-20260914/record.md"}>Markdown 원본</a></div></section>
  <footer className="site-footer"><b>화곡농장 · 공업용 선풍기 수리 기록</b><div><Link href="/">프로젝트 홈</Link><a href="https://softm.github.io/projects/">전체 프로젝트</a></div></footer>
</main>}
