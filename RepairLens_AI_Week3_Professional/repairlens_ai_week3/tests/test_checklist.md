# Manual QA Checklist

## Functional
- [ ] App starts with `streamlit run app.py`
- [ ] Image uploader accepts JPG/JPEG/PNG/WEBP
- [ ] Image preview renders
- [ ] Text input works
- [ ] Analysis modes switch correctly
- [ ] Live model request returns a result
- [ ] Result export downloads
- [ ] No-image state is handled
- [ ] Missing API key is handled
- [ ] Unsupported file type is blocked

## UX
- [ ] Layout works on laptop screen
- [ ] Result is readable
- [ ] Error messages are actionable
- [ ] No secret/API key appears in the UI
- [ ] Footer limitation is visible

## Safety / quality
- [ ] Output separates observations from inference
- [ ] Output states uncertainty when evidence is weak
- [ ] Safety warning appears when relevant
- [ ] No exact hidden component claim is accepted without evidence
