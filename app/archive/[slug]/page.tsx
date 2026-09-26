import Link from "next/link";
import { notFound } from "next/navigation";
import { archiveRecords } from "../../../archive/records";

export function generateStaticParams(){ return archiveRecords.map((record)=>({slug:record.slug})); }

export default async function ArchivePage({params}:{params:Promise<{slug:string}>}){
  const {slug}=await params;
  const record=archiveRecords.find((item)=>item.slug===slug);
  if(!record) notFound();
  return <main className="site-page">
    <section className="hub-hero"><div className="hub-hero-copy"><p className="kicker">HWAGOK FARM · ARCHIVE</p><h1>{record.title}</h1><p>{record.description}</p><Link className="primary-button" href="/">화곡농장 아카이브 홈</Link></div></section>
    <section className="hub-section"><div className="section-title"><p>{record.kind}</p><h2>아카이브 기록</h2><span>채팅마다 새 React 페이지를 만드는 대신 중앙 아카이브 데이터에서 이 화면을 생성합니다.</span></div>
    <article className="chat-card"><ul>{record.meta.map((x)=><li key={x}>{x}</li>)}</ul><p><b>자산 상태:</b> {record.assetStatus}</p>
    <div className="actions">{record.assets?.html&&<a className="primary-button" href={`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}${record.assets.html}`}>HTML 원본</a>}{record.assets?.md&&<a className="primary-button" href={`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}${record.assets.md}`}>Markdown 원본</a>}<Link className="primary-button" href={record.legacyPath}>기존 상세 기록</Link></div></article></section>
    <footer className="site-footer"><b>화곡농장 아카이브</b><div><Link href="/">프로젝트 홈</Link><a href="https://softm.github.io/projects/">전체 프로젝트</a></div></footer>
  </main>;
}