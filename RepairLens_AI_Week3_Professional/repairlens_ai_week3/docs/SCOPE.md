# Scope Statement — RepairLens AI

## Problem

A small family-owned mobile repair shop may receive a phone with limited context: a photo, a short WhatsApp-style complaint, and no standardized intake notes. This creates avoidable ambiguity before a technician physically inspects the device.

## Proposed solution

RepairLens AI is a multimodal intake assistant that combines:
- a customer-provided phone image,
- a short symptom description,
- an analysis mode,
- and a vision-capable language model accessed through LangChain.

It converts the mixed evidence into a consistent technician handoff.

## Success criteria

1. A user can upload a supported phone image.
2. A user can enter symptoms or a visual question.
3. LangChain sends text + image to a vision-capable model.
4. The output clearly separates observations, inference, limitations, safety, and next checks.
5. Missing image/API-key conditions are handled gracefully.
6. The project is documented well enough for another developer to run it without the author present.

## Non-goals

The tool does not guarantee a repair diagnosis, identify invisible internal damage, approve warranty claims, or autonomously instruct unsafe device disassembly.
