사이트 점검 및 수정 사항
-----------------------
- (해결) `_config.yml`에 `paginate` 키가 중복/빈 값으로 정의되어 페이지네이션 설정이 모호해지고 경고 가능성이 있었음 → 중복을 제거하고 주석 처리로 비활성화 의도를 명확히 정리.
- (해결) `feed.xml`에서 `site.name` 사용 및 `dc` 네임스페이스 누락으로 RSS 제목 공백/유효성 문제가 있었음 → `site.title` 사용, `absolute_url` 링크 적용, `xmlns:dc` 추가 및 `dc:creator` 기본값 설정.
- (해결) `pinhole camera model` 글의 이미지 경로가 `./assets`로 되어 있어 `/posts/.../assets/...`로 잘못 연결될 수 있었음 → `/assets/...` 절대 경로로 수정.
- (해결) `_posts` 파일명에 공백/대문자와 날짜 불일치가 있어 관리 및 링크 안정성에 문제 소지가 있었음 → 하이픈 기반 소문자 파일명으로 정리하고 날짜를 실제 포스트 날짜에 맞춤.
  - `2025-01-10-pinhole camera model.md` → `2026-01-10-pinhole-camera-model.md`
  - `2025-06-25-award ksbe.md` → `2025-06-25-award-ksbe.md`
  - `2025-12-26-Comparative Study on the Performance of NeRF and 3DGS based models.md` → `2025-12-26-comparative-study-on-the-performance-of-nerf-and-3dgs-based-models.md`
  - `2026-01-03-Segment Anything.md` → `2026-01-03-segment-anything.md`
  - `2026-01-04-Attention is all you need.md` → `2026-01-04-attention-is-all-you-need.md`
  - `2026-01-10-About paper seminar.md` → `2026-01-10-about-paper-seminar.md`

추가로 확인하면 좋은 사항
- 샘플 글(`2025-12-24-notice-sample.md`)이 실제 공개에 불필요하다면 삭제하거나 `_drafts`로 이동을 고려.
- 미사용 가능성이 있는 이미지 폴더(`assets/img/Paper-Review/Segment Any 3D Gaussians`)는 필요 시 정리해 용량/빌드 시간을 줄일 수 있음.
