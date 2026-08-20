"use client";

import Link from "next/link";
import { ProjectNav } from "../project-nav";

const fields = [
  { lot: "667-34", area: "559㎡", pyeong: "169.1평", crop: "들깨", fertilizer: "30kg", bags: "1.5포" },
  { lot: "667-3", area: "372㎡", pyeong: "112.5평", crop: "들깨", fertilizer: "20kg", bags: "1포" },
  { lot: "아래 밭", area: "420.3㎡", pyeong: "127.1평", crop: "들깨", fertilizer: "25kg", bags: "1.25포" },
  { lot: "667-4", area: "290㎡", pyeong: "87.7평", crop: "열무", fertilizer: "25kg", bags: "1.25포" },
];

const products = [
  { name: "맞춤18호", formula: "21-13-9 + 붕소", role: "복합비료 · 밑거름", note: "질소·인산·칼리를 공급하는 기본 밑거름. 파종 전 전체 살포 후 로터리로 혼합." },
  { name: "비황골드", formula: "20kg/포", role: "유기물·토양개량", note: "포대 표기 과수·원예 기준 1,000㎡당 15~20포. 화학비료와 병행할 때는 토양상태와 실제 시비량을 함께 고려." },
  { name: "명품비료", formula: "14-3-6", role: "복합비료", note: "칼슘·황·붕소·유기물 함유. 맞춤18호와 중복 투입할 때는 총 질소량이 과하지 않도록 조정." },
];

export default function FertilizerPlanPage() {
  return (
    <main className="site-page detail-page fertilizer-page">
      <ProjectNav current="fertilizer" />
      <section className="detail-hero">
        <div>
          <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>들깨·열무 밑거름 계획</b></p>
          <p className="kicker">화곡농장 · 4개 필지 · 밑거름 살포</p>
          <h1>들깨·열무<br />밑거름 시비 계획</h1>
          <p className="hero-description">화곡리 667-34, 667-3, 667-4와 아래 밭 총 1,641.3㎡(약 496.5평)의 작목 배치와 맞춤18호 살포량, 비황골드·명품비료의 역할, 트랙터 로터리 전 작업순서를 정리한 현장용 페이지입니다.</p>
        </div>
        <aside className="metric-card">
          <small>전체 재배면적</small><strong>1,641.3㎡</strong>
          <div><span><b>496.5평</b>약 500평</span><span><b>3필지</b>들깨</span><span><b>1필지</b>열무</span><span><b>5포</b>맞춤18호 기준</span></div>
        </aside>
      </section>

      <section className="quick-strip" aria-label="핵심 작업 요약">
        <div><span>01</span><p><b>비황골드</b>전체에 균일 살포</p></div>
        <div><span>02</span><p><b>맞춤18호</b>필지별 정량 살포</p></div>
        <div><span>03</span><p><b>트랙터 로터리</b>흙과 충분히 혼합</p></div>
        <div><span>04</span><p><b>두둑·파종</b>작목별 진행</p></div>
      </section>

      <section className="content-section" id="fields">
        <div className="section-title"><p>FIELD PLAN</p><h2>필지별 작목과 면적</h2><span>아래 밭·667-34·667-3은 들깨, 667-4는 열무입니다.</span></div>
        <div style={{overflowX:"auto"}}><table style={{width:"100%",borderCollapse:"collapse",background:"white"}}><thead><tr><th>필지</th><th>면적</th><th>평수</th><th>작물</th></tr></thead><tbody>{fields.map(f=><tr key={f.lot}><td><b>{f.lot}</b></td><td>{f.area}</td><td>{f.pyeong}</td><td>{f.crop}</td></tr>)}</tbody></table></div>
      </section>

      <section className="content-section tint" id="custom18">
        <div className="section-title"><p>CUSTOM 18</p><h2>맞춤18호 필지별 살포량</h2><span>20kg 한 포 기준 총 5포(100kg)를 작업 기준으로 나눈 표입니다.</span></div>
        <div style={{overflowX:"auto"}}><table style={{width:"100%",borderCollapse:"collapse",background:"white"}}><thead><tr><th>필지</th><th>작물</th><th>면적</th><th>맞춤18호</th><th>포대 환산</th></tr></thead><tbody>{fields.map(f=><tr key={f.lot}><td><b>{f.lot}</b></td><td>{f.crop}</td><td>{f.area}</td><td><b>{f.fertilizer}</b></td><td>{f.bags}</td></tr>)}</tbody><tfoot><tr><td colSpan={3}><b>합계</b></td><td><b>100kg</b></td><td><b>5포</b></td></tr></tfoot></table></div>
        <div className="warning-note"><b>들깨 주의:</b> 질소를 과하게 주면 웃자람과 도복 위험이 있으므로 추가 요소비료는 작물 상태를 본 뒤 결정합니다.</div>
      </section>

      <section className="content-section" id="products">
        <div className="section-title"><p>FERTILIZER NOTES</p><h2>사용 비료 비교</h2><span>현재 대화에서 확인한 포대 표기와 사용 목적을 기준으로 정리했습니다.</span></div>
        <div className="data-cards four">{products.map(p=><article key={p.name}><small>{p.role}</small><strong>{p.name}</strong><p><b>{p.formula}</b><br/>{p.note}</p></article>)}</div>
        <div className="info-note">비황골드 포대의 과수·원예 표기는 1,000㎡당 15~20포입니다. 다만 맞춤18호 같은 화학비료를 함께 쓰는 경우 제품 권장량을 단순 합산하기보다 토양검정·전작·퇴비 투입량을 고려해 조정하는 것이 안전합니다.</div>
      </section>

      <section className="content-section dark-section" id="workflow">
        <div className="section-title light"><p>TRACTOR WORKFLOW</p><h2>트랙터 갈기 전 살포방법</h2><span>밑거름은 두둑 한 곳에 몰지 말고 경작 예정 면적 전체에 최대한 균일하게 뿌립니다.</span></div>
        <div className="workflow-grid">
          <article><span>01</span><div><h3>필지별 양을 먼저 나누기</h3><p>포대를 밭에 들어가기 전에 필지별 목표량으로 구분합니다.</p></div></article>
          <article><span>02</span><div><h3>전체 면적에 고르게 살포</h3><p>한 방향으로 절반, 직각 방향으로 나머지 절반을 뿌리면 편차를 줄이기 좋습니다.</p></div></article>
          <article><span>03</span><div><h3>한곳에 쏟지 않기</h3><p>비료가 뭉치면 염류장해와 국부적인 과비 위험이 커집니다.</p></div></article>
          <article><span>04</span><div><h3>로터리로 혼합</h3><p>살포 후 트랙터 로터리 작업으로 표토와 밑거름을 골고루 섞습니다.</p></div></article>
          <article><span>05</span><div><h3>두둑 만들기</h3><p>로터리 후 작물에 맞게 두둑을 만들고 들깨·열무 파종을 준비합니다.</p></div></article>
          <article><span>06</span><div><h3>추비는 생육 보고 결정</h3><p>특히 들깨는 초기부터 질소를 과하게 더하지 않고 생육상태를 확인합니다.</p></div></article>
        </div>
      </section>

      <section className="content-section">
        <div className="section-title"><p>PHOTO RECORD</p><h2>대화에서 확인한 현장 사진자료</h2><span>맞춤18호 포대, 비황골드 포대 및 사용량 표기, 명품비료 14-3-6, 필지 지도 이미지를 근거로 이번 시비계획을 정리했습니다.</span></div>
        <div className="data-cards four"><article><small>첨부사진</small><strong>맞춤18호</strong><p>21-13-9 계열 복합비료 포대 확인</p></article><article><small>첨부사진</small><strong>비황골드</strong><p>20kg 포대 및 과수·원예 15~20포/1,000㎡ 표기 확인</p></article><article><small>첨부사진</small><strong>명품비료</strong><p>14-3-6 및 칼슘·황·붕소·유기물 표기 확인</p></article><article><small>첨부지도</small><strong>4개 필지</strong><p>667-34·667-3·667-4·아래 밭 면적 배치 확인</p></article></div>
      </section>

      <footer className="site-footer"><b>화곡농장 · 들깨·열무 밑거름 계획</b><Link href="/">프로젝트 홈으로 돌아가기</Link></footer>
    </main>
  );
}
