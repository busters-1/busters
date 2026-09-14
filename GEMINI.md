# Workspace System Instructions

## 유튜브 메타데이터 생성 규칙 (YouTube Metadata Rules)
유튜브 영상의 제목 및 설명란 작성 시 반드시 아래 규칙을 준수해야 합니다.
상세 규약은 `.agents/rules/youtube_metadata_rules.md`를 단일 진실 공급원(SSOT)으로 삼습니다.

### 필수 엄수 사항
1. **설명란 형식 불변**: '사령군주' 템플릿(3단계 분류 체계)을 100% 동일하게 유지합니다.
2. **불릿 항목 내 줄글 설명 절대 금지 (Zero-Explanation Rule)**:
   - `- {스킬명}` 형태로만 출력하며, 콜론(`:`)이나 괄호(`()`), 부연 설명을 일절 덧붙이지 않습니다.
3. **인게임 텔레그래프 명칭 유지**: 느낌표(`!`) 등 인게임 표기를 그대로 보존합니다.
4. **전용 검증 스크립트 활용**:
   - `python tools/generate_youtube_meta.py "{보스이름}"`를 통해 검증 및 생성된 결과를 사용합니다.
