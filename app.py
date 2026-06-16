import os
import tempfile
from flask import Flask, request, jsonify, render_template, send_file
import PyPDF2
from ai_engine.analyzer import get_summary, get_entities, get_sentiment, answer_question
from fpdf import FPDF

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        summary = get_summary(text)
        entities = get_entities(text)
        sentiment = get_sentiment(text)

        return jsonify({
            'summary': summary,
            'entities': entities,
            'sentiment': sentiment,
            'original_text': text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        text = ""
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if filename.endswith('.pdf'):
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        elif filename.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            os.remove(filepath)
            return jsonify({'error': 'Unsupported file type. Please upload .txt or .pdf'}), 400

        os.remove(filepath)

        if not text.strip():
             return jsonify({'error': 'Could not extract text from the file.'}), 400

        summary = get_summary(text)
        entities = get_entities(text)
        sentiment = get_sentiment(text)

        return jsonify({
            'summary': summary,
            'entities': entities,
            'sentiment': sentiment,
            'original_text': text
        })

    except Exception as e:
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

@app.route('/qa', methods=['POST'])
def qa_endpoint():
    try:
        data = request.json
        text = data.get('text', '')
        question = data.get('question', '')
        if not text or not question:
            return jsonify({'error': 'Missing text or question'}), 400
            
        answer = answer_question(text, question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['POST'])
def export_pdf():
    try:
        data = request.json
        summary = data.get('summary', 'No summary')
        entities = data.get('entities', {})
        sentiment = data.get('sentiment', 'Unknown')
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="NoteSense Matrix Log", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"Detected Sentiment: {sentiment}", ln=True)
        pdf.ln(5)
        
        pdf.cell(200, 10, txt="Extracted Summary:", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 10, txt=summary)
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Vital Entities:", ln=True)
        pdf.set_font("Arial", '', 11)
        
        for category, items in entities.items():
            if items:
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(200, 10, txt=f"{category}:", ln=True)
                pdf.set_font("Arial", '', 11)
                pdf.multi_cell(0, 10, txt=", ".join(items))
                
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, 'notesense_log.pdf')
        pdf.output(temp_path)
        
        return send_file(temp_path, as_attachment=True, download_name='NoteSense_Log.pdf')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
