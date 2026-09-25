# 5–10 Minute Screen Recording Script

Use your own voice and explain the project naturally. Do not read this word-for-word if it sounds unnatural.

## 0:00–0:45 — Introduction
"Assalam-o-Alaikum. My name is Irfan Shah. This is my Week 3 individual project, RepairLens AI, a multimodal AI tool for a family-owned mobile repair shop."

Explain the business problem: customers often provide a short complaint plus a photo, while technicians need structured intake information.

## 0:45–1:30 — Scope
Show `docs/SCOPE.md`.

Explain what is in scope and what the system deliberately does not claim to do.

## 1:30–2:30 — Architecture
Open `README.md` and explain:
Streamlit → image preprocessing → LangChain → Groq vision model → structured technician handoff.

Point out that LangChain is used to compose the multimodal message and system instructions.

## 2:30–4:30 — Live demonstration
Upload a real test image.
Enter a realistic customer complaint.
Select "Full repair triage."
Run the analysis.

Explain:
- visual observations,
- likely issue,
- confidence/limitations,
- technician next checks,
- safety,
- customer message.

## 4:30–6:00 — Second scenario
Try an error-message image or charging-port close-up.
Use OCR + reasoning or Damage Report mode.

Show how the same application handles a different repair-intake task.

## 6:00–7:00 — Edge cases
Demonstrate no image or explain the missing API-key protection.
Show `docs/TESTING.md`.

## 7:00–8:00 — What you learned
Explain your actual learning:
- multimodal message structure,
- LangChain integration,
- image preprocessing,
- prompt guardrails,
- uncertainty handling,
- Streamlit UX.

## 8:00–9:00 — Limitations and future work
Mention that visual AI cannot confirm hidden internal faults and physical inspection is still required.

Future work:
- repair knowledge base / RAG,
- ticket database,
- technician feedback,
- sensitive-data redaction,
- evaluation dataset.

## 9:00–10:00 — Closing
Show GitHub repository structure and briefly explain why another developer can understand and run the project.
