import base64
import os
import re
from datetime import datetime
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from PIL import Image

load_dotenv()

APP_NAME = "RepairLens AI"
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

st.set_page_config(
    page_title="RepairLens AI | Mobile Repair Intelligence",
    page_icon="assets/logo.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------
# Theme / UI
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #07111f;
    --panel: #0d1b2e;
    --panel2: #10243b;
    --line: rgba(148,163,184,.18);
    --text: #f8fafc;
    --muted: #9fb0c3;
    --accent: #39d98a;
    --accent2: #5eead4;
    --warning: #fbbf24;
}

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at 80% 0%, rgba(57,217,138,.12), transparent 28%),
      radial-gradient(circle at 0% 25%, rgba(94,234,212,.08), transparent 24%),
      var(--bg);
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: #081625;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    border: 1px solid var(--line);
    border-radius: 26px;
    padding: 30px 34px;
    background:
      linear-gradient(135deg, rgba(16,36,59,.94), rgba(8,22,37,.92));
    box-shadow: 0 20px 60px rgba(0,0,0,.22);
    margin-bottom: 22px;
}

.brand {
    display:flex;
    gap:14px;
    align-items:center;
}

.logo-dot {
    width: 48px;
    height: 48px;
    border-radius: 15px;
    display:flex;
    align-items:center;
    justify-content:center;
    background: linear-gradient(135deg, #39d98a, #5eead4);
    color:#06131f;
    font-size:24px;
    font-weight:800;
}

.hero h1 {
    font-family:"Space Grotesk", sans-serif;
    font-size: 2.45rem;
    margin: 8px 0 5px 0;
    letter-spacing:-1.4px;
}

.hero p {
    color: var(--muted);
    font-size: 1.02rem;
    max-width: 850px;
    line-height:1.65;
}

.badge {
    display:inline-block;
    border:1px solid rgba(57,217,138,.35);
    background:rgba(57,217,138,.08);
    color:#8df2bd;
    padding:5px 10px;
    border-radius:999px;
    font-size:.78rem;
    font-weight:700;
    letter-spacing:.3px;
}

.section-title {
    font-family:"Space Grotesk", sans-serif;
    font-size:1.2rem;
    font-weight:700;
    margin: 14px 0 10px;
}

.card {
    border:1px solid var(--line);
    border-radius:20px;
    padding:18px 20px;
    background:rgba(13,27,46,.72);
}

.metric {
    border:1px solid var(--line);
    border-radius:18px;
    padding:16px;
    background:rgba(16,36,59,.65);
}

.metric .label {
    color:var(--muted);
    font-size:.78rem;
    text-transform:uppercase;
    letter-spacing:.8px;
}

.metric .value {
    font-family:"Space Grotesk", sans-serif;
    font-size:1.35rem;
    font-weight:700;
    margin-top:5px;
}

.stButton > button {
    border-radius:12px;
    border:1px solid rgba(57,217,138,.45);
    background:linear-gradient(135deg, rgba(57,217,138,.95), rgba(94,234,212,.95));
    color:#041018;
    font-weight:800;
    min-height:44px;
    box-shadow:0 8px 25px rgba(57,217,138,.13);
}

.stButton > button:hover {
    border-color:#8df2bd;
    transform:translateY(-1px);
}

.stTextInput input, .stTextArea textarea {
    background:#091827 !important;
    color:#f8fafc !important;
    border:1px solid var(--line) !important;
    border-radius:12px !important;
}

[data-testid="stFileUploader"] {
    border:1px dashed rgba(94,234,212,.32);
    border-radius:18px;
    padding:8px;
    background:rgba(9,24,39,.45);
}

[data-baseweb="tab-list"] {
    gap:8px;
}

button[data-baseweb="tab"] {
    background:rgba(13,27,46,.7);
    border-radius:12px;
    color:#b8c5d4;
    padding:10px 16px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color:#07111f;
    background:linear-gradient(135deg, #39d98a, #5eead4);
}

.small {
    color:var(--muted);
    font-size:.82rem;
}

.footer {
    color:#71839a;
    text-align:center;
    padding:30px 0 5px;
    font-size:.78rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Helpers
# ---------------------------
def image_to_data_url(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((1600, 1600))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=88, optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}", image

def build_chain(model_name: str, temperature: float = 0.2):
    return ChatGroq(
        model=model_name,
        temperature=temperature,
        max_tokens=1600,
        api_key=os.getenv("GROQ_API_KEY"),
    )

SYSTEM_PROMPT = """You are RepairLens AI, a careful multimodal assistant for a family-owned
mobile phone repair shop.

Your job is to help a technician triage a phone issue from a customer-provided image plus text.
You are NOT a replacement for a qualified technician. Never claim certainty when the image is
ambiguous. Do not invent exact model numbers, internal component damage, prices, or repair
requirements that cannot be observed or verified.

For every analysis:
1) Separate direct visual observations from inferences.
2) Mention image limitations when relevant (angle, lighting, resolution, hidden components).
3) Prioritize safety: swollen batteries, exposed cells, liquid ingress, heat/burning, damaged
   charging ports, or cracked batteries should trigger an explicit stop-use / technician warning.
4) Give a practical triage path, not a reckless DIY repair procedure.
5) If text/OCR is visible, quote only what is legible and label uncertain text.
6) Recommend what a technician should inspect next.
7) Keep the answer useful to a small repair shop: intake summary, likely causes, next checks,
   customer-facing explanation, and urgency.

Return these headings exactly:
### Visual observations
### Likely issue
### Confidence & limitations
### Technician next checks
### Safety
### Customer message
"""

def analyze_image(chain, data_url, user_text, mode):
    mode_instructions = {
        "Full repair triage": "Perform a structured repair intake and visual triage.",
        "Visual Q&A": "Answer the customer's question using the image as evidence. Do not guess.",
        "OCR + reasoning": "Read any visible text/model labels/error messages, then reason about the repair context.",
        "Damage report": "Focus on visible physical damage, affected areas, and what should be inspected next.",
    }
    prompt = f"""{mode_instructions[mode]}

Customer/technician notes:
{user_text or "No additional notes were provided."}

Write a concise but professional shop-ready assessment.
"""
    msg = HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": data_url}},
    ])
    return chain.invoke([SystemMessage(content=SYSTEM_PROMPT), msg]).content

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.markdown("### ⚙️ Workspace")
    st.caption("Week 3 • Professional / Advanced Practical")
    st.divider()

    model_name = st.text_input(
        "Vision model",
        value=DEFAULT_MODEL,
        help="Use a vision-capable Groq model. The default is Qwen 3.8 27B.",
    )

    temperature = st.slider("Response creativity", 0.0, 0.8, 0.2, 0.1)

    st.divider()
    st.markdown("### 🔐 Connection")
    if os.getenv("GROQ_API_KEY"):
        st.success("Groq API key detected")
    else:
        st.warning("GROQ_API_KEY not found")
        st.caption("Add it to .env before running live analysis.")

    st.divider()
    st.markdown("### What it can do")
    st.markdown(
        "- 📷 Visual repair triage\n"
        "- 🔎 Visual Q&A\n"
        "- 🧾 OCR + reasoning\n"
        "- 🛠️ Damage reporting\n"
        "- 💬 Customer-ready explanation"
    )

# ---------------------------
# Main header
# ---------------------------
st.markdown("""
<div class="hero">
  <div class="brand">
    <div class="logo-dot">✦</div>
    <div>
      <span class="badge">MULTIMODAL • LANGCHAIN • GROQ</span>
      <h1>RepairLens AI</h1>
    </div>
  </div>
  <p>
    A visual intake and repair-triage assistant for a family-owned mobile repair shop.
    Upload a phone image, add the customer's symptoms, and turn mixed visual + text evidence
    into a structured technician handoff.
  </p>
</div>
""", unsafe_allow_html=True)

# Quick metrics
m1, m2, m3, m4 = st.columns(4)
for col, label, value in [
    (m1, "Input", "Text + Image"),
    (m2, "Workflow", "LangChain"),
    (m3, "Vision", "Qwen 3.8 27B"),
    (m4, "Output", "Triage + Handoff"),
]:
    with col:
        st.markdown(
            f'<div class="metric"><div class="label">{label}</div>'
            f'<div class="value">{value}</div></div>',
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🩺 Repair Intake", "📋 How It Works", "🧪 Test Scenarios"])

with tab1:
    left, right = st.columns([1.0, 1.15], gap="large")

    with left:
        st.markdown('<div class="section-title">1. Upload evidence</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Phone photo / screen / charging port / error message",
            type=["jpg", "jpeg", "png", "webp"],
            help="For best results use a clear, well-lit photo. Avoid uploading sensitive personal data.",
        )

        if uploaded:
            data_url, preview = image_to_data_url(uploaded)
            st.image(preview, caption="Uploaded evidence", use_container_width=True)

        st.markdown('<div class="section-title">2. Add customer context</div>', unsafe_allow_html=True)
        notes = st.text_area(
            "Symptoms / customer message",
            placeholder="Example: Phone fell yesterday. It still turns on, but the screen has a black patch and touch is intermittent.",
            height=125,
        )

        mode = st.selectbox(
            "Analysis mode",
            ["Full repair triage", "Visual Q&A", "OCR + reasoning", "Damage report"],
        )

        if mode == "Visual Q&A":
            question = st.text_input(
                "Visual question",
                placeholder="Example: Does the image show visible damage around the charging port?",
            )
            if question:
                notes = f"Customer question: {question}\nAdditional context: {notes}"

        run = st.button("✦ Analyze with RepairLens", use_container_width=True)

    with right:
        st.markdown('<div class="section-title">3. Technician-ready assessment</div>', unsafe_allow_html=True)

        if run:
            if not uploaded:
                st.error("Please upload an image before analysis.")
            elif not os.getenv("GROQ_API_KEY"):
                st.error("GROQ_API_KEY is missing. Copy .env.example to .env and add your Groq API key.")
            else:
                try:
                    with st.spinner("Inspecting image + reasoning over customer context…"):
                        chain = build_chain(model_name, temperature)
                        result = analyze_image(chain, data_url, notes, mode)

                    st.session_state["last_result"] = result
                    st.session_state["last_time"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
                    st.success("Assessment generated.")
                except Exception as exc:
                    st.error("The model request failed.")
                    st.code(str(exc))

        if "last_result" in st.session_state:
            st.markdown(
                f'<div class="card"><span class="badge">ANALYSIS COMPLETE</span>'
                f'<div class="small" style="margin-top:8px;">'
                f'Generated {st.session_state.get("last_time","")}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(st.session_state["last_result"])

            st.download_button(
                "⬇️ Export assessment as TXT",
                data=st.session_state["last_result"],
                file_name="repairlens_assessment.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown(
                '<div class="card">'
                '<h3 style="margin-top:0;">Ready for intake</h3>'
                '<p class="small">Your assessment will appear here with observations, likely issue, '
                'limitations, next checks, safety notes, and a customer-facing explanation.</p>'
                '</div>',
                unsafe_allow_html=True,
            )

with tab2:
    st.markdown('<div class="section-title">Architecture</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    stages = [
        ("01", "Capture", "Streamlit collects an image and symptom text."),
        ("02", "Compose", "LangChain builds a multimodal HumanMessage."),
        ("03", "Reason", "Groq vision model interprets image + text."),
        ("04", "Handoff", "Structured Markdown becomes a technician/customer handoff."),
    ]
    for col, (num, title, body) in zip([c1, c2, c3, c4], stages):
        with col:
            st.markdown(
                f'<div class="card"><span class="badge">{num}</span>'
                f'<h4>{title}</h4><p class="small">{body}</p></div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Why this is different from Weeks 1–2</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
    <p><b>Week 1:</b> recommendation workflow for a restaurant business.</p>
    <p><b>Week 2:</b> website quality/audit workflow for lifestyle websites.</p>
    <p><b>Week 3:</b> multimodal evidence handling for a physical repair operation — the input is
    not only text. The system must interpret a real-world image, combine it with a customer's
    description, surface uncertainty, and produce an actionable technician handoff.</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">Professional test matrix</div>', unsafe_allow_html=True)
    st.dataframe(
        [
            {"Scenario": "Clear cracked screen", "Expected": "Damage described + next inspection checks", "Status": "Ready"},
            {"Scenario": "Charging-port close-up", "Expected": "Visible debris/damage observations + safety caveat", "Status": "Ready"},
            {"Scenario": "Error-message photo", "Expected": "Legible OCR + contextual interpretation", "Status": "Ready"},
            {"Scenario": "Blurry / dark image", "Expected": "Low-confidence language + request for better photo", "Status": "Ready"},
            {"Scenario": "No image", "Expected": "Block analysis and request upload", "Status": "Handled"},
            {"Scenario": "Missing API key", "Expected": "Clear configuration error", "Status": "Handled"},
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Use the scenarios above as the basis for your Week 3 evidence screenshots and video walkthrough.")

st.markdown(
    '<div class="footer">RepairLens AI • Week 3 Advanced Practical Build • '
    'For technician triage support only — final diagnosis requires physical inspection.</div>',
    unsafe_allow_html=True,
)
