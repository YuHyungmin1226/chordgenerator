import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from music21 import stream, metadata

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core import (
    generate_progression,
    progression_to_part,
    generate_melody_part,
    analyze_harmony
)
from src.utils import create_musicxml_download

app = Flask(__name__)

@app.route('/')
def index():
    """메인 페이지 렌더링"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    """코드 진행 생성 API"""
    try:
        data = request.json
        tonic = data.get('tonic', 'C')
        mode = data.get('mode', 'major')
        time_sig = data.get('time_sig', '4/4')
        length = int(data.get('length', 8))
        structure = data.get('structure', 'A')
        add_melody = data.get('add_melody', True)
        rhythm_option = data.get('rhythm_option', 'random')
        use_slurs = data.get('use_slurs', False)
        use_ties = data.get('use_ties', False)
        only_melody = data.get('only_melody', False)

        # 코드 진행 생성
        def get_section(l):
            return generate_progression(tonic, mode, l)
        
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
        score.metadata.title = f"{tonic.upper()} {mode.capitalize()} Progression"
        
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
        
        # MusicXML 다운로드 링크 (HTML 태그 형태)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{tonic}_{mode}_progression_{timestamp}.musicxml"
        download_html = create_musicxml_download(score, filename)

        return jsonify({
            'success': True,
            'progression': prog,
            'progression_text': " | ".join(prog),
            'analysis': analysis,
            'download_html': download_html
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 로컬에서만 실행
    app.run(host='127.0.0.1', port=5000, debug=True)
