# RepairLens AI — Multi-Modal AI Tool for a Family-Owned Mobile Repair Shop

**Week 3 — Professional / Advanced Practical Build**

RepairLens AI is a Streamlit-based multimodal repair-intake assistant. It combines a phone image with customer/technician text and uses **LangChain + Groq vision inference** to produce a technician-ready triage assessment.

> **Important:** This is decision-support software, not a substitute for physical inspection by a qualified technician. The model is instructed to distinguish visual observations from inferences and to surface uncertainty.

## 1. Scope statement

A family-owned mobile repair shop often receives incomplete descriptions such as “screen is broken,” “phone is not charging,” or “there is a strange error.” RepairLens AI gives the shop a consistent visual intake workflow: the staff member uploads a photo, adds the customer's symptoms, selects an analysis mode, and receives a concise assessment containing observations, likely issue, confidence/limitations, next checks, safety notes, and a customer-facing explanation.

### In scope
- Phone/device image intake
- Text + image multimodal reasoning
- Visual Q&A
- OCR-oriented error/model-label reading
- Physical damage triage
- Technician next-check recommendations
- Customer-friendly explanation
- TXT export of the assessment
- Test matrix and edge-case handling

### Out of scope
- Autonomous repair decisions
- Exact repair pricing
- Parts ordering
- Warranty decisions
- Opening or modifying a device without technician supervision
- Guaranteed identification of hidden/internal component damage

## 2. Why the project is different from Weeks 1–2

| Week | Business | Core workflow |
|---|---|---|
| Week 1 | Restaurant chain | Text/product recommendation |
| Week 2 | Lifestyle websites | Website quality auditing |
| Week 3 | Family-owned mobile repair shop | **Multimodal image + text repair intake** |

The Week 3 build adds a new modality and a physical-world evidence workflow. The key engineering concern is not simply generating text: it is combining visual evidence with customer context while explicitly communicating uncertainty and safety.

## 3. Architecture

```text
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    │ image + text + mode │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Image preprocessing │
                    │ resize → JPEG → URL │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      LangChain      │
                    │ HumanMessage +      │
                    │ system instructions │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Groq Vision LLM  │
                    │   Qwen 3.8 27B      │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │ Technician-ready Markdown      │
              │ observations → issue → safety  │
              │ → next checks → customer text  │
              └────────────────────────────────┘
```

Groq's current vision documentation lists `qwen/qwen3.8-27b` as a multimodal model supporting image + text inputs, OCR, visual question answering, JSON mode, and reasoning. The model is currently described as a preview model, so the `GROQ_MODEL` environment variable is intentionally configurable.

## 4. Tech stack

- Python 3.10–3.12 recommended
- Streamlit
- LangChain Core
- LangChain Groq integration
- Groq multimodal vision model
- Pillow for image preprocessing
- python-dotenv for local configuration
- Git/GitHub for version control

## 5. Setup

### Windows PowerShell

```powershell
git clone <YOUR-GITHUB-REPO-URL>
cd repairlens-ai-week3

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

copy .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_real_key_here
GROQ_MODEL=qwen/qwen3.8-27b
```

Run:

```powershell
streamlit run app.py
```

The browser should open the RepairLens AI interface.

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## 6. How to use

1. Upload a clear phone image.
2. Add the customer's symptoms.
3. Select one of:
   - Full repair triage
   - Visual Q&A
   - OCR + reasoning
   - Damage report
4. Click **Analyze with RepairLens**.
5. Review the visual observations and uncertainty.
6. Use the technician next-checks section as an intake handoff.
7. Copy/export the customer-facing message when useful.

## 7. Testing performed / evidence plan

The project includes a professional test matrix in the app and `docs/TESTING.md`.

Recommended evidence scenarios:

| Test | Input | Expected behavior |
|---|---|---|
| T01 | Clear cracked screen | Visible damage described; next checks suggested |
| T02 | Charging-port close-up | Visible condition discussed; safety caveat |
| T03 | Error-message image | Legible text extracted and interpreted |
| T04 | Blurry/dark photo | Limitations acknowledged; better photo requested |
| T05 | No image | Analysis blocked with clear message |
| T06 | Missing API key | Configuration error shown without crashing |

Do not claim a test passed until you personally run it and capture evidence.

## 8. Professional design decisions

### Uncertainty-first prompting
The system is instructed to separate observation from inference and avoid claiming hidden damage as fact.

### Safety guardrail
Potentially hazardous conditions such as swelling, exposed cells, burning/heat, or liquid ingress trigger an explicit technician/safety warning.

### Client-oriented output
The result is designed around the shop workflow rather than a generic chatbot: intake summary → likely issue → limitations → technician checks → safety → customer message.

### Configurable model
The model name is controlled by `GROQ_MODEL`, making the repository easier to maintain if a hosted model is deprecated or replaced.

### Privacy
The app does not intentionally persist uploaded images to a database. The image is converted in memory for the model request. Do not upload unnecessary personal information, IMEI numbers, private documents, or customer data during demonstrations.

## 9. Known limitations

- A vision model cannot reliably confirm hidden/internal faults from a single external image.
- OCR quality depends on focus, lighting, resolution, and text size.
- Model availability and pricing can change.
- Final repair diagnosis requires physical inspection and technician measurements.
- The current version does not connect to a shop inventory, ticketing system, or CRM.

## 10. Future improvements

With more time, I would add:
1. A repair-ticket database with customer consent and access controls.
2. A retrieval layer containing the shop's approved repair procedures and device-specific guides.
3. Technician feedback capture so incorrect model observations can be reviewed.
4. Automated redaction of sensitive identifiers before model submission.
5. Evaluation datasets and a regression test suite with expected outputs.

## 11. Suggested GitHub repository structure

```text
repairlens-ai-week3/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── assets/
│   └── logo.svg
│
├── docs/
│   ├── SCOPE.md
│   ├── RESEARCH.md
│   ├── TESTING.md
│   ├── CHANGELOG.md
│   └── VIDEO_SCRIPT.md
│
├── evidence/
│   └── README.md
│
└── tests/
    └── test_checklist.md
```

## 12. Submission checklist

- [ ] Working Streamlit app
- [ ] GitHub repository is public/private as required by the internship
- [ ] README reviewed and no placeholders remain
- [ ] Real test screenshots captured
- [ ] Testing notes updated with actual results
- [ ] Changelog updated
- [ ] 5–10 minute screen recording completed
- [ ] Video clearly explains the tool, LangChain usage, workflow, and debugging
- [ ] Submission form/link completed

## 13. References

- Groq Vision documentation: https://console.groq.com/docs/vision
- Groq model documentation: https://console.groq.com/docs/models
- iFixit phone repair resources: https://www.ifixit.com/Device/Phone
- iFixit repair app / FixBot: https://www.ifixit.com/go/app
- Apple iPhone repair support: https://support.apple.com/iphone/repair
- Apple model identification: https://support.apple.com/en-gb/108044
