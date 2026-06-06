from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

# Set up logging to avoid transformers warnings
logging.getLogger("transformers").setLevel(logging.ERROR)

# Initialize the models once when the module is loaded
# Using "t5-small" for a good balance of speed and performance
try:
    print("Loading advanced summarization model (t5-small) with chunking capabilities...")
    summarizer = pipeline("summarization", model="t5-small")
    print("Summarization model loaded successfully.")
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer = None

def get_summary(text: str) -> str:
    """
    Generates a summary for the given text using an advanced chunking algorithm.
    This allows processing of documents much larger than the model's standard token limit.
    """
    if summarizer is None:
        return "Error: Summarization model is not loaded."

    # T5 models have a token limit. We chunk the text by words to stay within limits.
    max_chunk_length = 400 
    words = text.split()
    
    if len(words) == 0:
        return "No text provided to summarize."

    # If the text is short enough, summarize it directly
    if len(words) <= max_chunk_length:
        try:
            # Adjust max_length based on input length to prevent errors
            input_len = len(words)
            max_len = min(150, max(30, int(input_len * 0.8)))
            summary_result = summarizer(text, max_length=max_len, min_length=10, do_sample=False)
            return summary_result[0]['summary_text']
        except Exception as e:
            return f"Error during summarization: {e}"

    # Advanced Chunking Logic for large texts
    chunks = []
    for i in range(0, len(words), max_chunk_length):
        chunk = " ".join(words[i:i + max_chunk_length])
        chunks.append(chunk)

    summarized_chunks = []
    for idx, chunk in enumerate(chunks):
        try:
            # For chunks, we ask for a concise summary to combine later
            chunk_len = len(chunk.split())
            max_len = min(100, max(20, int(chunk_len * 0.6)))
            res = summarizer(chunk, max_length=max_len, min_length=10, do_sample=False)
            summarized_chunks.append(res[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing chunk {idx}: {e}")
            continue

    if not summarized_chunks:
        return "Error: Could not generate summary for any text chunks."

    combined_summary = " ".join(summarized_chunks)
    
    # If the combined summary is still very long, we can recursively summarize it
    # But for most use cases, returning the combined chunk summaries is sufficient and detailed.
    return combined_summary

def get_keywords(text: str) -> list:
    """
    Extracts top keywords using an advanced TF-IDF configuration.
    """
    try:
        # Improved parameters for better keyword extraction
        vectorizer = TfidfVectorizer(stop_words='english', max_features=8, ngram_range=(1, 2))
        vectorizer.fit_transform([text])
        keywords = vectorizer.get_feature_names_out()
        return list(keywords)
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []
