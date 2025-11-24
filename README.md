# NoteSense 📝✨

NoteSense is an intelligent note-taking application that leverages AI to automatically organize and summarize your notes, transforming raw text into clear, actionable insights.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)


## Features

- **AI-Powered Summarization**: Get concise summaries of your long-form notes with a single click.
- **Smart Topic Extraction**: Automatically detects and suggests relevant topics/keywords for your notes.
- **Interactive Web Interface**: Built with Streamlit for a clean and user-friendly experience.
- **Effortless Organization**: Categorize and find your notes faster using AI-generated tags.

## How It Works

NoteSense uses advanced Natural Language Processing (NLP) techniques to analyze your text. It identifies key sentences and phrases to generate summaries and extract the most relevant topics, helping you understand the essence of your notes at a glance.

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/abhranilsingharoy-cloud/NoteSense.git
    cd NoteSense
    ```

2.  **Install the required dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Navigate to the project directory.
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3.  Open your web browser to the local URL provided (usually `http://localhost:8501`).
4.  Paste or type your note into the text area.
5.  Click the button to generate an AI-powered summary and topic tags instantly!

## Project Structure
```

NoteSense/
├──app.py                 # Main Streamlit application
├──utils.py               # Helper functions for NLP processing
├──requirements.txt       # Python dependencies
└──README.md             # Project documentation (this file)

```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for any improvements.
