# SummarAI — ML Text Summarization App

> Abstractive text summarization powered by DistilBART · Built with Streamlit + HuggingFace Transformers · Deployable on Streamlit Cloud in minutes.

---

## 🧠 Model

| Property | Detail |
|----------|--------|
| Model | `sshleifer/distilbart-cnn-12-6` |
| Type | Abstractive Summarization |
| Framework | HuggingFace Transformers |
| Device | CPU (auto, no GPU needed) |
| Size | ~1.2 GB (downloaded on first run) |

DistilBART is a distilled version of Facebook's BART-Large-CNN, fine-tuned on CNN/DailyMail — delivering high-quality summaries at a fraction of the memory cost, making it perfect for free cloud deployment.

---

## 📁 Project Structure

```
├── app.py               ← Streamlit app (UI + ML in one file)
├── requirements.txt     ← Python dependencies
└── README.md
```

---

## 🚀 Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the app
streamlit run app.py
```

Opens automatically at **http://localhost:8501**

> ⏳ First run downloads the model (~1.2 GB). Subsequent runs load instantly from cache.

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to **GitHub**
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
3. Click **New App** → select your repo → set file to `app.py`
4. Click **Deploy**

Your app will be live at:
```
https://your-app-name.streamlit.app
```

---

## ⚙️ How It Works

```
User inputs text
      ↓
Streamlit UI collects text + slider params (max/min word length)
      ↓
HuggingFace pipeline runs DistilBART inference (CPU)
      ↓
Summary returned with word count + compression ratio stats
```

---

## 🖥️ Features

- 📝 Paste any long-form text — articles, reports, documents
- 🎚️ Adjustable summary length via Max / Min word sliders
- 📊 Live stats — original words, summary words, compression %
- 📋 One-click copy of the summary
- ⚡ Model cached after first load — fast repeated use
- 🌐 No backend server needed — everything runs in Streamlit

---

## 📦 Dependencies

```
streamlit>=1.35.0
transformers==4.40.0
torch>=2.6.0
sentencepiece>=0.2.0
accelerate>=0.26.0
```

> `transformers` is pinned to `4.40.0` for compatibility with Python 3.14 on Streamlit Cloud.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| UI & Server | Streamlit |
| ML Model | DistilBART (HuggingFace) |
| Deep Learning | PyTorch |
| Deployment | Streamlit Community Cloud |
