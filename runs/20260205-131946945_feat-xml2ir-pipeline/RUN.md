# RUN: 20260205-131946945_feat-xml2ir-pipeline

## Summary
- Implement xml2ir pipeline for e-Gov law XML to RegDoc IR bundle (IR + parser_profile + regdoc_profile + meta).
- Add CLI, models, serialization, and tests.
- Update README with usage and schema references.

## Verified (tests)
- as_of extraction yields "2026-05-01" from filename pattern.
- Article Num="3_2" generates nid "art3_2" and never "art32".
- Paragraph/Item/Subitem text is isolated (no contamination), and folded Article text uses ParagraphSentence only.

## Outputs
- Code: `src/qai_xml2ir/`
- Tests: `tests/`
- Config: `pyproject.toml`
- Docs: `README.md`
