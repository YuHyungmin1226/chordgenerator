document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generator-form');
    const lengthInput = document.getElementById('length');
    const lengthVal = document.getElementById('length-val');
    const addMelodyCheckbox = document.getElementById('add_melody');
    const melodyOptions = document.getElementById('melody-options');
    
    const welcomeView = document.getElementById('welcome-view');
    const resultView = document.getElementById('result-view');
    const loadingView = document.getElementById('loading-view');
    
    const progressionDisplay = document.getElementById('progression-display');
    const progressionGroups = document.getElementById('progression-groups');
    const analysisKey = document.getElementById('analysis-key');
    const analysisCadences = document.getElementById('analysis-cadences');
    const analysisProgressions = document.getElementById('analysis-progressions');
    const downloadContainer = document.getElementById('download-container');

    // Update length display
    lengthInput.addEventListener('input', (e) => {
        lengthVal.textContent = e.target.value;
    });

    // Toggle melody options
    addMelodyCheckbox.addEventListener('change', (e) => {
        melodyOptions.style.display = e.target.checked ? 'block' : 'none';
        melodyOptions.style.opacity = e.target.checked ? '1' : '0.5';
    });

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading
        welcomeView.style.display = 'none';
        resultView.style.display = 'none';
        loadingView.style.display = 'block';
        
        const formData = new FormData(form);
        const data = {
            tonic: formData.get('tonic'),
            mode: formData.get('mode'),
            time_sig: formData.get('time_sig'),
            length: formData.get('length'),
            structure: formData.get('structure'),
            add_melody: formData.get('add_melody') === 'on',
            rhythm_option: formData.get('rhythm_option'),
            use_slurs: formData.get('use_slurs') === 'on',
            use_ties: formData.get('use_ties') === 'on',
            only_melody: formData.get('only_melody') === 'on'
        };

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                renderResult(result);
            } else {
                alert('오류 발생: ' + result.error);
                loadingView.style.display = 'none';
                welcomeView.style.display = 'block';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('서버와 통신 중 오류가 발생했습니다.');
            loadingView.style.display = 'none';
            welcomeView.style.display = 'block';
        }
    });

    function renderResult(result) {
        // Display text progression
        progressionDisplay.textContent = result.progression_text;

        // Grouping display
        progressionGroups.innerHTML = '';
        const prog = result.progression;
        for (let i = 0; i < prog.length; i += 4) {
            const group = prog.slice(i, i + 4);
            const groupEl = document.createElement('div');
            groupEl.className = 'group-item';
            groupEl.innerHTML = `
                <span class="range">마디 ${i + 1}-${Math.min(i + 4, prog.length)}</span>
                <div class="group-text">${group.join(' | ')}</div>
            `;
            progressionGroups.appendChild(groupEl);
        }

        // Analysis
        const analysis = result.analysis;
        analysisKey.textContent = analysis.key;
        
        analysisCadences.innerHTML = '';
        analysis.cadences.forEach(c => {
            const li = document.createElement('li');
            li.textContent = c;
            analysisCadences.appendChild(li);
        });

        analysisProgressions.innerHTML = '';
        analysis.harmonic_progressions.forEach(p => {
            const li = document.createElement('li');
            li.textContent = p;
            analysisProgressions.appendChild(li);
        });

        // Download link
        downloadContainer.innerHTML = result.download_html;

        // Switch views
        loadingView.style.display = 'none';
        resultView.style.display = 'block';
        
        // Scroll to result on mobile
        if (window.innerWidth <= 900) {
            resultView.scrollIntoView({ behavior: 'smooth' });
        }
    }
});
