from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)

tokenizer = None
model = None

def load_ai_model():
    global tokenizer, model
    if model is None:
        try:
            print("==========================================================================", flush=True)
            print("🤖 Booting AI Engine... (Downloading model weights if first run, please wait!)", flush=True)
            print("==========================================================================", flush=True)
            tokenizer = AutoTokenizer.from_pretrained("t5-small")
            model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
            print("✅ Summarization model loaded successfully!", flush=True)
        except Exception as e:
            print(f"❌ Error loading summarization model: {e}", flush=True)
    return tokenizer, model

def get_summary(text: str) -> str:
    """
    Generates a summary for the given text using an advanced chunking algorithm.
    """
    tok, mod = load_ai_model()
    if mod is None or tok is None:
        return "Error: Summarization model is not loaded."

    # T5 models have a token limit. We chunk the text by words to stay within limits.
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

def get_keywords(text: str) -> list:
    """
    Extracts top keywords using an advanced TF-IDF configuration.
    """
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=8, ngram_range=(1, 2))
        vectorizer.fit_transform([text])
        keywords = vectorizer.get_feature_names_out()
        return list(keywords)
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []
