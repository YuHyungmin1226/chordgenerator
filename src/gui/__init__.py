"""
GUI 모듈

이 패키지는 tkinter 기반 GUI와 Streamlit 웹 인터페이스를 제공합니다.
"""

from .tkinter_gui import MusicGeneratorGUI
from .streamlit_app import main as streamlit_main

__all__ = [
    'MusicGeneratorGUI',
    'streamlit_main'
] 