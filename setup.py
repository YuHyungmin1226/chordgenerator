"""
코드 진행 생성기 설치 스크립트

이 파일은 코드 진행 생성기를 Python 패키지로 설치할 수 있도록 합니다.
"""

from setuptools import setup, find_packages
from pathlib import Path

# README 파일 읽기
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# requirements.txt 읽기
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="chord-progression-generator",
    version="1.0.0",
    author="YuHyungmin1226",
    author_email="",
    description="AI 기반 코드 진행 자동 생성 도구",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YuHyungmin1226/chordgenerator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "chord-generator=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="music, chord, progression, generation, ai, music21, streamlit",
    project_urls={
        "Bug Reports": "https://github.com/YuHyungmin1226/chordgenerator/issues",
        "Source": "https://github.com/YuHyungmin1226/chordgenerator",
        "Documentation": "https://github.com/YuHyungmin1226/chordgenerator#readme",
    },
) 