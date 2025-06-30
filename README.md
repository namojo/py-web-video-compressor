# 🎬 웹 동영상 압축기

현대적인 웹 인터페이스를 가진 동영상 압축 도구입니다. FFmpeg을 기반으로 하여 고품질의 동영상 압축을 제공합니다.

## ✨ 주요 기능

### 🌟 핵심 기능
- **웹 기반 UI**: 직관적이고 반응형 웹 인터페이스
- **드래그 앤 드롭**: 파일을 끌어다 놓기로 간편 업로드
- **다중 포맷 지원**: MP4, AVI, MOV, MKV, WMV, FLV, WebM 등
- **실시간 진행률**: 압축 진행 상황 실시간 모니터링
- **파일 크기 비교**: 압축 전후 크기 및 감소율 표시

### 🎨 UI/UX 기능
- **다크/라이트 테마**: 원클릭 테마 전환
- **테마 기억**: 브라우저 저장으로 설정 유지
- **부드러운 애니메이션**: 매끄러운 전환 효과
- **반응형 디자인**: 모바일/태블릿/데스크톱 지원

### ⚙️ 압축 설정
- **품질 선택**: 높음/보통/낮음
- **해상도 조정**: 원본/1080p/720p/480p/360p
- **출력 포맷**: MP4/AVI/MOV/WebM/MKV 선택

## 🚀 설치 및 실행

### 사전 요구사항

1. **Python 3.9+**
2. **FFmpeg 설치**

#### FFmpeg 설치 방법

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- [FFmpeg 공식 사이트](https://ffmpeg.org/download.html)에서 다운로드
- PATH 환경변수에 추가

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS/RHEL:**
```bash
sudo yum install ffmpeg
# 또는
sudo dnf install ffmpeg
```

### 설치 과정

1. **저장소 클론 또는 파일 다운로드**
```bash
git clone <repository-url>
cd video-compressor
```

2. **Python 의존성 설치**
```bash
pip install -r requirements.txt
```

3. **서버 실행**
```bash
python3 web_video_compressor.py
```

4. **브라우저에서 접속**
```
http://localhost:5001
```

## 📖 사용법

### 1. 기본 사용법

1. **파일 업로드**
   - "파일 선택" 버튼 클릭 또는
   - 파일을 업로드 영역에 드래그 앤 드롭

2. **압축 설정**
   - 품질: 파일 크기와 화질의 균형 선택
   - 해상도: 필요에 따라 해상도 조정
   - 출력 형식: 원하는 비디오 포맷 선택

3. **압축 실행**
   - "압축 시작" 버튼 클릭
   - 진행률 바에서 상태 확인

4. **결과 확인 및 다운로드**
   - 압축 완료 후 파일 크기 비교 확인
   - "다운로드" 버튼으로 파일 저장

### 2. 고급 사용법

#### 품질 설정 가이드
- **높음 (CRF 18)**: 최고 화질, 큰 파일 크기
- **보통 (CRF 23)**: 권장 설정, 균형잡힌 화질과 크기
- **낮음 (CRF 28)**: 작은 파일 크기, 화질 저하

#### 해상도 선택 가이드
- **원본 유지**: 해상도 변경 없음
- **1080p**: Full HD 품질
- **720p**: HD 품질, 웹 스트리밍 적합
- **480p**: SD 품질, 모바일 최적화
- **360p**: 최소 품질, 최대 압축

#### 출력 포맷 가이드
- **MP4**: 가장 호환성 좋음 (권장)
- **WebM**: 웹 최적화, 작은 파일 크기
- **AVI**: 구형 시스템 호환
- **MOV**: Apple 기기 최적화
- **MKV**: 고급 기능 지원

### 3. 테마 사용법

- **테마 전환**: 우측 상단 원형 버튼 클릭
- **라이트 모드**: 🌙 달 아이콘
- **다크 모드**: ☀️ 태양 아이콘
- **자동 저장**: 브라우저가 테마 설정 기억

## 📁 파일 구조

```
video-compressor/
├── web_video_compressor.py    # Flask 웹 서버
├── templates/
│   └── index.html            # 웹 인터페이스
├── uploads/                  # 업로드된 파일 (자동 생성)
├── outputs/                  # 압축된 파일 (자동 생성)
├── requirements.txt          # Python 의존성
└── README.md                # 사용 설명서
```

## 🔧 설정 및 커스터마이징

### 서버 설정 변경

`web_video_compressor.py`에서 다음 설정을 변경할 수 있습니다:

```python
# 포트 변경
app.run(host='0.0.0.0', port=5001, debug=True)

# 최대 파일 크기 변경 (현재: 2500MB)
app.config['MAX_CONTENT_LENGTH'] = 2500 * 1024 * 1024

# 업로드/출력 폴더 변경
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
```

### 지원 파일 형식 추가

```python
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v', '3gp'}
```

## 🛠️ 문제 해결

### 일반적인 문제

**1. FFmpeg를 찾을 수 없음**
```
해결: FFmpeg 설치 후 PATH 환경변수 확인
macOS: brew install ffmpeg
Windows: FFmpeg 다운로드 후 PATH 추가
Linux: apt install ffmpeg 또는 yum install ffmpeg
```

**2. 포트 5001이 사용 중**
```
해결: web_video_compressor.py에서 포트 번호 변경
app.run(host='0.0.0.0', port=5002, debug=True)
```

**3. 파일 업로드 실패**
```
해결: 파일 크기 확인 (2500MB 제한)
지원 형식 확인 (MP4, AVI, MOV, MKV, WMV, FLV, WebM)
```

**4. 압축 실패**
```
해결: 
- 입력 파일 손상 여부 확인
- 디스크 공간 확인
- FFmpeg 설치 상태 확인
```

### 성능 최적화

**대용량 파일 처리:**
- 충분한 디스크 공간 확보
- 메모리 사용량 모니터링
- 필요시 해상도 낮춰서 처리

**서버 성능:**
- `debug=False`로 프로덕션 모드 사용
- 필요시 멀티프로세싱 구현

## 🔒 보안 고려사항

- 업로드 파일 크기 제한 (2500MB)
- 파일 형식 검증
- 임시 파일 자동 정리
- 안전한 파일명 처리

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 지원

문제가 발생하거나 질문이 있으시면:
- GitHub Issues 생성
- 이메일 문의

## 🎯 향후 계획

- [ ] 배치 압축 (여러 파일 동시 처리)
- [ ] 압축 프리셋 저장/불러오기
- [ ] 클라우드 스토리지 연동
- [ ] 모바일 앱 버전
- [ ] 압축 품질 미리보기

---

**즐거운 동영상 압축 되세요! 🎬✨**
