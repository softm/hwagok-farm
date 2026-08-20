"use client";

import { ProjectNav } from "../project-nav";

export default function MoskillRecordPage(){
  return <main className="site-page spray-page">
    <ProjectNav current="moskill" />
    <section className="spray-hero">
      <div>
        <p className="breadcrumb"><a href="/">화곡농장</a><span>›</span>방제 기록</p>
        <p className="kicker">FIELD LOG · 2026. 05. 27.</p>
        <h1>박밭 잎벌레 피해<br/><em>모스킬 방제 기록</em></h1>
        <p className="hero-description">박 유묘에 잎벌레류가 대량 발생해 모스킬(브로플라닐라이드 액상수화제)을 살포한 기록입니다. 오후 2시 30분경 살포를 시작했고 오후 6시경 비가 내리기 시작했습니다.</p>
        <div className="hero-actions"><a className="primary-button" href="#record">방제 기록 보기</a><a className="outline-button" href="#effect">방제 효과 보기</a></div>
      </div>
      <aside className="spray-dose-card" aria-label="살포량 요약">
        <small>총 살포액</small><strong>약 50<em>L</em></strong>
        <dl><div><dt>분무기</dt><dd>20L × 약 2.5회</dd></div><div><dt>대상 구역</dt><dd>3개 두둑</dd></div><div><dt>강우 전 시간</dt><dd>약 3시간 30분</dd></div></dl>
      </aside>
    </section>

    <section className="spray-summary-strip" aria-label="작업 핵심 정보">
      <div><span>01</span><p><small>방제일</small><b>2026년 5월 27일</b></p></div>
      <div><span>02</span><p><small>살포 시작</small><b>오후 2시 30분경</b></p></div>
      <div><span>03</span><p><small>강우 시작</small><b>오후 6시경</b></p></div>
      <div><span>04</span><p><small>사용 약제</small><b>모스킬</b></p></div>
    </section>

    <section className="content-section" id="record">
      <div className="section-title"><p>APPLICATION RECORD</p><h2>살포 및 구매 기록</h2><span>현장에서 확인한 실제 작업 내용을 기준으로 정리했습니다.</span></div>
      <div className="spray-record-layout">
        <article className="spray-table-card">
          <div><span>방제일</span><strong>2026년 5월 27일</strong></div>
          <div><span>사용 약제</span><strong>모스킬 · 브로플라닐라이드 액상수화제</strong></div>
          <div><span>구매처</span><strong>대산읍 한국농자재마트</strong></div>
          <div><span>구매가격</span><strong>13,000원</strong></div>
          <div><span>살포 구역</span><strong>박 재배 3개 두둑</strong></div>
          <div><span>살포량</span><strong>20L 분무기 × 약 2.5회 = 약 50L</strong></div>
          <div><span>살포 시각</span><strong>오후 2시 30분경</strong></div>
          <div><span>강우 시각</span><strong>오후 6시경 · 살포 약 3시간 30분 후</strong></div>
        </article>
        <aside className="spray-note-card"><small>FIELD NOTE</small><h3>살포 후<br/>약효가 현장에서 확인됨</h3><p>약제를 맞은 잎벌레들이 흐느적거리고 정상적으로 날지 못하는 모습이 관찰됐습니다. 약효가 나타난 개체 약 100마리는 손으로 직접 제거했습니다.</p><div><b>약 100마리</b><span>직접 제거</span><strong>1차 방제</strong></div></aside>
      </div>
    </section>

    <section className="content-section tint" id="effect">
      <div className="section-title"><p>PEST & EFFECT</p><h2>피해 양상과 방제 효과</h2><span>박 유묘 잎을 심하게 갉아먹는 주황색 잎벌레류가 다수 확인되었습니다.</span></div>
      <div className="spray-record-layout">
        <article className="spray-table-card">
          <div><span>피해 형태</span><strong>잎 표면 식해 · 구멍 · 잎맥만 남는 심한 피해</strong></div>
          <div><span>발생 정도</span><strong>한 포기에 다수의 성충이 모여 섭식</strong></div>
          <div><span>살포 직후 반응</span><strong>움직임 둔화 · 비행 능력 저하 · 흐느적거림</strong></div>
          <div><span>강우 영향</span><strong>살포 후 약 3시간 30분 뒤 강우 시작</strong></div>
          <div><span>현장 판단</span><strong>비가 오기 전 이미 약효가 상당 부분 발현된 것으로 관찰</strong></div>
        </article>
        <aside className="spray-note-card"><small>FOLLOW-UP</small><h3>다음날<br/>새 피해를 확인</h3><p>재살포는 즉시 반복하기보다 다음날 살아 있는 개체 수와 새 잎 피해가 계속되는지를 확인한 뒤 제품 라벨의 사용 간격과 횟수에 맞춰 판단합니다.</p></aside>
      </div>
    </section>

    <section className="spray-check-section">
      <div><p>RECORD NOTE</p><h2>이번 방제에서<br/>남긴 핵심 기록</h2></div>
      <ul>
        <li><span>01</span><div><b>살포 후 3시간 30분 뒤 비</b><p>살포 직후 바로 내린 비는 아니며 그 전에 해충 행동 저하가 관찰됐습니다.</p></div></li>
        <li><span>02</span><div><b>대량 발생 확인</b><p>박 유묘 잎에 주황색 잎벌레류가 집중적으로 붙어 심한 식해 피해가 있었습니다.</p></div></li>
        <li><span>03</span><div><b>약효 발현 확인</b><p>흐느적거리고 날지 못하는 개체가 다수 나타났습니다.</p></div></li>
        <li><span>04</span><div><b>물리적 제거 병행</b><p>약효가 나타난 개체 약 100마리를 손으로 직접 제거했습니다.</p></div></li>
      </ul>
    </section>

    <footer className="site-footer"><b>화곡농장 · 모스킬 방제 기록</b><span>2026년 5월 27일 · 박밭 잎벌레 방제</span></footer>
  </main>
}
