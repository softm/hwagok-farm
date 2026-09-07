"use client";

import { useEffect, useState } from "react";
import { ProjectNav } from "../project-nav";

const photos = [
  { src: "/assets/irrigation-20260905/01-1000064654.jpg", title: "수도 분배기와 자동급수 타이머", group: "타이머 설치" },
  { src: "/assets/irrigation-20260905/02-1000064653.jpg", title: "수도 분배기와 타이머 연결 상태", group: "타이머 설치" },
  { src: "/assets/irrigation-20260905/03-1000064652.jpg", title: "하우스 내부 급수 설비", group: "급수 설비" },
  { src: "/assets/irrigation-20260905/04-1000064651.jpg", title: "하우스 내부 호스와 릴선", group: "급수 설비" },
  { src: "/assets/irrigation-20260905/05-1000064649.jpg", title: "Ehico 타이머 설정 화면", group: "설정 확인" },
  { src: "/assets/irrigation-20260905/06-1000064648.jpg", title: "화이트클로버 종자", group: "파종 종자" },
  { src: "/assets/irrigation-20260905/01-20260906_082546.jpg", title: "스프링클러와 호스 배치", group: "급수 현장" },
  { src: "/assets/irrigation-20260905/02-20260906_082537.jpg", title: "하우스 앞 파종 구역 전경", group: "파종 구역" },
  { src: "/assets/irrigation-20260905/03-20260906_082509.jpg", title: "화이트클로버 파종 후 토양 표면", group: "파종 구역" },
  { src: "/assets/irrigation-20260905/04-20260906_082459.jpg", title: "파종 구역 근접 모습", group: "파종 구역" },
  { src: "/assets/irrigation-20260905/05-20260906_081346.jpg", title: "하우스 출입구와 호스 동선", group: "급수 설비" },
  { src: "/assets/irrigation-20260905/06-20260906_081341.jpg", title: "하우스 출입구와 수도 위치", group: "급수 설비" },
  { src: "/assets/irrigation-20260905/07-20260906_081315.jpg", title: "하우스에서 밭으로 연결된 호스", group: "급수 설비" },
];

const videos = ["1000064646.mp4","1000064647.mp4","20260906_081352.mp4","20260906_082501.mp4","20260906_082539.mp4"];

export default function IrrigationPage() {
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  const [selected, setSelected] = useState<(typeof photos)[number] | null>(null);
  useEffect(() => {
    const close = (event: KeyboardEvent) => event.key === "Escape" && setSelected(null);
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, []);
  return (
    <main className="site-page spray-page">
      <ProjectNav current="irrigation" />
      <section className="spray-hero">
        <div>
          <p className="breadcrumb"><a href={`${basePath}/`}>화곡농장</a><span>›</span>관수·작업기록</p>
          <p className="kicker">WHITE CLOVER IRRIGATION · 2026. 09. 05.</p>
          <h1>하우스 앞밭<br /><em>화이트클로버 자동급수</em></h1>
          <p className="hero-description">화이트클로버 파종 직후 표토의 수분을 유지하기 위해 수도 4구 분배기, Ehico 자동급수 타이머, 호스와 회전식 스프링클러를 설치한 기록입니다.</p>
          <div className="hero-actions"><a className="primary-button" href="#record">설정 기록 보기</a><a className="outline-button" href="#photos">현장 사진 보기</a></div>
        </div>
        <aside className="spray-dose-card" aria-label="자동급수 핵심 설정">
          <small>1회 급수</small><strong>1<em>분</em></strong>
          <dl>
            <div><dt>간격</dt><dd>2시간마다</dd></div>
            <div><dt>시작</dt><dd>22:41</dd></div>
            <div><dt>대상</dt><dd>화이트클로버</dd></div>
          </dl>
        </aside>
      </section>
      <section className="spray-summary-strip" aria-label="작업 요약">
        <div><span>01</span><p><small>작업일</small><b>2026-09-05</b></p></div>
        <div><span>02</span><p><small>급수시간</small><b>1회 1분</b></p></div>
        <div><span>03</span><p><small>급수간격</small><b>2시간마다</b></p></div>
        <div><span>04</span><p><small>장비</small><b>Ehico 타이머</b></p></div>
      </section>
      <section className="content-section" id="record">
        <div className="section-title"><p>IRRIGATION RECORD</p><h2>설치 및 설정값</h2><span>현장 사진과 타이머 화면에 표시된 값을 기준으로 정리했습니다.</span></div>
        <div className="spray-record-layout">
          <article className="spray-table-card">
            <div><span>설치 장소</span><strong>화곡농장 비닐하우스 및 하우스 앞밭</strong></div>
            <div><span>대상 작물</span><strong>새로 파종한 화이트클로버</strong></div>
            <div><span>급수 설정</span><strong>2시간마다 1분간 급수</strong></div>
            <div><span>기준 시작시각</span><strong>22:41</strong></div>
            <div><span>구성</span><strong>4구 분배기 · 자동급수 타이머 · 호스 · 회전식 스프링클러</strong></div>
            <div><span>확인 촬영</span><strong>2026-09-06 08:13~08:25 및 타이머 화면</strong></div>
          </article>
          <aside className="spray-note-card"><small>TIMER CHECK</small><h3>NEXT START<br />23 HRS</h3><p>23:20 확인 당시 당일 시작시각 22:41이 이미 지나, 다음 날 22:41까지 대기한다는 표시입니다. 이후 2시간 간격으로 반복될 것으로 해석됩니다.</p></aside>
        </div>
      </section>
      <section className="content-section tint">
        <div className="section-title"><p>OPERATION CHECK</p><h2>바로 작동 여부를 확인하는 방법</h2></div>
        <div className="spray-table-card">
          <div><span>01</span><strong>시작시각을 현재보다 2~3분 뒤로 설정</strong></div>
          <div><span>02</span><strong>물이 실제로 나오고 1분 뒤 멈추는지 확인</strong></div>
          <div><span>03</span><strong>확인 후 원하는 기준 시작시각으로 다시 설정</strong></div>
        </div>
      </section>
      <section className="content-section" id="photos">
        <div className="section-title"><p>FIELD PHOTOS</p><h2>파종 구역·타이머·스프링클러</h2><span>사진을 누르면 크게 볼 수 있습니다. 공개 페이지에는 웹용 경량본을 사용했습니다.</span></div>
        <div className="spray-photo-grid">
          {photos.map((photo) => <button type="button" key={photo.src} onClick={() => setSelected(photo)}><div><img src={`${basePath}${photo.src}`} alt={photo.title}/><span>확대 보기</span></div><small>{photo.group}</small><strong>{photo.title}</strong></button>)}
        </div>
      </section>
      <section className="content-section tint">
        <div className="section-title"><p>FIELD CARE</p><h2>파종 직후 관리 메모</h2></div>
        <div className="spray-table-card">
          <div><span>표토</span><strong>발아 전 씨앗이 놓인 얕은 표면이 완전히 마르지 않도록 유지</strong></div>
          <div><span>과습</span><strong>물이 고이거나 씨앗·흙이 흐르면 급수시간을 줄이거나 간격을 늘림</strong></div>
          <div><span>건조</span><strong>표면이 계속 밝게 마르면 1회 시간 또는 낮 시간대 급수 조정</strong></div>
          <div><span>발아 후</span><strong>뿌리가 자리 잡으면 과습을 피하도록 횟수를 단계적으로 줄임</strong></div>
        </div>
      </section>
      <section className="content-section">
        <div className="section-title"><p>VIDEO ARCHIVE</p><h2>현장 영상 5개</h2><span>원본 영상은 정리 ZIP에 보관했습니다.</span></div>
        <div className="spray-table-card">{videos.map((name,index)=><div key={name}><span>{String(index+1).padStart(2,"0")}</span><strong>{name}</strong></div>)}</div>
      </section>
      <section className="download-banner">
        <div><p>TEXT ARCHIVE</p><h2>Markdown 기록 보기</h2><span>설치 구성, 타이머 설정과 관리 메모를 문서로 보관합니다.</span></div>
        <a href={`${basePath}/downloads/20260905-white-clover-irrigation.md`}>MD 열기</a>
      </section>
      <footer className="site-footer"><b>화곡농장 · 화이트클로버 자동급수 기록</b><span>2026년 9월 5일</span></footer>
      {selected && <div className="spray-modal" role="dialog" aria-modal="true" aria-label={selected.title} onClick={()=>setSelected(null)}><button type="button" aria-label="닫기" onClick={()=>setSelected(null)}>×</button><figure onClick={e=>e.stopPropagation()}><img src={`${basePath}${selected.src}`} alt={selected.title}/><figcaption>{selected.title}</figcaption></figure></div>}
    </main>
  );
}
