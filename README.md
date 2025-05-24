# 🌐 네트워크 학습 포털 (Network Learning Portal)

> 경제학도를 위한 네트워크 개념 학습 및 NetworkX 시각화 실습 플랫폼

## 🚀 Live Demo
🔗 **[네트워크 학습 포털 방문하기](https://cschung7.github.io/ai-finance/)**

## 📋 프로젝트 개요

이 프로젝트는 경제학도들이 네트워크 이론과 실제 구현을 학습할 수 있도록 설계된 통합 웹 플랫폼입니다.

### 🎯 주요 기능

1. **📚 네트워크 기초 개념 인포그래픽**
   - 네트워크 효과와 메트칼프 법칙
   - 네트워크 구조 (중앙 집중형 vs. 분산형)
   - 네트워크 경제학과 AI 시대

2. **🔬 NetworkX 시각화 연습장**
   - Python NetworkX 라이브러리를 활용한 실습
   - 기본 그래프 생성 및 시각화
   - 중심성 측정과 노드 색상 매핑
   - 가중치 기반 엣지 표현

### 🛠️ 사용 기술

- **Frontend**: HTML5, Tailwind CSS, Anime.js
- **Backend**: Python, FastAPI, NetworkX, Matplotlib
- **Visualization**: NetworkX, Matplotlib, Korean font support
- **Deployment**: GitHub Pages

### 📁 프로젝트 구조

```
ai-finance/
├── index.html                 # 메인 랜딩 페이지
├── networkx_playground.html   # NetworkX 실습 페이지
├── gemini_doc.html           # 네트워크 개념 문서
├── main.py                   # FastAPI 서버 (로컬 개발용)
├── static/                   # 정적 파일들
├── templates/               # 서버 템플릿들
└── utils/                   # 유틸리티 스크립트들
```

### 🚀 로컬 실행 방법

1. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **FastAPI 서버 실행**
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. **브라우저에서 접속**
   ```
   http://localhost:8000
   ```

### 🌟 GitHub Pages 배포

이 프로젝트는 GitHub Pages를 통해 자동으로 배포됩니다:

1. `main` 브랜치에 푸시
2. GitHub Actions에서 자동 빌드 및 배포
3. `https://cschung7.github.io/ai-finance/`에서 접속 가능

### 📊 NetworkX 예제

프로젝트에 포함된 주요 NetworkX 시각화 예제들:

- **Karate Club 그래프**: 사회 네트워크 분석
- **중심성 측정**: Betweenness, Closeness, Eigenvector 중심성
- **가중치 그래프**: 엣지 가중치 시각화
- **커뮤니티 탐지**: 네트워크 클러스터링

### 🎨 디자인 특징

- **다크 모드 기본**: 현대적이고 눈에 편한 디자인
- **반응형 웹**: 모바일과 데스크톱 모두 지원
- **애니메이션**: Anime.js를 활용한 부드러운 전환
- **한국어 폰트**: Noto Sans KR로 최적화된 한글 표시

### 🔧 개발 환경

- Python 3.8+
- Node.js (선택사항, 개발 도구용)
- 최신 브라우저 (Chrome, Firefox, Safari, Edge)

### 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

### 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Made with ❤️ for Economics Students** 