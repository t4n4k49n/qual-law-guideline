# WHO LBM v9 table/order reconstruction check

## 判定
- PASS: Chapter 1 表・表間本文の child 順 — cha1.sec1.tbl1 -> cha1.sec1.stmt1 -> cha1.sec1.tbl2 -> cha1.sec1.i1 -> cha1.sec1.i2 -> cha1.sec1.i3 -> cha1.sec1.i4 -> cha1.sec1.stmt2 -> cha1.sec1.tbl3 -> cha1.sec1.stmt3
- PASS: cha1.sec1.text は Table 1 前で止まる — Throughout this manual, references are made to the relative hazards of infective microorganisms by risk group (WHO Risk ...
- PASS: Table 1 直後の本文 — Laboratory facilities are designated as basic – Biosafety Level 1, basic – Biosafety Level 2, containment – Biosafety Le...
- PASS: Table 2 後・Table 3 前の本文 — The assignment of an agent to a biosafety level for laboratory work must be based on a risk assessment. Such an assessme...
- PASS: Table 3 直後の本文 — Thus, the assignment of a biosafety level takes into consideration the organism (pathogenic agent) used, the facilities ...
- PASS: 全親ノードの table/statement/item/subitem/figure 順序
- PASS: Table A4-2 行数 — 22
- PASS: Table A4-2 先頭行 — ['Faulty design or construction', '', '']
- PASS: Table A4-2 domestic refrigerator 行 — ['Explosion in domestic-', 'Dangerous chemical not', '• Store low-flashpoint solvents']
- PASS: Table A4-2 flame photometer note 行 — ['Fire in flame', 'Incorrect reassembly of', '• Train and supervise staff.']
- PASS: Table A5-1 行数 — 701
- PASS: Table A5-1 index 過剰取り込みなし — A5 table rows do not contain `alarms 21, 60`; the phrase exists only in Index text.
- PASS: Table A5-1 Acetaldehyde 行 — ['Acetaldehyde', 'Colourless liquid or', 'Mild eye and', 'Extremely flammable;', 'No open flames, no', 'Can form explosive']
- PASS: 項番なし heading: Access
- PASS: 項番なし heading: Personal protection
- PASS: 項番なし heading: Infectious materials
- PASS: 項番なし heading: Chemicals and radioactive substances
- PASS: 小文字 infectious materials heading なし
- PASS: 欠落語句補正: The Laboratory biosafety manual has
- PASS: 欠落語句補正: The  has なし
- PASS: 不要改行除去確認: Wear gloves...
- PASS: RUN配下テキストの末尾空白なし
- PASS: RUN配下テキストのタブなし

## Chapter 1 再結合確認

- `cha1.sec1.tbl1` / `table` / `Table 1. Classification of infective microorganisms by risk group`
- `cha1.sec1.stmt1` / `statement` / `Laboratory facilities are designated as basic – Biosafety Level 1, basic – Biosafety Level 2, contai...`
- `cha1.sec1.tbl2` / `table` / `Table 2. Relation of risk groups to biosafety levels, practices and equipment`
- `cha1.sec1.i1` / `item` / `Pathogenicity of the organism.`
- `cha1.sec1.i2` / `item` / `Mode of transmission and host range of the organism. These may be influenced by existing levels of i...`
- `cha1.sec1.i3` / `item` / `Local availability of effective preventive measures. These may include: prophylaxis by immunization ...`
- `cha1.sec1.i4` / `item` / `Local availability of effective treatment. This includes passive immunization, postexposure vaccinat...`
- `cha1.sec1.stmt2` / `statement` / `The assignment of an agent to a biosafety level for laboratory work must be based on a risk assessme...`
- `cha1.sec1.tbl3` / `table` / `Table 3. Summary of biosafety level requirements`
- `cha1.sec1.stmt3` / `statement` / `Thus, the assignment of a biosafety level takes into consideration the organism (pathogenic agent) u...`

## Table A4-2 sample

| row | Accident | Accident cause | Reducing or eliminating the hazard |
|---:|---|---|---|
| 1 | Faulty design or construction |  |  |
| 2 | Electrical fires in | No over-temperature cut-out | • Compliance with national |
| 3 | incubators |  | standards. |
| 4 | Electrical shock | Failure to provide reliable |  |
| 5 |  | earthing/grounding |  |
| 6 | Improper use |  |  |
| 14 | Explosion in domestic- | Dangerous chemical not | • Store low-flashpoint solvents |
| 20 | Fire in flame | Incorrect reassembly of | • Train and supervise staff. |

## Table A5-1 sample

| row | Chemical | Physical properties | Health hazards | Fire hazards | Safety precautions | Incompatible chemicals / other hazards |
|---:|---|---|---|---|---|---|
| 1 | Acetaldehyde | Colourless liquid or | Mild eye and | Extremely flammable; | No open flames, no | Can form explosive |
| 2 | CH3CHO | gas with a pungent, | respiratory tract | vapour/air mixtures | sparks, no smoking, | peroxides in contact |
| 3 |  | fruity odour; | irritation. Effects on | are explosive; | no contact with hot | with air. May polymerize |
| 4 |  | m.p. –121 °C | the central nervous | flash point –39 °C | surfaces. Store in | under influence of acids, |
| 5 |  | b.p. 21 °C. | system, respiratory | flammable range | tightly sealed | alkaline materials, in |

## Notes

- 結合セルはMarkdownでは表現せず、空セルまたは同一カラムの連続行として保持している。
- Table 3脚注は table row として保持され、直後の `stmt3` が本文として続く。
