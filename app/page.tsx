import Link from "next/link";
import { archiveRecords } from "../archive/records";

export default function Home(){
 return <main className="site-page">
  <section className="hub-hero"><div className="hub-hero-copy"><p className="kicker">HWAGOK FARM · ARCHIVE</p><h1>화곡농장<br/><em>채팅 아카이브</em></h1><p>재배·방제·관수·수확·농기계 기록을 중앙 아카이브 목록으로 관리합니다. 새 기록마다 별도 React 페이지를 추가하지 않습니다.</p><a className="primary-button" href="#archive">아카이브 보기</a></div><aside className="hub-status"><span className="status-label">공개 아카이브</span><strong>{archiveRecords.length}</strong><b>기록</b><div><span>프로젝트</span><b>화곡농장</b></div><div><span>최근 기록</span><b>2026. 9. 24.</b></div></aside></section>
  <section className="hub-section" id="archive"><div className="section-title"><p>ARCHIVE RECORDS</p><h2>화곡농장 기록</h2><span>중앙 manifest에서 생성되는 아카이브 목록입니다.</span></div><div className="chat-grid">{archiveRecords.map((r,i)=><article className="chat-card" key={r.slug}><div className="chat-card-top"><span>{String(i+1).padStart(2,"0")}</span><small>{r.kind}</small></div><h3>{r.title}</h3><p>{r.description}</p><ul>{r.meta.map(x=><li key={x}>{x}</li>)}</ul><Link className="chat-card-link" href={`/archive/${r.slug}/`}><b>아카이브 열기</b><span>↗</span></Link></article>)}</div></section>
  <section className="hub-section"><div className="section-title"><p>REPOSITORIES · PRIVATE ACCESS</p><h2>저장소와 비공개 인증</h2><span>프로젝트 비밀번호와 Vercel Deployment Protection은 서로 다른 인증입니다.</span></div><div className="chat-grid">
   <a className="chat-card" href="https://github.com/softm/hwagok-farm"><h3>GitHub 공개 저장소</h3><p>공개 아카이브 원본과 사이트 소스</p></a>
   <a className="chat-card" href="https://github.com/softm/hwagok-farm-private"><h3>🔒 GitHub 비공개 저장소</h3><p>권한 있는 GitHub 계정으로 원본 접근</p></a>
   <a className="chat-card" href="https://hwagok-farm-private.vercel.app/"><h3>🔑 프로젝트 비밀번호로 열기</h3><p>애플리케이션 자체 비밀번호 인증</p></a>
   <a className="chat-card" href="https://hwagok-farm-private.vercel.app/"><h3>▲ Vercel 계정 인증으로 열기</h3><p>Deployment Protection이 활성화된 경우 Vercel 로그인 후 접근</p></a>
  </div></section>
  <section className="structure-section"><div><p>ARCHIVE POLICY</p><h2>기록은 데이터로,<br/>화면은 하나의 구조로</h2></div><ol><li><span>01</span><div><b>중앙 아카이브 manifest</b><p>기록 목록과 메타데이터를 archive/records.ts에서 관리합니다.</p></div></li><li><span>02</span><div><b>공통 상세 화면</b><p>모든 기록은 /archive/[slug] 공통 화면으로 표시합니다.</p></div></li><li><span>03</span><div><b>원본 자산 보존</b><p>MD·HTML·사진·영상·ZIP을 가능한 범위에서 아카이브 자산으로 보존하고 누락은 상태값으로 표시합니다.</p></div></li></ol></section>
  <footer className="site-footer"><b>화곡농장 프로젝트</b><div><a href="https://softm.github.io/projects/">전체 프로젝트</a><a href="https://hwagok-farm-private.vercel.app/">비공개 사이트</a><a href="https://github.com/softm/hwagok-farm-private">Private GitHub</a></div></footer>
 </main>;
}