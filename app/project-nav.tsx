import Link from "next/link";

type Current = "perilla" | "cctv" | "shade" | "clover" | "machine" | "moskill" | "spray" | "harvest" | "onion" | "onionSource" | "sprinkler" | "fertilizer" | "freezer" | "awning";

const chats = [
  { id: "perilla" as Current, href: "/perilla-sowing-after-rain", kind: "재배·파종", title: "12mm 강우 후 늦파종 들깨 파종", meta: "비가 그친 뒤 흙 상태·깊이·복토" },
  { id: "cctv" as Current, href: "/cctv-internet-20260821", kind: "통신·CCTV", title: "농막·하우스 CCTV 인터넷 연결", meta: "핫스팟·Extender N3·Tapo 모델 비교" },
  { id: "shade" as Current, href: "/shade-net-20260807", kind: "시설·차양", title: "6평 농막 그늘막 예상 설치", meta: "긴 면 7.3m·세로 1.8~1.9m·권장 규격" },
  { id: "clover" as Current, href: "/white-clover", kind: "재배·파종", title: "화이트클로버 파종계획", meta: "1kg 종자·황토 배합·살포구역" },
  { id: "machine" as Current, href: "/farm-machine-rental", kind: "농기계·행정", title: "서산시 농기계 임대·운반 서비스", meta: "북부분소·준비서류·파종 장비" },
  { id: "moskill" as Current, href: "/moskill-20260527", kind: "방제·작업기록", title: "2026-05-27 모스킬 잎벌레 방제", meta: "오후 2:30 살포·약 50L·강우 18시" },
  { id: "spray" as Current, href: "/spray-record-20260813", kind: "방제·작업기록", title: "농막 아랫밭 나방노린채 살포", meta: "오전 7시·20L 2통·약제 10mL/통" },
  { id: "harvest" as Current, href: "/20260811-gourd-harvest/", kind: "수확·작업기록", title: "2026-08-11 박 수확 기록", meta: "약 50통·사진 53장·재배지 전경" },
  { id: "onion" as Current, href: "/onion-purchase-20260811", kind: "구매·보관", title: "2026-08-11 양파 구입·저온창고 보관", meta: "구매비 453,000원·약 37망 참고·저온창고" },
  { id: "onionSource" as Current, href: "/onion-sourcing-20260810", kind: "구매·거래처", title: "2026-08-10 양파 구매처 조사", meta: "15kg×30망·총 450kg·가격 및 회신 현황" },
  { id: "sprinkler" as Current, href: "/sprinkler-thread-20260820", kind: "관수·부품", title: "스프링클러 나사 규격", meta: "1/2″·3/4″·수나사 외경 비교" },
  { id: "fertilizer" as Current, href: "/fertilizer-plan", kind: "재배·시비", title: "들깨·열무 밑거름 시비계획", meta: "4개 필지·맞춤18호 5포·비료 비교" },
  { id: "freezer" as Current, href: "/freezer-electric-20260711", kind: "시설·전기", title: "2026-07-11 냉동고 전기 증설", meta: "10SQ 20m·누전차단기 40A" },
  { id: "awning" as Current, href: "/farm-awning-repair-20260711", kind: "시설·행정", title: "2026-07-11 농막 차양막 시정조치", meta: "지면 기둥 개선·대각선 보강·사진 8장" },
];

export function ProjectNav({ current }: { current?: Current }) {
  return (
    <header className="project-header">
      <Link className="project-brand" href="/"><span>화</span><b>화곡농장</b></Link>
      <nav>
        <a href="https://softm.github.io/projects/">전체 프로젝트</a>
        <Link className={current ? "" : "active"} href="/">화곡농장 홈</Link>
        <a href="https://hwagok.softm.chatgpt.site/#hwagok">비공개 사이트</a>
        <details className="chat-switcher">
          <summary><span>채팅별 페이지</span><b>{chats.length}개</b></summary>
          <div className="chat-menu-panel">
            <p><small>화곡농장 프로젝트</small><strong>채팅별 웹사이트</strong></p>
            {chats.map((chat) => (
              <Link
                aria-current={current === chat.id ? "page" : undefined}
                className={current === chat.id ? "current" : ""}
                href={chat.href}
                key={chat.id}
              >
                <small>{current === chat.id ? "현재 페이지" : chat.kind}</small>
                <strong>{chat.title}</strong>
                <span>{chat.meta}</span>
              </Link>
            ))}
          </div>
        </details>
      </nav>
    </header>
  );
}
