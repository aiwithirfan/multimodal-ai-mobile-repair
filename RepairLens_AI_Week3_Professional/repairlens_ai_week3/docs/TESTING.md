# Testing & Validation

## Test matrix

| ID | Scenario | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T01 | Cracked screen | Clear front-phone photo + symptom | Observes crack; suggests technician checks | Fill after running | Pending |
| T02 | Charging port | Close-up port photo | Discusses visible debris/damage; safety note | Fill after running | Pending |
| T03 | OCR | Error message/model-label photo | Reads only legible text; states uncertainty | Fill after running | Pending |
| T04 | Poor image | Dark/blurry photo | Low-confidence response; asks for clearer image | Fill after running | Pending |
| T05 | Missing image | No upload | App blocks analysis | Handled in code | Ready |
| T06 | Missing key | No GROQ_API_KEY | App shows setup error | Handled in code | Ready |
| T07 | Unsupported file | PDF/text file | Streamlit uploader rejects it | Handled by file type filter | Ready |

## How to document a real test

For every live model test, record:
- date/time,
- test ID,
- image description,
- prompt/symptoms,
- model name,
- expected behavior,
- actual behavior,
- issue found,
- fix applied,
- screenshot filename.

Example:

```text
T04 — Poor image
Issue: Initial prompt sounded too certain.
Fix: Added explicit observation-vs-inference and image-quality limitation rules.
Evidence: evidence/T04_blurry_image.png
```

## Quality criteria

A test is not "passed" because the UI runs. It is passed only when the generated response is reviewed against the expected behavior.
