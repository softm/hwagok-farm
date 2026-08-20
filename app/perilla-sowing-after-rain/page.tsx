import Link from "next/link";
import { ProjectNav } from "../project-nav";

export default function PerillaSowingAfterRainPage() {
  return (
    <main className="site-page detail-page">
      <ProjectNav current="perilla" />

      <section className="detail-hero clover-hero" id="top">
        <div>
          <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>늦파종 들깨 파종</b></p>
          <p className="kicker">2026. 8. 20. 계획 · 8. 21. 오전 10시까지 예상 강수량 12mm</p>
          <h1>비가 그친 뒤 흙이 붙지 않을 때<br /><em>두둑 위에 얕게 심습니다.</em></h1>
          <p className="hero-description">8월 21일 오전 10시까지 약 12mm의 비가 내린 뒤, 이미 만들어 둔 두둑에 늦게 심는 들깨 종자를 직파하는 조건을 기준으로 정리했습니다.</p>
        </div>
        <aside className="metric-card">
          <small>현장 판단</small>
          <strong>파종 가능</strong>
          <div>
            <span><b>12mm</b>파종 전 강우</span>
            <span><b>0.5~1cm</b>파종 깊이</span>
            <span><b>당일 오후</b>흙이 들러붙지 않으면</span>
            <span><b>다음 날</b>질거나 끈적이면</span>
          </div>
        </aside>
      </section>

      <section className="quick-strip" aria-label="핵심 요약">
        <div><span>01</span><p><b>비가 멎은 뒤</b>표면 물기부터 확인</p></div>
        <div><span>02</span><p><b>얕게 파종</b>0.5~1cm 이내</p></div>
        <div><span>03</span><p><b>가볍게 눌러</b>종자와 흙 밀착</p></div>
        <div><span>04</span><p><b>추가 관수</b>흙이 촉촉하면 생략</p></div>
      </section>

      <section className="content-section" id="decision">
        <div className="section-title"><p>FIELD DECISION</p><h2>12mm면 파종 전 수분으로 대체로 충분합니다</h2><span>강수량 숫자만 보지 말고 비가 그친 뒤 두둑 표면과 속흙의 상태를 함께 확인합니다.</span></div>
        <div className="data-cards three">
          <article><small>파종해도 되는 상태</small><h3>뭉쳤다가 쉽게 부서짐</h3><p>손으로 쥐면 가볍게 뭉치지만 손가락으로 건드리면 부서지고, 장갑이나 신발에 진흙이 심하게 묻지 않는 상태입니다.</p></article>
          <article><small>조금 기다릴 상태</small><h3>눌렀을 때 번들거리거나 달라붙음</h3><p>흙이 반죽처럼 늘어나거나 발자국에 물이 차면 파종 구멍이 뭉개지고 과습해질 수 있으므로 표면이 마를 때까지 기다립니다.</p></article>
          <article><small>늦파종 조건</small><h3>마르면 바로 파종</h3><p>파종 시기가 이미 늦으므로 며칠씩 미루기보다, 비가 그친 당일 오후나 다음 날 아침 중 작업 가능한 첫 시점을 택합니다.</p></article>
        </div>
        <div className="info-note"><b>간단한 현장 확인:</b> 두둑 위 흙을 한 줌 쥐어 보고, 손에 진흙이 심하게 묻지 않으면서 덩어리가 가볍게 부서지면 파종하기 좋습니다.</div>
      </section>

      <section className="content-section tint" id="method">
        <div className="section-title"><p>SOWING METHOD</p><h2>두둑 위 직파 순서</h2><span>들깨 종자는 작기 때문에 깊게 묻지 않고, 가는 흙으로 얇게 덮어 수분 접촉을 유지하는 것이 핵심입니다.</span></div>
        <div className="step-grid">
          <article><span>1</span><div><h3>얕은 구멍 만들기</h3><p>두둑 위에 최종 포기 간격 약 20~30cm를 기준으로 0.5~1cm 깊이의 얕은 구멍이나 홈을 만듭니다.</p></div></article>
          <article><span>2</span><div><h3>여러 알 점파</h3><p>발아 불균형을 고려해 한 곳에 약 5~8알씩 떨어뜨립니다. 너무 한곳에 뭉치지 않게 손끝으로 나눠 넣습니다.</p></div></article>
          <article><span>3</span><div><h3>고운 흙으로 얇게 복토</h3><p>종자가 보이지 않을 정도로만 0.5cm 안팎의 고운 흙을 덮습니다. 1cm보다 깊어지지 않게 합니다.</p></div></article>
          <article><span>4</span><div><h3>손바닥으로 가볍게 누르기</h3><p>세게 다지지 말고 종자와 젖은 흙이 밀착될 정도로만 눌러 마르는 속도를 줄입니다.</p></div></article>
        </div>
        <div className="notice-card"><small>관수 판단</small><h3>파종할 때 속흙이 촉촉하면 물을 더 주지 않아도 됩니다</h3><p>표면이 빠르게 하얗게 마르거나 며칠간 비가 없을 때만 가는 물줄기나 분무 형태로 보충합니다. 강한 물줄기는 작은 종자를 씻어내거나 한곳에 몰리게 할 수 있습니다.</p></div>
      </section>

      <section className="content-section" id="aftercare">
        <div className="section-title"><p>AFTERCARE</p><h2>발아 후에는 튼튼한 포기만 남깁니다</h2><span>늦파종은 생육 기간이 짧으므로 발아 상태를 빨리 확인하고 초기 경쟁을 줄입니다.</span></div>
        <div className="data-cards three">
          <article><h3>발아 확인</h3><p>따뜻한 시기에는 대체로 며칠 안에 싹이 보이기 시작합니다. 표면이 굳어 갈라지거나 완전히 마르지 않는지 살핍니다.</p></article>
          <article><h3>솎아주기</h3><p>본잎이 나오고 상태가 구분되면 한 자리에서 튼튼한 1~2포기만 남깁니다.</p></article>
          <article><h3>빈자리 보완</h3><p>발아하지 않은 자리는 초기에만 추가 파종하거나 여분 모종이 있으면 옮겨 심어 재배 기간 손실을 줄입니다.</p></article>
        </div>
        <div className="warning-note"><b>피해야 할 작업:</b> 비가 내리는 중 파종, 물이 고인 흙에 파종, 1cm를 넘는 깊은 복토, 파종 직후 강한 호스 관수는 피합니다.</div>
      </section>

      <section className="content-section dark-section" id="conclusion">
        <div className="section-title light"><p>FINAL PLAN</p><h2>이번 작업의 권장 순서</h2><span>오전 10시경 비가 멎는다는 전제에서 현장 상태에 따라 다음 순서로 진행합니다.</span></div>
        <div className="data-cards three">
          <article><small>오전</small><h3>비가 멎은 뒤 배수 확인</h3><p>두둑에 고인 물이 없는지 보고 표면 물기가 빠질 때까지 기다립니다.</p></article>
          <article><small>오후</small><h3>흙이 붙지 않으면 바로 파종</h3><p>얕게 점파하고 고운 흙으로 덮은 뒤 가볍게 눌러 마무리합니다.</p></article>
          <article><small>다음 날</small><h3>질면 하루만 늦춰 파종</h3><p>흙이 반죽처럼 달라붙는 경우 다음 날 아침 다시 확인하되, 늦파종이므로 작업 가능해지는 즉시 심습니다.</p></article>
        </div>
      </section>

      <footer className="site-footer"><b>화곡농장 · 12mm 강우 후 늦파종 들깨 파종</b><div><Link href="/">프로젝트 홈</Link><a href="#top">맨 위로</a></div></footer>
    </main>
  );
}
