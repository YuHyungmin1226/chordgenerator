# 🎵 코드 진행 생성기 (Chord Progression Generator)

AI 기반 코드 진행 자동 생성 로컬 웹 애플리케이션입니다. Flask와 Music21을 사용하여 음악 이론에 기반한 코드 진행과 멜로디를 생성합니다. 프리미엄 글래스모피즘 UI와 다크 모드를 지원합니다.

## ✨ 주요 기능

### 🎼 코드 진행 생성
- **장조/단조 지원**: 다양한 조성의 코드 진행 생성
- **다양한 패턴**: 클래식, 팝, 록, 발라드 등 다양한 스타일
- **구조화**: A, AABA, AB 구조 지원
- **종지 처리**: 자연스러운 종지 패턴 적용

### 🎶 멜로디 생성
- **코드 기반 멜로디**: 생성된 코드에 맞는 멜로디 라인
- **리듬 패턴**: 다양한 리듬 옵션 (전체, 반, 4분, 8분음표)
- **표현 기법**: 이음줄, 붙임줄 지원
- **옥타브 제한**: 적절한 음역대 유지

### 📊 프리미엄 사용자 인터페이스
- **현대적인 UI**: 글래스모피즘(Glassmorphism) 기반의 유려한 디자인
- **다크 모드**: 시력을 보호하는 고급스러운 다크 테마
- **반응형 레이아웃**: 데스크톱과 모바일 모두 최적화
- **실시간 생성**: 클릭 한 번으로 즉시 결과 확인 및 분석
- **MusicXML 내보내기**: 표준 악보 형식 다운로드

### 🛠️ 추가 도구
- **tkinter GUI**: 데스크톱 애플리케이션 인터페이스
- **MusicXML 편집기**: MusicXML 파일 편집 및 변환 도구

## 🚀 설치 및 실행

### 필수 요구사항
- Python 3.8 이상
- pip (Python 패키지 관리자)

### 설치 방법

1. **저장소 클론**
```bash
git clone https://github.com/YuHyungmin1226/chordgenerator.git
cd chordgenerator
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **애플리케이션 실행**

#### 방법 1: 배치 파일 사용 (Windows 사용자용, 가장 권장)
- 폴더 내의 `run.bat` 파일을 더블 클릭하면 메뉴를 통해 원하는 모드를 선택하여 실행할 수 있습니다.

#### 방법 2: 통합 실행 파일 사용
```bash
# 로컬 웹 앱 실행 (Flask)
python main.py --web

# tkinter GUI 실행
python main.py --gui

# MusicXML 편집기 실행
python main.py --musicxml-editor

# 도움말 보기
python main.py --help
```

#### 방법 2: 직접 실행
```bash
# Flask 웹 앱
python src/web/app.py

# tkinter GUI
python src/gui/tkinter_gui.py

# MusicXML 편집기
python src/gui/musicxml_editor.py
```

4. **브라우저에서 접속** (웹 앱 실행 시)
```
http://localhost:5000
```

## 🎹 사용 방법

### 기본 설정
1. **키 (Key)**: C, C#, D, Eb, E, F, F#, G, Ab, A, Bb, B 중 선택
2. **조성**: 장조 (major) 또는 단조 (minor)
3. **박자**: 4/4, 3/4, 6/8 중 선택
4. **마디 수**: 2~64마디 설정

### 구조 설정
- **A**: 단일 반복 구조
- **AABA**: 팝송에서 많이 사용하는 32마디 구조
- **AB**: 2부 형식 (클래식 소나타 등)

### 멜로디 설정
- **멜로디 추가**: 코드 진행에 맞는 멜로디 생성
- **이음줄 사용**: 프레이즈 단위 이음줄 추가
- **붙임줄 사용**: 마디 넘어가는 같은 음 연결
- **멜로디만 출력**: 코드 반주 없이 멜로디 라인만 출력

## 🎼 생성되는 코드 진행 패턴

### 장조 패턴
- **기본 클래식**: I-IV-V-I, I-vi-IV-V
- **캐논 진행**: I-V-vi-IV, vi-IV-I-V
- **팝/록 스타일**: I-V-IV-V, vi-V-IV-V
- **발라드 스타일**: I-iii-IV-vi, I-vi-iii-IV

### 단조 패턴
- **기본 단조**: i-iv-V-i, i-VI-iv-V
- **자연 단조**: i-VII-VI-V, i-III-VI-iv
- **드라마틱**: i-V-VI-iv, i-VII-IV-V
- **감정적**: i-VI-ii°-V, i-III-iv-V

## 📁 파일 구조

```
chordgenerator/
├── main.py                       # 메인 실행 파일
├── setup.py                      # 패키지 설치 스크립트
├── requirements.txt              # Python 의존성
├── README.md                     # 프로젝트 문서
├── LICENSE                       # MIT 라이선스
├── src/                          # 소스 코드
│   ├── core/                     # 핵심 기능 모듈
│   │   ├── __init__.py
│   │   └── chord_generator.py    # 코드 진행 생성 핵심 로직
│   ├── web/                      # Flask 웹 인터페이스 [NEW]
│   │   ├── app.py                # Flask 서버
│   │   ├── templates/            # HTML 템플릿
│   │   └── static/               # CSS, JS 정적 파일
│   ├── gui/                      # 데스크톱 인터페이스
│   │   ├── __init__.py
│   │   ├── tkinter_gui.py        # tkinter 데스크톱 GUI
│   │   └── musicxml_editor.py    # MusicXML 편집 도구
│   └── utils/                    # 유틸리티 모듈
│       ├── __init__.py
│       └── file_utils.py         # 파일 처리 유틸리티
```

## 🛠️ 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **음악 이론**: Music21
- **UI/UX**: Glassmorphism, Dark Mode
- **버전 관리**: Git & GitHub

## 🎵 출력 형식

### 화면 출력
- 코드 진행 로마숫자 표기
- 4마디씩 그룹화된 표시
- 화성학적 분석 결과 (조성, 종지 등)

### 파일 출력
- **MusicXML**: 표준 악보 형식
- **호환 프로그램**: MuseScore, Finale, Sibelius, Dorico
- **파일명**: `{Key}_{Mode}_progression_{Timestamp}.musicxml`

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👨‍💻 개발자

**YuHyungmin1226** - [GitHub](https://github.com/YuHyungmin1226)

## 🙏 감사의 말

- [Music21](https://web.mit.edu/music21/) - 음악 이론 및 분석 라이브러리
- [Flask](https://flask.palletsprojects.com/) - 웹 애플리케이션 프레임워크
- 음악 이론 커뮤니티 - 코드 진행 패턴 제공

---

⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요!