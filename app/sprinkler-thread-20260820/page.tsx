import Link from "next/link";
import { ProjectNav } from "../project-nav";

const threadRows = [
  ["1/2″", "15A", "약 20.9mm", "온라인에서 20mm·2.0cm급으로 표기되기도 함"],
  ["3/4″", "20A", "약 26.4mm", "온라인에서 25mm·2.5cm급으로 표기되기도 함"],
  ["1″", "25A", "약 33.2mm", "25mm라는 단순 길이 환산과는 다른 배관 나사 규격"],
];

export default function SprinklerThreadPage() {
  return (
    <main className="site-page detail-page">
      <ProjectNav current="sprinkler" />

      <section className="detail-hero" id="top">
        <div>
          <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>스프링클러 나사 규격</b></p>
          <p className="kicker">2026. 8. 20. · 스프링클러 연결부 규격 확인</p>
          <h1>1/2인치는 12.7mm가 아니라<br /><em>수나사 외경 약 20.9mm</em>입니다.</h1>
          <p className="hero-description">스프링클러 상품의 1/2″, 3/4″ 배관 나사와 판매자가 적어놓은 2.0cm·2.5cm 표기를 서로 대응시켜 정리했습니다. 배관의 인치 표기는 실제 나사 바깥지름을 그대로 뜻하지 않는 호칭 규격입니다.</p>
        </div>
        <aside className="metric-card">
          <small>핵심 대응</small><h2>스프링클러 수나사</h2>
          <dl>
            <div><dt>1/2″</dt><dd>약 20.9mm</dd></div>
            <div><dt>3/4″</dt><dd>약 26.4mm</dd></div>
            <div><dt>1″</dt><dd>약 33.2mm</dd></div>
          </dl>
        </aside>
      </section>

      <section className="quick-strip" aria-label="핵심 요약">
        <div><span>01</span><p><b>1/2″</b>20~21mm급</p></div>
        <div><span>02</span><p><b>3/4″</b>25~26mm급</p></div>
        <div><span>03</span><p><b>1″</b>약 33mm급</p></div>
        <div><span>04</span><p><b>암나사</b>같은 호칭끼리 체결</p></div>
      </section>

      <section className="content-section" id="standard">
        <div className="section-title"><p>PIPE THREAD SIZE</p><h2>배관 나사 호칭과 실제 수나사 외경</h2><span>인치 숫자를 25.4mm로 단순 곱해서 실제 나사 외경을 계산하면 맞지 않습니다.</span></div>
        <div className="office-table" role="table" aria-label="배관 나사 규격표">
          <div role="row"><strong role="cell">호칭</strong><span role="cell">배관 호칭</span><span role="cell">수나사 최대 외경 · 해석</span></div>
          {threadRows.map(([inch,a,od,note]) => <div role="row" key={inch}><strong role="cell">{inch}</strong><span role="cell">{a}</span><span role="cell"><b>{od}</b> · {note}</span></div>)}
        </div>
        <div className="info-note"><b>중요:</b> “1인치 = 25.4mm”는 길이 단위 환산입니다. 배관 나사에서 1″는 호칭이며, 표준 수나사 외경은 약 33.2mm입니다.</div>
      </section>

      <section className="content-section tint" id="products">
        <div className="section-title"><p>PRODUCT MATCH</p><h2>이번에 본 두 제품은 어떻게 대응하나?</h2><span>첫 제품의 “1/2인치 외부 나사산”과 두 번째 제품의 2.0cm·2.5cm 옵션을 비교했습니다.</span></div>
        <div className="data-cards three">
          <article><small>첫 번째 제품</small><h3>1/2″ 외부 수나사</h3><p>표준 배관 나사 기준으로 수나사 바깥지름이 약 20.9mm인 규격입니다.</p></article>
          <article><small>두 번째 제품</small><h3>2.0cm 옵션</h3><p>판매자의 거친 외경 표기로 보면 20mm급이므로 첫 번째 제품의 1/2″와 대응하는 쪽입니다.</p></article>
          <article><small>두 번째 제품</small><h3>2.5cm 옵션</h3><p>25~26mm급으로 보면 3/4″ 규격 쪽에 해당합니다. 판매 이미지의 “2.5cm / 1inch” 표기는 표준 배관 나사 호칭과 일치하지 않습니다.</p></article>
        </div>
        <div className="notice-card"><small>결론</small><h3>처음 본 1/2″ 스프링클러와 같은 크기를 고른다면 2.0cm 쪽</h3><p>연결 부품은 “1/2″ 암나사”를 선택하는 것이 기준입니다. 암나사 부품의 바깥 몸통 폭이 20mm라는 뜻이 아니라, 약 20.9mm 외경의 1/2″ 수나사와 맞물리는 내부 나사 규격이라는 의미입니다.</p></div>
      </section>

      <section className="content-section" id="male-female">
        <div className="section-title"><p>MALE & FEMALE THREAD</p><h2>수나사 20.9mm와 암나사 내경이 다르게 보이는 이유</h2><span>나사산은 봉우리와 골이 반복되므로 어디를 재는지에 따라 값이 달라집니다.</span></div>
        <div className="data-cards three">
          <article><h3>수나사</h3><p>나사산 봉우리의 가장 바깥쪽끼리 재는 최대지름이 약 20.9mm입니다.</p></article>
          <article><h3>암나사</h3><p>수나사의 봉우리가 들어가는 암나사 골 쪽 최대 직경은 같은 규격에 맞도록 만들어집니다.</p></article>
          <article><h3>입구를 재면</h3><p>암나사 안쪽에서 튀어나온 나사산 봉우리끼리 재면 최대 직경보다 작게 측정될 수 있습니다.</p></article>
        </div>
        <div className="info-note"><b>쉽게 기억:</b> 수나사의 산이 암나사의 골에 들어가 맞물립니다. 따라서 “1/2 수나사 ↔ 1/2 암나사”처럼 같은 호칭끼리 연결합니다.</div>
      </section>

      <section className="content-section dark-section" id="buying">
        <div className="section-title light"><p>BUYING CHECK</p><h2>구매할 때 확인할 것</h2><span>온라인 판매 페이지는 mm·cm·인치를 혼용하는 경우가 있어 호칭과 실제 외경을 함께 확인하는 게 안전합니다.</span></div>
        <div className="data-cards three">
          <article><h3>① 호칭 우선</h3><p>현재 첫 제품이면 1/2″ 암나사를 우선 찾습니다.</p></article>
          <article><h3>② 실측 보조</h3><p>수나사 바깥지름이 약 20~21mm인지 확인하면 1/2″ 여부를 빠르게 가늠할 수 있습니다.</p></article>
          <article><h3>③ 나사 방식 확인</h3><p>PT/BSP 계열과 NPT 등 나사 형식·피치가 다른 제품은 같은 외경급이어도 체결이 맞지 않을 수 있으므로 상품 규격표를 확인합니다.</p></article>
        </div>
      </section>

      <footer className="site-footer"><b>화곡농장 · 스프링클러 나사 규격</b><div><Link href="/">프로젝트 홈</Link><a href="#top">맨 위로</a></div></footer>
    </main>
  );
}
