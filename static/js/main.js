document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const summarizeBtn = document.getElementById('summarize-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadForm = document.getElementById('upload-form');
    const textInput = document.getElementById('text-input');
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name-display');
    
    // Status & Result Elements
    const loader = document.getElementById('loader');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const resultsContent = document.getElementById('results-content');
    const emptyState = document.getElementById('empty-state');
    const summaryText = document.getElementById('summary-text');
    
    // New Elements
    const sentimentBadge = document.getElementById('sentiment-badge');
    const personList = document.getElementById('person-list');
    const orgList = document.getElementById('org-list');
    const locList = document.getElementById('loc-list');
    const exportBtn = document.getElementById('export-btn');
    const qaBtn = document.getElementById('qa-btn');
    const qaInput = document.getElementById('qa-input');
    const qaAnswer = document.getElementById('qa-answer');
    
    let currentOriginalText = "";
    let currentSummary = "";
    let currentEntities = {};
    let currentSentiment = "";
    // --- 3D Initialization ---
    if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(document.querySelectorAll(".bento-box"), {
            max: 5,
            speed: 400,
            glare: true,
            "max-glare": 0.05,
        });
    }

    if (typeof THREE !== 'undefined') {
        initThreeJS();
    }

    function initThreeJS() {
        const canvas = document.getElementById('three-bg');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 2000;
        const posArray = new Float32Array(particlesCount * 3);
        
        for(let i = 0; i < particlesCount * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 15;
        }
        
        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        
        const material = new THREE.PointsMaterial({
            size: 0.02,
            color: 0x00f0ff,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending
        });
        
        const particlesMesh = new THREE.Points(particlesGeometry, material);
        scene.add(particlesMesh);
        
        camera.position.z = 3;
        
        let mouseX = 0;
        let mouseY = 0;
        let targetX = 0;
        let targetY = 0;
        const windowHalfX = window.innerWidth / 2;
        const windowHalfY = window.innerHeight / 2;
        
        document.addEventListener('mousemove', (event) => {
            mouseX = (event.clientX - windowHalfX);
            mouseY = (event.clientY - windowHalfY);
        });
        
        const clock = new THREE.Clock();
        
        function animate() {
            requestAnimationFrame(animate);
            const elapsedTime = clock.getElapsedTime();
            
            targetX = mouseX * 0.001;
            targetY = mouseY * 0.001;
            
            particlesMesh.rotation.y += 0.05 * (targetX - particlesMesh.rotation.y);
            particlesMesh.rotation.x += 0.05 * (targetY - particlesMesh.rotation.x);
            particlesMesh.rotation.z += 0.001; // slow continuous rotation
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }
    // --- End 3D Initialization ---

    // File input change listener for UI updates
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileNameDisplay.textContent = e.target.files[0].name;
            fileNameDisplay.style.color = 'var(--accent-color)';
        } else {
            fileNameDisplay.textContent = 'Choose a file or drag it here';
            fileNameDisplay.style.color = '';
        }
    });

    function setProcessingState(isProcessing) {
        if (isProcessing) {
            loader.style.display = 'flex';
            emptyState.style.display = 'none';
            resultsContent.style.display = 'none';
            errorMessage.style.display = 'none';
        } else {
            loader.style.display = 'none';
        }
        summarizeBtn.disabled = isProcessing;
        uploadBtn.disabled = isProcessing;
    }

    function showResults(summary, entities, sentiment, originalText) {
        currentSummary = summary;
        currentEntities = entities;
        currentSentiment = sentiment;
        currentOriginalText = originalText;
        
        summaryText.textContent = summary;
        
        sentimentBadge.textContent = 'TONE: ' + sentiment.toUpperCase();
        if(sentiment === 'Positive') {
            sentimentBadge.style.background = 'var(--neon-cyan)';
            sentimentBadge.style.color = '#000';
        } else if(sentiment === 'Negative') {
            sentimentBadge.style.background = 'var(--neon-magenta)';
            sentimentBadge.style.color = '#fff';
        } else {
            sentimentBadge.style.background = '#737373';
            sentimentBadge.style.color = '#fff';
        }
        
        function populateList(listElem, items) {
            listElem.innerHTML = '';
            if (items && items.length > 0) {
                items.forEach(kw => {
                    const li = document.createElement('li');
                    li.textContent = kw;
                    listElem.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = 'None detected';
                li.style.opacity = '0.5';
                listElem.appendChild(li);
            }
        }
        
        populateList(personList, entities.Person);
        populateList(orgList, entities.Organization);
        populateList(locList, entities.Location);

        resultsContent.style.display = 'block';
        emptyState.style.display = 'none';
        
        qaInput.value = '';
        qaAnswer.style.display = 'none';
        qaAnswer.textContent = '';
    }

    function showError(msg) {
        errorText.textContent = msg;
        errorMessage.style.display = 'flex';
        emptyState.style.display = 'block';
        resultsContent.style.display = 'none';
    }

    // Handle Text Summarization
    summarizeBtn.addEventListener('click', async () => {
        const text = textInput.value;
        if (!text.trim()) {
            showError('Please paste some text to summarize.');
            return;
        }

        setProcessingState(true);
        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();
            if (response.ok) {
                showResults(data.summary, data.entities, data.sentiment, data.original_text);
            } else {
                showError(data.error || 'An error occurred during summarization.');
            }
        } catch (error) {
            showError('Failed to connect to the AI engine.');
            console.error(error);
        } finally {
            setProcessingState(false);
        }
    });

    // Handle File Upload Summarization
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (fileInput.files.length === 0) {
            showError('Please select a .txt or .pdf file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        setProcessingState(true);
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (response.ok) {
                showResults(data.summary, data.entities, data.sentiment, data.original_text);
            } else {
                showError(data.error || 'An error occurred while processing the file.');
            }
        } catch (error) {
            showError('Failed to connect to the AI engine.');
            console.error(error);
        } finally {
            setProcessingState(false);
            uploadForm.reset();
            fileNameDisplay.textContent = 'Choose a file or drag it here';
            fileNameDisplay.style.color = '';
        }
    });

    // Handle Q&A
    qaBtn.addEventListener('click', async () => {
        const question = qaInput.value;
        if (!question.trim() || !currentOriginalText) return;
        
        qaBtn.textContent = 'QUERYING...';
        qaBtn.disabled = true;
        
        try {
            const response = await fetch('/qa', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: currentOriginalText, question: question })
            });
            const data = await response.json();
            if(response.ok) {
                qaAnswer.textContent = '>> ' + data.answer;
                qaAnswer.style.display = 'block';
            } else {
                qaAnswer.textContent = '>> ERROR: ' + data.error;
                qaAnswer.style.display = 'block';
            }
        } catch(e) {
            console.error(e);
        } finally {
            qaBtn.textContent = 'QUERY';
            qaBtn.disabled = false;
        }
    });
    
    // Handle Export
    exportBtn.addEventListener('click', async () => {
        if(!currentSummary) return;
        
        exportBtn.innerHTML = '<i class="ph ph-spinner"></i> EXPORTING...';
        exportBtn.disabled = true;
        
        try {
            const response = await fetch('/export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    summary: currentSummary,
                    entities: currentEntities,
                    sentiment: currentSentiment
                })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'NoteSense_Log.pdf';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            }
        } catch(e) {
            console.error(e);
        } finally {
            exportBtn.innerHTML = '<i class="ph ph-download-simple"></i> EXPORT LOG';
            exportBtn.disabled = false;
        }
    });
});
