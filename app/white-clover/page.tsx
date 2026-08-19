"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ProjectNav } from "../project-nav";

type PreviewImage = { src: string; alt: string; caption: string };

const images: PreviewImage[] = [
  { src: "https://hwagok.softm.chatgpt.site/assets/target-area.png", alt: "파란색으로 표시된 화이트클로버 살포 대상 구역", caption: "① 파란 살포 대상구역" },
  { src: "https://hwagok.softm.chatgpt.site/assets/product-info.png", alt: "화이트클로버 상품의 파종정보", caption: "② 상품 파종정보" },
  { src: "https://hwagok.softm.chatgpt.site/assets/seed-zones.png", alt: "75평 단위로 구분한 화이트클로버 살포계획 지도", caption: "③ 75평 단위 살포계획" },
];

const qaRows = [
  ["제초 후 파종", "마른 풀을 걷어내 씨앗이 맨흙에 닿게 하고, 사용한 제초제의 재파종 가능 기간을 확인합니다."],
  ["경사지", "표면에 뿌린 뒤 발·롤러·넓은 판으로 눌러 밀착하고 집중호우 직전은 피합니다."],
  ["코팅종자", "물에 불리지 않고 마른 황토와 파종 직전에 섞습니다. 젖었다면 저장하지 말고 바로 파종합니다."],
  ["자연 확산", "꽃이 씨를 맺게 일부 남기고, 땅 위 포복경이 마디에서 뿌리내리도록 관리합니다."],
  ["파종량", "1kg/30~50평은 촘촘한 조경 피복 기준입니다. 이 농장은 1kg/300평의 저밀도 도입 방식입니다."],
];

export default function WhiteCloverPage() {
  const [preview, setPreview] = useState<PreviewImage | null>(null);

  useEffect(() => {
    const close = (event: KeyboardEvent) => event.key === "Escape" && setPreview(null);
    document.addEventListener("keydown", close);
    return () => document.removeEventListener("keydown", close);
  }, []);

  return (
    <main className="site-page detail-page clover-page">
      <ProjectNav current="clover" />
      <section className="detail-hero clover-hero" id="top">
        <div>
          <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>화이트클로버 파종계획</b></p>
          <p className="kicker">2026. 8. 18. · 충남 서산</p>
          <h1>엄나무밭<br />화이트클로버 파종계획</h1>
          <p className="hero-description">파란 표시구역 약 622평을 종자 2kg으로 저밀도 도입하고, 마른 황토를 이용해 손으로 균일하게 흩어뿌리는 현장 실행안입니다.</p>
          <div className="hero-actions"><a className="primary-button" href="#zones">살포구역 보기</a><a className="outline-button" href="https://hwagok.softm.chatgpt.site/downloads/hwagok-white-clover-report.zip" download>전체 보고서 ZIP</a></div>
        </div>
        <aside className="metric-card">
          <small>최종 실행기준</small><strong>1kg / 300평</strong>
          <div><span><b>2kg</b>전체 종자</span><span><b>622평</b>표시 면적</span><span><b>20kg</b>1포당 황토</span><span><b>250g</b>75평 작업분</span></div>
        </aside>
      </section>

      <section className="quick-strip" aria-label="핵심 작업 요약">
        <div><span>01</span><p><b>종자 1포</b>1kg을 4등분</p></div>
        <div><span>02</span><p><b>마른 황토</b>20kg을 4등분</p></div>
        <div><span>03</span><p><b>한 작업분</b>250g＋황토 5kg</p></div>
        <div><span>04</span><p><b>교차 살포</b>75평 가로·세로</p></div>
      </section>

      <section className="content-section" id="zones">
        <div className="section-title"><p>SEEDING ZONES</p><h2>75평 단위 살포계획</h2><span>지도 경계는 위성사진의 면적비로 나눈 작업용 근사선이며, 현장에서는 엄나무 열과 통로에 맞춰 조정합니다.</span></div>
        <button className="featured-map" type="button" onClick={() => setPreview(images[2])} aria-label="살포계획 지도 확대">
          <img src="https://hwagok.softm.chatgpt.site/assets/seed-zones.png" alt="75평 단위 화이트클로버 살포계획 지도" /><span>눌러서 크게 보기</span>
        </button>
        <div className="data-cards four">
          <article><small>기본구역</small><strong>1~7</strong><p>각 75평 · 종자 250g</p></article>
          <article><small>왼쪽 잔여</small><strong>9평</strong><p>종자 약 31g</p></article>
          <article><small>상단 잔여</small><strong>46평</strong><p>종자 약 154g</p></article>
          <article><small>하단 잔여</small><strong>41평</strong><p>종자 약 138g</p></article>
        </div>
        <div className="info-note">622평을 정확히 계산하면 약 2.07kg이지만, 엄나무 줄기 반경 50cm와 통로를 제외하므로 실제 준비량은 2kg으로 맞춥니다.</div>
      </section>

      <section className="content-section tint" id="mix">
        <div className="section-title"><p>DRY YELLOW SOIL</p><h2>황토 단독 배합</h2><span>황토는 비료나 복토용이 아니라 코팅종자를 손으로 균일하게 뿌리기 위한 부피재입니다.</span></div>
        <div className="mix-layout">
          <div className="formula-card"><p>종자 1kg 한 포대</p><div><strong>1kg</strong><i>＋</i><strong>20kg</strong></div><small>코팅종자　　마른 황토</small><hr /><p>75평 한 작업분</p><div><strong>250g</strong><i>＋</i><strong>5kg</strong></div><small>코팅종자　　마른 황토</small></div>
          <div className="step-grid">
            <article><span>1</span><div><h3>바싹 말리기</h3><p>수분이 있으면 황토와 종자가 뭉쳐 한곳에 떨어집니다.</p></div></article>
            <article><span>2</span><div><h3>체로 거르기</h3><p>돌·풀뿌리·찰흙 덩어리를 제거합니다.</p></div></article>
            <article><span>3</span><div><h3>나누어 섞기</h3><p>3~4번에 나누어 넣고 아래에서 위로 뒤집습니다.</p></div></article>
            <article><span>4</span><div><h3>즉시 살포</h3><p>코팅종자는 물에 불리지 않고 혼합 뒤 바로 뿌립니다.</p></div></article>
          </div>
        </div>
        <div className="warning-note"><b>사용 금지:</b> 젖은 황토, 제초제·농약·고농도 비료가 섞인 흙, 손으로 흩어지지 않는 큰 덩어리</div>
      </section>

      <section className="content-section" id="workflow">
        <div className="section-title"><p>FIELD WORKFLOW</p><h2>현장 작업순서</h2></div>
        <div className="workflow-grid">
          {[ ["01","제초제 확인","약제 라벨에서 파종·재식 가능 기간을 확인합니다."], ["02","마른 잡초 정리","낮게 예초하고 풀·낙엽을 걷어 씨앗이 맨흙에 닿게 합니다."], ["03","구역 표시","엄나무 줄기 반경 50cm와 통로를 비우고 75평 경계를 표시합니다."], ["04","황토 혼합","종자 250g과 마른 황토 5kg을 한 작업분으로 준비합니다."], ["05","가로·세로 살포","절반은 한 방향, 나머지는 직각 방향으로 걸으며 뿌립니다."], ["06","눌러 밀착","발·롤러·넓은 판으로 누르고 복토는 0~5mm만 처리합니다."] ].map(([no,title,body]) => <article key={no}><span>{no}</span><div><h3>{title}</h3><p>{body}</p></div></article>)}
        </div>
      </section>

      <section className="content-section dark-section">
        <div className="section-title light"><p>SELLER Q&amp;A REVIEW</p><h2>판매자 질의답변 핵심</h2><span>도움 되는 정보는 반영하고 서로 다른 답변은 화곡농장 조건에 맞춰 정리했습니다.</span></div>
        <div className="qa-grid">{qaRows.map(([title, body]) => <article key={title}><h3>{title}</h3><p>{body}</p></article>)}</div>
        <div className="dark-note">판매자가 제시한 발아율 80%는 현장 피복률 보장이 아닙니다. 토양 접촉, 수분, 유실, 잔존 잡초 때문에 빈 곳은 후속 보충합니다.</div>
      </section>

      <section className="content-section">
        <div className="section-title"><p>REFERENCE IMAGES</p><h2>지도와 상품자료</h2><span>각 이미지를 누르면 원본 크기의 레이어 화면으로 확인할 수 있습니다.</span></div>
        <div className="media-grid">{images.map((item) => <button type="button" key={item.src} onClick={() => setPreview(item)}><img src={item.src} alt={item.alt} /><span>{item.caption}</span></button>)}</div>
      </section>

      <section className="download-banner"><div><p>OFFLINE REPORT</p><h2>전체 자료를 내려받으세요.</h2><span>Markdown, HTML, 원본 지도, 상품정보, 75평 살포계획 지도가 포함됩니다.</span></div><a href="https://hwagok.softm.chatgpt.site/downloads/hwagok-white-clover-report.zip" download>전체 보고서 ZIP</a></section>
      <footer className="site-footer"><b>화곡농장 · 화이트클로버 파종계획</b><Link href="/">프로젝트 홈으로 돌아가기</Link></footer>

      {preview && <div className="layer-modal" role="dialog" aria-modal="true" aria-label={preview.caption} onClick={() => setPreview(null)}><button type="button" onClick={() => setPreview(null)} aria-label="닫기">×</button><figure onClick={(event) => event.stopPropagation()}><img src={preview.src} alt={preview.alt} /><figcaption>{preview.caption}</figcaption></figure></div>}
    </main>
  );
}
