import Link from "next/link";
import { ProjectNav } from "../project-nav";

const connectionRows = [
  ["기본 임시안", "데이터함께쓰기 유심 + 남는 핸드폰 핫스팟", "가장 현실적인 1차 구성. 핫스팟 자동 꺼짐과 발열 관리 필요"],
  ["랜선 전용 CCTV", "핫스팟 → ipTIME Extender N3 → LAN → CCTV", "Wi-Fi를 유선 LAN으로 바꿔 연결. DDNS 직접 접속은 어려움"],
  ["장기 운영안", "LTE/5G 라우터 + UPS + CCTV", "전원 복구 후 자동 재접속과 상시 운영 안정성이 가장 좋음"],
  ["저가 USB 동글", "4G LTE USB Wi-Fi 동글", "인식 가능성은 있지만 5G 불가, 장시간 안정성은 검증 필요"],
];

const tapoRows = [
  ["Tapo C110", "실내용", "고정", "3MP", "냉동고 표시창만 고정 확인할 때"],
  ["Tapo C210", "실내용", "회전", "3MP", "냉동고와 컨트롤박스를 번갈아 볼 때"],
  ["Tapo C320WS", "실외용", "고정", "4MP", "농막 외부·하우스 습기·방수 필요 시"],
  ["Tapo C325WB", "실외용", "고정", "4MP", "야간 화질이 매우 중요할 때"],
  ["Tapo C500/C520WS", "실외용", "회전", "2MP~2K", "외부에서 넓은 영역을 돌려볼 때"],
];

const checklist = [
  "핫스팟 이름은 영문/숫자로 단순하게 설정",
  "CCTV·핫스팟폰·Extender N3 모두 상시 전원 연결",
  "CCTV가 제조사 앱/P2P/Cloud/UID 등록 방식을 지원하는지 확인",
  "DDNS·포트포워딩 직접 접속 방식은 핫스팟 환경에서 기대하지 않기",
  "전원 차단 알림과 냉동고 온도센서는 CCTV와 별도로 검토",
];

export default function CctvInternetPage() {
  return (
    <main className="site-page detail-page">
      <ProjectNav current="cctv" />

      <section className="detail-hero" id="top">
        <div>
          <p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>농막·하우스 CCTV 인터넷 연결</b></p>
          <p className="kicker">2026. 8. 21. · LTE 핫스팟·유심·CCTV 연결 검토</p>
          <h1>유선 인터넷이 안 되는 농막은<br /><em>핫스팟으로 먼저 연결하고</em> 라우터로 안정화합니다.</h1>
          <p className="hero-description">농막에는 기존 CCTV가 있으나 인터넷이 없어 실시간 확인이 어렵고, 하우스 냉동고 전원 차단 사고 이후 냉동고·컨트롤박스 상태 확인용 CCTV 구성이 필요합니다. 현재는 SKT 데이터함께쓰기 유심과 남는 핸드폰 핫스팟을 이용한 임시 인터넷 구성이 가장 현실적입니다.</p>
        </div>
        <aside className="metric-card">
          <small>1차 구성</small><h2>핸드폰 핫스팟</h2>
          <dl>
            <div><dt>유심</dt><dd>SKT 5G Nano USIM</dd></div>
            <div><dt>연결</dt><dd>핫스팟 Wi-Fi</dd></div>
            <div><dt>랜선 CCTV</dt><dd>Extender N3 경유</dd></div>
          </dl>
        </aside>
      </section>

      <section className="quick-strip" aria-label="핵심 요약">
        <div><span>01</span><p><b>유선 인터넷</b>현재 설치 불가 판단</p></div>
        <div><span>02</span><p><b>핫스팟</b>즉시 가능한 임시안</p></div>
        <div><span>03</span><p><b>DDNS</b>핫스팟에서는 부적합</p></div>
        <div><span>04</span><p><b>장기안</b>LTE 라우터 + UPS</p></div>
      </section>

      <section className="content-section" id="network">
        <div className="section-title"><p>NETWORK PLAN</p><h2>인터넷 확보 방식</h2><span>핸드폰 핫스팟은 임시 운영용, LTE/5G 라우터는 장기 운영용으로 봅니다.</span></div>
        <div className="office-table" role="table" aria-label="인터넷 구성 비교표">
          <div role="row"><strong role="cell">구분</strong><span role="cell">구성</span><span role="cell">판단</span></div>
          {connectionRows.map(([name, config, note]) => <div role="row" key={name}><strong role="cell">{name}</strong><span role="cell">{config}</span><span role="cell">{note}</span></div>)}
        </div>
        <div className="info-note"><b>핵심:</b> 핫스팟은 밖으로 인터넷 접속은 가능하지만, 외부에서 안으로 직접 들어오는 DDNS·포트포워딩 방식은 어렵습니다. 제조사 앱의 P2P·Cloud 원격보기를 기준으로 테스트해야 합니다.</div>
      </section>

      <section className="content-section tint" id="lan-cctv">
        <div className="section-title"><p>LAN ONLY CCTV</p><h2>랜선만 되는 CCTV 연결 방식</h2><span>ipTIME Extender N3가 핫스팟 Wi-Fi를 받아 LAN 포트로 내보내는 중간 장비 역할을 합니다.</span></div>
        <div className="notice-card"><small>연결 구조</small><h3>핸드폰 핫스팟 → ipTIME Extender N3 → 랜선 → CCTV</h3><p>Extender N3를 핫스팟 Wi-Fi에 연결한 뒤, N3의 LAN 포트와 CCTV를 랜선으로 연결합니다. CCTV는 DHCP 자동 IP를 받아야 하며, 원격 확인은 제조사 앱/P2P 방식이어야 성공 가능성이 높습니다.</p></div>
        <div className="data-cards three">
          <article><h3>설정 1</h3><p>핫스팟 이름과 비밀번호를 영문·숫자 위주로 단순하게 설정합니다.</p></article>
          <article><h3>설정 2</h3><p>Extender N3를 초기화한 후 핫스팟 Wi-Fi에 연결하고 LAN 포트를 활성화합니다.</p></article>
          <article><h3>설정 3</h3><p>CCTV를 재부팅하고 제조사 앱에서 온라인 상태와 원격보기 가능 여부를 확인합니다.</p></article>
        </div>
      </section>

      <section className="content-section" id="camera">
        <div className="section-title"><p>CAMERA SELECTION</p><h2>Tapo 모델별 용도 판단</h2><span>냉동고만 볼 때와 외부 감시까지 할 때는 필요한 모델이 다릅니다.</span></div>
        <div className="office-table" role="table" aria-label="Tapo 모델 비교표">
          <div role="row"><strong role="cell">모델</strong><span role="cell">야외용 여부</span><span role="cell">회전</span><span role="cell">화질</span><span role="cell">추천 용도</span></div>
          {tapoRows.map(([model, outdoor, rotate, quality, use]) => <div role="row" key={model}><strong role="cell">{model}</strong><span role="cell">{outdoor}</span><span role="cell">{rotate}</span><span role="cell">{quality}</span><span role="cell">{use}</span></div>)}
        </div>
        <div className="info-note"><b>현재 판단:</b> 하우스 내부 냉동고만 고정으로 보면 C110도 가능하지만, 냉동고와 컨트롤박스를 함께 보려면 C210이 편합니다. 습기·물방울·외부 설치 가능성이 있으면 C320WS가 더 안전합니다.</div>
      </section>

      <section className="content-section tint" id="storage">
        <div className="section-title"><p>STORAGE & USIM</p><h2>SD카드·유심·저가 동글 판단</h2><span>microSD는 녹화 저장용, 유심은 인터넷 연결용입니다.</span></div>
        <div className="data-cards three">
          <article><small>microSD</small><h3>128GB 이상은 microSDXC</h3><p>32GB는 움직임이 적은 냉동고 확인용으로 가능하지만, 외부 감시와 나무 흔들림까지 있으면 64GB 이상이 안정적입니다.</p></article>
          <article><small>SKT 5G USIM</small><h3>LTE 단말에서는 LTE로 동작</h3><p>5G 유심이라도 4G LTE 동글·라우터에 꽂으면 5G가 아니라 LTE 접속만 가능합니다.</p></article>
          <article><small>저가 USB 동글</small><h3>테스트용은 가능, 상시용은 주의</h3><p>밴드가 맞아도 APN, 단말 제한, 발열, 자동 재접속 안정성 문제가 있을 수 있습니다.</p></article>
        </div>
      </section>

      <section className="content-section dark-section" id="checklist">
        <div className="section-title light"><p>FIELD CHECKLIST</p><h2>현장 설치 전 확인 목록</h2><span>인터넷보다 중요한 것은 끊긴 뒤 다시 살아나는지입니다.</span></div>
        <div className="data-cards two">
          {checklist.map((item, index) => <article key={item}><h3>{String(index + 1).padStart(2, "0")}</h3><p>{item}</p></article>)}
        </div>
      </section>

      <footer className="site-footer"><b>화곡농장 · 농막·하우스 CCTV 인터넷 연결</b><div><Link href="/">프로젝트 홈</Link><a href="#top">맨 위로</a></div></footer>
    </main>
  );
}
