"""
Streamlit 기반 웹 애플리케이션

이 모듈은 코드 진행 생성기의 Streamlit 기반 웹 인터페이스를 제공합니다.
"""

import streamlit as st
import random
from music21 import stream, metadata
from datetime import datetime
from typing import Optional, Dict, Any
import sys
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 오류 처리를 강화한 import
try:
    from src.core import (
        roman_to_chord,
        generate_progression,
        progression_to_part,
        generate_melody_part,
        analyze_harmony,
        print_analysis
    )
    from src.utils import create_musicxml_download
except ImportError as e:
    st.error(f"모듈을 가져올 수 없습니다: {e}")
    st.info("필요한 패키지를 설치해주세요: pip install -r requirements.txt")
    st.stop()

# 페이지 설정
st.set_page_config(
    page_title="🎵 코드 진행 생성기",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링 (다크모드 호환)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: var(--primary-color, #1f77b4);
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: var(--text-color, inherit);
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: var(--secondary-background-color, rgba(31, 119, 180, 0.1));
        color: var(--text-color, inherit);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary-color, #1f77b4);
        margin: 1rem 0;
    }
    .success-box {
        background-color: rgba(40, 167, 69, 0.1);
        color: var(--text-color, inherit);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        background-color: rgba(220, 53, 69, 0.1);
        color: var(--text-color, inherit);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    /* 브라우저 다크모드 감지 */
    @media (prefers-color-scheme: dark) {
        .info-box {
            background-color: rgba(31, 119, 180, 0.2) !important;
            color: #ffffff !important;
        }
        .success-box {
            background-color: rgba(40, 167, 69, 0.2) !important;
            color: #ffffff !important;
        }
        .error-box {
            background-color: rgba(220, 53, 69, 0.2) !important;
            color: #ffffff !important;
        }
        .sub-header {
            color: #ffffff !important;
        }
        .main-header {
            color: #58a6ff !important;
        }
    }
    
    /* 다크모드 대응 (Streamlit 테마) */
    [data-theme="dark"] .info-box,
    .stApp[data-theme="dark"] .info-box {
        background-color: rgba(31, 119, 180, 0.2) !important;
        color: #ffffff !important;
    }
    [data-theme="dark"] .success-box,
    .stApp[data-theme="dark"] .success-box {
        background-color: rgba(40, 167, 69, 0.2) !important;
        color: #ffffff !important;
    }
    [data-theme="dark"] .error-box,
    .stApp[data-theme="dark"] .error-box {
        background-color: rgba(220, 53, 69, 0.2) !important;
        color: #ffffff !important;
    }
    [data-theme="dark"] .sub-header,
    .stApp[data-theme="dark"] .sub-header {
        color: #ffffff !important;
    }
    [data-theme="dark"] .main-header,
    .stApp[data-theme="dark"] .main-header {
        color: #58a6ff !important;
    }
    
    /* 라이트모드 대응 */
    [data-theme="light"] .info-box,
    .stApp[data-theme="light"] .info-box {
        background-color: #d1ecf1 !important;
        color: #0c5460 !important;
    }
    [data-theme="light"] .success-box,
    .stApp[data-theme="light"] .success-box {
        background-color: #d4edda !important;
        color: #155724 !important;
    }
    [data-theme="light"] .error-box,
    .stApp[data-theme="light"] .error-box {
        background-color: #f8d7da !important;
        color: #721c24 !important;
    }
    [data-theme="light"] .sub-header,
    .stApp[data-theme="light"] .sub-header {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """메인 애플리케이션 함수"""
    # 세션 유지를 위한 Heartbeat (10분마다 자동 새로고침)
    # key는 고유해야 하며, limit은 최대 새로고침 횟수 (None은 무제한)
    st_autorefresh(interval=10 * 60 * 1000, key="heartbeat")

    # 헤더
    st.markdown('<h1 class="main-header">🎵 코드 진행 생성기</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI 기반 코드 진행 자동 생성 웹 애플리케이션</p>', unsafe_allow_html=True)
    
    # 사이드바 설정
    with st.sidebar:
        st.header("🎼 설정")
        
        # 기본 설정
        tonic = st.selectbox(
            "키 (Key)",
            ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"],
            index=0
        )
        
        mode = st.selectbox(
            "조성 (Mode)",
            ["major", "minor"],
            index=0
        )
        
        time_sig = st.selectbox(
            "박자 (Time Signature)",
            ["4/4", "3/4", "6/8"],
            index=0
        )
        
        length = st.slider(
            "마디 수 (Measures)",
            min_value=2,
            max_value=64,
            value=8,
            step=1
        )
        
        structure = st.selectbox(
            "구조 (Structure)",
            ["A", "AABA", "AB"],
            index=0,
            help="A: 단일 반복, AABA: 팝송 구조, AB: 2부 형식"
        )
        
        # 멜로디 설정
        st.header("🎶 멜로디 설정")
        add_melody = st.checkbox("멜로디 추가", value=True)
        
        if add_melody:
            rhythm_option = st.selectbox(
                "리듬 패턴",
                ["random", "whole", "half", "quarter", "eighth"],
                index=0,
                help="random: 랜덤, whole: 온음표, half: 2분음표, quarter: 4분음표, eighth: 8분음표"
            )
            
            use_slurs = st.checkbox("이음줄 사용", value=False)
            use_ties = st.checkbox("붙임줄 사용", value=False)
            only_melody = st.checkbox("멜로디만 출력", value=False)
        else:
            rhythm_option = "random"
            use_slurs = True
            use_ties = True
            only_melody = False
    
    # 메인 컨텐츠
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎼 코드 진행 생성")
        
        if st.button("🎵 코드 진행 생성하기", type="primary"):
            with st.spinner("코드 진행을 생성하고 있습니다..."):
                try:
                    # 코드 진행 생성
                    def get_section(length):
                        return generate_progression(tonic, mode, length)
                    
                    if structure == 'A':
                        prog = get_section(length)
                    elif structure == 'AABA':
                        a_len = length // 4
                        b_len = length - a_len * 3
                        prog = get_section(a_len) * 2 + get_section(b_len) + get_section(a_len)
                    else:  # AB
                        a_len = length // 2
                        b_len = length - a_len
                        prog = get_section(a_len) + get_section(b_len)
                    
                    # 스코어 생성
                    score = stream.Score()
                    score.metadata = metadata.Metadata()
                    score.metadata.title = f"{tonic.upper()} {mode.capitalize()} 코드 진행"
                    
                    # 멜로디 추가
                    if add_melody:
                        melody_part = generate_melody_part(
                            prog, tonic, mode, time_sig,
                            rhythm_option, use_slurs, use_ties
                        )
                        score.append(melody_part)
                        if not only_melody:
                            chord_part = progression_to_part(prog, tonic, mode, time_sig)
                            score.append(chord_part)
                    else:
                        chord_part = progression_to_part(prog, tonic, mode, time_sig)
                        score.append(chord_part)
                    
                    # 화성 분석
                    analysis = analyze_harmony(prog, tonic, mode)
                    
                    # 결과 표시
                    st.success("✅ 코드 진행이 성공적으로 생성되었습니다!")
                    
                    # 코드 진행 표시
                    st.subheader("📝 생성된 코드 진행")
                    progression_text = " | ".join(prog)
                    st.code(progression_text, language="text")
                    
                    # 4마디씩 그룹화
                    st.subheader("📊 4마디 그룹화")
                    for i in range(0, len(prog), 4):
                        group = prog[i:i+4]
                        group_text = " | ".join(group)
                        st.text(f"마디 {i+1}-{min(i+4, len(prog))}: {group_text}")
                    
                    # 화성 분석 결과
                    st.subheader("🎼 화성학적 분석")
                    with st.expander("분석 결과 보기"):
                        st.write(f"**조성**: {analysis['key']}")
                        
                        if analysis['cadences']:
                            st.write("**종지 분석**:")
                            for cadence in analysis['cadences']:
                                st.write(f"- {cadence}")
                        
                        if analysis['harmonic_progressions']:
                            st.write("**화성 진행 분석**:")
                            for prog_analysis in analysis['harmonic_progressions']:
                                st.write(f"- {prog_analysis}")
                    
                    # MusicXML 다운로드
                    st.subheader("💾 다운로드")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{tonic}_{mode}_progression_{timestamp}.musicxml"
                    
                    download_link = create_musicxml_download(score, filename)
                    st.markdown(download_link, unsafe_allow_html=True)
                    

                    
                except Exception as e:
                    st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                    st.exception(e)
    
    with col2:
        st.header("ℹ️ 정보")
        
        st.markdown("""
        <div class="info-box">
        <h4>🎵 사용 방법</h4>
        <ol>
        <li>왼쪽 사이드바에서 설정을 조정하세요</li>
        <li>"코드 진행 생성하기" 버튼을 클릭하세요</li>
        <li>생성된 코드 진행을 확인하세요</li>
        <li>MusicXML 파일을 다운로드하세요</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h4>🎼 지원 형식</h4>
        <ul>
        <li><strong>조성</strong>: C, C#, D, Eb, E, F, F#, G, Ab, A, Bb, B</li>
        <li><strong>박자</strong>: 4/4, 3/4, 6/8</li>
        <li><strong>구조</strong>: A, AABA, AB</li>
        <li><strong>출력</strong>: MusicXML (MuseScore, Finale 호환)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="success-box">
        <h4>✨ 주요 기능</h4>
        <ul>
        <li>AI 기반 코드 진행 생성</li>
        <li>멜로디 자동 생성</li>
        <li>화성학적 분석</li>
        <li>MusicXML 내보내기</li>
        <li>다크모드 지원</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main() 