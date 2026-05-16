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
  python main.py --web                    # 로컬 웹 앱 실행
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
        '--web', 
        action='store_true',
        help='로컬 웹 애플리케이션 실행 (Flask)'
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
    if not any([args.gui, args.web, args.musicxml_editor]):
        args.gui = True
    
    try:
        if args.gui:
            print("[GUI] Starting tkinter GUI...")
            from src.gui.tkinter_gui import main as gui_main
            gui_main()
            
        elif args.web:
            print("[WEB] Starting local web app...")
            print("Please open http://localhost:5000 in your browser.")
            
            from src.web.app import app
            # 로컬 환경이므로 바로 실행
            app.run(host='127.0.0.1', port=5000, debug=False)
            
        elif args.musicxml_editor:
            print("[EDITOR] Starting MusicXML Editor...")
            from src.gui.musicxml_editor import main as editor_main
            editor_main()
            
    except ImportError as e:
        print(f"[ERROR] Could not import module: {e}")
        print("Please install required packages:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 