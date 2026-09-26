import Link from "next/link";
import { notFound } from "next/navigation";
import { archiveRecords } from "../../../archive/records";

export function generateStaticParams() {
  return archiveRecords.map((record) => ({ slug: record.slug }));
}

export default async function ArchivePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const record = archiveRecords.find((item) => item.slug === slug);
  if (!record) notFound();
  const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  const documentUrl = record.assets?.html ? `${base}${record.assets.html}` : undefined;
  if (record.assetStatus === "complete" && documentUrl) {
    return <main>
      <meta httpEquiv="refresh" content={`0; url=${documentUrl}`} />
      <h1>{record.title}</h1>
      <p><a href={documentUrl}>사진·영상이 포함된 전체 아카이브 열기</a></p>
    </main>;
  }
  return <main className="site-page">
    <section className="hub-hero"><div className="hub-hero-copy">
      <p className="kicker">HWAGOK FARM · ARCHIVE</p>
      <h1>{record.title}</h1><p>{record.description}</p>
      <Link className="primary-button" href="/">화곡농장 아카이브 홈</Link>
    </div></section>
    <section className="hub-section"><div className="section-title"><p>{record.kind}</p><h2>기록과 첨부자료</h2></div>
      <article className="chat-card"><ul>{record.meta.map((item) => <li key={item}>{item}</li>)}</ul>
        <p>자산 점검 상태: {record.assetStatus}</p>
        <div className="actions">
          {documentUrl && <a className="primary-button" href={documentUrl}>HTML 기록</a>}
          {record.assets?.md && <a className="primary-button" href={`${base}${record.assets.md}`}>Markdown</a>}
          {record.assets?.zip && <a className="primary-button" href={`${base}${record.assets.zip}`} download>전체 ZIP</a>}
          <Link className="primary-button" href={record.legacyPath}>기존 상세 기록</Link>
        </div>
      </article>
    </section>
    <footer className="site-footer"><b>화곡농장 아카이브</b><div><Link href="/">프로젝트 홈</Link><a href="https://softm.github.io/projects/">전체 프로젝트</a></div></footer>
  </main>;
}
