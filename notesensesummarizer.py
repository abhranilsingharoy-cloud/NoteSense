from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)

tokenizer = None
model = None
qa_pipeline = None
nlp = None
sia = None

def load_ai_model():
    global tokenizer, model, nlp, sia
    if model is None:
        try:
            print("==========================================================================", flush=True)
            print("🤖 Booting AI Engine... (Loading Summarization, NER, and Sentiment)", flush=True)
            print("==========================================================================", flush=True)
            tokenizer = AutoTokenizer.from_pretrained("t5-small")
            model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
            
            try:
                nlp = spacy.load("en_core_web_sm")
            except Exception as e:
                print(f"Warning: Failed to load spaCy model: {e}")
                
            try:
                sia = SentimentIntensityAnalyzer()
            except Exception as e:
                print(f"Warning: Failed to load NLTK VADER: {e}")
                
            print("✅ Core AI models loaded successfully!", flush=True)
        except Exception as e:
            print(f"❌ Error loading models: {e}", flush=True)
    return tokenizer, model

def load_qa_pipeline():
    global qa_pipeline
    if qa_pipeline is None:
        print("🤖 Loading Q&A Pipeline (lazy load)...", flush=True)
        qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    return qa_pipeline

def get_summary(text: str) -> str:
    tok, mod = load_ai_model()
    if mod is None or tok is None:
        return "Error: Summarization model is not loaded."

    max_chunk_length = 400 
    words = text.split()
    
    if len(words) == 0:
        return "No text provided to summarize."

    def summarize_chunk(chunk_text, max_len, min_len):
        inputs = tok("summarize: " + chunk_text, return_tensors="pt", max_length=512, truncation=True)
        outputs = mod.generate(
            inputs.input_ids, 
            max_length=max_len, 
            min_length=min_len, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True
        )
        return tok.decode(outputs[0], skip_special_tokens=True)

    if len(words) <= max_chunk_length:
        try:
            input_len = len(words)
            max_len = min(150, max(30, int(input_len * 0.8)))
            return summarize_chunk(text, max_len, 10)
        except Exception as e:
            return f"Error during summarization: {e}"

    chunks = []
    for i in range(0, len(words), max_chunk_length):
        chunk = " ".join(words[i:i + max_chunk_length])
        chunks.append(chunk)

    summarized_chunks = []
    for idx, chunk in enumerate(chunks):
        try:
            chunk_len = len(chunk.split())
            max_len = min(100, max(20, int(chunk_len * 0.6)))
            res = summarize_chunk(chunk, max_len, 10)
            summarized_chunks.append(res)
        except Exception as e:
            print(f"Error summarizing chunk {idx}: {e}")
            continue

    if not summarized_chunks:
        return "Error: Could not generate summary for any text chunks."

    combined_summary = " ".join(summarized_chunks)
    return combined_summary

def get_entities(text: str) -> dict:
    load_ai_model()
    if nlp is None:
        return {"Person": [], "Organization": [], "Location": []}
    
    doc = nlp(text)
    entities = {"Person": set(), "Organization": set(), "Location": set()}
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["Person"].add(ent.text)
        elif ent.label_ == "ORG":
            entities["Organization"].add(ent.text)
        elif ent.label_ in ["GPE", "LOC"]:
            entities["Location"].add(ent.text)
            
    return {
        "Person": list(entities["Person"])[:5],
        "Organization": list(entities["Organization"])[:5],
        "Location": list(entities["Location"])[:5]
    }

def get_sentiment(text: str) -> str:
    load_ai_model()
    if sia is None:
        return "Unknown"
        
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def answer_question(text: str, question: str) -> str:
    qa = load_qa_pipeline()
    try:
        result = qa(question=question, context=text)
        return result['answer']
    except Exception as e:
        return f"Error answering question: {e}"
