#!/usr/bin/env python3
"""
코드 진행 생성기 메인 실행 파일

이 파일은 코드 진행 생성기의 다양한 인터페이스를 실행할 수 있는
통합 진입점을 제공합니다.
"""

import sys
import argparse
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="🎵 코드 진행 생성기 - AI 기반 코드 진행 자동 생성 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python main.py --gui                    # tkinter GUI 실행
  python main.py --streamlit              # Streamlit 웹 앱 실행
  python main.py --musicxml-editor        # MusicXML 편집기 실행
  python main.py --help                   # 도움말 표시
        """
    )
    
    parser.add_argument(
        '--gui', 
        action='store_true',
        help='tkinter 기반 데스크톱 GUI 실행'
    )
    
    parser.add_argument(
        '--streamlit', 
        action='store_true',
        help='Streamlit 기반 웹 애플리케이션 실행'
    )
    
    parser.add_argument(
        '--musicxml-editor', 
        action='store_true',
        help='MusicXML 편집기 실행'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='코드 진행 생성기 v1.0.0'
    )
    
    args = parser.parse_args()
    
    # 옵션이 지정되지 않은 경우 기본값으로 GUI 실행
    if not any([args.gui, args.streamlit, args.musicxml_editor]):
        args.gui = True
    
    try:
        if args.gui:
            print("🎵 tkinter GUI를 시작합니다...")
            from src.gui.tkinter_gui import main as gui_main
            gui_main()
            
        elif args.streamlit:
            print("🌐 Streamlit 웹 앱을 시작합니다...")
            print("브라우저에서 http://localhost:8501 을 열어주세요.")
            import subprocess
            import os
            
            # Streamlit 앱 실행
            streamlit_app_path = project_root / "src" / "gui" / "streamlit_app.py"
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", 
                str(streamlit_app_path),
                "--server.port", "8501",
                "--server.address", "localhost"
            ])
            
        elif args.musicxml_editor:
            print("📝 MusicXML 편집기를 시작합니다...")
            from src.gui.musicxml_editor import main as editor_main
            editor_main()
            
    except ImportError as e:
        print(f"❌ 모듈을 가져올 수 없습니다: {e}")
        print("필요한 패키지를 설치해주세요:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 