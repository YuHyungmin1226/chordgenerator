"""
파일 처리 유틸리티 모듈

이 모듈은 파일 경로 관리, 파일 생성, 다운로드 등의
파일 관련 유틸리티 기능을 제공합니다.
"""

import os
import sys
from datetime import datetime
from typing import Optional
import io
import base64
from music21 import stream


def get_documents_dir() -> str:
    """
    사용자의 문서 폴더 경로를 가져옵니다.
    
    Returns:
        str: 문서 폴더 경로
    """
    try:
        if sys.platform == "win32":
            # Windows
            return os.path.join(os.environ['USERPROFILE'], 'Documents')
        elif sys.platform == "darwin":
            # macOS
            return os.path.join(os.path.expanduser("~"), "Documents")
        else:
            # Linux 및 기타
            return os.path.join(os.path.expanduser("~"), "Documents")
    except Exception as e:
        print(f"[ERROR] 문서 폴더 경로 가져오기 실패: {e}")
        # 기본 경로 반환
        return os.path.join(os.path.expanduser("~"), "Documents")


def get_unique_filename(base_name: str, ext: str, save_dir: str) -> str:
    """
    고유한 파일명을 생성합니다.
    
    Args:
        base_name: 기본 파일명
        ext: 파일 확장자
        save_dir: 저장 디렉토리
    
    Returns:
        str: 고유한 파일 경로
    """
    today = datetime.now().strftime("%Y%m%d")
    n = 1
    # Score 폴더 생성
    score_dir = os.path.join(save_dir, "Score")
    os.makedirs(score_dir, exist_ok=True)
    
    while True:
        filename = f"{base_name}_{today}_{n}.{ext}"
        full_path = os.path.join(score_dir, filename)
        if not os.path.exists(full_path):
            return full_path
        n += 1


def create_musicxml_download(score: stream.Score, filename: str) -> str:
    """
    MusicXML 파일을 다운로드 가능한 형태로 변환합니다.
    
    Args:
        score: music21 Score 객체
        filename: 파일명
    
    Returns:
        str: base64로 인코딩된 다운로드 링크
    """
    try:
        # 임시 파일을 사용하여 MusicXML 생성
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.musicxml', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # MusicXML 파일로 저장
            score.write('musicxml', fp=temp_path)
            
            # 파일 읽기
            with open(temp_path, 'rb') as f:
                file_data = f.read()
            
            # base64 인코딩
            b64 = base64.b64encode(file_data).decode('utf-8')
            
            # 다운로드 링크 생성
            href = f'<a href="data:application/vnd.recordare.musicxml+xml;base64,{b64}" download="{filename}">📁 {filename} 다운로드</a>'
            
            return href
            
        finally:
            # 임시 파일 삭제
            try:
                os.unlink(temp_path)
            except:
                pass
                
    except Exception as e:
        print(f"MusicXML 다운로드 생성 실패: {e}")
        return f"<p>다운로드 생성 실패: {e}</p>" 