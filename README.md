# NoteSense - Advanced AI Notes Summarizer (CyberBento Edition)

NoteSense is an intelligent, modern, and highly advanced web application that leverages Natural Language Processing (NLP) to generate concise summaries, answer questions, and extract key themes from extensive text or documents.

Designed for students, professionals, and power users who need to quickly digest large volumes of information, NoteSense supports direct text input as well as `.txt` and `.pdf` file uploads.

## ✨ Advanced Features

- **3D CyberBento Interface**: Built with a sleek, dark-mode glassmorphism interface featuring a Three.js interactive matrix background and 3D Vanilla-tilt hover cards.
- **Advanced Text Chunking Engine**: NoteSense intelligently chunks massive documents, summarizes the pieces with `t5-small`, and seamlessly stitches them back together.
- **Smart Entity Categorization (NER)**: Uses `spaCy` to intelligently identify and categorize **Persons**, **Organizations**, and **Locations** within your text.
- **VADER Sentiment Analysis**: Lightning-fast tone detection that displays the overall sentiment of the uploaded data.
- **Document Query Matrix (Q&A)**: Uses a distilled transformer model (`distilbert-squad`) to let you ask direct questions about the uploaded text.
- **Matrix Log Export**: Instantly generate and download a perfectly formatted PDF containing your summary and extracted entities.
- **Privacy-First Architecture**: Files are processed locally and instantly wiped from the server to ensure maximum confidentiality.

## 🚀 Getting Started

Follow these instructions to run the advanced NoteSense application on your local machine.

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

4. **Download the AI Datasets (spaCy and NLTK):**
   ```bash
   python -m spacy download en_core_web_sm
   python -c "import nltk; nltk.download('vader_lexicon')"
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

*(Note: The first time you run the application or summarize a text, the Hugging Face models will be downloaded automatically.)*

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI / NLP Engine**: Hugging Face Transformers (`t5-small`, `distilbert-squad`), spaCy (`en_core_web_sm`), NLTK (VADER)
- **Document Processing & Export**: PyPDF2, fpdf2
- **Frontend Architecture**: HTML5, Vanilla CSS, Vanilla JavaScript, Three.js, Vanilla-tilt.js

## 👨‍💻 Developer
Developed with passion by **Abhranil Singha Roy**.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check the [issues page](https://github.com/abhranilsingharoy-cloud/NoteSense/issues) if you want to contribute.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
