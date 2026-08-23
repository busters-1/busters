# ⚔️ 브리미르(Brimir) 버스터즈 — 배포 가이드

공식 도메인: `https://busters.kr/`

## 📁 배포 파일 목록 (`dist/`)
- `index.html`: 브리미르 버스터즈 426종 룬 도감 & 덱 시뮬레이터 (정제 완료)
- `CNAME`: `busters.kr` 커스텀 도메인 설정
- `.nojekyll`: 깃허브 페이지 빌드 가드
- `robots.txt`: 검색엔진 크롤링 최적화
- `sitemap.xml`: 사이트맵

## 🚀 GitHub 배포 명령어
```bash
git init
git add dist .github build_public.py
git commit -m "feat: release Brimir Busters for busters.kr"
git branch -M main
git remote add origin https://github.com/<GITHUB_USERNAME>/<REPO_NAME>.git
git push -u origin main
```
