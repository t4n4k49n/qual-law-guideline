# HEADING / TABLE REVIEW

- Document: `jp_pmda_aseptic_processing_guideline_20110420`
- Source PDF: `000206144.pdf`
- Review target: heading hierarchy and Tables 1, 2, 3

## Heading Review

PDF/source headings show nested structure such as:

- `7.1 清浄度レベルによる作業所の分類`
- `7.1.1 重要区域（グレード A）`
- `7.1.2 直接支援区域（グレード B）`
- `7.1.3 その他の支援区域（グレード C 及びグレード D）`

Reviewed output:

- `cha7.sec7_1`: `section`, heading `清浄度レベルによる作業所の分類`
- `cha7.sec7_1.p7_1_1`: child `paragraph`
- `cha11.sec11_3`: `section`, heading `環境モニタリング判定基準例`

Chapter 2 definitions remain `paragraph` entries because `2.1` through `2.52` are glossary-style term definitions, not grouping headings.

## Table 1

- PDF page: 20
- Heading: `表１ 清浄区域の分類`
- Generated rows: `4`
- Source order: table appears under `cha7.sec7_1` before `cha7.sec7_1.p7_1_1`
- Duplicate parent note removed; notes are kept as table notes.

Generated header:

```text
名称 区分 | 名称 区域 | 空気の清浄度レベル注1） | 最大許容微粒子数（個／m3） 非作業時 ≧0.5μm | 最大許容微粒子数（個／m3） 非作業時 ≧5.0μm | 最大許容微粒子数（個／m3） 作業時 ≧0.5μm | 最大許容微粒子数（個／m3） 作業時 ≧5.0μm
```

Merged headers retained in `header_structure.spanning_headers`:

- `名称`
- `最大許容微粒子数（個／m3）`
- `非作業時`
- `作業時`

## Table 2

- PDF page: 33
- Heading: `表２ 微生物管理に係る環境モニタリングの頻度`
- Generated rows: `4`

Generated header:

```text
グレード | 区域 | 空中浮遊微粒子 | 空中微生物 | 表面付着微生物 装置，壁など | 表面付着微生物 手袋，作業衣
```

Merged header retained:

- `表面付着微生物`

## Table 3

- PDF page: 33
- Heading: `表 3 環境微生物の許容基準(作業時) 注）1`
- Generated rows: `4`

Generated header:

```text
グレード | 空中微生物 浮遊菌 (CFU/m3) | 空中微生物 落下菌注）2 (CFU/plate) | 表面付着微生物 コンタクトプレート (CFU/24～30cm2) | 表面付着微生物 手袋 (CFU/5指)
```

Merged headers retained:

- `空中微生物`
- `表面付着微生物`

## Decision

Promote visually reconstructed records to `table_row` for Tables 1, 2, and 3. Keep raw extracted lines as trace metadata and keep merged header structures in `header_structure`.
