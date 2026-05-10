import streamlit as st
import torch

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SummarAI",
    page_icon="📝",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0d0d0f;
    color: #f0ede8;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 2rem;
    max-width: 1000px;
}

.summar-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3rem;
    font-weight: 700;
    color: #f0ede8;
    letter-spacing: -0.02em;
    margin-bottom: 0;
    line-height: 1;
}

.summar-title span { color: #e8c547; }

.summar-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #7a7a8a;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 6px;
    margin-bottom: 32px;
    border-bottom: 1px solid #2a2a35;
    padding-bottom: 20px;
}

.stat-row {
    display: flex;
    gap: 16px;
    margin-top: 24px;
}

.stat-card {
    flex: 1;
    background: #16161a;
    border: 1px solid #2a2a35;
    border-radius: 8px;
    padding: 16px 20px;
}

.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}

.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #7a7a8a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.yellow { color: #e8c547; }
.green  { color: #5fd4a0; }
.amber  { color: #c97d4e; }

.summary-box {
    background: #16161a;
    border: 1px solid #2a2a35;
    border-left: 3px solid #e8c547;
    border-radius: 8px;
    padding: 24px 28px;
    font-family: 'Playfair Display', Georgia, serif;
    font-style: italic;
    font-size: 1.05rem;
    line-height: 1.9;
    color: #f0ede8;
    margin-top: 8px;
}

.model-badge {
    display: inline-block;
    background: #16161a;
    border: 1px solid #2a2a35;
    border-radius: 4px;
    padding: 4px 12px;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #7a7a8a;
    margin-bottom: 24px;
}

.dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #5fd4a0;
    margin-right: 6px;
    vertical-align: middle;
}

.bar-wrap {
    height: 4px;
    background: #2a2a35;
    border-radius: 2px;
    margin-top: 8px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, #c97d4e, #e8c547);
}

div[data-testid="stTextArea"] textarea {
    background: #16161a !important;
    color: #f0ede8 !important;
    border: 1px solid #2a2a35 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    min-height: 240px !important;
}

div[data-testid="stButton"] button {
    background: #e8c547 !important;
    color: #0d0d0f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 10px 32px !important;
    width: 100% !important;
}

label[data-testid="stWidgetLabel"] p {
    color: #7a7a8a !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
</style>
""", unsafe_allow_html=True)


# ── Load model (cached, import inside to avoid startup crash on Py 3.14) ──────
@st.cache_resource
def load_model():
    from transformers import pipeline
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",  # lightweight, fits Streamlit free tier
        device=-1  # CPU only
    )


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="summar-title">Summar<span>AI</span></div>
<div class="summar-sub">ML-Powered Text Condensation · DistilBART-CNN</div>
""", unsafe_allow_html=True)

st.markdown('<div class="model-badge"><span class="dot"></span>sshleifer/distilbart-cnn-12-6 · HuggingFace Transformers</div>', unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    input_text = st.text_area(
        "INPUT TEXT",
        placeholder="Paste your article, document, or any long-form text here. Minimum 50 characters required…",
        height=280,
    )
    word_count = len(input_text.split()) if input_text.strip() else 0
    st.caption(f"📝 {word_count} words")

with col2:
    max_len = st.slider("Max summary words", min_value=60, max_value=300, value=150, step=10)
    min_len = st.slider("Min summary words", min_value=20, max_value=100, value=40, step=5)
    st.write("")
    summarize_btn = st.button("Summarize →", use_container_width=True)

# ── Summarize ─────────────────────────────────────────────────────────────────
if summarize_btn:
    if not input_text.strip():
        st.error("⚠ Please enter some text to summarize.")
    elif len(input_text.strip()) < 50:
        st.error("⚠ Text too short. Please provide at least 50 characters.")
    elif min_len >= max_len:
        st.error("⚠ Min words must be less than Max words.")
    else:
        with st.spinner("Loading model & running inference…"):
            summarizer = load_model()
            result = summarizer(
                input_text,
                max_length=max_len,
                min_length=min_len,
                do_sample=False,
                truncation=True
            )

        summary = result[0]["summary_text"]
        orig_words = len(input_text.split())
        summ_words = len(summary.split())
        compression = round((1 - summ_words / orig_words) * 100, 1)

        st.markdown("---")
        st.markdown("#### Summary")
        st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
        st.code(summary, language=None)

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card">
                <div class="stat-value yellow">{orig_words:,}</div>
                <div class="stat-label">Original Words</div>
            </div>
            <div class="stat-card">
                <div class="stat-value green">{summ_words:,}</div>
                <div class="stat-label">Summary Words</div>
            </div>
            <div class="stat-card">
                <div class="stat-value amber">{compression}%</div>
                <div class="stat-label">Compression</div>
                <div class="bar-wrap">
                    <div class="bar-fill" style="width:{compression}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
