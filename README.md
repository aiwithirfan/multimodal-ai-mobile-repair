RepairLens AI — Multi-Modal AI Tool for a Family-Owned Mobile Repair Shop

Week 3 — Professional / Advanced Practical Build

Live Demo: https://multimodal-ai-mobile-repair-nul39qfbuzcwgjcm2pwfze.streamlit.app/

RepairLens AI is a Streamlit-based multimodal repair-intake assistant for a family-owned mobile repair shop. It combines text + image inputs and uses LangChain + Groq vision inference to generate a structured technician-ready triage assessment.

«Important: RepairLens AI is a decision-support tool, not a substitute for physical inspection by a qualified technician. Final diagnosis and repair decisions require physical inspection and appropriate diagnostic procedures.»

1. Scope

A family-owned mobile repair shop often receives incomplete descriptions such as "screen is broken," "phone is not charging," or "there is a strange error."

RepairLens AI provides a consistent visual intake workflow:

Upload image → Add customer symptoms → Analyze → Generate technician-ready assessment

The assessment includes:

- Visual observations
- Likely issue
- Confidence and limitations
- Recommended technician checks
- Safety notes
- Customer-friendly explanation

In Scope

- Phone/device image intake
- Text + image multimodal reasoning
- Visual Q&A
- OCR-oriented error/model-label reading
- Physical damage triage
- Technician next-check recommendations
- Customer-friendly explanations
- TXT assessment export
- Test scenarios and edge-case handling

Out of Scope

- Autonomous repair decisions
- Exact repair pricing
- Parts ordering
- Warranty decisions
- Unsupervised device opening or modification
- Guaranteed identification of hidden/internal damage

---

2. Why This Project Is Different

Week| Business| Core Workflow
Week 1| Restaurant Chain| Text-based product recommendation
Week 2| Lifestyle Websites| Website quality auditing
Week 3| Family-Owned Mobile Repair Shop| Multimodal image + text repair intake

Week 3 introduces a new modality and a physical-world evidence workflow. The main engineering challenge is combining visual evidence with customer context while clearly communicating uncertainty and safety considerations.

---

3. Architecture

                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    │ image + text + mode │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Image Preprocessing │
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
                    │    Qwen 3.8 27B     │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │ Technician-Ready Assessment    │
              │ observations → issue → safety  │
              │ → next checks → customer text  │
              └────────────────────────────────┘

---

4. Tech Stack

- Python 3.10–3.12
- Streamlit
- LangChain Core
- LangChain Groq
- Groq Vision Model
- Pillow
- python-dotenv
- Git & GitHub

AI Model

The current project uses:

qwen/qwen3.8-27b

The model is configurable through the "GROQ_MODEL" environment variable so that the application can be updated if model availability changes.

---

5. Main Features

📷 Visual Repair Triage

Analyzes visible phone damage such as cracked screens, damaged frames, and other external conditions.

🔎 Visual Q&A

Combines a user's question with the uploaded image to provide visual analysis.

🧾 OCR + Reasoning

Can analyze visible error messages, labels, or other readable text in an uploaded image.

🛠️ Damage Reporting

Produces structured observations and recommended technician checks.

💬 Customer-Ready Explanation

Converts technical findings into a clear explanation suitable for communicating with customers.

⚠️ Safety Awareness

Highlights potential safety concerns such as damaged glass, possible battery problems, heat, or liquid exposure.

---

6. Setup

Windows PowerShell

git clone <YOUR-REPOSITORY-URL>
cd multimodal-ai-mobile-repair

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

copy .env.example .env

Open ".env" and add:

GROQ_API_KEY=your_real_key_here
GROQ_MODEL=qwen/qwen3.8-27b

Run the application:

streamlit run app.py

Linux / macOS

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

streamlit run app.py

---

7. How to Use

1. Upload a clear phone image.
2. Enter the customer's symptoms or question.
3. Select an analysis mode.
4. Run the analysis.
5. Review the visual observations.
6. Review limitations and uncertainty.
7. Use the technician next-check section as an intake handoff.
8. Use or export the customer-facing explanation.

Available Analysis Modes

- Full Repair Triage
- Visual Q&A
- OCR + Reasoning
- Damage Report

---

8. Testing

The application was tested using realistic mobile-repair scenarios.

Test Scenario 1 — Cracked Screen

Input: Cracked smartphone screen image + customer symptoms.

Result: PASS

The system identified visible screen damage, considered the reported touch issue, provided technician checks, identified limitations, and generated a customer-facing explanation.

Test Scenario 2 — Severe Display Damage

Input: Severely cracked display image + reported black patch and intermittent touch.

Result: PASS

The system identified significant screen damage, discussed possible display/digitizer problems, recommended additional inspection, and included safety guidance.

Recommended Additional Tests

Test| Input| Expected Behavior
T01| Clear cracked screen| Identify visible damage and suggest checks
T02| Charging-port image| Analyze visible port condition and mention limitations
T03| Error-message image| Read visible text and explain the issue
T04| Blurry/dark image| Acknowledge insufficient visual evidence
T05| No image| Prevent analysis with a clear message
T06| Missing API key| Show configuration error without crashing

«Only tests that are personally executed should be marked as completed in the final evidence.»

---

9. Professional Design Decisions

Uncertainty-First Prompting

The system is instructed to separate direct visual observations from possible inferences and avoid presenting hidden damage as confirmed fact.

Safety Guardrails

Potentially hazardous conditions such as battery swelling, exposed components, burning/heat, or liquid ingress should trigger appropriate safety warnings and technician inspection.

Client-Oriented Output

The output follows a real repair-shop workflow:

Intake Summary
      ↓
Visual Observations
      ↓
Likely Issue
      ↓
Limitations
      ↓
Technician Next Checks
      ↓
Safety Notes
      ↓
Customer Explanation

Configurable Model

The model is controlled through:

GROQ_MODEL=qwen/qwen3.8-27b

This makes the application easier to maintain if the hosted model is changed or deprecated.

Privacy

The application does not intentionally store uploaded images in a database. Images are processed for the model request.

For demonstrations, avoid uploading unnecessary personal information, IMEI numbers, private documents, or real customer data.

---

10. Known Limitations

- A vision model cannot reliably confirm hidden/internal faults from a single external image.
- OCR performance depends on image quality, lighting, focus, resolution, and text size.
- Model availability and usage limits can change.
- Final repair diagnosis requires physical inspection and technician measurements.
- The current version does not connect to inventory, ticketing, CRM, or repair-shop databases.
- Stock or watermarked images may reduce the reliability of visual assessment.

---

11. Future Improvements

With additional development time, I would add:

1. A repair-ticket database with customer consent and access controls.
2. A retrieval layer containing approved repair procedures and device-specific guides.
3. Technician feedback capture for reviewing incorrect observations.
4. Automatic redaction of sensitive identifiers before model submission.
5. A dedicated evaluation dataset and regression test suite.
6. Device-specific repair guidance based on verified model information.

---

12. Repository Structure

multimodal-ai-mobile-repair/
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

---

13. Submission Checklist

- [x] Working Streamlit application
- [x] Multimodal text + image workflow
- [x] LangChain integration
- [x] Groq vision model integration
- [x] Technician-ready assessment
- [x] Customer-facing explanation
- [x] Safety and limitation handling
- [x] Realistic test scenarios
- [ ] Final testing evidence/screenshots
- [ ] Changelog updated
- [ ] 5–10 minute screen-recording completed
- [ ] Video explains the project, LangChain workflow, testing, and debugging
- [ ] Submission form/link completed

---

14. Project Summary

RepairLens AI demonstrates how multimodal AI can support a practical small-business workflow. Instead of treating the system as a general chatbot, the project focuses on a specific operational problem: converting a customer's image and symptom description into a structured repair-intake assessment.

The application demonstrates practical use of LangChain, multimodal vision inference, Streamlit, image preprocessing, uncertainty handling, safety-aware prompting, testing, and professional documentation.

The final diagnosis remains the responsibility of a qualified technician after physical inspection.

---

15. References

- Groq Vision Documentation: https://console.groq.com/docs/vision
- Groq Models Documentation: https://console.groq.com/docs/models
- iFixit Phone Repair Resources: https://www.ifixit.com/Device/Phone
- iFixit Repair App: https://www.ifixit.com/go/app
- Apple iPhone Repair Support: https://support.apple.com/iphone/repair
- Apple Model Identification: https://support.apple.com/en-gb/108044
