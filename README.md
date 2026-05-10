# SummarAI — Text Summarization App

ML-powered text summarization using Facebook's BART-Large-CNN model via HuggingFace Transformers.

---

## 🧠 Model
- **facebook/bart-large-cnn** — Fine-tuned on CNN/DailyMail for abstractive summarization
- Runs locally via HuggingFace `pipeline`
- GPU supported (auto-detected); falls back to CPU

---

## 📁 Project Structure

```
summarizer_backend/
  app.py             ← Flask API server
  requirements.txt   ← Python dependencies

summarizer_frontend/
  index.html         ← Full frontend (open in browser)
```

---

## 🚀 Setup & Run

### 1. Backend (Flask + ML)

```bash
cd summarizer_backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Server starts at: **http://localhost:5000**

> ⏳ First run downloads the BART model (~1.6GB). Subsequent runs are instant.

---

### 2. Frontend

Simply open `summarizer_frontend/index.html` in your browser.

No build step needed — it's pure HTML/JS that calls the Flask API.

---

## 🔌 API Endpoints

### `POST /summarize`
Summarize a piece of text.

**Request:**
```json
{
  "text": "Your long text here...",
  "max_length": 150,
  "min_length": 40
}
```

**Response:**
```json
{
  "summary": "Condensed version of the text.",
  "original_word_count": 450,
  "summary_word_count": 82,
  "compression_ratio": 81.8
}
```

### `GET /health`
Check if the server and model are loaded.

---

## ⚙️ Configuration

You can adjust these in the frontend sliders:
- **Max Words** (60–300): Maximum length of the summary
- **Min Words** (20–100): Minimum length of the summary

---

## 🛠 Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| ML Model  | facebook/bart-large-cnn (HuggingFace) |
| Backend   | Python, Flask, Flask-CORS          |
| Frontend  | Vanilla HTML/CSS/JS                |

---

## 📋 Requirements

- Python 3.9+
- ~2GB disk space (model weights)
- 4GB+ RAM recommended (8GB for comfortable CPU inference)
