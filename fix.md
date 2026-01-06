사이트 점검 및 수정 사항
-----------------------
- (해결) 모든 포스트가 2025~2026년 미래 날짜라 기본 설정(future: false)에서 목록에 노출되지 않음 → `_config.yml`에 `future: true`를 추가해 실제 포스트가 보이도록 수정.
- (해결) 여러 논문 리뷰 글에서 이미지 경로를 `./assets/...`로 작성해 빌드 후 `/posts/.../assets/...`로 잘못 연결되던 문제 → 모든 경로를 `/assets/...`로 고쳐 홈 기준 절대 경로로 정상 표시되게 수정.
- (해결) 메인 페이지 Award 섹션이 `where` 필터로 배열을 직접 비교해 매칭이 안 될 수 있었음 → `where_exp`로 변경해 `categories`에 `Award`가 포함된 글이 제대로 노출되도록 수정.
- (해결) `index.html`이 프론트매터 시작(`---`)이 빠져 정적 파일로 처리되면서 페이지네이션 경고가 발생하고 제목이 비어 있었음 → 프론트매터를 복원하고 `title: Home`을 추가해 정상 페이지로 빌드되도록 수정.
- (해결) 홈에서 “Latest Posts” 섹션을 제거하고 정적 소개/교육/연구/수상만 노출하도록 단순화. 페이지네이션도 비활성화(`paginate` 제거)해 불필요한 page2 생성 및 빈 페이지 노출을 방지.
- (개선) 관련 글 영역을 한 행에 4개 카드가 가로로 배치되도록(`row-cols-4 flex-nowrap overflow-auto`) 수정해 가독성 향상.
- (보호) 내부 점검용 `fix.md`가 공개 빌드에 포함되지 않도록 `_config.yml` `exclude`에 추가.
- (메모) `bundle exec jekyll serve --future --detach`는 샌드박스 포트 제한(Errno::EPERM)으로 실행하지 못했고, 대신 `bundle exec jekyll build --future`로 빌드 검증 완료.

추가로 확인하면 좋은 사항
- Award/Publication용 레이아웃은 의도적으로 홈으로 리다이렉트하고 있으므로 그대로 유지했습니다.
