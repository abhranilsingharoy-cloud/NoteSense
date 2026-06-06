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
    const keywordsList = document.getElementById('keywords-list');

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

    function showResults(summary, keywords) {
        summaryText.textContent = summary;
        
        keywordsList.innerHTML = '';
        if (keywords && keywords.length > 0) {
            keywords.forEach(kw => {
                const li = document.createElement('li');
                li.textContent = kw;
                keywordsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No keywords extracted';
            li.style.opacity = '0.5';
            keywordsList.appendChild(li);
        }

        resultsContent.style.display = 'block';
        emptyState.style.display = 'none';
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
                showResults(data.summary, data.keywords);
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
                showResults(data.summary, data.keywords);
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
});
