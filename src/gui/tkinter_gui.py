"""
tkinter 기반 GUI 모듈

이 모듈은 코드 진행 생성기의 tkinter 기반 데스크톱 GUI를 제공합니다.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import queue
import os
import gc
import psutil
from datetime import datetime
from typing import Optional, Dict, Any

from music21 import stream, metadata

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core import (
    generate_progression,
    progression_to_part,
    generate_melody_part
)
from src.utils import get_documents_dir


class MusicGeneratorGUI:
    """코드 진행 생성기 tkinter GUI 클래스"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("코드 진행 생성기")
        self.root.geometry("900x800")  # 창 크기 최적화
        self.root.resizable(True, True)
        
        # 전체 창 크기 조절 설정
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.work_queue = queue.Queue()
        self.is_running = False
        self.current_process: Optional[threading.Thread] = None
        self.setup_gui()
        
    def setup_gui(self):
        """GUI 구성 요소를 설정합니다."""
        # 스타일 설정
        style = ttk.Style()
        style.configure('TLabel', padding=5)
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        style.configure('TCombobox', padding=5)
        style.configure('TLabelframe', padding=10)
        style.configure('TFrame', padding=10)

        # 메인 프레임
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)

        # 메인 프레임 그리드 설정
        main_frame.grid_columnconfigure(0, weight=1)
        for i in range(5):  # 5개의 주요 섹션
            main_frame.grid_rowconfigure(i, weight=1)

        # 입력 섹션 프레임 (전체 높이의 40%)
        input_frame = ttk.LabelFrame(main_frame, text="기본 설정")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.grid_columnconfigure(1, weight=3)  # 입력 필드 칸을 더 넓게
        input_frame.grid_columnconfigure(2, weight=1)  # 설명 칸은 좁게

        # 입력 필드
        row = 0
        field_width = 35  # 입력 필드 기본 너비

        # 키 입력
        ttk.Label(input_frame, text="키:").grid(row=row, column=0, sticky=tk.W, padx=(10, 5))
        self.tonic_var = tk.StringVar(value="C")
        ttk.Entry(input_frame, textvariable=self.tonic_var, width=field_width).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(input_frame, text="(예: C, D, F# 등)").grid(row=row, column=2, sticky=tk.W, padx=5)

        # 조성 선택
        row += 1
        ttk.Label(input_frame, text="조성:").grid(row=row, column=0, sticky=tk.W, padx=(10, 5))
        self.mode_var = tk.StringVar(value="major")
        mode_combo = ttk.Combobox(input_frame, textvariable=self.mode_var, values=["major", "minor"], width=field_width-3)
        mode_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        mode_combo.state(['readonly'])

        # 박자 선택
        row += 1
        ttk.Label(input_frame, text="박자:").grid(row=row, column=0, sticky=tk.W, padx=(10, 5))
        self.time_sig_var = tk.StringVar(value="4/4")
        time_sig_combo = ttk.Combobox(input_frame, textvariable=self.time_sig_var, values=["4/4", "3/4", "6/8"], width=field_width-3)
        time_sig_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        time_sig_combo.state(['readonly'])

        # 마디 수 입력
        row += 1
        ttk.Label(input_frame, text="마디 수:").grid(row=row, column=0, sticky=tk.W, padx=(10, 5))
        self.length_var = tk.StringVar(value="8")
        ttk.Entry(input_frame, textvariable=self.length_var, width=field_width).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)

        # 구조 선택
        row += 1
        ttk.Label(input_frame, text="구조:").grid(row=row, column=0, sticky=tk.W, padx=(10, 5))
        self.structure_var = tk.StringVar(value="A")
        structure_combo = ttk.Combobox(input_frame, textvariable=self.structure_var, values=["A", "AABA", "AB"], width=field_width-3)
        structure_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        structure_combo.state(['readonly'])

        # 리듬 패턴 선택
        row += 1
        ttk.Label(input_frame, text="리듬 패턴:").grid(row=row, column=0, sticky=tk.W, padx=(10, 5))
        self.rhythm_var = tk.StringVar(value="random")
        rhythm_combo = ttk.Combobox(input_frame, textvariable=self.rhythm_var, 
                                    values=["random", "whole", "half", "quarter", "eighth"], width=field_width-3)
        rhythm_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        rhythm_combo.state(['readonly'])

        # 옵션 섹션 프레임 (전체 높이의 20%)
        option_frame = ttk.LabelFrame(main_frame, text="추가 옵션")
        option_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        option_frame.grid_columnconfigure(0, weight=1)
        option_frame.grid_columnconfigure(1, weight=1)

        # 옵션 체크박스를 2x2 그리드로 배치
        self.add_melody_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(option_frame, text="멜로디 추가", variable=self.add_melody_var).grid(row=0, column=0, sticky=tk.W, padx=20, pady=5)

        self.use_slurs_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(option_frame, text="이음줄 사용", variable=self.use_slurs_var).grid(row=0, column=1, sticky=tk.W, padx=20, pady=5)
        
        self.use_ties_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(option_frame, text="붙임줄 사용", variable=self.use_ties_var).grid(row=1, column=0, sticky=tk.W, padx=20, pady=5)

        self.only_melody_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(option_frame, text="멜로디만 출력", variable=self.only_melody_var).grid(row=1, column=1, sticky=tk.W, padx=20, pady=5)

        # 저장 위치 선택 프레임 (전체 높이의 15%)
        save_frame = ttk.LabelFrame(main_frame, text="저장 위치")
        save_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        save_frame.grid_columnconfigure(0, weight=4)
        save_frame.grid_columnconfigure(1, weight=1)

        self.save_path_var = tk.StringVar(value=os.path.join(get_documents_dir(), "Score"))
        ttk.Entry(save_frame, textvariable=self.save_path_var).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        ttk.Button(save_frame, text="찾아보기", command=self.browse_save_path).grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)

        # 상태 표시 프레임 (전체 높이의 15%)
        status_frame = ttk.LabelFrame(main_frame, text="상태")
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        status_frame.grid_columnconfigure(0, weight=1)

        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(10, 5))

        status_info_frame = ttk.Frame(status_frame)
        status_info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        status_info_frame.grid_columnconfigure(0, weight=1)
        status_info_frame.grid_columnconfigure(1, weight=1)

        self.status_label = ttk.Label(status_info_frame, text="준비")
        self.status_label.grid(row=0, column=0, sticky=tk.W)

        self.memory_label = ttk.Label(status_info_frame, text="메모리 사용량: 0%")
        self.memory_label.grid(row=0, column=1, sticky=tk.E)

        # 버튼 프레임 (전체 높이의 10%)
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="생성 시작", command=self.start_generation, width=20).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="취소", command=self.cancel_generation, width=20).grid(row=0, column=1, padx=5)

        # 메모리 모니터링 시작
        self.start_memory_monitoring()
        
    def browse_save_path(self):
        """저장 위치 선택 다이얼로그"""
        path = filedialog.askdirectory(initialdir=self.save_path_var.get())
        if path:
            self.save_path_var.set(path)
            
    def get_unique_filename(self, base_name: str, ext: str) -> str:
        """저장 경로를 고려한 고유 파일명 생성"""
        save_dir = self.save_path_var.get()
        os.makedirs(save_dir, exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        n = 1
        while True:
            filename = f"{base_name}_{today}_{n}.{ext}"
            full_path = os.path.join(save_dir, filename)
            if not os.path.exists(full_path):
                return full_path
            n += 1
        
    def start_memory_monitoring(self):
        """메모리 사용량 모니터링 시작"""
        def update_memory():
            if self.is_running:
                process = psutil.Process()
                memory_percent = process.memory_percent()
                self.memory_label.config(text=f"메모리 사용량: {memory_percent:.1f}%")
                
                if memory_percent > 90:
                    self.show_warning("메모리 사용량이 높습니다. 작업을 일시 중지합니다.")
                    self.cancel_generation()
            
            self.root.after(1000, update_memory)
        
        self.root.after(1000, update_memory)
        
    def validate_input(self) -> bool:
        """입력값 검증"""
        try:
            tonic = self.tonic_var.get().strip().capitalize()
            if not tonic:
                raise ValueError("키를 입력해주세요.")
                
            mode = self.mode_var.get().strip().lower()
            if mode not in ['major', 'minor']:
                raise ValueError("조성은 major 또는 minor여야 합니다.")
                
            time_sig = self.time_sig_var.get().strip()
            if time_sig not in ['4/4', '3/4', '6/8']:
                raise ValueError("박자는 4/4, 3/4, 6/8 중 하나여야 합니다.")
                
            length = int(self.length_var.get().strip())
            if length < 1:
                raise ValueError("마디 수는 1 이상이어야 합니다.")
                
            structure = self.structure_var.get().strip().upper()
            if structure not in ['A', 'AABA', 'AB']:
                raise ValueError("구조는 A, AABA, AB 중 하나여야 합니다.")
                
            rhythm = self.rhythm_var.get().strip().lower()
            if rhythm not in ['random', 'whole', 'half', 'quarter', 'eighth']:
                raise ValueError("리듬 패턴이 올바르지 않습니다.")
                
            return True
        except ValueError as e:
            self.show_error(str(e))
            return False
            
    def start_generation(self):
        """음악 생성 시작"""
        if self.is_running:
            return
            
        if not self.validate_input():
            return
            
        self.is_running = True
        self.progress.start()
        self.status_label.config(text="생성 중...")
        
        # 작업 파라미터 설정
        params = {
            'tonic': self.tonic_var.get().strip().capitalize(),
            'mode': self.mode_var.get().strip().lower(),
            'time_sig': self.time_sig_var.get().strip(),
            'length': int(self.length_var.get().strip()),
            'structure': self.structure_var.get().strip().upper(),
            'rhythm_option': self.rhythm_var.get().strip().lower(),
            'add_melody': self.add_melody_var.get(),
            'use_slurs': self.use_slurs_var.get(),
            'use_ties': self.use_ties_var.get(),
            'only_melody': self.only_melody_var.get()
        }
        
        # 별도 스레드에서 음악 생성
        self.current_process = threading.Thread(target=self.generate_music, args=(params,))
        self.current_process.daemon = True
        self.current_process.start()
        
    def generate_music(self, params: Dict[str, Any]):
        """음악 생성 작업"""
        try:
            # 코드 진행 생성
            def get_section(length):
                return generate_progression(params['tonic'], params['mode'], length)
                
            if params['structure'] == 'A':
                prog = get_section(params['length'])
            elif params['structure'] == 'AABA':
                a_len = params['length'] // 4
                b_len = params['length'] - a_len * 3
                prog = get_section(a_len) * 2 + get_section(b_len) + get_section(a_len)
            else:  # AB
                a_len = params['length'] // 2
                b_len = params['length'] - a_len
                prog = get_section(a_len) + get_section(b_len)
                
            # 스코어 생성
            score = stream.Score()
            score.metadata = metadata.Metadata()
            score.metadata.title = f"{params['tonic'].upper()} {params['mode'].capitalize()} 코드 진행"
            
            # 멜로디 추가
            if params['add_melody']:
                melody_part = generate_melody_part(
                    prog, params['tonic'], params['mode'], params['time_sig'],
                    params['rhythm_option'], params['use_slurs'], params['use_ties']
                )
                score.append(melody_part)
                if not params['only_melody']:
                    chord_part = progression_to_part(prog, params['tonic'], params['mode'], params['time_sig'])
                    score.append(chord_part)
            else:
                chord_part = progression_to_part(prog, params['tonic'], params['mode'], params['time_sig'])
                score.append(chord_part)
                
            # 파일 저장
            base_name = f"{params['tonic']}_{params['mode']}_progression"
            save_dir = self.save_path_var.get()
            filename = self.get_unique_filename(base_name, "musicxml")
            score.write('musicxml', fp=filename)
            
            self.root.after(0, lambda: self.show_success(f"MusicXML 파일이 저장되었습니다: {filename}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"오류 발생: {str(e)}"))
        finally:
            self.root.after(0, self.cleanup)
            
    def cancel_generation(self):
        """생성 작업 취소"""
        if self.is_running:
            self.is_running = False
            if self.current_process and self.current_process.is_alive():
                self.current_process.join(timeout=1.0)
            self.cleanup()
            
    def cleanup(self):
        """정리 작업"""
        self.is_running = False
        self.progress.stop()
        self.status_label.config(text="준비")
        gc.collect()
        
    def show_error(self, message: str):
        """오류 메시지 표시"""
        messagebox.showerror("오류", message)
        
    def show_warning(self, message: str):
        """경고 메시지 표시"""
        messagebox.showwarning("경고", message)
        
    def show_success(self, message: str):
        """성공 메시지 표시"""
        messagebox.showinfo("완료", message)
        
    def run(self):
        """GUI 실행"""
        self.root.mainloop()


def main():
    """메인 함수"""
    app = MusicGeneratorGUI()
    app.run()


if __name__ == "__main__":
    main() 