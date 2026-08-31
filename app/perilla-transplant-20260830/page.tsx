"use client";

import { useEffect, useState } from "react";
import { ProjectNav } from "../project-nav";

const photos = [
  { src: "/assets/perilla-transplant-20260830/photo-01.svg", title: "들깨 정식 후 농지 전경과 구획 표시", group: "정식·구획" },
  { src: "/assets/perilla-transplant-20260830/photo-02.svg", title: "농지 가장자리와 정식 구간 전경", group: "정식·구획" },
  { src: "/assets/perilla-transplant-20260830/photo-03.svg", title: "정식한 들깨 모종 근접 사진", group: "모종 상태" },
  { src: "/assets/perilla-transplant-20260830/photo-04.svg", title: "스프링클러 관수 중인 들깨 정식 농지", group: "관수" },
  { src: "/assets/perilla-transplant-20260830/photo-05.svg", title: "정식 구간과 주변 식생·경사 전경", group: "농지 전경" },
];

const videos = [
  ["1000064328.mp4", "16초", "들깨 정식 농지 현장 영상 1"],
  ["1000064301.mp4", "11초", "들깨 정식 농지 현장 영상 2"],
  ["1000064285.mp4", "18초", "들깨 정식 농지 현장 영상 3"],
  ["1000064331.mp4", "16초", "들깨 정식 및 구획 표시 현장 영상 4"],
  ["1000064341.mp4", "14초", "관수·농지 전경 현장 영상 5"],
];

export default function PerillaTransplantPage() {
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  const [selected, setSelected] = useState<(typeof photos)[number] | null>(null);

  useEffect(() => {
    const close = (event: KeyboardEvent) => event.key === "Escape" && setSelected(null);
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, []);

  return (
    <main className="site-page spray-page">
      <ProjectNav />

      <section className="spray-hero">
        <div>
          <p className="breadcrumb"><a href={`${basePath}/`}>화곡농장</a><span>›</span>재배·작업기록</p>
          <p className="kicker">PERILLA TRANSPLANT LOG · 2026. 08. 30–31.</p>
          <h1>663-1·667-35<br /><em>들깨 정식 기록</em></h1>
          <p className="hero-description">당숙모에게 받은 들깨 모종 3판을 대산읍 화곡리 663-1·667-35번지에 정식하고, 고추대와 줄로 재배 구역을 표시한 뒤 관수한 현장 기록입니다. 8월 31일 농산물품질관리원에 연락했고 같은 날 현장 확인 예정입니다.</p>
          <div className="hero-actions"><a className="primary-button" href="#record">작업 기록 보기</a><a className="outline-button" href="#photos">현장 사진 보기</a></div>
        </div>
        <aside className="spray-dose-card" aria-label="작업 핵심 정보">
          <small>정식 모종</small><strong>3<em>판</em></strong>
          <dl>
            <div><dt>정식일</dt><dd>2026-08-30</dd></div>
            <div><dt>필지</dt><dd>663-1 · 667-35</dd></div>
            <div><dt>농관원</dt><dd>8/31 현장확인 예정</dd></div>
          </dl>
        </aside>
      </section>

      <section className="spray-summary-strip" aria-label="작업 요약">
        <div><span>01</span><p><small>작물</small><b>들깨</b></p></div>
        <div><span>02</span><p><small>모종</small><b>당숙모 제공 3판</b></p></div>
        <div><span>03</span><p><small>구획</small><b>고추대 + 줄 표시</b></p></div>
        <div><span>04</span><p><small>후속</small><b>농관원 현장확인</b></p></div>
      </section>

      <section className="content-section" id="record">
        <div className="section-title"><p>FIELD RECORD</p><h2>들깨 정식·구획 표시·관수</h2><span>사용자가 제공한 작업 설명과 첨부 사진·동영상을 기준으로 정리했습니다.</span></div>
        <div className="spray-record-layout">
          <article className="spray-table-card">
            <div><span>대상 농지</span><strong>충남 서산시 대산읍 화곡리 663-1, 667-35</strong></div>
            <div><span>정식</span><strong>2026-08-30 · 들깨 모종 3판</strong></div>
            <div><span>모종 출처</span><strong>당숙모에게 받은 모종</strong></div>
            <div><span>구획 표시</span><strong>고추대를 꽂고 줄을 연결하여 재배 구역 표시</strong></div>
            <div><span>정식 후 관리</span><strong>스프링클러 관수</strong></div>
            <div><span>농관원</span><strong>2026-08-31 연락 · 같은 날 현장 방문 확인 예정</strong></div>
          </article>
          <aside className="spray-note-card">
            <small>FIELD CHECK</small><h3>현장확인 전<br />준비 상태</h3>
            <p>정식한 들깨 모종, 구획을 표시한 고추대·줄, 관수 상태가 사진에 남아 있습니다. 현장확인 결과는 방문 완료 후 별도로 추가 기록합니다.</p>
          </aside>
        </div>
      </section>

      <section className="content-section tint">
        <div className="section-title"><p>TIMELINE</p><h2>작업 경과</h2></div>
        <div className="spray-table-card">
          <div><span>2026-08-30</span><strong>들깨 모종 3판을 663-1·667-35번지에 정식</strong></div>
          <div><span>정식 당일</span><strong>고추대와 줄을 이용해 재배 구역·필지 경계 표시</strong></div>
          <div><span>정식 후</span><strong>스프링클러를 이용해 관수</strong></div>
          <div><span>2026-08-31</span><strong>농산물품질관리원 연락 · 당일 현장확인 예정</strong></div>
        </div>
      </section>

      <section className="content-section" id="photos">
        <div className="section-title"><p>FIELD PHOTOS</p><h2>정식·구획·관수 현장</h2><span>사진을 누르면 레이어 화면으로 확인할 수 있습니다. 공개 페이지에는 웹용 경량본을 사용했습니다.</span></div>
        <div className="spray-photo-grid">
          {photos.map((photo) => (
            <button type="button" key={photo.src} onClick={() => setSelected(photo)}>
              <div><img src={`${basePath}${photo.src}`} alt={photo.title} /><span>확대 보기</span></div>
              <small>{photo.group}</small><strong>{photo.title}</strong>
            </button>
          ))}
        </div>
      </section>

      <section className="content-section tint">
        <div className="section-title"><p>VIDEO ARCHIVE</p><h2>현장 동영상 5개</h2><span>원본 동영상은 정리 ZIP에 보관하고, 공개 페이지에는 파일명과 길이를 기록합니다.</span></div>
        <div className="spray-table-card">
          {videos.map((video, index) => (
            <div key={video[0]}><span>{String(index + 1).padStart(2, "0")} · {video[1]}</span><strong>{video[2]} · {video[0]}</strong></div>
          ))}
        </div>
      </section>

      <section className="spray-check-section">
        <div><p>NATIONAL AGRICULTURAL PRODUCTS QUALITY MANAGEMENT SERVICE</p><h2>농관원 현장확인<br />설명 요지</h2></div>
        <ul>
          <li><span>01</span><div><b>정식 시점</b><p>2026년 8월 30일 들깨 모종 3판 정식</p></div></li>
          <li><span>02</span><div><b>대상 필지</b><p>화곡리 663-1, 667-35번지</p></div></li>
          <li><span>03</span><div><b>구획 표시</b><p>두 필지의 재배 구역을 고추대와 줄로 표시</p></div></li>
          <li><span>04</span><div><b>관리 상태</b><p>정식 후 스프링클러 관수</p></div></li>
        </ul>
      </section>

      <section className="download-banner">
        <div><p>TEXT ARCHIVE</p><h2>Markdown 기록 보기</h2><span>정식·구획 표시·농관원 현장확인 예정 내용을 텍스트 문서로도 보관합니다.</span></div>
        <a href={`${basePath}/downloads/20260831-hwagok-perilla-transplant-record.md`}>MD 열기</a>
      </section>

      <footer className="site-footer"><b>화곡농장 · 들깨 정식 및 농관원 현장확인 기록</b><span>2026년 8월 30–31일</span></footer>

      {selected && (
        <div className="spray-modal" role="dialog" aria-modal="true" aria-label={selected.title} onClick={() => setSelected(null)}>
          <button type="button" aria-label="닫기" onClick={() => setSelected(null)}>×</button>
          <figure onClick={(event) => event.stopPropagation()}><img src={`${basePath}${selected.src}`} alt={selected.title} /><figcaption>{selected.title}</figcaption></figure>
        </div>
      )}
    </main>
  );
}
