"use client";

import { useEffect, useState } from "react";
import { ProjectNav } from "../project-nav";

const photos = [
  { src: "/assets/spray-20260813/01-1000060294.jpg", title: "약제 및 살포 준비 1", group: "약제·준비" },
  { src: "/assets/spray-20260813/02-1000060293.jpg", title: "약제 및 살포 준비 2", group: "약제·준비" },
  { src: "/assets/spray-20260813/03-1000060292.jpg", title: "농막 아랫밭 1", group: "살포 현장" },
  { src: "/assets/spray-20260813/04-1000060291.jpg", title: "농막 아랫밭 2", group: "살포 현장" },
  { src: "/assets/spray-20260813/05-1000060290.jpg", title: "농막 아랫밭 3", group: "살포 현장" },
];

export default function SprayRecordPage() {
  const [selected, setSelected] = useState<(typeof photos)[number] | null>(null);

  useEffect(() => {
    const close = (event: KeyboardEvent) => event.key === "Escape" && setSelected(null);
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, []);

  return (
    <main className="site-page spray-page">
      <ProjectNav current="spray" />

      <section className="spray-hero">
        <div>
          <p className="breadcrumb"><a href="/">화곡농장</a><span>›</span>방제 기록</p>
          <p className="kicker">FIELD LOG · 2026. 08. 13.</p>
          <h1>농막 아랫밭<br /><em>나방노린채 살포</em></h1>
          <p className="hero-description">들깨밭에 오전 7시부터 살충제를 살포한 작업 기록입니다. 20L 분무기 2통에 약제를 각 10mL씩 사용했습니다.</p>
          <div className="hero-actions"><a className="primary-button" href="#record">작업 기록 보기</a><a className="outline-button" href="#photos">현장 사진 보기</a></div>
        </div>
        <aside className="spray-dose-card" aria-label="살포량 요약">
          <small>총 살포액</small><strong>40<em>L</em></strong>
          <dl><div><dt>분무기</dt><dd>20L × 2통</dd></div><div><dt>통당 약제</dt><dd>10mL</dd></div><div><dt>총 약제량</dt><dd>20mL</dd></div></dl>
        </aside>
      </section>

      <section className="spray-summary-strip" aria-label="작업 핵심 정보">
        <div><span>01</span><p><small>작업 일시</small><b>8월 13일 오전 7시</b></p></div>
        <div><span>02</span><p><small>작업 장소</small><b>농막 아랫밭</b></p></div>
        <div><span>03</span><p><small>재배 작물</small><b>들깨</b></p></div>
        <div><span>04</span><p><small>사용 약제</small><b>나방노린채 액상수화제</b></p></div>
      </section>

      <section className="content-section" id="record">
        <div className="section-title"><p>APPLICATION RECORD</p><h2>살포 기록</h2><span>현장에서 사용한 양을 기준으로 정리한 실제 작업 기록입니다.</span></div>
        <div className="spray-record-layout">
          <article className="spray-table-card">
            <div><span>작업 일시</span><strong>2026년 8월 13일 오전 7시</strong></div>
            <div><span>작업 장소</span><strong>화곡농장 농막 아랫밭</strong></div>
            <div><span>재배 작물</span><strong>들깨</strong></div>
            <div><span>사용 약제</span><strong>나방노린채 액상수화제</strong></div>
            <div><span>희석 기준</span><strong>물 20L당 약제 10mL</strong></div>
            <div><span>총 사용량</span><strong>살포액 40L · 약제 20mL</strong></div>
          </article>
          <aside className="spray-note-card"><small>WORK NOTE</small><h3>이른 아침에<br />2통 살포 완료</h3><p>한낮의 고온 시간을 피해 오전 7시에 작업했습니다. 20L 분무기 2통을 사용했으며 각 통에 약제 10mL를 넣었습니다.</p><div><b>10mL</b><span>× 2통</span><strong>20mL</strong></div></aside>
        </div>
      </section>

      <section className="content-section tint" id="photos">
        <div className="section-title"><p>FIELD PHOTOS</p><h2>약제와 살포 현장</h2><span>사진을 누르면 원본 크기의 레이어 화면으로 확인할 수 있습니다.</span></div>
        <div className="spray-photo-grid">
          {photos.map((photo) => <button type="button" key={photo.src} onClick={() => setSelected(photo)}><div><img src={photo.src} alt={photo.title} /><span>확대 보기</span></div><small>{photo.group}</small><strong>{photo.title}</strong></button>)}
        </div>
      </section>

      <section className="spray-check-section">
        <div><p>FOLLOW-UP</p><h2>다음 작업 때<br />함께 기록할 항목</h2></div>
        <ul><li><span>01</span><div><b>살포 후 강우</b><p>약제가 마르기 전 비가 왔는지 기록</p></div></li><li><span>02</span><div><b>방제 효과</b><p>해충 감소 여부와 확인 날짜 기록</p></div></li><li><span>03</span><div><b>약해 유무</b><p>잎 변색·말림 등 이상 여부 확인</p></div></li><li><span>04</span><div><b>안전사용기준</b><p>다음 살포 전 라벨의 사용 시기와 횟수 재확인</p></div></li></ul>
      </section>

      <section className="download-banner"><div><p>ORIGINAL ARCHIVE</p><h2>정리 문서와 사진 내려받기</h2><span>Markdown · HTML · 원본 사진 5장이 들어 있습니다.</span></div><a href="/downloads/20260813-hwagok-spray-record.zip" download>ZIP 다운로드</a></section>
      <footer className="site-footer"><b>화곡농장 · 방제 작업 기록</b><span>2026년 8월 13일 농막 아랫밭</span></footer>

      {selected && <div className="spray-modal" role="dialog" aria-modal="true" aria-label={selected.title} onClick={() => setSelected(null)}><button type="button" aria-label="닫기" onClick={() => setSelected(null)}>×</button><figure onClick={(event) => event.stopPropagation()}><img src={selected.src} alt={selected.title} /><figcaption>{selected.title}</figcaption></figure></div>}
    </main>
  );
}
