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
    <section className="hub-section"><div className="section-title"><p>{record.kind}</p><h2>작업 기록</h2><span>{slug==="deodeok-harvest-20260923"?"촬영 시각 순으로 더덕 씨앗 채취와 수확 과정을 보존합니다.":"중앙 아카이브 데이터에서 생성된 기록입니다."}</span></div>
    {slug==="deodeok-harvest-20260923" && <div className="chat-grid"><article className="chat-card"><h3>12:47 · 더덕 씨앗·삭과</h3><p>더덕 줄기에서 별 모양의 삭과를 확인하고 채취한 기록입니다. 녹색 삭과와 갈색으로 성숙해 가는 삭과가 함께 확인됩니다.</p><ul><li>12:47:11 사진 — 줄기와 삭과 현장</li><li>12:47:13 영상 — 씨앗·삭과 현장</li><li>12:47:25 영상 — 채취 과정</li><li>12:47:28·29 사진 — 삭과 근접 기록</li></ul></article><article className="chat-card"><h3>13:54 · 더덕 굴취·수확</h3><p>밭에서 더덕 뿌리를 굴취했습니다. 굵은 주근과 여러 갈래로 분지된 뿌리를 여러 각도에서 기록했습니다.</p><ul><li>13:54:37 사진 — 수확한 더덕</li><li>13:54:39 영상 — 수확 현장</li><li>13:54:41·42·45 사진 — 굵기·분지 형태</li></ul></article><article className="chat-card"><h3>원본 미디어</h3><p>사진 7장 · 동영상 3개 · MD · HTML · ZIP 원본이 확보되어 있습니다.</p><ul><li>사진: 124711, 124728, 124729, 135437, 135441, 135442, 135445</li><li>영상: 124713, 124725, 135439</li></ul></article></div>}
    <article className="chat-card"><ul>{record.meta.map((x)=><li key={x}>{x}</li>)}</ul><p><b>자산 상태:</b> {record.assetStatus}</p>
    <div className="actions">{record.assets?.html&&<a className="primary-button" href={`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}${record.assets.html}`}>HTML 원본</a>}{record.assets?.md&&<a className="primary-button" href={`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}${record.assets.md}`}>Markdown 원본</a>}<Link className="primary-button" href={record.legacyPath}>기존 상세 기록</Link></div></article></section>
    <footer className="site-footer"><b>화곡농장 아카이브</b><div><Link href="/">프로젝트 홈</Link><a href="https://softm.github.io/projects/">전체 프로젝트</a></div></footer>
  </main>;
}