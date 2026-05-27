# RUN: 20260527-154956369_fix-text2ir-section-kind-raw

## 目的

text2irで番号付き `section` の `kind_raw` がprofileの固定例示値になる問題を修正する。

PIC/S Annex 11の正規化RUN準備中に、入力では `14. Electronic Signature` であるにもかかわらず、IRでは `ann11.sec14.kind_raw` が `4.` になっていることを確認した。これは `section_int_dot` profileの `kind_raw: "4."` がraw tokenより優先されていたため。

## ブランチ

- `fix-text2ir-section-kind-raw`

## 変更

- `src/qai_text2ir/text_parser.py`
  - `section` も `paragraph` / `item` / `subitem` と同様に、matchしたraw tokenを `kind_raw` として保持する。
- `tests/fixtures/pics_annex11_profile_fixture.txt`
  - `14. Electronic Signature` のfixtureを追加。
- `tests/test_pics_annex11_profile.py`
  - `section_14.kind_raw == "14."` を検証。

## 検証

- `.\.venv\Scripts\python.exe -m pytest tests/test_pics_annex11_profile.py -q`: PASS
- `.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_bundle.py tests/test_text2ir_profiles_pics.py -q`: PASS
- 実データ再生成確認:
  - `out/20260527-154956369_fix-text2ir-section-kind-raw/pics_annex11_check/pics_pe00917_annex11_20230825.regdoc_ir.yaml`
  - `ann11.sec14.kind_raw` が `14.` として出力されることを確認。

## 次の扱い

この修正をmainに反映後、`pics_pe00917_annex11_20230825` の正規化RUNを再生成し、promotion candidateを作り直す。
