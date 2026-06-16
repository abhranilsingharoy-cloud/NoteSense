<div align="center">
  
# 🌌 NoteSense 

**An Advanced AI-Powered NLP Document Analyzer & Summarization Matrix**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)](https://flask.palletsprojects.com/)
[![Three.js](https://img.shields.io/badge/Three.js-3D%20Rendering-white?logo=three.js)](https://threejs.org/)

</div>

---

## 📖 Overview

**NoteSense** is an intelligent, modern, and highly advanced web application designed to leverage Natural Language Processing (NLP) for instantaneous document digestion. It effortlessly processes large volumes of raw text, `.txt`, and `.pdf` files to generate concise summaries, answer specific questions, and extract critical intelligence.

Built for students, researchers, and professionals, NoteSense combines a powerful Hugging Face backend with an immersive, **3D CyberBento** frontend interface.

---

## ✨ Core Features

*   **Immersive 3D UI:** A sleek, dark-mode glassmorphism interface featuring a reactive Three.js particle matrix background and Vanilla-tilt 3D hover cards.
*   **Advanced Text Chunking:** Intelligently bypasses standard token limits by chunking massive documents, summarizing individual segments via `t5-small`, and seamlessly stitching them back together.
*   **Smart Entity Categorization (NER):** Utilizes `spaCy` to contextually identify and categorize data into **Persons**, **Organizations**, and **Locations**.
*   **Document Query Matrix (Q&A):** Ask direct questions about your uploaded document! Powered by a distilled transformer (`distilbert-squad`), the AI scans your text to provide accurate answers on demand.
*   **VADER Sentiment Analysis:** Lightning-fast tone detection that instantly calculates whether the uploaded data leans Positive, Negative, or Neutral.
*   **Matrix Log Export:** Generate and download a perfectly formatted PDF report containing your generated summary, sentiment analysis, and vital entities in one click.
*   **Privacy-First:** All files are processed locally and wiped instantly from the server upon completion to guarantee maximum confidentiality.

---

## 📂 Project Structure

```text
NoteSense/
├── app.py                      # Main Flask application and API routing
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── Dockerfile                  # Container deployment instructions
├── render.yaml                 # Infrastructure as Code for Render.com
│
├── ai_engine/                  # NLP Core Services
│   ├── __init__.py
│   └── analyzer.py             # Summarization, NER, Q&A, Sentiment logic
│
├── static/                     # Static assets (CSS, JS)
│   ├── css/
│   │   └── style.css           # 3D styling, animations, and CyberBento grid
│   └── js/
│       └── main.js             # API integrations, Three.js logic, UI state
│
├── templates/                  # HTML templates
│   └── index.html              # Main frontend UI structure
│
└── uploads/                    # Temporary storage for document processing
```

---

## 🚀 Getting Started

Follow these instructions to set up and run NoteSense on your local machine.

### Prerequisites

*   **Python 3.8** or higher installed.
*   **Git** installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/abhranilsingharoy-cloud/NoteSense.git
cd NoteSense
```

### 2. Environment Setup

It is highly recommended to use a virtual environment to manage dependencies securely.

```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Download AI Datasets

NoteSense requires specific language models for NER and Sentiment Analysis. Download them using the following commands:

```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 5. Launch the Server

Start the Flask application:

```bash
python app.py
```

Open your web browser and navigate to: **http://127.0.0.1:5000/**

> **Note:** The first time you summarize text or ask a question, the Hugging Face transformer models (`t5-small`, `distilbert-squad`) will be automatically downloaded to your machine.

---

## 🛠️ Technology Stack

| Domain | Technologies |
| :--- | :--- |
| **Backend Framework** | Python, Flask |
| **NLP & AI Engine** | Hugging Face Transformers (`t5-small`, `distilbert-squad`) |
| **Entity & Sentiment**| `spaCy` (`en_core_web_sm`), NLTK (VADER) |
| **Data Processing** | `PyPDF2` (Parsing), `fpdf2` (PDF Generation) |
| **Frontend UI** | HTML5, Vanilla CSS3 (Variables, Grid), Vanilla JavaScript |
| **Frontend 3D Visuals**| Three.js, Vanilla-tilt.js |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
If you have suggestions for improving NoteSense, feel free to check the [issues page](https://github.com/abhranilsingharoy-cloud/NoteSense/issues).

---

## 📝 License

This project is open-source and distributed under the terms of the [MIT License](LICENSE). 

---
<div align="center">
  <i>Developed with passion by <b>Abhranil Singha Roy</b></i>
</div>
