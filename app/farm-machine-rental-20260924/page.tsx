import Link from "next/link";
import { ProjectNav } from "../project-nav";
import { RentalPhotoArchive, RentalVideoArchive } from "./media-archive";

const photos = [
"1000066165.jpg","1000066167.jpg","1000066168.jpg","1000066169.jpg","1000066170.jpg","1000066171.jpg","1000066172.jpg","1000066173.jpg","1000066174.jpg",
"1000066175.jpg","1000066176.jpg","1000066177.jpg","1000066178.jpg","1000066180.jpg","1000066192.jpg","1000066193.jpg","1000066195.jpg","1000066196.jpg"];
const videos=["1000066166.mp4","1000066179.mp4"];
const bp=process.env.NEXT_PUBLIC_BASE_PATH ?? "";

export default function Page(){return <main className="site-page detail-page machine-page">
<ProjectNav current="machineVisit"/>
<section className="detail-hero machine-hero"><div><p className="breadcrumb"><Link href="/">화곡농장</Link><span>›</span><b>2026-09-24 관리기 임대·출고</b></p><p className="kicker">2026. 9. 24. · 서산시농업기술센터 북부 농업기계 임대사업소</p><h1 style={{wordBreak:"keep-all"}}>관리기 임대부터<br/><em>화곡농장 현장 하차까지</em></h1><p className="hero-description">사업소 방문, 이용안내 확인, 아세아 관리기 실물·조작부 확인, 출고, 운송차량 적재, 크레인 하차까지 실제 현장 자료를 순서대로 정리한 작업 기록입니다.</p></div>
<aside className="metric-card machine-card"><small>현장 아카이브</small><h2>2026-09-24</h2><dl><div><dt>사진</dt><dd>18장</dd></div><div><dt>영상</dt><dd>2개</dd></div><div><dt>장비</dt><dd>아세아 관리기</dd></div><div><dt>사업소</dt><dd>북부 · 대산</dd></div></dl></aside></section>

<section className="content-section"><div className="section-title"><p>01 · VISIT</p><h2>북부 농업기계 임대사업소 방문</h2><span>대산읍 대산1로 70 · 041-681-1006</span></div>
<div className="data-cards three"><article><h3>이용 대상</h3><p>관내 농업인. 농업경영체등록증 제출.</p></article><article><h3>임대기간</h3><p>1농가당 1대 원칙, 사용기간 3일 이내.</p></article><article><h3>출고 조건</h3><p>출고 전 안전교육. 자주형 농기계·작업기는 농업인 NH안전보험 가입증명서 확인.</p></article></div>
<div className="info-note"><b>반납:</b> 장비 세척 및 연료 보충. 타인 재임대 금지. 안내문상 고장·파손 시 수리·배상 책임이 명시되어 있습니다.</div></section>

<section className="content-section tint"><div className="section-title"><p>02 · MACHINE</p><h2>아세아 관리기 실물 확인</h2><span>엔진, 배터리, 로터리 작업부, 조향 핸들 및 각종 조작 레버를 현장에서 확인했습니다.</span></div>
<div className="process-grid"><article><span>01</span><div><h3>장비 확인</h3><p>임대사업소 보관 장비 중 사용할 관리기를 확인했습니다.</p></div></article><article><span>02</span><div><h3>조작 설명</h3><p>담당자에게 장비 취급과 조작에 관한 현장 설명을 받았습니다.</p></div></article><article><span>03</span><div><h3>로터리 확인</h3><p>관리기 후방 로터리 작업부와 연결 상태를 사진으로 기록했습니다.</p></div></article><article><span>04</span><div><h3>출고 준비</h3><p>운송 전 장비 상태와 구성품을 확인했습니다.</p></div></article></div></section>

<section className="content-section"><div className="section-title"><p>03 · TRANSPORT</p><h2>운송차량 적재 및 현장 하차</h2></div><p>관리기는 농업기술센터 크레인 장착 화물차로 운송됐으며, 현장 도착 후 크레인을 이용해 하차했습니다. 하차 후 도로에서 장비 상태와 조작 상태를 다시 확인했습니다.</p></section>

<section className="content-section tint"><div className="section-title"><p>04 · PHOTO ARCHIVE</p><h2>현장 사진 18장</h2><span>채팅에 첨부된 원본 파일명을 유지했습니다.</span></div>
<RentalPhotoArchive photos={photos} basePath={bp}/></section>

<section className="content-section"><div className="section-title"><p>05 · VIDEO ARCHIVE</p><h2>현장 동영상 2개</h2></div>
<RentalVideoArchive videos={videos} basePath={bp}/></section>

<section className="content-section dark-section"><div className="section-title light"><p>06 · CONTACT & RETURN</p><h2>연락처와 반납 체크</h2></div>
<div className="contact-layout"><article><small>북부 농업기계 임대사업소</small><h3>대산읍 대산1로 70</h3><a href="tel:0416811006">041-681-1006</a></article><article><h3>반납 전</h3><ul><li>관리기 세척</li><li>연료 보충</li><li>파손·이상 유무 확인</li><li>약속한 기간 내 반납</li></ul></article></div>
<div className="info-note"><b>현장 수기 메모:</b> 대산농협 · 041-660-9900 · 7916. 정확한 용도는 자료만으로 확정하지 않고 원기록 그대로 보존합니다.</div></section>

<section className="content-section"><div className="section-title"><p>07 · SOURCE FILES</p><h2>정리 원본</h2></div><div className="hero-actions"><a className="primary-button" href={bp+"/archive/farm-machine-rental-20260924/record.html"}>HTML 정리본</a><a className="outline-button" href={bp+"/archive/farm-machine-rental-20260924/record.md"}>Markdown 원본</a></div></section>
<footer className="site-footer"><b>화곡농장 · 관리기 임대·출고 기록</b><div><Link href="/">프로젝트 홈</Link><a href="https://softm.github.io/projects/">전체 프로젝트</a></div></footer></main>}
