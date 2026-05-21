# PROFILE_FIX_REVIEW

## 結論

確認RUNで `profile変更で済む` と分類した課題に着手し、PIC/S Annex 15、Annex 11、Annex 2A、Part IIのprofile課題を改善した。文書固有の見出し文字列を `text_parser` 本体へ直書きせず、profile設定と汎用の見出し継続オプションで対応した。

## 修正内容

| 文書/課題 | 対応 | 変更ファイル | 検証 |
|---|---|---|---|
| PIC/S Annex 15 見出し継続 | `allow_single_word_caps` と `allow_next_regexes` をprofileに追加し、section見出しの次行結合を許容 | `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml`, `src/qai_text2ir/text_parser.py` | `tests/test_pics_annex15_profile.py` |
| PIC/S Annex 11 section見出し抽出 | `section` を `structural_kinds` に追加 | `src/qai_text2ir/profiles/pics_annex11_default_v1.yaml` | `tests/test_pics_annex11_profile.py` |
| PIC/S Annex 2A Part B/B1階層 | `B1.` 等をsection markerとして追加 | `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml` | `tests/test_pics_annex2a_profile.py` |
| PIC/S Part II section heading/text分離 | `section` を `structural_kinds` に追加 | `src/qai_text2ir/profiles/pics_part2_default_v1.yaml` | `tests/test_pics_part2_v1.py` |

## 実データ確認

- Annex 15: `ORGANISING AND PLANNING FOR QUALIFICATION AND VALIDATION` が1つのsection headingになる。
- Annex 15: `QUALIFICATION STAGES FOR EQUIPMENT, FACILITIES, UTILITIES AND SYSTEMS.` が1つのsection headingになる。
- Annex 11: `Risk Management`, `Personnel`, `Suppliers and Service Providers`, `Validation` がsection headingとして分離される。
- Part II: `Objective`, `Scope`, `Principles` がsection headingとして分離される。
- Annex 2A: 既存のPart A/Part B章に加え、`B1. ANIMAL SOURCED PRODUCTS` がsectionとして分離される。

## 境界判断

- Annex 15の見出し継続は汎用オプションを追加したが、有効化はprofile側で制御する。
- Annex 11/Part IIの修正はprofileの `structural_kinds` 調整であり、本体に文書固有処理は入れていない。
- Annex 2AのB1階層はprofile marker追加で対応した。

## テスト結果

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_pics_annex15_profile.py tests\test_pics_annex11_profile.py tests\test_pics_annex2a_profile.py tests\test_pics_part2_v1.py
.\.venv\Scripts\python.exe -m pytest -q
```

結果:

- `7 passed`
- `160 passed, 1 skipped`
