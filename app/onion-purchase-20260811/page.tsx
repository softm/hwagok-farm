"use client";

import { useEffect, useState } from "react";
import { ProjectNav } from "../project-nav";

const photos = [
  { src: "/assets/onion-20260811/1000060287.jpg", title: "서산태안농협 하나로마트 영수증", group: "영수증" },
  { src: "/assets/onion-20260811/1000060288.png", title: "대산농협 하나로마트 영수증", group: "영수증" },
  { src: "/assets/onion-20260811/1000060105.jpg", title: "차량 적재 전경", group: "운반 기록" },
  { src: "/assets/onion-20260811/1000060106.jpg", title: "양파망 적재 근접", group: "운반 기록" },
];

export default function OnionPurchasePage() {
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  const [selected, setSelected] = useState<(typeof photos)[number] | null>(null);

  useEffect(() => {
    const close = (event: KeyboardEvent) => event.key === "Escape" && setSelected(null);
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, []);

  return (
    <main className="site-page spray-page">
      <ProjectNav current="onion" />

      <section className="spray-hero">
        <div>
          <p className="breadcrumb"><a href={`${basePath}/`}>화곡농장</a><span>›</span>구매·보관 기록</p>
          <p className="kicker">PURCHASE & STORAGE LOG · 2026. 08. 11.</p>
          <h1>양파 구입 및<br /><em>저온창고 보관</em></h1>
          <p className="hero-description">서산태안농협 하나로마트와 대산농협 하나로마트에서 양파를 구입해 차량으로 운반하고, 화곡농장 저온창고에 보관한 기록입니다.</p>
          <div className="hero-actions"><a className="primary-button" href="#record">구입 내역 보기</a><a className="outline-button" href="#photos">증빙 사진 보기</a></div>
        </div>
        <aside className="spray-dose-card" aria-label="양파 구매비 요약">
          <small>양파 구매비 합계</small><strong>453<em>천원</em></strong>
          <dl>
            <div><dt>서산태안농협</dt><dd>153,000원</dd></div>
            <div><dt>대산농협</dt><dd>300,000원</dd></div>
            <div><dt>보관</dt><dd>화곡농장 저온창고</dd></div>
          </dl>
        </aside>
      </section>

      <section className="spray-summary-strip" aria-label="구매 및 보관 핵심 정보">
        <div><span>01</span><p><small>구입 일자</small><b>2026년 8월 11일</b></p></div>
        <div><span>02</span><p><small>구입처</small><b>농협 하나로마트 2곳</b></p></div>
        <div><span>03</span><p><small>양파 구매비</small><b>453,000원</b></p></div>
        <div><span>04</span><p><small>보관 장소</small><b>화곡농장 저온창고</b></p></div>
      </section>

      <section className="content-section" id="record">
        <div className="section-title"><p>PURCHASE RECORD</p><h2>양파 구입 내역</h2><span>영수증과 당시 기록을 기준으로 양파 항목만 분리해 정리했습니다.</span></div>
        <div className="spray-record-layout">
          <article className="spray-table-card">
            <div><span>서산태안농협 하나로마트</span><strong>11:02:17 · 9,000원 × 17 = 153,000원</strong></div>
            <div><span>대산농협 하나로마트</span><strong>13:38:06 · 양파 300,000원</strong></div>
            <div><span>양파 구매비 합계</span><strong>453,000원</strong></div>
            <div><span>대산농협 영수증 전체 매출</span><strong>312,080원 · 카드 결제 309,680원</strong></div>
            <div><span>운반</span><strong>차량 적재 후 화곡농장으로 이동</strong></div>
            <div><span>보관</span><strong>화곡농장 저온창고 보관</strong></div>
          </article>
          <aside className="spray-note-card">
            <small>QUANTITY NOTE</small><h3>수량은<br />약 37망 참고</h3>
            <p>대산농협 구입분을 기존 문의가격인 15kg 한 망 15,000원으로 계산하면 약 20망입니다. 서산태안농협 영수증 수량 17을 더하면 관리상 약 37망으로 볼 수 있습니다.</p>
            <div><b>17</b><span>+ 약 20망</span><strong>약 37망</strong></div>
          </aside>
        </div>
        <p style={{marginTop:"18px",lineHeight:1.8,color:"var(--muted)"}}>두 구입분이 모두 15kg 규격이라고 가정하면 약 555kg이지만, 서산태안농협 영수증에는 중량 규격이 직접 표시되어 있지 않아 수량·중량은 참고값으로만 기록합니다.</p>
      </section>

      <section className="content-section tint" id="photos">
        <div className="section-title"><p>RECEIPTS & FIELD PHOTOS</p><h2>영수증과 차량 적재 기록</h2><span>사진을 누르면 레이어 화면으로 크게 확인할 수 있습니다. 공개 페이지에는 웹용 경량본을 사용했습니다.</span></div>
        <div className="spray-photo-grid">
          {photos.map((photo) => (
            <button type="button" key={photo.src} onClick={() => setSelected(photo)}>
              <div><img src={`${basePath}${photo.src}`} alt={photo.title} /><span>확대 보기</span></div>
              <small>{photo.group}</small><strong>{photo.title}</strong>
            </button>
          ))}
        </div>
      </section>

      <section className="spray-check-section">
        <div><p>STORAGE RECORD</p><h2>구입 후<br />저온창고 보관</h2></div>
        <ul>
          <li><span>01</span><div><b>양파 구입</b><p>서산태안농협·대산농협에서 당일 구입</p></div></li>
          <li><span>02</span><div><b>차량 적재</b><p>양파망을 차량 적재공간에 나누어 적재</p></div></li>
          <li><span>03</span><div><b>화곡농장 운반</b><p>구입 후 농장으로 이동한 현장 기록 보관</p></div></li>
          <li><span>04</span><div><b>저온창고 보관</b><p>화곡농장 저온창고에 보관</p></div></li>
        </ul>
      </section>

      <section className="download-banner">
        <div><p>TEXT ARCHIVE</p><h2>Markdown 기록 보기</h2><span>구매 내역·수량 참고 계산·보관 기록을 텍스트 문서로도 보관합니다.</span></div>
        <a href={`${basePath}/downloads/20260811-hwagok-onion-record.md`}>MD 열기</a>
      </section>

      <footer className="site-footer"><b>화곡농장 · 양파 구매 및 보관 기록</b><span>2026년 8월 11일</span></footer>

      {selected && (
        <div className="spray-modal" role="dialog" aria-modal="true" aria-label={selected.title} onClick={() => setSelected(null)}>
          <button type="button" aria-label="닫기" onClick={() => setSelected(null)}>×</button>
          <figure onClick={(event) => event.stopPropagation()}><img src={`${basePath}${selected.src}`} alt={selected.title} /><figcaption>{selected.title}</figcaption></figure>
        </div>
      )}
    </main>
  );
}
