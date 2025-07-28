"""
코드 진행 생성 핵심 모듈

이 모듈은 코드 진행 생성, 멜로디 생성, 화성 분석 등의
핵심 기능을 제공합니다.
"""

import random
from music21 import stream, chord, key, metadata, note, meter, roman, scale, expressions, spanner, tie
from typing import List, Dict, Any, Optional
from music21 import pitch


def roman_to_chord(roman: str, tonic: str, mode: str = 'major') -> chord.Chord:
    """
    로마숫자 코드를 실제 화음으로 변환합니다.
    
    Args:
        roman: 로마숫자 코드 (예: 'I', 'IV', 'V7')
        tonic: 조성 (예: 'C', 'F#')
        mode: 조성 타입 ('major' 또는 'minor')
    
    Returns:
        music21.chord.Chord: 변환된 화음
    """
    k = key.Key(tonic, mode)
    rn_obj = k.romanNumeral(roman)
    if roman.upper() == 'V':
        rn_obj.figure += '7'
    base_pitches = list(rn_obj.pitches)
    
    # 전위(1전위, 2전위) 랜덤 적용
    inversion = random.choice([0, 1, 2]) if len(base_pitches) > 2 else 0
    pitches = base_pitches[inversion:] + base_pitches[:inversion]
    
    # 옥타브 분산 (C3~C5)
    chord_notes = []
    base_octave = 3
    for i, p in enumerate(pitches):
        np = p.transpose(12 * (base_octave + i // len(pitches) - p.octave))
        # 옥타브 범위 제한
        while np.octave < 3:
            np = np.transpose(12)
        while np.octave > 5:
            np = np.transpose(-12)
        chord_notes.append(np)
    
    rn = chord.Chord(chord_notes)
    return rn


def generate_progression(tonic: str = 'C', mode: str = 'major', length: int = 8) -> List[str]:
    """
    코드 진행을 생성합니다.
    
    Args:
        tonic: 조성 (예: 'C', 'F#')
        mode: 조성 타입 ('major' 또는 'minor')
        length: 마디 수
    
    Returns:
        List[str]: 로마숫자 코드 진행 리스트
    """
    # 대한민국 교과서 스타일: I, IV, V, vi만 사용, 반복적이고 예측 가능한 패턴
    if mode == 'major':
        basic_patterns = [
            ['I', 'IV', 'V', 'I'],
            ['I', 'vi', 'IV', 'V'],
            ['I', 'IV', 'I', 'V'],
            ['I', 'IV', 'V', 'I'],
        ]
        cadences = [
            ['IV', 'ii', 'V7', 'I'],
            ['vi', 'ii', 'V7', 'I'],
            ['ii', 'V7', 'I'],
            ['IV', 'V', 'I'],
            ['IV', 'I'],
            ['V', 'vi'],  # Deceptive
        ]
    else:
        basic_patterns = [
            ['i', 'iv', 'V', 'i'],
            ['i', 'VI', 'iv', 'V'],
            ['i', 'iv', 'i', 'V'],
            ['i', 'iv', 'V', 'i'],
        ]
        cadences = [
            ['iv', 'ii°', 'V7', 'i'],
            ['VI', 'ii°', 'V7', 'i'],
            ['ii°', 'V7', 'i'],
            ['iv', 'V', 'i'],
            ['iv', 'i'],
            ['V', 'VI'],  # Deceptive
        ]
    
    # 4마디 단위 반복
    base = random.choice(basic_patterns)
    progression = (base * ((length // 4) + 1))[:length]
    
    # 종지 처리: 마지막 3~4마디를 종지 패턴으로 대체
    if length >= 3:
        cadence = random.choice(cadences)
        c_len = min(len(cadence), length)
        progression[-c_len:] = cadence[-c_len:]
    
    return progression


def progression_to_part(prog: List[str], tonic: str, mode: str = 'major', 
                       time_sig: str = '4/4', analysis: Optional[Dict] = None) -> stream.Part:
    """
    코드 진행을 악보 파트로 변환합니다.
    
    Args:
        prog: 로마숫자 코드 진행 리스트
        tonic: 조성
        mode: 조성 타입
        time_sig: 박자
        analysis: 화성 분석 결과 (선택사항)
    
    Returns:
        music21.stream.Part: 코드 파트
    """
    p = stream.Part()
    p.append(key.Key(tonic, mode))
    p.append(meter.TimeSignature(time_sig))
    from music21 import clef
    p.append(clef.BassClef())  # 낮은음자리표 추가
    
    for i, rn in enumerate(prog):
        m = stream.Measure(number=i+1)  # 마디 번호 명시적으로 지정
        c = roman_to_chord(rn, tonic, mode)
        c.quarterLength = 4 if time_sig == '4/4' else 3 if time_sig == '3/4' else 3
        m.append(c)
        if i == len(prog) - 1:
            m.rightBarline = 'final'
        p.append(m)
    
    p.id = 'Chords'
    return p


def get_rhythm_pattern(style: str = 'basic') -> List[List[float]]:
    """
    리듬 패턴 템플릿을 반환합니다.
    
    Args:
        style: 리듬 스타일 ('basic', 'syncopated', 'swing', 'complex')
    
    Returns:
        List[List[float]]: 리듬 패턴 리스트
    """
    patterns = {
        'basic': [
            [4.0],  # 온음표
            [2.0, 2.0],  # 2분음표 2개
            [1.0, 1.0, 1.0, 1.0],  # 4분음표 4개
        ],
        'syncopated': [
            [1.5, 0.5, 1.5, 0.5],  # 당김음
            [0.75, 0.25, 0.75, 0.25, 1.0, 1.0],  # 당김음 변형
            [1.0, 0.5, 0.5, 1.0, 1.0],  # 셋잇단음표 느낌
        ],
        'swing': [
            [0.66, 0.34, 0.66, 0.34, 1.0, 1.0],  # 스윙
            [1.66, 0.34, 1.0, 1.0],  # 스윙 변형
        ],
        'complex': [
            [0.25, 0.25, 0.5, 0.5, 0.5, 1.0, 1.0],  # 16분음표 혼합
            [0.5, 0.25, 0.25, 1.0, 1.0, 1.0],  # 부점 리듬
            [1.0, 0.5, 0.25, 0.25, 1.0, 1.0],  # 혼합 리듬
        ]
    }
    return patterns.get(style, patterns['basic'])


def apply_rhythm_pattern(notes: List[note.Note], pattern: List[float]) -> List[note.Note]:
    """
    음표들에 리듬 패턴을 적용합니다.
    
    Args:
        notes: 음표 리스트
        pattern: 리듬 패턴
    
    Returns:
        List[note.Note]: 리듬이 적용된 음표 리스트
    """
    if not notes:
        return []
    
    total_duration = sum(pattern)
    if total_duration != 4.0:  # 4/4 박자 기준
        # 패턴 길이 조정
        scale_factor = 4.0 / total_duration
        pattern = [d * scale_factor for d in pattern]
    
    result = []
    pattern_idx = 0
    note_idx = 0
    
    while note_idx < len(notes):
        if pattern_idx >= len(pattern):
            pattern_idx = 0
        
        notes[note_idx].quarterLength = pattern[pattern_idx]
        result.append(notes[note_idx])
        
        note_idx += 1
        pattern_idx += 1
    
    return result


def generate_melody_part(prog: List[str], tonic: str, mode: str = 'major', 
                        time_sig: str = '4/4', rhythm_option: str = 'random', 
                        use_slurs: bool = True, use_ties: bool = True) -> stream.Part:
    """
    코드 진행에 맞는 멜로디 파트를 생성합니다.
    
    Args:
        prog: 로마숫자 코드 진행 리스트
        tonic: 조성
        mode: 조성 타입
        time_sig: 박자
        rhythm_option: 리듬 옵션
        use_slurs: 이음줄 사용 여부
        use_ties: 붙임줄 사용 여부
    
    Returns:
        music21.stream.Part: 멜로디 파트
    """
    melody = stream.Part()
    melody.append(meter.TimeSignature(time_sig))
    k = key.Key(tonic, mode)
    melody.append(k)
    s = scale.MajorScale(tonic) if mode == 'major' else scale.MinorScale(tonic)
    scale_degrees = s.getPitches()
    tonic_pitch = pitch.Pitch(tonic)
    prev_note = None
    all_notes = []  # 모든 음 저장(이음줄/붙임줄용)
    
    # 박자별 리듬 패턴 설정
    if time_sig == '4/4':
        measure_length = 4.0
        rhythm_patterns = {
            'random': [
                [4.0], [2.0, 2.0], [1.0, 1.0, 1.0, 1.0], [2.0, 1.0, 1.0],
                [1.0, 2.0, 1.0], [0.5]*8, [1.0, 0.5, 0.5, 2.0],
                [0.5, 0.5, 1.0, 2.0], [2.0, 0.5, 0.5, 1.0], [1.0, 1.0, 0.5, 0.5, 1.0],
            ],
            'whole': [[4.0]], 'half': [[2.0, 2.0]], 
            'quarter': [[1.0, 1.0, 1.0, 1.0]], 'eighth': [[0.5]*8]
        }
    elif time_sig == '3/4':
        measure_length = 3.0
        rhythm_patterns = {
            'random': [
                [3.0], [1.5, 1.5], [1.0, 2.0], [2.0, 1.0], [1.0, 1.0, 1.0],
                [0.5, 0.5, 2.0], [2.0, 0.5, 0.5], [0.5, 1.0, 1.5],
                [0.5, 0.5, 1.0, 1.0], [0.5]*6
            ],
            'whole': [[3.0]], 'half': [[1.5, 1.5]], 
            'quarter': [[1.0, 1.0, 1.0]], 'eighth': [[0.5]*6]
        }
    elif time_sig == '6/8':
        measure_length = 3.0
        rhythm_patterns = {
            'random': [
                [3.0], [1.5, 1.5], [1.0, 2.0], [2.0, 1.0], [1.0, 1.0, 1.0],
                [0.5, 0.5, 2.0], [2.0, 0.5, 0.5], [0.5, 1.0, 1.5],
                [0.5, 0.5, 1.0, 1.0], [0.5]*6
            ],
            'whole': [[3.0]], 'half': [[1.5, 1.5]], 
            'quarter': [[1.0, 1.0, 1.0]], 'eighth': [[0.5]*6]
        }
    else:
        measure_length = 4.0
        rhythm_patterns = {
            'random': [[4.0]], 'whole': [[4.0]], 'half': [[2.0, 2.0]], 
            'quarter': [[1.0, 1.0, 1.0, 1.0]], 'eighth': [[0.5]*8]
        }
    
    for i, rn in enumerate(prog):
        c = roman_to_chord(rn, tonic, mode)
        m = stream.Measure(number=i+1)  # 마디 번호 명시적으로 지정
        pattern = random.choice(rhythm_patterns[rhythm_option]) if rhythm_option in rhythm_patterns else random.choice(rhythm_patterns['random'])
        notes = []
        
        for j, dur in enumerate(pattern):
            is_cadence_zone = (i >= len(prog) - 3)
            if j == 0:
                if is_cadence_zone:
                    n = note.Note(tonic_pitch)
                else:
                    choices = [c.root(), c.third, c.fifth, tonic_pitch]
                    n = note.Note(random.choice(choices))
            elif i == len(prog) - 1 and j == len(pattern) - 1:
                n = note.Note(tonic_pitch)
            elif is_cadence_zone:
                choices = [c.third, c.fifth, tonic_pitch]
                n = note.Note(random.choice(choices))
            else:
                if prev_note:
                    candidates = [p for p in scale_degrees if abs(p.midi - prev_note.pitch.midi) <= 2]
                    n = note.Note(random.choice(candidates)) if candidates else note.Note(random.choice(scale_degrees))
                else:
                    n = note.Note(random.choice(scale_degrees))
            
            n.quarterLength = dur
            if n.pitch.octave is None:
                n.pitch.octave = 4
            while n.pitch.octave < 4:
                n.pitch.octave += 1
            while n.pitch.octave > 6:
                n.pitch.octave -= 1
            notes.append(n)
            prev_note = n
        
        for n in notes:
            m.append(n)
            all_notes.append(n)
        
        total_len = sum([n.quarterLength for n in m.notes])
        if abs(total_len - measure_length) > 0.01:
            print(f"⚠️ 경고: {i+1}번째 마디의 음표 길이 합({total_len})이 박자({measure_length})와 일치하지 않습니다.")
        
        if i == len(prog) - 1:
            m.rightBarline = 'final'
        melody.append(m)
    
    # 프레이즈 단위(4마디) 이음줄 추가
    if use_slurs:
        for i in range(0, len(all_notes), 4):
            if i+3 < len(all_notes):
                slur = spanner.Slur()
                for n in all_notes[i:i+4]:
                    slur.addSpannedElements(n)
                melody.insert(0, slur)

    # 붙임줄(마디 넘어가는 같은 음)
    if use_ties:
        for i in range(len(all_notes)-1):
            n1 = all_notes[i]
            n2 = all_notes[i+1]
            if n1.nameWithOctave == n2.nameWithOctave:
                if n1.tie is None:
                    n1.tie = tie.Tie('start')
                else:
                    n1.tie = tie.Tie('continue')
                n2.tie = tie.Tie('stop')
    
    melody.id = 'Melody'
    return melody


def analyze_harmony(prog: List[str], tonic: str, mode: str = 'major') -> Dict[str, Any]:
    """
    화성학적 분석을 수행합니다.
    
    Args:
        prog: 로마숫자 코드 진행 리스트
        tonic: 조성
        mode: 조성 타입
    
    Returns:
        Dict[str, Any]: 분석 결과
    """
    k = key.Key(tonic, mode)
    s = scale.MajorScale(tonic) if mode == 'major' else scale.MinorScale(tonic)
    
    analysis = {
        'key': f"{tonic} {mode}",
        'cadences': [],
        'harmonic_progressions': [],
        'scale_usage': {},
        'tensions': [],
        'voice_leading': [],
        'cadence_measures': [],
        'circle_measures': []
    }
    
    # 종지 분석 및 마디 위치 기록
    if len(prog) >= 2:
        last_two = prog[-2:]
        if mode == 'major':
            if last_two == ['V', 'I']:
                analysis['cadences'].append('Authentic Cadence')
                analysis['cadence_measures'].append({'measure': len(prog)-2, 'text': 'Authentic Cadence (V-I) 종지'})
            elif last_two == ['IV', 'I']:
                analysis['cadences'].append('Plagal Cadence')
                analysis['cadence_measures'].append({'measure': len(prog)-2, 'text': 'Plagal Cadence (IV-I) 종지'})
        else:
            if last_two == ['V', 'i']:
                analysis['cadences'].append('Authentic Cadence')
                analysis['cadence_measures'].append({'measure': len(prog)-2, 'text': 'Authentic Cadence (V-i) 종지'})
            elif last_two == ['iv', 'i']:
                analysis['cadences'].append('Plagal Cadence')
                analysis['cadence_measures'].append({'measure': len(prog)-2, 'text': 'Plagal Cadence (iv-i) 종지'})
    
    # 화성 진행 분석 및 5도권 마디 위치 기록
    for i in range(len(prog) - 1):
        current = prog[i]
        next_chord = prog[i + 1]
        if mode == 'major':
            circle_prog = ['I', 'IV', 'vii°', 'iii', 'vi', 'ii', 'V', 'I']
            if current in circle_prog and next_chord in circle_prog:
                if circle_prog.index(next_chord) == (circle_prog.index(current) + 1) % len(circle_prog):
                    analysis['harmonic_progressions'].append(f"Circle of Fifths: {current} -> {next_chord}")
                    analysis['circle_measures'].append({'measure': i, 'text': f'5도권 진행: {current}->{next_chord}'})
        else:
            circle_prog = ['i', 'iv', 'VII', 'III', 'VI', 'ii°', 'V', 'i']
            if current in circle_prog and next_chord in circle_prog:
                if circle_prog.index(next_chord) == (circle_prog.index(current) + 1) % len(circle_prog):
                    analysis['harmonic_progressions'].append(f"Circle of Fifths: {current} -> {next_chord}")
                    analysis['circle_measures'].append({'measure': i, 'text': f'5도권 진행: {current}->{next_chord}'})
    
    # 음계 사용 분석
    scale_degrees = s.getPitches()
    for chord in prog:
        rn = roman.RomanNumeral(chord, k)
        for p in rn.pitches:
            if p in scale_degrees:
                degree = scale_degrees.index(p) + 1
                analysis['scale_usage'][f"Degree {degree}"] = analysis['scale_usage'].get(f"Degree {degree}", 0) + 1
    
    # 텐션 분석
    for chord in prog:
        if '7' in chord or '9' in chord or 'sus' in chord:
            analysis['tensions'].append(f"{chord} contains tension")
    
    # 음성진행 분석
    for i in range(len(prog) - 1):
        current = roman.RomanNumeral(prog[i], k)
        next_chord = roman.RomanNumeral(prog[i + 1], k)
        
        # 공통음 유지
        common_tones = set(current.pitches) & set(next_chord.pitches)
        if common_tones:
            analysis['voice_leading'].append(f"Common tone between {prog[i]} and {prog[i+1]}")
        
        # 반음 진행
        for p1 in current.pitches:
            for p2 in next_chord.pitches:
                if abs(p1.midi - p2.midi) == 1:
                    analysis['voice_leading'].append(f"Half-step motion between {prog[i]} and {prog[i+1]}")
    
    return analysis


def print_analysis(analysis: Dict[str, Any]) -> None:
    """
    분석 결과를 출력합니다.
    
    Args:
        analysis: 화성 분석 결과
    """
    print("\n=== 화성학적 분석 ===")
    print(f"조성: {analysis['key']}")
    
    print("\n종지 분석:")
    if analysis['cadences']:
        for cadence in analysis['cadences']:
            print(f"- {cadence}")
    else:
        print("- 종지 패턴이 명확하지 않음")
    
    print("\n화성 진행 분석:")
    if analysis['harmonic_progressions']:
        for prog in analysis['harmonic_progressions']:
            print(f"- {prog}")
    else:
        print("- 특별한 화성 진행 패턴이 없음")
    
    print("\n음계 사용 분석:")
    for degree, count in analysis['scale_usage'].items():
        print(f"- {degree}: {count}회 사용")
    
    print("\n텐션 분석:")
    if analysis['tensions']:
        for tension in analysis['tensions']:
            print(f"- {tension}")
    else:
        print("- 텐션이 사용되지 않음")
    
    print("\n음성진행 분석:")
    if analysis['voice_leading']:
        for leading in analysis['voice_leading']:
            print(f"- {leading}")
    else:
        print("- 특별한 음성진행 패턴이 없음") 