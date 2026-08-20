"use client";

import Link from "next/link";
import { useState } from "react";
import { ProjectNav } from "../project-nav";

const measurements = [
  ["긴 면(전·후면) 예상 가로", "약 7.3 m", "차양막 바깥쪽 설치 가능 구간 기준"],
  ["짧은 면(측면) 예상 가로", "약 4.6 m", "차양막 바깥쪽 설치 가능 구간 기준"],
  ["바닥 → 난간 상단", "약 1.15 m", "데크 상판을 바닥 기준으로 추정"],
  ["바닥 → 차양막 하단", "약 2.65 m", "낮은 쪽 기준 추정"],
  ["바닥 → 차양막 최고", "약 2.85 m", "높은 쪽 기준 추정"],
  ["차양막 하단 → 난간 상단", "약 1.8~1.9 m", "그늘막 실제 유효 세로 길이"],
];

export default function ShadeNetPage() {
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  const src = `${basePath}/shade-net-20260807/measurement-summary.jpg`;
  const [open, setOpen] = useState(false);

  return (
    <main className="site-page detail-page">
      <ProjectNav current="shade" />

      <section className="detail-hero" id="top">
        <div>
          <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>농막 그늘막 예상 설치</b></p>
          <p className="kicker">2026. 8. 7. · 6평 농막 · 바닥 기준 사진 추정</p>
          <h1>차양막 하단에서 난간까지<br/><em>그늘막 설치 크기</em>를 잡았습니다.</h1>
          <p className="hero-description">첨부 사진을 기준으로 긴 면과 짧은 면의 예상 설치 폭, 데크 바닥에서 차양막·난간까지의 높이, 구매할 쉐이드네트 규격을 정리했습니다. 아래 수치는 실측 전 구매 규격을 잡기 위한 개략치입니다.</p>
        </div>
        <aside className="metric-card">
          <small>구매 권장</small><h2>쉐이드네트</h2>
          <dl>
            <div><dt>긴 면</dt><dd>2 × 8 m</dd></div>
            <div><dt>짧은 면</dt><dd>2 × 5 m</dd></div>
            <div><dt>유효 세로</dt><dd>1.8~1.9 m</dd></div>
          </dl>
        </aside>
      </section>

      <section className="quick-strip" aria-label="핵심 요약">
        <div><span>01</span><p><b>긴 면</b>약 7.3m</p></div>
        <div><span>02</span><p><b>짧은 면</b>약 4.6m</p></div>
        <div><span>03</span><p><b>난간 높이</b>약 1.15m</p></div>
        <div><span>04</span><p><b>차양막 하단</b>약 2.65m</p></div>
      </section>

      <section className="content-section" id="summary">
        <div className="section-title"><p>MEASUREMENT SUMMARY</p><h2>바닥 기준 예상 치수</h2><span>데크 상판을 0 기준으로 사진 비례를 이용해 추정했습니다.</span></div>
        <div className="office-table" role="table" aria-label="농막 그늘막 추정 치수">
          <div role="row"><strong role="cell">항목</strong><span role="cell">추정치</span><span role="cell">기준</span></div>
          {measurements.map(([label,value,note]) => <div role="row" key={label}><strong role="cell">{label}</strong><span role="cell"><b>{value}</b></span><span role="cell">{note}</span></div>)}
        </div>
        <div className="info-note"><b>주의:</b> 사진 원근·촬영 각도·데크 높이 차이 때문에 약 ±10~15cm 이상 오차가 생길 수 있으므로, 최종 재단과 고정은 현장 실측값을 우선합니다.</div>
      </section>

      <section className="content-section tint" id="purchase">
        <div className="section-title"><p>RECOMMENDED SIZE</p><h2>구매는 2m 높이 제품으로</h2><span>고정·접힘·수축과 끝단 여유를 포함한 권장 규격입니다.</span></div>
        <div className="data-cards three">
          <article><small>긴 면</small><h3>2m × 8m</h3><p>실제 예상 필요 크기는 약 7.3m × 1.8~1.9m입니다. 좌우 고정 여유까지 포함하면 8m 길이가 적당합니다.</p></article>
          <article><small>짧은 면</small><h3>2m × 5m</h3><p>실제 예상 필요 크기는 약 4.6m × 1.8~1.9m입니다. 측면 역시 고정 여유를 확보합니다.</p></article>
          <article><small>설치 방식</small><h3>탈착·말아올림 권장</h3><p>강풍 때 그늘막 전체가 돛처럼 풍압을 받으므로 완전 고정보다는 걷거나 말아 올릴 수 있는 방식이 관리에 유리합니다.</p></article>
        </div>
      </section>

      <section className="content-section" id="diagram">
        <div className="section-title"><p>ANNOTATED PLAN</p><h2>예상 설치 위치와 바닥 기준 치수</h2><span>첨부 사진들을 바탕으로 만든 종합 개략도입니다. 클릭하면 크게 볼 수 있습니다.</span></div>
        <button type="button" onClick={() => setOpen(true)} style={{display:"block",width:"100%",padding:0,border:0,background:"transparent",cursor:"zoom-in"}}>
          <img src={src} alt="농막 그늘막 바닥 기준 예상 치수 종합도" style={{display:"block",width:"100%",height:"auto",borderRadius:"18px"}} />
        </button>
      </section>

      <section className="content-section dark-section" id="measure">
        <div className="section-title light"><p>FINAL FIELD CHECK</p><h2>구매 전에 세 곳만 실측</h2><span>사진 추정치를 실제 구매 치수로 확정하는 최소 확인 지점입니다.</span></div>
        <div className="data-cards three">
          <article><h3>① 긴 면 폭</h3><p>긴 면 차양막 좌끝에서 우끝까지 실제 고정 가능한 폭을 줄자로 확인합니다.</p></article>
          <article><h3>② 짧은 면 폭</h3><p>짧은 면 차양막 앞끝에서 뒤끝까지 실제 고정 가능한 폭을 확인합니다.</p></article>
          <article><h3>③ 세로 높이</h3><p>차양막 하단 프레임에서 난간 상단 프레임까지 수직거리를 확인합니다.</p></article>
        </div>
      </section>

      <footer className="site-footer"><b>화곡농장 · 농막 그늘막 예상 설치</b><div><Link href="/">프로젝트 홈</Link><a href="#top">맨 위로</a></div></footer>

      {open && <div role="dialog" aria-modal="true" onClick={() => setOpen(false)} style={{position:"fixed",inset:0,zIndex:9999,background:"rgba(0,0,0,.92)",display:"flex",alignItems:"center",justifyContent:"center",padding:"28px"}}>
        <button type="button" onClick={() => setOpen(false)} aria-label="닫기" style={{position:"fixed",right:"24px",top:"16px",fontSize:"38px",color:"#fff",border:0,background:"transparent",cursor:"pointer"}}>×</button>
        <img onClick={(e) => e.stopPropagation()} src={src} alt="농막 그늘막 바닥 기준 예상 치수 종합도 확대" style={{maxWidth:"96vw",maxHeight:"90vh",objectFit:"contain"}} />
      </div>}
    </main>
  );
}
