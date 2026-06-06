# NoteSense - AI Notes Summarizer

NoteSense is an intelligent, modern web application that leverages Natural Language Processing (NLP) to generate concise summaries and extract key themes from extensive text or documents. Designed for students, professionals, and anyone who needs to quickly digest large volumes of information, NoteSense supports direct text input, as well as `.txt` and `.pdf` file uploads.

## ✨ Features

- **Instant Summarization**: Powered by Hugging Face's `t5-small` model for fast and coherent text summarization.
- **Keyword Extraction**: Identifies the most important themes and terms in your text using TF-IDF.
- **File Upload Support**: Seamlessly process plain text (`.txt`) and PDF (`.pdf`) documents.
- **Sleek, Responsive UI**: A clean, modern interface that works beautifully across all devices.
- **Privacy-First**: Files are processed locally and immediately deleted from the server to ensure maximum privacy.

## 🚀 Getting Started

Follow these instructions to set up NoteSense on your local machine for development and testing.

### Prerequisites

- **Python 3.8+** installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abhranilsingharoy-cloud/NoteSense.git
   cd NoteSense
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

*(Note: The first time you run the application or summarize a text, the `t5-small` model will be downloaded automatically by the transformers library.)*

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI / NLP**: Hugging Face Transformers (`t5-small`), Scikit-learn (TF-IDF)
- **File Processing**: PyPDF2
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check the [issues page](https://github.com/abhranilsingharoy-cloud/NoteSense/issues) if you want to contribute.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
