# RUN: mock-ui article paragraph1 display-only dedup

## Task
- Fix the remaining e-Gov "Article 1 / Paragraph 1" mock UI rendering bug.
- In common-ancestor omission mode, enabling "各条第一項の統合表示" must not cause the article heading to reappear above paragraph 2 or later.

## History Reviewed
- `f737b46 fix(xml2ir): remove egov article fold and enforce article->paragraph`
  - IR stopped folding article and first paragraph together.
  - This is the important invariant: article and paragraph remain separate logical nodes.
- `81953fd refactor: centralize egov merge option plumbing`
  - Mock UI added the e-Gov first-paragraph merge option as a render option.
- `f0ea4c5 refactor: apply egov line-template before header/item split`
  - Render pipeline began applying the e-Gov display template over the combined header/item chain.
- `5748530 fix: align prefix dedup context with rendered chain`
  - Prefix dedup began comparing against the previous rendered context chain, including item lines.

## Root Cause
- With `egov_merge_article_p1=True`, the first paragraph is displayed as:
  - `第一条　<paragraph 1 text>`
- The following sibling paragraph still has the logical article ancestor header:
  - `第一条`
- Prefix dedup compared these as different strings, so the article header was shown again above paragraph 2.
- The bug was therefore in the display-chain comparison, not in the IR tree.

## Fix
- Keep the IR unchanged.
- Keep article and paragraph 1 as separate logical nodes in the render plan.
- Split render planning into:
  - logical dedup context: article and paragraph remain separate and are used for ancestor/sibling omission.
  - display lines: only when `egov_merge_article_p1=True`, paragraph 1 is shown with the article label and without the paragraph number.
- Avoid using rendered strings such as `第一条　...` as dedup conditions.
- Preserve the paragraph 1 render block so its checklist checkbox remains visible.

## Verification
- `python -m pytest tests/test_mock_ui_render.py -q`
  - `17 passed`
- Manual render check:
  - selected: `art1.p1`, `art1.p2`, `art1.p3`
  - mode: prefix/common-ancestor omission
  - render option: `egov_merge_article_p1=True`
  - result: no standalone `第一条` line appears above paragraph 2 or 3.
- Follow-up after browser report:
  - Reproduced the app-effective profile by forcing `force_article_p1_text=True` for paragraph/item/subitem/statement rules.
  - Debug trace confirmed `art1.p2` and `art1.p3` have empty `header_lines_after_dedup`.
  - Restarted the Streamlit process on port `8501` because browser reload does not restart the Python server process.
- Number display follow-up:
  - `art1.p1` had raw/display paragraph number `1`, while `art1.p2` and `art1.p3` had `２` and `３`.
  - Normalized article-child paragraph display heads from ASCII digits to fullwidth digits.
  - Applied the same normalization to the mock UI human labels so candidate and checklist displays match.
- Root-fix follow-up:
  - Removed the string-shape workaround from dedup logic.
  - Added logical dedup fields to `_SelectionPlan`.
  - Covered both `prefix` and `exact` dedup modes with regression tests.
- Subitem parent-context follow-up:
  - Found leftover mock-only overrides in `_mock_purpose()`.
  - Removed `subitem` `include_chapeau_text=False`; it hid the unselected parent item when a child subitem was selected.
  - Removed mock-side forced `force_article_p1_text=True`; normalized IR already carries paragraph 1 through the ancestor chain.
  - Added a regression for selected `art1.p1.i12.ro` with unselected parent `十二` context.
- Legacy cleanup follow-up:
  - Removed `force_article_p1_text` from the renderer logic and tests.
  - Added `_normalize_effective_purpose()` in the mock app so stale custom profiles cannot reintroduce `force_article_p1_text`.
  - The same normalization forces ordinary selected hierarchy rules (`subitem`/`item`/`paragraph`/`statement`) to keep ancestor chapeau text, preserving parent context.
  - Added app-level regression coverage for stale profile normalization.
