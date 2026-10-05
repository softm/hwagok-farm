# ZIP·폴더 아카이브 배포 — 최신 기준 적용

기준일: 2026-10-05 / 대상: `softm/hwagok-farm`

## 적용 근거

운영 기준의 원문은 중앙 저장소의 다음 두 파일이다. 실행마다 Git blob SHA를 비교하며, 검토하지 않은 새 정책 버전이면 자동 완료하지 않고 입력을 보존한다.

- `softm/softm.github.io/projects/archive-deployment/archive_deployment_prompt.md`
- `softm/softm.github.io/projects/archive-deployment/20261005_아카이브배포_ZIP폴더_Workflow_처리기준.md`

## 실제 처리 순서

`입력 → 단위 테스트 → 정책 버전 확인 → 전체 본문·원본 보존 → 원본 해시 검증 → 소스 커밋 → 기존 Pages 배포 명시적 호출 → 운영 원본 바이트·본문·미디어 검증 → 중앙 projects.json 동기화 → 서비스 홈·중앙 프로젝트 홈·최상위 projects 실제 렌더링 최종 검증 → 별도 cleanup 커밋`

기록 생성과 배포 완료를 혼동하지 않는다. 수집함이 비어 있는 경우에도 기존 기록 전체가 검증됐다고 보고하지 않는다.

## 변경 사항

| 항목 | 적용 내용 |
|---|---|
| ZIP/폴더 | `zip/*.zip` 및 `zip/<기록폴더>/`를 동일한 처리 단위로 지원한다. |
| 원본·본문 | 새 기록은 입력의 실제 파일을 `source/`에 바이트 그대로 보존하고, 전체 Markdown/HTML 본문을 상세 문서로 사용한다. 원래 문서가 없으면 파일 목록만 있는 문서를 성공 처리하지 않는다. |
| 날짜·제목 | 사건 날짜와 실제 본문 제목을 공유 메타데이터로 기록한다. 날짜 범위는 `dateEnd`와 본문 기간으로 보존한다. 실행일을 사건 날짜로 대체하지 않는다. |
| 기존 경로 | 기존 slug/디렉토리를 이름만 어렵다는 이유로 변경하지 않는다. 동일 입력은 기존 기록을 해시 검증한 뒤 재사용한다. 충돌·미확인 구형 메타데이터는 입력을 보존한다. |
| 폴더 변경 판정 | 폴더 전체의 상대 경로·크기·SHA-256으로 판정한다. `None == None`으로 변경된 폴더를 동일 입력 취급하지 않는다. |
| 공공 범위 | 비공개 표시, 개인정보·의료·계약·농지증여·경영체 등 민감 가능 메타데이터가 있으면 공개 처리/배포를 보류한다. 기존 원문은 임의 삭제하지 않는다. |
| 링크 | 제목은 실제 웹 상세 URL, slug는 실제 GitHub 디렉토리 URL로 연결한다. 이미 인코딩된 한글 URL을 이중 인코딩하지 않는다. |
| 배포 연결 | 기본 `GITHUB_TOKEN` 커밋의 후속 push 이벤트에 의존하지 않고 기존 Pages workflow를 명시적으로 호출한다. 저장소·도메인·Pages 설정은 유지한다. |
| 운영 검증 | 원본 전체 바이트 해시, 실제 브라우저 이미지 디코딩, 영상/음성 재생 진행, 제목 일치, 모바일 화면, 중앙 카드·기록 수까지 검사한다. |
| 중앙 동기화 | 관련 프로젝트의 `links`만 병합하고 다른 프로젝트와 비공개 항목을 보존한다. 권한이 없으면 제안 JSON과 실패 증거를 남기며 입력은 지우지 않는다. |
| 삭제 | 동일 실행·동일 소스 커밋·동일 입력 해시에 연결된 모든 검증 결과가 있어야 한다. 동시 업로드나 원본 변경이 감지되면 삭제하지 않는다. |

## 중앙 저장소 권한

화곡농장 workflow의 기본 토큰은 중앙 `softm/softm.github.io` 쓰기 토큰이 아니다. 중앙 목록에 변경이 필요할 때는 `ARCHIVE_INDEX_TOKEN`이 중앙 저장소의 **Contents: write / Actions: write** 권한을 갖도록 구성해야 한다. 기존 GitHub App 설치 토큰 또는 적절히 제한된 토큰을 사용하며 토큰 값은 Secret에만 둔다.

중앙 데이터가 이미 정확하면 불필요한 쓰기는 하지 않는다. 권한 미설정·쓰기 실패·중앙 운영 반영 지연은 완료가 아니며 cleanup을 차단한다. `.archive-run/central-proposal.json`에 적용 대상 메타데이터가 남는다.

## 실행 파일

- `.github/workflows/process-archive-inbox.yml`: 파이프라인 전체, 실패 시 증거 업로드
- `.github/workflows/deploy-static-pages.yml`: 기존 배포 방식 재사용, 명시적 Pages 빌드/배포 확인
- `scripts/archive_inbox.py`: 전체 본문 변환, 안전 해제, 원본·해시·canonical 메타데이터
- `scripts/archive_completion.py`: 정책 확인, 중앙 동기화, 증거 검증 및 cleanup
- `scripts/verify_archive_live.py`: 운영 파일·실제 브라우저·홈/중앙 검증
- `scripts/audit_archive_public.py`: 공개 범위 사전 검사
- `tests/test_archive_inbox.py`: 보존·충돌·안전 해제·삭제 조건 회귀 검사

## 완료 증거

GitHub Actions의 `archive-completion-evidence`에 `plan.json`, `live.json`, `index-sync.json`, `final.json`, 화면 캡처를 남긴다. cleanup 성공 시 `.archive-ledger/`에 입력 해시와 최종 검증 증거를 별도 커밋으로 남긴다.

**구현·테스트 통과와 기존 29개 기록의 실제 배포/미디어 검증 완료는 별개다.** 기존 기록의 일괄 이동·축약·파일 삭제 또는 공개 범위 변경은 이 코드 반영만으로 수행하지 않는다.
