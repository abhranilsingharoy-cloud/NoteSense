# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set the working directory
WORKDIR /app

# Install system dependencies (required for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download required NLTK and spaCy datasets
RUN python -m spacy download en_core_web_sm
RUN python -c "import nltk; nltk.download('vader_lexicon')"

# Pre-download the HuggingFace models during the build process
# This prevents the application from timing out on the first request
RUN python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline; AutoTokenizer.from_pretrained('t5-small'); AutoModelForSeq2SeqLM.from_pretrained('t5-small'); pipeline('question-answering', model='distilbert-base-cased-distilled-squad')"

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Start the application using Gunicorn
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
