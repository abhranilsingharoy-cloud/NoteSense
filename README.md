# NoteSense - Advanced AI Notes Summarizer

NoteSense is an intelligent, modern, and highly advanced web application that leverages Natural Language Processing (NLP) to generate concise summaries and extract key themes from extensive text or documents. 

Designed for students, professionals, and power users who need to quickly digest large volumes of information, NoteSense supports direct text input as well as `.txt` and `.pdf` file uploads.


## ✨ Advanced Features

- **Premium UI/UX Design**: Built with a sleek, dark-mode glassmorphism interface. Features smooth animations, dynamic gradient backgrounds, and intuitive interactions.
- **Advanced Text Chunking Engine**: NoteSense isn't limited by standard AI token limits. It intelligently chunks massive documents (like huge PDFs or long transcripts), summarizes the pieces, and seamlessly stitches them back together for comprehensive results.
- **Key Entity Extraction**: Identifies the most critical themes and terms in your text using an advanced TF-IDF algorithm configured for high relevance.
- **Universal Support**: Process raw text, `.txt`, and `.pdf` files efficiently.
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

### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

*(Note: The first time you run the application or summarize a text, the `t5` model will be downloaded automatically by the transformers library.)*

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI / NLP Engine**: Hugging Face Transformers (`t5-small`), Scikit-learn (TF-IDF)
- **Document Processing**: PyPDF2
- **Frontend Architecture**: HTML5, CSS3 Variables, Glassmorphism UI, Vanilla JavaScript

## 👨‍💻 Developer
Developed with passion by **Abhranil Singha Roy**.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check the [issues page](https://github.com/abhranilsingharoy-cloud/NoteSense/issues) if you want to contribute.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
