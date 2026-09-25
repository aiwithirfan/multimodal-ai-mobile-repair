# Professional Reference Review

## 1. iFixit — Phone repair knowledge

iFixit organizes phone repair around device identification, troubleshooting, guides, parts, and tools. Its phone resources include common faults such as black screens, charging problems, overheating, and battery issues.

**Professional lesson:** Repair support becomes more useful when it is organized around device/problem context rather than a generic chatbot response.

Source: https://www.ifixit.com/Device/Phone

## 2. iFixit FixBot / App

iFixit describes FixBot as an AI repair helper with visual recognition, smart answers, troubleshooting, repair guidance, and hands-free coaching.

**Professional lesson:** A repair AI can be more valuable when it connects visual recognition to practical next actions instead of producing only an image caption.

Source: https://www.ifixit.com/go/app

## 3. Apple Support — iPhone repair

Apple's repair workflow asks users to identify what is happening with the iPhone, provides troubleshooting/service paths, and separates estimated service information from final inspection.

**Professional lesson:** Customer-facing repair systems should set expectations and avoid presenting a remote estimate/diagnosis as a guaranteed final answer.

Source: https://support.apple.com/iphone/repair

## 4. Apple Support — Model identification

Apple provides a dedicated model-identification workflow using model numbers and device details.

**Professional lesson:** Device identity is a critical part of repair intake. RepairLens therefore includes an OCR + reasoning mode but explicitly treats model identification from an image as uncertain when evidence is incomplete.

Source: https://support.apple.com/en-gb/108044

## 5. Groq Vision

Groq's vision documentation describes multimodal models for image interpretation, visual Q&A, caption generation, and OCR. The current Qwen 3.8 27B model page describes image + text input and vision/OCR capabilities.

**Professional lesson:** A multimodal foundation model is suitable for the perception/reasoning layer, while the application should provide domain-specific prompts, safety boundaries, and workflow structure.

Sources:
- https://console.groq.com/docs/vision
- https://console.groq.com/docs/models

## Design takeaway

The professional pattern used in RepairLens is:

**evidence → context → multimodal reasoning → uncertainty → next action**

rather than:

**image → generic caption**

That distinction is the main practical upgrade for Week 3.
