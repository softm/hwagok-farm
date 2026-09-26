# 아세아 관리기 엔진 정지 · 원본 업로드 상태

현재 이 저장소에는 본문 Markdown과 자동 반영 코드가 등록되어 있습니다. **사진 7장과 원본 ZIP의 저장소 전송은 아직 완료되지 않았습니다.** 사진 대신 누락 상태를 표시합니다.

## 남은 작업: 원본 ZIP 한 파일

이 폴더에 `source.zip`을 업로드해 기존 `main` 브랜치에 커밋합니다. 새 저장소·브랜치는 필요하지 않습니다.

- 업로드: https://github.com/softm/hwagok-farm/upload/main/public/archive/asea-engine-stop-20260922
- 파일: 대화에서 제공한 사진 포함 원본 ZIP과 동일한 파일을 `source.zip`으로 저장한 것
- 크기: 4,547,477바이트
- SHA-256: `54b16715901581fd10e04b77e184fa05c53faa0041ebd29ddd8d25ea3261c84f`

기존 `npm run build`의 prebuild가 ZIP의 해시를 확인하고 원본 PNG 7장·MD·HTML을 추출합니다. 사진은 자르거나 재압축하지 않습니다. 다른 ZIP이면 기존 기록을 덮어쓰지 않고 빌드가 중단됩니다.

`archive/records.ts`는 빌드 시 기존 항목을 보존하면서 이 기록만 추가·갱신합니다. 공통 아카이브 화면과 화곡농장 홈에 자동 연결됩니다. 정리일 2026-09-22는 자료에 기록된 날짜이며 실제 촬영일을 뜻하지 않습니다.

## 확인 주소

- 본문: https://softm.github.io/hwagok-farm/archive/asea-engine-stop-20260922/record.html
- 상태: https://softm.github.io/hwagok-farm/archive/asea-engine-stop-20260922/status.json
- 아카이브: https://softm.github.io/hwagok-farm/archive/asea-engine-stop-20260922/
- 전체 프로젝트: https://softm.github.io/projects/

`publishedImages: 7`, 원본 ZIP 다운로드, 일곱 사진의 표시까지 확인한 뒤 사진 포함 공개배포 완료로 판단합니다.
