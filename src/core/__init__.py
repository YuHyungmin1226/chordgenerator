"""
코드 진행 생성기 핵심 모듈

이 패키지는 코드 진행 생성, 멜로디 생성, 음악 이론 분석 등의
핵심 기능을 제공합니다.
"""

from .chord_generator import (
    roman_to_chord,
    generate_progression,
    progression_to_part,
    generate_melody_part,
    analyze_harmony,
    print_analysis
)

__all__ = [
    'roman_to_chord',
    'generate_progression', 
    'progression_to_part',
    'generate_melody_part',
    'analyze_harmony',
    'print_analysis'
] 