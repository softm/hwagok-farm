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
  const target = `${base}${record.legacyPath}`;

  // 아카이브 공통 화면은 기존 상세 페이지를 대체하지 않는다.
  // 기존 상세 본문·사진·영상 UI가 있는 페이지를 항상 우선 열어
  // 중앙 목록 때문에 내용이 축약되어 보이지 않도록 한다.
  return <main>
    <meta httpEquiv="refresh" content={`0; url=${target}`} />
    <h1>{record.title}</h1>
    <p>기존 상세 기록으로 이동합니다.</p>
    <p><a href={target}>상세 본문·사진·영상 기록 열기</a></p>
    <p><Link href="/">화곡농장 아카이브 홈</Link></p>
  </main>;
}
