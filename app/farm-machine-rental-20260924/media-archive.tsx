import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import manifest from "../../archive/farm-machine-rental-20260924.manifest.json";
import styles from "./media-archive.module.css";

const directory = path.join(process.cwd(), "public", "archive", manifest.record);
const validity = new Map<string, boolean>();
function present(name: string): boolean {
  if (validity.has(name)) return validity.get(name)!;
  const expected = manifest.files.find((item) => item.path === `assets/${name}`);
  let valid = false;
  if (expected) {
    try {
      const data = readFileSync(path.join(directory, expected.path));
      valid = data.length === expected.bytes && createHash("sha256").update(data).digest("hex") === expected.sha256;
    } catch { valid = false; }
  }
  validity.set(name, valid);
  return valid;
}
function url(basePath: string, name: string): string {
  return `${basePath}/archive/${manifest.record}/assets/${encodeURIComponent(name)}`;
}
function Pending({ names, label }: { names: string[]; label: string }) {
  if (!names.length) return null;
  return <div className={styles.pending} role="status">
    <strong>{label}: 원본 파일의 웹 반영이 아직 완료되지 않았습니다.</strong>
    <p>실제 파일과 원본 검증값이 확인된 미디어만 표시합니다. 미반영 파일을 정상 배포된 것처럼 표시하지 않습니다.</p>
    <details><summary>미반영 파일 {names.length}개 확인</summary><ul>{names.map((name) => <li key={name}>{name}</li>)}</ul></details>
  </div>;
}
export function RentalPhotoArchive({ photos, basePath }: { photos: string[]; basePath: string }) {
  const ready = photos.filter(present);
  const missing = photos.filter((name) => !present(name));
  return <div className={styles.archive}>
    <p className={styles.status}>웹 배포 확인: 사진 {ready.length} / {photos.length}장</p>
    <Pending names={missing} label="사진" />
    <div className={styles.photos}>{ready.map((name) => <figure className={styles.figure} key={name}>
      <a href={url(basePath, name)} target="_blank" rel="noopener noreferrer" aria-label={`${name} 원본 사진 열기`}>
        <img src={url(basePath, name)} alt={`2026-09-24 관리기 임대 현장 사진 ${photos.indexOf(name) + 1}`} loading="lazy" decoding="async" />
      </a>
      <figcaption>{String(photos.indexOf(name) + 1).padStart(2, "0")} · {name}<span>사진을 누르면 원본이 열립니다.</span></figcaption>
    </figure>)}</div>
  </div>;
}
export function RentalVideoArchive({ videos, basePath }: { videos: string[]; basePath: string }) {
  const playback = (name: string) => name.replace(/\.mp4$/, ".browser.mp4");
  const poster = (name: string) => name.replace(/\.mp4$/, ".poster.jpg");
  const ready = videos.filter((name) => present(name) && present(playback(name)));
  const missing = videos.flatMap((name) => [name, playback(name)].filter((file) => !present(file)));
  return <div className={styles.archive}>
    <p className={styles.status}>웹 재생 준비: 영상 {ready.length} / {videos.length}개 · 촬영 원본은 별도 보존</p>
    <Pending names={missing} label="영상" />
    <div className={styles.videos}>{ready.map((name) => <figure className={styles.figure} key={name}>
      <video controls playsInline preload="metadata" poster={present(poster(name)) ? url(basePath, poster(name)) : undefined} aria-label={`현장 영상 ${videos.indexOf(name) + 1}`}>
        <source src={url(basePath, playback(name))} type="video/mp4" />
        <a href={url(basePath, playback(name))}>영상 파일 열기</a>
      </video>
      <figcaption>영상 {videos.indexOf(name) + 1} · {name}<span><a href={url(basePath, name)} download>촬영 원본</a> · <a href={url(basePath, playback(name))} download>H.264 웹 재생본</a></span></figcaption>
    </figure>)}</div>
  </div>;
}
